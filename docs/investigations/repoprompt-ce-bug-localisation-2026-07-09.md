# RepoPrompt CE Bug Localisation — Issue #399 (Supervisor sessions ingest raw child transcripts)

日期：2026-07-09
方法：read-only source trace against local clone `repoprompt/repoprompt-ce` @ `c255548d` (v1.0.26-1)
任务：为 upstream issue #399 定位一个 root-cause，并产出 evidence memo。Investigation only — no PR (submitter `zwtang119` not in `.github/APPROVED_CONTRIBUTORS`).

## Bug

- **Issue**: `repoprompt/repoprompt-ce#399` — "Supervisor sessions ingest raw child tool outputs; child results should be reports, not transcripts"
- **One-line impact**: 当 supervisor 通过 `agent_run` wait/poll/steer 收集 child session 结果时，默认返回的 `AgentRunMCPSnapshot` 把 child 的原始尾部 assistant 文本（含模型 echo 的 tool output 摘录、长代码块、reasoning）以 `assistant_text` 形式直接灌回 supervisor 上下文；不存在 issue 要求的"结构化 report"（status / outcome / concise summary / key findings / changed files / verification）。原始 transcript 也没有"显式 log op 才可达"的隔离——只有 `agent_manage.extract_handoff` 这一显式 XML 导出通道，与默认 wait/poll 路径并行存在。
- **Upstream link**: https://github.com/repoprompt/repoprompt-ce/issues/399（issue 文本按本任务 context 摘要引用，未从 GitHub fetch）

**Affected areas named in the issue (与代码对照)**:
- `Sources/RepoPrompt/Infrastructure/MCP/Agent/` —— 确认：本目录下的 `AgentRunMCPToolService.swift`、`AgentRunMCPSnapshot.swift`、`AgentRunSessionStore.swift`、`AgentExploreMCPToolService.swift` 构成默认 wait/poll/steer 响应装配链。
- "adjacent runtime files" —— 确认：真正的 raw-transcript 读取落在 `Sources/RepoPrompt/Features/AgentMode/Runtime/Transcript/AgentTranscriptServices.swift` 与 `Sources/RepoPrompt/Features/AgentMode/ViewModels/AgentModeViewModel.swift`。

## Hypothesis（读码前声明）

我**先**假设 root cause 是：`AgentRunMCPToolService` 在 wait/poll/steer 返回时，把 `AgentRunMCPSnapshot` 的某个"快照正文"字段直接当作 child 结果回传；该正文来自 `AgentModeViewModel` 对 child transcript 的"深拷贝"——即 child 的 trailing assistant 文本被原样取来，没有 report-shaped 的中间层。即存在一条 `transcript.activity.text → snapshot.<正文> → MCP response.<正文>` 的 pass-through，且**没有** `Report`/`distilledSummary`/`keyFindings` 这一类 shaping 类型参与。证据需回答两点：(1) 该字段是哪个；(2) shaping 步骤是否真的缺失。

证据将证实第一点并对第二点给出强否定结论（确实缺失），见 Trace 与 Root cause。

## Trace（数据流，file:line）

### 1. 入口：wait / poll / steer 都走 `AgentRunMCPSnapshot`

`AgentRunMCPToolService.execute(args:)`（`Sources/RepoPrompt/Infrastructure/MCP/Agent/AgentRunMCPToolService.swift:278-304`）按 `op` 分派：
- `poll`/`wait` → `executeWait`（`:724`）
- `steer` → `executeSteer`（`:884`）

三条路径最终都汇入 `decoratedRunValue(snapshot:...)`（`:1898-1932`），它只是把 `snapshot.asObject()` 装进 MCP `Value`，再补 `_meta`/`wait`/`workflow` 等装饰字段。装饰层不改变正文。

### 2. `Assistant_text` 是 raw transcript 文本的出口

`AgentRunMCPSnapshot.asObject()`（`Sources/RepoPrompt/Infrastructure/MCP/Agent/AgentRunMCPSnapshot.swift:373-429`）构造回包对象。其中：

```swift
// AgentRunMCPSnapshot.swift:386-388
if let latestAssistantPreview, !latestAssistantPreview.isEmpty {
    obj["assistant_text"] = .string(latestAssistantPreview)
}
```

`latestAssistantPreview` 在该结构体定义注释中也写明语义（`:314-316`）："Serialized as `preview` while the run is active and as `output` once the run reaches a terminal state."——也即 supervisor 收到的 child 正文，一条路通吃。

### 3. 快照构建：正文来自 `mcpResolvedAssistantPreview`

`AgentModeViewModel.mcpSnapshot(for:)`（`Sources/RepoPrompt/Features/AgentMode/ViewModels/AgentModeViewModel.swift:4797-4938`）是唯一的 live 快照构造点：

```swift
// AgentModeViewModel.swift:4919-4930（节选关键字段）
return AgentRunMCPSnapshot(
    sessionID: resolvedSessionID,
    ...
    status: status,
    statusText: resolvedStatusText,
    latestAssistantPreview: mcpResolvedAssistantPreview(session: session, status: status),
    interaction: interaction,
    ...
)
```

### 4. `mcpResolvedAssistantPreview` → 直接读 transcript 活动

`AgentModeViewModel.mcpResolvedAssistantPreview(session:status:)`（`AgentModeViewModel.swift:15344-15381`）按状态分派，但所有分支都落回 `AgentTranscriptIO`：

```swift
// AgentModeViewModel.swift:15344-15381
private func mcpResolvedAssistantPreview(session: TabSession, status: AgentRunMCPSnapshot.Status) -> String? {
    switch status {
    case .expired: return nil
    case .running, .waitingForInput:
        ...
        return AgentTranscriptIO.latestAssistantPreviewText(in: lastTurn)        // ← raw
    case .completed, .failed, .cancelled:
        let transcriptPreview = session.transcript.turns.last.flatMap {
            AgentTranscriptIO.terminalAssistantResponseText(in: $0)              // ← raw
        }
        let sourcePreview = AgentTranscriptIO.terminalAssistantResponseText(from: session.items) // ← raw
        ...
        return session.items.isEmpty ? transcriptPreview : sourcePreview
    }
}
```

注意：分支选择只决定"从 transcript 还是从 items"与"latest turn 还是全 trailing"，二者**都**是原始文本读取，没有 distill 步骤。

### 5. `AgentTranscriptIO` 把活动 `text` 原样吐出

`Sources/RepoPrompt/Features/AgentMode/Runtime/Transcript/AgentTranscriptServices.swift`:

```swift
// AgentTranscriptServices.swift:2938-2948
static func latestAssistantPreviewText(in turn: AgentTranscriptTurn) -> String? {
    if let activity = conclusionActivity(in: turn),
       AgentDisplayableText.hasDisplayableBody(activity.text)
    {
        return activity.text.trimmingCharacters(in: .whitespacesAndNewlines)   // ← 原样
    }
    for activity in turn.allActivities.reversed()
        where (activity.itemKind == .assistant || activity.itemKind == .assistantInline)
        && AgentDisplayableText.hasDisplayableBody(activity.text)
    {
        return activity.text.trimmingCharacters(in: .whitespacesAndNewlines)    // ← 原样
    }
    return nil
}
```

terminal 路径用 `contiguousTrailingAssistantText`（`:2972-2986`）把所有 trailing 的 `.assistant`/`.assistantInline` 的 `fragment.text` 直接 `joined()`，同样不做提炼：

```swift
// AgentTranscriptServices.swift:2972-2986
private static func contiguousTrailingAssistantText(
    _ fragments: [(kind: AgentChatItemKind, text: String)]
) -> String? {
    var trailingFragments: [String] = []
    for fragment in fragments.reversed() {
        guard fragment.kind == .assistant || fragment.kind == .assistantInline else { break }
        trailingFragments.append(fragment.text)
    }
    guard !trailingFragments.isEmpty else { return nil }
    let text = trailingFragments.reversed().joined()
        .trimmingCharacters(in: .whitespacesAndNewlines)
    return AgentDisplayableText.hasDisplayableBody(text) ? text : nil
}
```

`AgentTranscriptActivity.text` 之于 `AgentChatItem.text`（`Sources/RepoPrompt/Features/AgentMode/Models/AgentChatModels.swift:135-152` 的 `init(from item:)`）逐字拷贝，而 `AgentTranscriptActivity.toItem()`（`:154-174`）也保留 `text`。transcript layer 因此照原样保留 assistant 内容——既不剔除模型 echo 的 tool 输出，也不抽取 changed files / verification / outcome。

### 6. `AgentRunSessionStore`：纯透传

`AgentRunSessionStore`（`Sources/RepoPrompt/Infrastructure/MCP/Agent/AgentRunSessionStore.swift`）是 wait/poll 取用 stored 快照的中介：
- `noteSnapshot` / `ingestSnapshot`（`:151-161`, `:305-358`）：把传入 snapshot 直接写进 `latestSnapshot`。
- `snapshot(for:)`（`:453-461`）只 `return latestSnapshot(...)`。
- `acceptedSnapshot`（`:518-533`）只比 status/timestamp 决胜，**不重塑正文**。

故 multi-wait 路径 `decoratedMultiWaitValue`（`AgentRunMCPToolService.swift:1934-1959`）里 `obj["snapshots"] = .array(snapshots.map { .object($0.asObject()) })` 把每个 child 的完整 raw `assistant_text` 数组化回传——issue 描述的 "wait/poll responses can surface large raw tool-output-heavy child content" 精确命中此处。

### 7. MCP 人类可读渲染层：同样原样输出

`ToolOutputFormatter.formatAgentControlRun`（`Sources/RepoPrompt/Infrastructure/MCP/ToolOutputFormatter.swift:5207-5388`）把 `assistant_text` 在 terminal 时作为 "Output"、非 terminal 时作为 "Preview" 直接拼进文本回包（`:5243`, `:5383-5386`）：

```swift
// ToolOutputFormatter.swift:5383-5386
if let assistantText, !assistantText.isEmpty {
    let heading = isTerminal ? "Output" : "Preview"
    lines.append("\n**\(heading)**\n\n\(assistantText)")
}
```

这一渲染层也没有任何 report shaping——进一步证明 end-to-end 通路里没有任何"提炼"环节。

### 8. "Report" 数据类型不存在（系统性反证）

对整仓 `Sources/RepoPrompt` 用 `struct .*Report|enum .*Report|ShapedReport|ChildReport|SupervisorReport|struct.*Findings|changed_files.*summary|verification.*outcome` 做 grep，命中均为无关子系统（GC 报告、benchmark 报告、workspace switching、`extract_handoff` 通道）。agent_run 默认返回路径上**没有任何** issue 描述的 `status/outcome/concise summary/key findings/changed files/verification` 结构。唯一近似"report-like"的现有通道是 `agent_manage.extract_handoff`（`Sources/RepoPrompt/Infrastructure/MCP/Agent/AgentManageMCPToolService.swift:66`、`:299`、`:410`；`ToolOutputFormatter.swift:5513-5543`），它把 transcript + 文件状态序列化成 `<forked_session ...>` XML，**但这是显式 log op，正是 issue 想保留的“raw transcript via explicit ops”**——它不替代 #399 要求的默认 report。

`AgentRunOracleReviewSource` / `AgentOracleExport.oracleMarkdown`（`AgentRunMCPToolService.swift:59-94`）是给 child 的 plan/review Oracle 打包通道（写盘 → 让 child `read_file`），方向与 #399 所求（child→supervisor 的 distilled report）相反，不能复用为默认 child 回包。

## Root Cause

行为偏离 issue 期望的确切位置是：**`AgentRunMCPSnapshot.latestAssistantPreview` 字段的填充策略**——它把 child transcript 的原始尾部 assistant 文本（含模型可能 inline 的 tool 输出摘录、长代码、un-massaged reasoning）直接当作 supervisor 收到的 child 结果回传，且全程无 report-shaped 中间层。

具体 file:line（root cause 主点 + 必经节点）：

1. **主因（缺 report shaping 的填充点）** —— `Sources/RepoPrompt/Features/AgentMode/ViewModels/AgentModeViewModel.swift:4930`：
   `latestAssistantPreview: mcpResolvedAssistantPreview(session: session, status: status)` 把 raw transcript 文本作为唯一正文喂进快照。该字段在同文件 `:15344-15381` 的实现里只调用 `AgentTranscriptIO.latestAssistantPreviewText` / `terminalAssistantResponseText`，二者均为"原样取 `.text`"。

2. **正文出口** —— `Sources/RepoPrompt/Features/AgentMode/Runtime/Transcript/AgentTranscriptServices.swift:2938-2948` 与 `:2972-2986`：`activity.text` 被 trim 后直接返回，无提炼。

3. **快照序列化把它原样外抛** —— `Sources/RepoPrompt/Infrastructure/MCP/Agent/AgentRunMCPSnapshot.swift:386-388`：`obj["assistant_text"] = .string(latestAssistantPreview)`。multi-wait 路径 `AgentRunMCPToolService.swift:1955-1957` 再把它阵列化。

4. **中介层不重塑** —— `Sources/RepoPrompt/Infrastructure/MCP/Agent/AgentRunSessionStore.swift:305-358`（`ingestSnapshot`）与 `:453-461`（`snapshot(for:)`）：透传 snapshot，正文一字不改。

"Report 数据类型/ shaping 步骤" **事实上不存在**（见 Trace §8 反证）。这与 issue 所述"默认应是 report 而非 transcript"形成直接缺口。

## Fix Sketch（non-binding）

- 在 `AgentRunMCPSnapshot` 引入一个 `report: AgentRunChildReport?` 可选结构（字段：status、outcome、concise summary、key findings、changed files、verification），与 `latestAssistantPreview` 并列；`asObject()` 在存在 report 时默认序列化 `report`、将 `assistant_text` 降级为"raw transcript preview"并在 `_meta` 标注可达性。改点：`AgentRunMCPSnapshot.swift` struct 定义 + `asObject()`（`:373-429`）。
- 在 `AgentModeViewModel.mcpSnapshot(for:)`（`:4919-4938`）与 `mcpResolvedAssistantPreview`（`:15344-15381`）之间插入一个 report shaping 步骤：扫描 child transcript 的 tool calls/results 与 assistant conclusion，提炼 changed files（geographic heuristic / `toolResultJSON` 里的 path）、key findings（抽取 prose 段落）、verification（识别 test/CI tool 结果），并在 wait/poll/steer 终态时优先填 `report`。该 shaping 的原料读取应落在 `AgentTranscriptServices` 新增 API（与 `terminalAssistantResponseText` 平行），避免污染既有 raw 读取函数。
- 让 `AgentRunMCPToolService.decoratedRunValue`（`:1898-1932`）与 `decoratedMultiWaitValue`（`:1934-1959`）在存在 `report` 时不再把 child 的 `assistant_text` 放进 `snapshots` 数组正文（仅保留 `transcript_item_count` 与 `report`）；原始 transcript 继续仅由 `agent_manage.extract_handoff` 提供，与 issue 描述的"raw transcript stays reachable only via explicit log ops"一致。

## Confidence + Blast Radius

- **Confidence**: **high**（根因链 5 步 file:line 闭环；反证一条 grep 已覆盖整仓；行为与 issue 文本逐条对齐）。唯一会让 confidence 降到 med 的开口是"assistant 文本里到底混了多大比例的 raw tool output 仍需真实 session 样本佐证"——但 issue #399 的主诉求是"默认应 report 而非 transcript"，这一点已被结构性证据定死，与样例数据无关。
- **真实改动涉及的文件数**: ~5–8 个（`AgentRunMCPSnapshot.swift`、`AgentModeViewModel.swift` 的 report 构造与 shaping、`AgentTranscriptServices.swift` 新增提炼 API、`AgentRunMCPToolService.swift` 装饰层、`AgentExploreMCPToolService.swift` 共享控制路径、`ToolOutputFormatter.swift` 渲染层、以及测试）。属于"中等 blast radius"——MCP 结构体与 store 可纯加 additive（保持 backward-compat），但 shaping 提炼需新写一段 transcript 扫描逻辑，且 `mcpResolvedAssistantPreview` 的现有调用方（含 notification `notifyAgentTurnComplete`，`AgentModeViewModel.swift:15294-15302`）需评估是否要切到 report。
- **测试需改动**: 至少 `Tests/RepoPromptTests/AgentMode/Transcript/AgentTranscriptAssistantPreviewTests.swift`（断言 `terminalAssistantResponseText` 返回 raw）与 `Tests/RepoPromptTests/AgentMode/AgentModeMCPWaitEpochTests.swift`（`:532/564/606-607/652/721` 直接断言 `latestAssistantPreview`/`assistant_text` 的内容）需要新增 report-shaped 断言，但**不应破坏**现有 raw 断言（raw 仍需可达）。
- **是否适合非 approved contributor 的 first PR**: **否**。虽然 root-cause 是结构性而非 provider-runtime 深处，但 fix 的 shaping 语义（"concise summary / key findings / changed files / verification"如何定义、阈值与回调契约）需要与 upstream maintainer 先达成 schema 共识，且触及 supervisor↔child 的稳定行为契约，属设计性改动，不适合"不见面"的 drive-by PR。本 memo 的价值是先把 root-cause 与 schema 缺口钉死，供后续对话或 approved contributor 接手。

## Bug Pivoted Away From (if any)

未 pivot。按指示优先做 #399；在本次会话内已能局部化到单一 root cause + file:line 闭环，故未切换至 #402 / #400。#399 的 blast radius 虽中等（5-8 文件），但 root cause 收敛于 `AgentRunMCPSnapshot.latestAssistantPreview` 填充策略 + 缺失 report 类型，不需触及 provider runtime，因此无需 retreat。

## 交叉引用

- 本 memo：`auto-research/docs/investigations/repoprompt-ce-bug-localisation-2026-07-09.md`
- 审稿风格参考：`auto-research/docs/investigations/experiment-success-evaluation-2026-07-08.md`
- 调研对象 clone：`/Users/tangzw119/Documents/GitHub/0ref/repoprompt-ce/`（clean, `main`, `c255548d`, v1.0.26-1）
- Issue 仓上游：`repoprompt/repoprompt-ce#399`
