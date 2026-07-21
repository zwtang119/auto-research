# institute-one 对 CDS4WorldCup 的可借鉴性审计

> **类型**: audit / decision-support
> **状态**: reviewed
> **日期**: 2026-06-12
> **作者**: kimi-k2.6
> **审阅时间**: 2026-06-12
> **来源**: 对 `/Users/tangzw119/Documents/GitHub/0ref/institute-one` 的静态代码审计

## 1. 审计目的与范围

institute-one 是一套单节点 AI 研究基础设施（FastAPI + SQLite + Obsidian Vault），其功能覆盖分析师 roster 管理、线性工作流引擎、APScheduler 调度器、内存事件总线、深度研究优先级队列、白板协作、邮件箱以及 Vault 安全写入。本审计在**不引入数据库、不启动常驻进程、不破坏 Marginalia 协议**三项硬约束下，将其机制与 CDS4WorldCup 当前以人工 MiMo sprint 为核心的运营模式进行系统性对比，识别可轻量移植的优化点，并按实施优先级排序。

**审计范围**: institute-one 的 executor、scheduler、bus、vault/writer、workflows、research、prompts、analysts.json 及 ROADMAP。审计方法为静态代码阅读与架构映射，未进行运行时验证。

## 2. 两项目核心差异

| 维度 | institute-one | CDS4WorldCup |
|---|---|---|
| **运行时** | 常驻 Python 进程，APScheduler 调度 8 个周期性任务 | 无常驻进程，人工启动 12-24 小时 MiMo sprint |
| **状态持久化** | SQLite（tasks、events、queues、workflow_runs 表） | JSON 文件（campaign_state.json、task_queue.json） |
| **事件系统** | 内存总线 + events 表持久化 + SSE 推送 | Marginalia 页内批注，无全局事件时间线 |
| **任务执行** | executor.submit/spawn，全局信号量（默认 3）+ per-hand 互斥锁 | 无统一执行层，MiMo 直接读写文件 |
| **工作流** | JSON 定义线性步骤引擎，变量替换，条件认领 | 自由文本任务描述，无步骤化拆分 |
| **角色系统** | catalog/analysts.json 配置化 10 个分析师 | 无配置化角色，依赖 MiMo 总控文档约束 |
| **Prompt 工程** | 标准化三明治（日期锚点 → 人格 → 上下文 → 任务 → 引用规范 → 文件交付物） | 总控文档定义纪律，无统一 prompt 构建层 |
| **产出写入** | VaultWriter（原子写入 + sha256 ledger + 冲突旁支 + 跳过未变更） | 直接写文件，无冲突检测或版本管理 |
| **跟随机制** | dailies/research 自动 spawn 白板主题 + 邮件线程，per-source cap 有界 | 任务之间无自动联动，依赖人工拆分 |
| **审计脊柱** | 每行模型调用 = tasks 表一行，支持孤儿恢复 | 无统一审计表，状态分散在 JSON 和文件系统中 |
| **来源纪律** | prompt 内 CITATION_MANDATE 约束 | source-policy.md 三级来源 + Green Source 硬性闸门 |

## 3. 可借鉴机制（按优先级）

### P1 · Prompt 三明治标准化（零依赖，立即可做）

institute-one 的 `prompts.py` 定义了统一的 prompt 结构：

```
日期锚点 → 人格块 → 上下文块 → 任务 → 引用规范 → 文件交付物
```

CDS4WorldCup 的 `docs/ops/mimo-season-campaign.md` 已有来源纪律和交付规范，但**每次 prompt 的拼接是自由文本**。可以：

- 在 `src/utils/prompt_builder.py` 中实现轻量的 prompt 构建器（零依赖纯 Python）。
- 为 CDS 场景定义固定块：`date_anchor()`、`source_policy_block()`、`path_card_context_block()`、`file_deliverable(filename)`。
- 标准化 MiMo 启动 prompt 的结构，减少每次 sprint 的 prompt drift。

**约束兼容性**: 完全兼容。不引入新依赖，不修改 schema/。

### P1 · 条件认领惯用法应用于 task_queue（零依赖，轻量改造）

institute-one 的 executor 使用 `UPDATE … SET status='running' WHERE id=? AND status='pending'`，通过 rowcount 判断是否竞争成功。这使得：

- 并发 tick 不会重复认领同一任务。
- 重启后可以从 durable state 恢复，不丢失进度。

CDS4WorldCup 的 `data/ops/task_queue.json` 是单文件 JSON，并发写入无锁。可以：

- 不引入 SQLite，但借鉴**状态机思维**：task 状态必须是 `pending → running → done|failed`，running 必须带 `started_at` 和 `runner_id`。
- 在 `task_queue.json` 中增加 `version` 字段，写回时检查乐观锁（读取时的 version 与当前 version 是否一致）。
- sprint 开始时扫描所有 `running` 任务，超期未完成的标记为 `stalled`，允许下一轮认领。

**约束兼容性**: 完全兼容。纯 JSON 文件改造。

### P2 · VaultWriter 安全规则应用于 candidate/ 和 mimo_outputs/（零依赖，建议做）

institute-one 的 VaultWriter 有五个规则：

1. 原子写入（tmp + os.replace）
2. 所有权标记（managed: institute）
3. hash ledger（人类编辑过的文件永不覆盖，生成冲突旁支）
4. 跳过未变更（sha256 一致则跳过）
5. 可重建（doctor 可对比 ledger vs 磁盘）

CDS4WorldCup 当前的问题是：MiMo 和人类可能同时编辑 `data/ops/candidate/` 或 `data/ops/mimo_outputs/` 下的文件，**存在覆盖风险**。可以：

- 在 `src/utils/vault_writer.py` 中实现轻量版本（不需要 SQLite ledger，用同级 `.ledger.jsonl` 记录 sha256）。
- 写入 `candidate/` 和 `mimo_outputs/` 时遵循：先写 `.tmp.` 文件再 rename；检测到人类编辑（文件 sha 与 ledger 不一致）时写旁支文件 `(institute update <date>).md`。
- 这对 `wiki/` **不做**，因为 wiki 是人类主控区，保持 Marginalia 协议的简洁性。

**约束兼容性**: 兼容。零依赖，只影响 ops 目录。

### P2 · 事件批注惯用法（零依赖，可选）

institute-one 的 `bus.py` 将所有事件写入 events 表，同时推送到 SSE 和注册处理器。

CDS4WorldCup 的 Marginalia 批注 `> [!memo] YYYY-MM-DD 内容` 实际上已经是事件的一种投影，但：

- 分散在各 wiki 页面中，没有全局时间线。
- 任务完成、来源审计、路径卡更新之间没有联动。

可以：

- 在 `data/ops/events.jsonl` 中维护一个只追加的事件日志（每行一个 JSON）。
- 每次 sprint checkpoint、任务完成、审核请求提交时追加一行。
- `scripts/audit.py` 扩展一个 `--events` 子命令，按时间线输出全局事件摘要。

**约束兼容性**: 兼容。纯追加 JSONL，不引入数据库。

### P2 · 工作流 JSON 化标准任务（零依赖，中期做）

institute-one 的 `workflows/*.json` 定义了步骤化工作流：

```json
{
  "id": "research",
  "steps": [
    {"id": "01_scout", "analyst": "macro-analyst", "prompt": "...", "output_file": "01_侦察.md"},
    {"id": "02_deep", "analyst": "equity-analyst", "prompt": "...", "output_file": "02_深度.md"}
  ]
}
```

CDS4WorldCup 的 `docs/ops/mimo-season-campaign.md` 第 5 节定义了 8 种标准任务类型（Path Card Audit、Match Context Candidate 等），但**每个任务都是自由文本描述**。可以：

- 在 `data/ops/workflows/` 下为每种标准任务定义 JSON 工作流模板。
- 每个步骤对应一个子任务，有明确的输入文件、输出文件、prompt 模板、source_level 要求。
- MiMo sprint 中，将大任务拆分为步骤化的子任务，每完成一步更新 `task_queue.json` 的 `current_step`，而不是一次性完成整个任务。

**收益**: 提高任务输出的可复现性，减少"完成 3 个任务但每个只有结论清单"的问题。

**约束兼容性**: 兼容。纯 JSON 模板，不引入工作流引擎运行时（MiMo 自己按步骤执行即可）。

### P2 · 跟随机制与有界递归（概念借鉴，可选）

institute-one 的一个核心设计是：**dailies 和 research 产出 follow-ups → 主题打开白板 → 问题打开邮件线程 → 输出落入 vault**，但通过 per-source caps、topic dedup、2-active-board limit、replies/cards 不再递归 来有界。

CDS4WorldCup 当前没有这种联动：Path Card Audit 发现缺口后，不会自动 spawn 一个 Source Gap Audit 任务；Match Context 完成后不会自动 spawn Prediction Card 任务。

可以：

- 在 `task_queue.json` 中增加 `spawned_by` 和 `spawn_triggers` 字段。
- 定义规则：当 Path Card Audit 输出包含 `source_gap` 项时，自动在队列末尾追加一个 Source Gap Audit 任务（带 `spawned_by` 引用）。
- **严格有界**：每个任务最多 spawn 2 个后续任务，depth ≤ 2，防止无限递归。

**约束兼容性**: 兼容。纯队列逻辑扩展。

### P3 · 分析师角色配置化（轻量，可选）

institute-one 的 `catalog/analysts.json` 将分析师定义为配置：id、name、focus、persona、hand、model。

CDS4WorldCup 可以定义自己的"分析师"角色（不是真正的 AI agent，而是 MiMo 在 sprint 中切换的 prompt 人格）：

- `path-analyst`：路径空间分析师，负责夺冠路径推演。
- `source-auditor`：来源审计员，负责 source_level 判定和缺口识别。
- `match-context-analyst`：比赛上下文分析师，负责赛前准备。
- `settlement-analyst`：结算分析师，负责赛后事实核对。
- `cognitive-auditor`：认知审计员，负责偏差总结。

每个角色有固定的 persona、focus 和 prompt 块，存储在 `data/ops/roles/` 下。MiMo 在执行任务时按角色加载对应 prompt 块。

**收益**: 减少 prompt drift，让不同 sprint 中同一类型任务的输出风格一致。

**约束兼容性**: 兼容。纯配置化，无新依赖。

> **P1-P3 综合分析**: institute-one 的可借鉴机制呈现清晰的"由近及远"层次。P1 的 Prompt 三明治和条件认领属于**零依赖、零架构改动**的即时优化，其核心价值在于将隐性约束显性化——把目前分散在总控文档中的纪律转化为可复用的代码层，降低人类操作者的认知负荷。P2 的 VaultWriter 和事件批注则触及 CDS4WorldCup 当前架构的一个隐性脆弱点：MiMo 与人类在 `candidate/` 和 `mimo_outputs/` 上的并发写入缺乏仲裁机制，覆盖风险虽低但一旦发生便难以追溯。P3 的角色配置化和跟随机制属于**中期增强**，其价值取决于前两个阶段是否跑通；如果 Prompt 标准化和队列状态机未落地，角色配置只会增加配置负担而不会提升输出质量。总体判断：优先实施 P1，验证后再进入 P2，P3 视赛季中期运营反馈决定。

## 4. 不建议引入的机制

| 机制 | 不建议原因 |
|---|---|
| **SQLite + FastAPI 常驻进程** | CDS4WorldCup 明确约束"不引入数据库或在线服务"，且当前无常驻进程需求。引入常驻进程会彻底改变项目架构。 |
| **Hands / CLI 调度层** | institute-one 的 hands 层是为了调度 claude/codex/gemini CLI。CDS4WorldCup 的 MiMo 是单一长程 agent，没有多 hand 调度需求。 |
| **SSE / Web UI** | 当前项目通过 GitHub Pages 发布静态结果，没有实时 Web UI 需求。Obsidian 插件也不适用（项目使用 Marginalia 而非 Obsidian vault）。 |
| **APScheduler 自动调度** | 项目约束 MiMo 为"人工启动的 12-24 小时 sprint"，不是全自动运行。自动调度会违反当前运营模型。 |
| **FTS5 / sqlite-vec 搜索** | 知识库是纯 Markdown，搜索可以通过 `scripts/audit.py` 或简单 grep 完成。引入 sqlite-vec 需要数据库。 |
| **MCP 服务器接口** | 当前没有外部工具需要查询 CDS4WorldCup 的需求。未来如果有，可以单独评估。 |

## 5. 优先级与行动建议

```
Phase 1（本周可做，零依赖）
  ├── src/utils/prompt_builder.py — Prompt 三明治构建器
  ├── task_queue.json 状态机 + 乐观锁 + 超期回收
  └── docs/ops/mimo-season-campaign.md 引用 prompt_builder 规范

Phase 2（下周可做，零依赖）
  ├── src/utils/vault_writer.py — candidate/ 和 mimo_outputs/ 的安全写入
  ├── data/ops/events.jsonl + scripts/audit.py --events
  └── data/ops/workflows/ — 标准任务 JSON 模板（Path Card Audit、Settlement 等）

Phase 3（赛季中期，可选）
  ├── data/ops/roles/ — 分析师角色配置化
  └── task_queue.json 跟随机制（spawned_by + depth cap）
```

## 6. 关键设计原则与综合结论

institute-one 的架构设计贯穿了一条核心主线：**将不确定性隔离在边界内，让可恢复性成为默认属性**。这条主线在 CDS4WorldCup 的约束条件下需要被转译为 Markdown 和 JSON 语境下的等价实践。

Prompt 是研究基础设施的产品形态，而非可随意重构的辅助文本。institute-one 的 `CLAUDE.md` 将"Never paraphrase existing prompt strings"列为硬规则，其背后是对 prompt 作为行为契约的尊重——一旦 prompt 措辞漂移，输出分布便会不可预测地偏移。CDS4WorldCup 若实施 Prompt 三明治标准化，必须同样遵守"只移动和拼接，不改写措辞"的原则，将总控文档中的纪律性表述原封不动地编码为 `prompt_builder.py` 的常量。

状态与产出的分离是另一项关键原则。institute-one 用 SQLite rows 承载 truth，Obsidian notes 承载人类可读的 projections。CDS4WorldCup 的等价设计是 `task_queue.json` 与 `campaign_state.json` 作为 truth source，`candidate/` 和 `mimo_outputs/` 作为可重建的投影——这意味着任何对产出文件的直接编辑都应被视为临时操作，持久状态必须回流到 JSON truth 中。

容错与有界性是长程自动化不可妥协的底线。MiMo sprint 中单个任务的失败不应中断整个 sprint，正如 institute-one 的 scheduler jobs 被 `metered()` 包裹后永远不会 raise 到调度器层面。同理，任何任务间联动机制——无论是 follow-up spawn 还是自动审计触发——都必须携带硬性上限：深度不超过 2 层，每任务 spawn 不超过 2 个后续任务，防止认知劳动的无限膨胀侵蚀人类审核的边界。

并发控制虽然在当前单线程 MiMo sprint 中看似不必要，却是未来扩展的隐形门槛。条件认领惯用法（`UPDATE … WHERE status='pending'`）的 JSON 等价物是乐观锁：`version` 字段在读取时 snapshot，写回时比对， mismatch 则放弃当前操作并重新读取。这一机制的成本极低——一个整数字段、一次比对逻辑——却能在未来任何并发场景下避免静默的数据丢失。

综上，institute-one 对 CDS4WorldCup 的最大价值不在于其技术栈的移植，而在于其**设计原则的转译**：将常驻进程中的并发安全、状态持久化和有界递归，映射到无进程、纯文件的约束环境中，找到最小可行实现。

## 7. 相关页面

- [[decisions/mimo-season-campaign-ops]]
- [[decisions/cds4worldcup2026-path-space-spec]]
- [[concepts/cds]]

> [!memo] 2026-06-12 完成对 institute-one 的静态审计
>
> 来源：用户要求研究 `/Users/tangzw119/Documents/GitHub/0ref/institute-one` 对 CDS4WorldCup 的可优化点。
> 上下文：审计覆盖了 institute-one 的 executor、scheduler、bus、vault/writer、workflows、research、prompts、analysts.json 和 ROADMAP。结论是可借鉴的机制集中在 prompt 工程、状态机、安全写入和任务模板化，不建议引入常驻进程、数据库或 Web UI。

---

## 8. 第二轮深度审计：GLM-5V-Turbo 补充洞察

> **审计者**: GLM-5V-Turbo
> **审计时间**: 2026-06-12
> **审计方法**: 源码级实现模式提取 + CDS4WorldCup 运营文档交叉映射
> **范围**: 聚焦于第一轮审计未覆盖的**运行时行为模式**、**错误处理哲学**、**上下文管理策略**及**运营卫生机制**

### 8.1 审计方法论说明

第一轮审计（kimi-k2.6 执行）已系统性地覆盖了 institute-one 的**架构层**可借鉴点（prompt 三明治、条件认领、VaultWriter、事件批注、工作流 JSON、跟随机制、角色配置化）。本轮融资不重复上述内容，而是深入到**实现细节层**，提取那些在代码审查中才能发现的隐性设计模式，并评估它们在 CDS4WorldCup 的 MiMo sprint 运营场景中的转译可行性。

### 8.2 上下文压缩引擎：`previous_steps_block()` 模式

#### 已有审计的覆盖边界

第一轮 P1 提到了"Prompt 三明治标准化"，聚焦于 prompt 的**结构**（日期锚点 → 人格 → 上下文 → 任务 → 引用规范 → 交付物）。但未触及一个更深层的问题：**多步骤工作流中，前序步骤的输出如何注入后续步骤而不撑爆上下文窗口**。

#### institute-one 的解法

[institute-one/app/institute/prompts.py](file:///Users/tangzw119/Documents/GitHub/0ref/institute-one/app/institute/prompts.py#L51-L63) 中的 `previous_steps_block()` 函数：

```python
def previous_steps_block(results: list[tuple[str, str]], budget_chars: int = 8000) -> str:
    """results: [(title, summary)]. Bounded context from earlier steps."""
    if not results:
        return ""
    parts = ["## 前序步骤结论（摘要）"]
    per = max(500, budget_chars // max(len(results), 1))
    for title, summary in results:
        s = (summary or "").strip()
        if len(s) > per:
            s = s[:per] + "…"
        parts.append(f"### {title}\n{s}")
    block = "\n\n".join(parts)
    return block[:budget_chars]
```

关键设计决策：
1. **硬性预算约束**：`budget_chars=8000`，无论多少步骤，总上下文不超过此值
2. **均摊 + 下限**：每个步骤至少 500 字符 (`max(500, budget_chars // n)`)，防止步骤过多时被压缩为零
3. **智能摘要优先**：[extract_summary()](file:///Users/tangzw119/Documents/GitHub/0ref/institute-one/app/institute/prompts.py#L91-L99) 先尝试抽取 `## 核心结论` 段，失败才截断头部
4. **渐进式累积**：在 [workflows._drive()](file:///Users/tangzw119/Documents/GitHub/0ref/institute-one/app/institute/workflows.py#L163-L199) 中，每完成一步就 `prior.append((title, summary))`，下一步自动获得所有前序摘要

#### 对 CDS4WorldCup 的转译价值

CDS4WorldCup 的 MiMo sprint 中存在天然的多步骤任务链。以 [mimo-season-campaign.md 第 5 节](file:///Users/tangzw119/Documents/GitHub/cds4worldcup/docs/ops/mimo-season-campaign.md#L347-L507) 定义的 9 种标准任务为例：

| 任务链 | 步骤数 | 上下文膨胀风险 |
|--------|--------|---------------|
| Path Card Audit → Source Gap Audit → Formal Change Proposal | 3 | 高：每队路径卡 ~2KB，48 队 = 96KB 原始 |
| Match Context → Prediction Card → Settlement → Autopsy | 4 | 极高：每场比赛上下文包可能 >5KB |
| Source Fetch Diagnostics → Source Gap Audit → Baseline Population | 3 | 中：诊断日志可能很长 |

当前问题：MiMo 在执行这些链式任务时，倾向于把前序任务的完整输出塞入后续 prompt，导致：
- 后续步骤的 prompt 被"历史噪声"稀释
- 关键信号（source gap、settlement_rule 不一致）淹没在冗余信息中
- token 预算浪费在重复信息上

**建议实施方案**：

在 `src/utils/context_compressor.py` 中实现轻量版：

```python
def compress_prior_outputs(
    outputs: list[dict],  # [{"title": ..., "content": ..., "key_findings": [...]}]
    budget_tokens: int = 2000,
) -> str:
    """将前序任务输出压缩为有界上下文块。"""
```

核心规则：
- 每个 output 保留 `key_findings` 列表（结构化抽取），而非原始文本
- 总 token 数不超过 `budget_tokens`
- 最后一步总是包含完整的前一步输出（最近邻不压缩）
- 压缩后的块以 `## 前序任务摘要` 标题注入下一个 prompt

**约束兼容性**: 完全兼容。纯 Python 函数，零依赖，可作为 `prompt_builder.py` 的 companion 模块。

### 8.3 错误隔离哲学：`metered()` 装饰器与三层容错

#### 已有审计的覆盖边界

第一轮在第 6 节"关键设计原则"中提到了"scheduler jobs 被 `metered()` 包裹后永远不会 raise 到调度器层面"，但未展开其**完整的错误处理栈**和**对 CDS4WorldCup 的具体转译模式**。

#### institute-one 的三层容错栈

通过源码分析，institute-one 实际上实现了**三层错误隔离**：

**第一层：调度器边界 — `metered()` 装饰器**
[institute-one/app/institute/scheduler.py](file:///Users/tangzw119/Documents/GitHub/0ref/institute-one/app/institute/scheduler.py#L52-L68)：

```python
def metered(name: str, *, gated: bool = False) -> Callable[..., Callable[..., None]]:
    def deco(fn):
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs):
            try:
                if gated and await get_maintenance():
                    return  # 安全区：维护模式下跳过
                t0 = time.monotonic()
                await fn(*args, **kwargs)
                dt = time.monotonic() - t0
                log.log(logging.INFO if dt >= 1.0 else logging.DEBUG, ...)
            except Exception:  # noqa: BLE001 - 永远不 raise
                log.exception("job %s failed", name)
        return wrapper
    return deco
```

关键属性：
- **永不传播异常**：`except Exception` 吞掉所有错误，调度器永远存活
- **可选维护门控**：`gated=True` 时检查 maintenance flag，全局暂停非关键任务
- **耗时感知日志**：>=1s 的任务记 INFO，否则 DEBUG

**第二层：执行器边界 — `executor._execute()` 异常分类**
[institute-one/app/router/executor.py](file:///Users/tangzw119/Documents/GitHub/0ref/institute-one/app/router/executor.py#L113-L193) 将异常分为四类，每类有不同的恢复策略：

| 异常类型 | 处理方式 | 状态标记 | 是否重试 |
|----------|---------|----------|---------|
| `asyncio.TimeoutError` | 记录 rate_limit，标记 expired | 不重试 | 否 |
| `asyncio.CancelledError` | 标记 cancelled，re-raise | 向上传播 | 否 |
| Hand crash (Exception) | compact_error，标记 failed | 不重试 | 否 |
| Rate limit | 自动 fallback 到 chain 中下一个 hand | 重试一次 | 是 |

**第三层：工作流驱动器边界 — `_drive()` 的 step 级隔离**
[institute-one/app/institute/workflows.py](file:///Users/tangzw119/Documents/GitHub/0ref/institute-one/app/institute/workflows.py#L146-L222)：

```python
for i, step in enumerate(wf["steps"]):
    current = await db.query_one(...)  # 每步开始前检查 run 是否仍为 running
    if current is None or current["status"] != "running":
        return  # 已取消，优雅退出
    # ... 执行 step ...
    if task.status != "completed":
        await _finish_run(run_id, "failed", error=...)
        return  # 单步失败，终止整个 workflow（但不 raise）
```

关键设计：
- **步间取消检测**：每步开始前检查 run status，支持外部取消
- **fail-fast 语义**：任何一步失败立即终止整个 workflow（不跳过、不继续）
- **永不 raise**：最外层的 `except Exception` 确保 create_task 的调用者不会收到异常

#### 对 CDS4WorldCup 的转译价值

当前 CDS4WorldCup 的 MiMo sprint 错误处理隐含在 [mimo-season-campaign.md 4.3](file:///Users/tangzw119/Documents/GitHub/cds4worldcup/docs/ops/mimo-season-campaign.md#L244-L277) 的文字描述中（"如果无法达到以上深度，不要把任务标记为 done，应标记为 partial"），但没有**代码级的强制执行机制**。

建议实施**MiMo 任务错误分类表**，写入 `docs/ops/` 或编码为 `src/utils/task_guard.py`：

| 错误类别 | 触发条件 | MiMo 行为 | task_queue 状态 | 是否生成 follow-up |
|----------|---------|-----------|-----------------|-------------------|
| `source_blocked` | 外部来源抓取全失败（经 2.1.2 诊断后） | 标记 blocked，写 diagnostics | `blocked` + `blocking_reason` | 是：生成 source_mirror_task |
| `auth_required` | 需要修改正式文件但无 APPROVE_FORMAL_MUTATION | 转 formal change proposal | `waiting_approval` | 否：等人类 |
| `partial_complete` | 任务部分完成，有明确缺口 | 标记 partial，列 gaps | `partial` + `gap_list` | 是：每个 gap 一个补证任务 |
| `context_overflow` | 输出超过预算深度（4.3.1） | 标记 partial，压缩后提交 | `partial` + `depth_note` | 可选 |
| `tool_failure` | 工具/权限/文件系统不可恢复错误 | 写诊断，结束 sprint | `failed` + `diagnostics` | 否 |

**特别值得借鉴的是 `gated` 概念**：CDS4WorldCup 可以引入一个 `data/ops/ops_state.json` 中的 `maintenance_mode` 字段。当设为 true 时，MiMo 只执行"安全任务"（review_queue_quality_audit、candidate_source_package 等），不执行可能触发正式变更的任务。

### 8.4 结构化跟随输出：从自由文本到机器可解析的 action block

#### 已有审计的覆盖边界

第一轮 P2 提到了"跟随机制与有界递归"的概念（task_queue 中增加 `spawned_by` 和 `spawn_triggers`），但未涉及**跟随输出的数据格式**问题。

#### institute-one 的解法

[institute-one/app/institute/research.py](file:///Users/tangzw119/Documents/GitHub/0ref/institute-one/app/institute/research.py#L186-L268) 中的 follow-up 机制要求研究最后一步输出一个**严格的 JSON block**：

```json
{
  "whiteboard_topics": [
    {"topic": "主题", "question": "具体问题"}
  ],
  "mailbox_followups": [
    {"analyst_id": "名册id", "subject": "追问标题", "body": "追问内容"}
  ]
}
```

然后由 [parse_followups()](file:///Users/tangzw119/Documents/GitHub/0ref/institute-one/app/institute/research.py#L195-L223) 进行**防御性解析**：

```python
def parse_followups(text: str) -> dict[str, list[dict]]:
    """Extract the follow-ups JSON block. Defensive: any failure -> empty lists."""
    out = {"whiteboard_topics": [], "mailbox_followups": []}
    # ... 正则提取 ```json ... ``` block ...
    # ... 类型校验、字段截断（MAX_FOLLOWUP_TOPICS=3, MAX_FOLLOWUP_MAILS=2） ...
    return out
```

关键设计属性：
1. **Schema 强制**：JSON 结构是 prompt 的一部分，不是可选的
2. **防御性解析**：任何解析失败返回空列表，不会崩溃
3. **硬性上限**：topics ≤ 3, mails ≤ 2，在解析层截断
4. **程序化分发**：解析结果直接调用 `whiteboard.add_topic()` 和 `mailbox.create_thread()`

#### 对 CDS4WorldCup 的转译价值

当前 CDS4WorldCup 的 MiMo 任务产出中，"后续行动"通常以自然语言段落形式出现在 `next_actions` 或 review_notes 中。这意味着：
- 人类需要阅读整个输出才能提取后续任务
- MiMo 无法在新 sprint 中自动读取上一轮的"建议后续动作"
- `task_queue.json` 的新任务依赖人工转录

建议为 CDS4WorldCup 定义**标准化的 action block schema**，嵌入每种标准任务类型的 prompt 尾部：

```json
{
  "spawn_tasks": [
    {
      "type": "source_gap_audit | match_context | settlement | path_card_patch",
      "priority": "high | medium | low",
      "target": "team_id 或 match_id 或 topic",
      "triggered_by": "当前任务中哪条发现触发了此任务",
      "depends_on_approval": false,
      "safe_without_approval": true
    }
  ],
  "blocking_issues": [
    {
      "type": "source_blocked | auth_required | data_conflict",
      "description": "...",
      "suggested_unblock_task": "..."
    }
  ]
}
```

然后在 sprint 开始时，增加一个**action block 解析步骤**：扫描上一轮 `candidate/` 和 `mimo_outputs/` 中所有包含 `## 后续行动` 或 action block JSON 的文件，将 `spawn_tasks` 自动追加到 `task_queue.json`。

**约束兼容性**: 完全兼容。纯约定层改动——在任务类型定义中增加 output schema 要求，在 sprint 启动流程中增加解析逻辑。

### 8.5 Janitor 模式：运营卫生自动化

#### 已有审计的覆盖边界

第一轮完全未提及 institute-one 的 janitor（运维清理）机制。

#### institute-one 的解法

[institute-one/app/institute/scheduler.py](file:///Users/tangzw119/Documents/GitHub/0ref/institute-one/app/institute/scheduler.py#L116-L176) 中的 `_janitor()` 函数每 60 分钟执行一次，负责四项清理：

| 清理项 | 规则 | 目的 |
|--------|------|------|
| 卡死的 workflow runs | running >6h 且无活跃 task → 标记 expired | 释放被占用的逻辑资源 |
| 过期的 topic pool 条目 | pending >14 天 → 标记 expired | 防止队列无限增长 |
| 旧 adhoc workspaces | 创建 >7 天 → 删除 | 回收磁盘空间 |
| 数据库备份 | 03:00-05:00 SGT 窗口，每日一次 | 灾难恢复 |

关键设计原则：
- **只标记不删除**（除了 workspace）：状态变更为 expired/failed，不物理删除业务数据
- **时间窗口限制**：备份只在低峰期执行
- **幂等性**：重复执行安全

#### 对 CDS4WorldCup 的转译价值

CDS4WorldCup 当前没有自动清理机制。随着 sprint 轮次增加，以下目录会持续增长：

| 目录 | 增长速度 | 风险 |
|------|---------|------|
| `data/ops/mimo_outputs/` | 每 sprint ~10 个文件（checkpoint、日志、诊断） | 磁盘占用 + 干扰人类查找 |
| `data/ops/candidate/` | 每 sprint ~5-15 个文件 | 过时 candidate 污染审核队列 |
| `data/ops/review_queue/` | 已审核文件不会被自动归档 | 人工需手动区分已审/待审 |
| `results/ops/` | 每 sprint 1 个 sprint summary | 低风险，但有积累 |

建议实现 `scripts/janitor.py`（零依赖 Python 3.10+）：

```python
# 伪代码
def cleanup():
    # 1. 归档 >7 天的 mimo_outputs 到 archive/
    # 2. 标记 >14 天且 status=approved 的 review_queue 为 archived
    # 3. 报告各目录文件数和总大小
    # 4. 可选：清理 >30 天的 candidate 文件（移至 archive/）
```

并在每次 sprint 启动时自动运行（作为 4.1 恢复状态的一部分）。

**约束兼容性**: 完全兼容。纯脚本，不影响任何运行时行为，只做文件整理。

### 8.6 Per-Entity 幂等守卫：防重复执行

#### 已有审计的覆盖边界

第一轮未提及 per-entity completion guard 模式。

#### institute-one 的解法

[institute-one/app/institute/analyst_daily.py](file:///Users/tangzw119/Documents/GitHub/0ref/institute-one/app/institute/analyst_daily.py#L41-L62) 中的 `_guard_key()` / `_mark()` / `_get_record()` 组合：

```python
def _guard_key(date: str | None = None) -> str:
    return f"analyst_daily:{date or work_date()}"

async def _mark(analyst_id: str, status: str) -> None:
    record = await _get_record()
    record[analyst_id] = status
    await db.execute(...)  # upsert admin_state

# 使用处：
if record.get(analyst_id) == "completed":
    return {"skipped": "already completed today"}
```

效果：每个分析师每天最多执行一次日报，即使 scheduler 误触发多次也不会重复消耗 quota。

#### 对 CDS4WorldCup 的转译价值

CDS4WorldCup 存在类似的重复执行风险：
- 同一球队在同一 sprint 内被多次执行 Path Card Audit
- 同一比赛同时生成 Match Context 和 Prediction Card 导致上下文不一致
- Source Gap Audit 对同一 topic 反复执行

建议在 `campaign_state.json` 中增加 `entity_completion_log` 字段：

```json
{
  "entity_completion_log": {
    "path_card_audit": {"BRA": "sprint-003", "ARG": "sprint-003"},
    "match_context": {"BRA-ARG-2026-06-23": "sprint-003"},
    "source_gap_audit": {"team_registry_completeness": "sprint-002"}
  }
}
```

规则：
- 同一 entity + 同一任务类型在同一 sprint 内只执行一次
- 新 sprint 开始时清空（或保留跨 sprint cooldown）
- MiMo 选择任务时先查此 log，已完成的跳过

**约束兼容性**: 完全兼容。纯 JSON 字段扩展，一行逻辑。

### 8.7 Session Workspace 隔离：防止跨 Sprint 污染

#### 已有审计的覆盖边界

第一轮未提及 workspace 隔离模式。

#### institute-one 的解法

每次 workflow run 创建独立 session：
[institute-one/app/institute/workflows.py](file:///Users/tangzw119/Documents/GitHub/0ref/institute-one/app/institute/workflows.py#L87-L104)：

```python
session = await sessions.create_session(f"{wf['name']} {work_date()}", kind="workflow")
# session 有独立的 workspace_dir：workspaces/<session_id>/
```

所有步骤的输入输出都在同一 workspace 内完成。完成后 [archive.snapshot_session()](file:///Users/tangzw119/Documents/GitHub/0ref/institute-one/app/institute/archive.py#L31-L88) 将产物复制到 archive tree，workspace 可被 janitor 安全删除。

#### 对 CDS4WorldCup 的转译价值

当前 CDS4WorldCup 的 MiMo 所有输出都直接写到共享目录（`data/ops/candidate/`、`data/ops/mimo_outputs/`）。这导致：
- 不同 sprint 的文件混在一起，只能靠文件名日期区分
- 无法区分"本轮新生成的"和"之前遗留的"
- sprint 间切换时需要人工清理或冒着使用过时数据的风险

建议为每轮 sprint 创建隔离 workspace：

```
data/ops/sprints/
  sprint-2026-06-12-s001/     ← 本轮 sprint 的专属 workspace
    candidate/                ← 本轮生成的候选材料
    outputs/                  ← 本轮的 checkpoint 和日志
    workspace.json            ← 元数据：启动时间、任务列表、状态
```

Sprint 结束时：
- 将需要审核的文件**链接或复制**到 `review_queue/`
- 将需要持久化的结果**复制**到 `results/ops/`
- 整个 sprint directory 可被 janitor 归档或删除

**约束兼容性**: 兼容。需要调整 `mimo-season-campaign.md` 第 2.3 节的允许写入目录清单，但本质上是目录结构的重组。

### 8.8 综合优先级评估：新增项如何融入现有 Phase 计划

将本轮融资发现映射到第一轮的 Phase 计划：

| 新发现 | 优先级 | 融入 Phase | 理由 |
|--------|--------|-----------|------|
| 上下文压缩引擎 (`context_compressor.py`) | **P1 提升** | Phase 1 | 直接解决 MiMo sprint 中"任务越做越长、上下文越来越噪"的核心痛点；实现成本极低（~100 行纯函数） |
| 错误分类表 + gated maintenance | **P1 提升** | Phase 1 | 将隐含在文字描述中的错误处理策略显式化为可执行的规则；`maintenance_mode` 概念对授权阻塞场景（4.2.1）有直接价值 |
| 结构化 action block schema | **P2** | Phase 2 | 依赖 Phase 1 的 prompt_builder 基础设施；能让"跟随机制"从概念变为可自动化执行 |
| Per-entity 幂等守卫 | **P2** | Phase 1（附带） | 一行 JSON 字段 + 一行判断逻辑，几乎零成本，应随 Phase 1 一起实施 |
| Session workspace 隔离 | **P3** | Phase 2 或 3 | 需要调整目录结构和 campaign doc，属于中等规模的运营重构 |
| Janitor 清理脚本 | **P3** | Phase 2（附带） | 可作为 vault_writer 或独立脚本实施；不紧急但随着时间推移会越来越必要 |

### 8.9 关键差异再确认：为什么这些模式在第一轮中被遗漏

第一轮审计采用了**架构组件映射**的方法（executor ↔ ?, scheduler ↔ ?, bus ↔ ?），这种方法擅长识别"大模块"级别的对应关系，但容易遗漏以下类型的模式：

1. **函数级惯用法**：`previous_steps_block()`、`extract_summary()`、`parse_followups()`、`compact_error()` —— 这些是几十行的工具函数，不属于任何"模块"，却在运行时质量中扮演关键角色。
2. **装饰器/中间件模式**：`metered()` —— 它是一个横切关注点，不属于任何业务域，却定义了整个系统的错误处理哲学。
3. **运营卫生机制**：janitor —— 它不直接参与"研究"功能，却是系统长期运行的保障。
4. **数据格式约定**：follow-up JSON schema —— 它不是一个"功能"，而是一个"约定"，隐藏在 prompt 文本和解析函数之间。

这些模式的共同特征是：**它们不在架构图上，但在日志里、在 debug 会话里、在"为什么这个任务又跑了第二次"的疑问里**。对于 CDS4WorldCup 这样一个以 MiMo sprint 为核心运营模式的项目，这些"隐形模式"的价值可能比显式架构组件更高——因为 MiMo sprint 的主要挑战不是"缺少某个功能"，而是**运行的稳定性、产出的可追溯性和运营的可持续性**。

> [!memo] 2026-06-12 GLM-5V-Turbo 第二轮深度审计完成
>
> 来源：用户要求研究 `/Users/tangzw119/Documents/GitHub/0ref/institute-one` 对 CDS4WorldCup 的可优化点（补充审计）。
> 方法论：源码级实现模式提取，聚焦于第一轮（kimi-k2.6 执行）未覆盖的运行时行为模式。
> 核心发现：(1) 上下文压缩引擎 `previous_steps_block()` 可直接解决 MiMo 多步骤任务上下文膨胀问题；(2) `metered()` 三层容错栈的错误分类哲学可转译为 MiMo 任务错误分类表；(3) 结构化 follow-up JSON schema 可让"后续行动"从自由文本变为机器可解析的 action block；(4) janitor / per-entity guard / workspace isolation 三项运营卫生机制。
> 结论：新增发现中，上下文压缩和错误分类应提升至 P1 与第一轮的 Prompt 三明治并行实施；其余融入 Phase 2。

---

## 9. 补充认知：AI-first 开发范式与测试策略

> **作者**: GLM-5
> **时间**: 2026-06-12
> **研究方法**: 深度代码审计 + 架构映射 + 实践模式提取

### 8.1 Vibe-coding 工作流：从代码生成到知识生成

institute-one 的 ROADMAP.md 揭示了一个关键设计哲学：**整个代码库是由 AI agents 在一天内完成的**，并且设计为持续保持"易于用 AI agents 扩展"的特性。这种 AI-first 开发范式对 CDS4WorldCup 的 MiMo sprint 模式具有直接的借鉴价值。

**核心机制**：每个 ROADMAP 里程碑都是自包含的，包含：
- **Grounding**：明确指向 proposal 的哪个章节、哪个 legacy 源码、哪些当前文件
- **Ready-to-paste prompt**：关键里程碑附带可直接粘贴给 AI agent 的完整 prompt
- **Effort estimate**：S/M/L 工作量评估（基于 AI agent 执行时间）
- **Dependency arrows**：清晰的依赖关系图

**对 CDS4WorldCup 的启示**：当前的 `docs/ops/mimo-season-campaign.md` 定义了 8 种标准任务类型，但每个任务都是自由文本描述。可以借鉴 ROADMAP 的结构化方式，为每种任务类型创建"自包含里程碑"：

```markdown
# Path Card Audit 任务模板

**Grounding**: wiki/concepts/path-card.md + data/ops/task_queue.json
**Effort**: M (约 1 小时 MiMo 执行时间)
**Dependencies**: 无

**Ready-to-paste prompt**:
> 执行 Path Card Audit 任务：
> 1. 读取 data/processed/teams.json 获取所有 48 支球队
> 2. 对每支球队，检查 wiki/teams/{team_id}.md 是否存在
> 3. 验证每个 Path Card 包含：夺冠概率、关键路径、来源等级
> 4. 输出到 data/ops/candidate/path_card_audit_{date}.md
> 5. 更新 task_queue.json 标记完成
```

这种结构化的任务模板能够显著降低 MiMo sprint 的 prompt drift，让不同 sprint 中同一类型任务的输出风格保持一致。更重要的是，它将"任务定义"从"任务执行"中分离出来，使得任务本身成为可版本控制、可迭代优化的知识资产。

**战略意义**：institute-one 的 vibe-coding 工作流实际上是一种"元编程"实践——用 prompt 定义系统行为，用 ROADMAP 管理系统演进。CDS4WorldCup 可以将这种模式移植到 MiMo sprint 中，将每个标准任务类型视为一个"可 vibe 的里程碑"，从而实现"用 AI 管理 AI"的闭环。这不仅提高了任务执行的可复现性，更重要的是建立了一种"知识沉淀 → prompt 优化 → 任务改进"的正向循环机制。

### 8.2 零配额测试策略：echo hand 的完整实现

institute-one 的测试策略展示了一种优雅的"零配额测试"模式，这对 CDS4WorldCup 如何验证 MiMo sprint 的正确性具有重要借鉴意义。

**核心设计**：
- **Echo hand**：内置的测试用 hand，不调用任何真实 API，只通过 `WRITE_FILE:` prompt 约定写入文件
- **conftest.py**：在导入任何 app 模块之前配置环境，禁用所有真实 CLI hand，强制使用 echo hand
- **Fresh DB per test**：每个测试都从干净的数据库状态开始，测试结束后清理所有后台任务
- **Module-level primitives rebinding**：asyncio locks、semaphores 等模块级原语在每个测试中重新绑定到当前 event loop

**测试示例分析**（`test_whiteboard.py`）：
```python
async def test_tick_drives_board_to_completed_on_echo():
    # 1. 准备测试数据
    await whiteboard.add_topic("宏观利率走向", "美联储下一步会怎么走？", source="test")
    board_id = await whiteboard.kickoff()

    # 2. 驱动状态机直到完成
    for _ in range(20):
        await whiteboard.tick()
        await _drain_bg()  # 等待后台任务完成
        board = await whiteboard.get_board(board_id)
        if board["status"] != "active":
            break

    # 3. 验证最终状态
    assert board["status"] == "completed"
    assert all(c["status"] == "completed" for c in cards)
    assert all(c["summary"] for c in cards)
```

**对 CDS4WorldCup 的启示**：当前项目缺乏对 MiMo sprint 的自动化测试机制。可以借鉴 institute-one 的模式：

1. **创建 `src/utils/echo_executor.py`**：模拟 MiMo 的执行行为，不调用真实 API，通过文件系统约定验证输出
2. **定义测试约定**：每个标准任务类型都有对应的测试用例，验证输入 → 输出的转换逻辑
3. **Fresh state per test**：每次测试都从干净的 `data/ops/` 状态开始，测试结束后清理
4. **后台任务 draining**：MiMo sprint 可能产生后台任务（如 follow-up spawn），需要等待所有任务完成后再验证

**实施建议**：
```python
# tests/test_path_card_audit.py
async def test_path_card_audit_generates_valid_output():
    # 准备测试数据
    setup_test_teams_data()

    # 执行任务（使用 echo executor）
    result = await execute_path_card_audit(use_echo=True)

    # 验证输出
    assert result["status"] == "completed"
    assert Path(result["output_file"]).exists()
    assert "夺冠概率" in Path(result["output_file"]).read_text()
```

**战略意义**：零配额测试策略的核心价值在于"将验证成本降至零"。institute-one 通过 echo hand 实现了"每次代码变更都可以运行完整测试套件而不消耗任何 API 配额"，这对 CDS4WorldCup 的 MiMo sprint 迭代至关重要。当前项目的 MiMo sprint 缺乏自动化验证机制，每次修改 prompt 或任务逻辑后都需要人工启动一次完整的 sprint 来验证正确性，这不仅消耗时间，更重要的是消耗了"快速迭代"的能力。引入 echo executor 后，可以在几分钟内验证整个 sprint 的逻辑正确性，从而建立"修改 → 测试 → 部署"的快速反馈循环。

### 8.3 合约优先的并行生成：防止 drift 的架构约束

institute-one 的 ROADMAP.md 提出了一个关键原则：**"Contracts before fan-out"**。这一原则对 CDS4WorldCup 的 MiMo sprint 如何组织多个并行任务具有深刻的指导意义。

**核心思想**：
> When generating multiple modules in parallel, write the shared interfaces (schema, function signatures) first, by hand or in one shot — generators that read contracts don't drift.

**实践模式**：
1. **先定义合约**：schema、函数签名、数据结构
2. **并行生成实现**：多个 AI agent 同时基于合约生成代码
3. **合约作为约束**：生成器读取合约，不会漂移

**对 CDS4WorldCup 的启示**：当前项目的 MiMo sprint 在执行多个并行任务时，容易出现"任务间不一致"的问题。例如：
- Path Card Audit 输出的球队 ID 格式与 Match Context Candidate 期望的格式不一致
- 不同任务对"来源等级"的定义理解不同
- 输出文件的命名约定在不同任务间漂移

可以借鉴"合约优先"原则，在 `data/ops/contracts/` 下定义：

```json
// data/ops/contracts/team_id_schema.json
{
  "team_id": {
    "type": "string",
    "pattern": "^[a-z]{3}$",
    "description": "FIFA 三字母代码，小写",
    "examples": ["arg", "bra", "ger"]
  }
}

// data/ops/contracts/source_level_schema.json
{
  "source_level": {
    "type": "string",
    "enum": ["green", "yellow", "red"],
    "description": "来源可信度等级",
    "semantics": {
      "green": "官方来源，可直接作为因子输入",
      "yellow": "半官方来源，需要交叉验证",
      "red": "非官方来源，仅作为叙事材料"
    }
  }
}
```

**实施建议**：
1. **创建 `data/ops/contracts/` 目录**：存放所有共享的数据结构定义
2. **MiMo sprint 启动时加载合约**：在 prompt 中明确引用合约文件
3. **验证输出符合合约**：任务完成后自动检查输出是否符合 schema
4. **合约版本控制**：合约变更需要显式更新，并在 wiki 中记录原因

**战略意义**："合约优先"原则的本质是将"隐性的共同理解"显性化为"显性的共享约束"。institute-one 通过这一原则实现了"多个 AI agent 并行生成代码而不漂移"，这对 CDS4WorldCup 的 MiMo sprint 具有同等价值。当前项目的 8 种标准任务类型之间存在大量隐性的数据依赖和格式约定，这些约定分散在各个文档和代码中，容易在多次 sprint 中漂移。引入显式合约后，可以将这些隐性约定固化下来，使得"任务间的协作"从"基于理解的默契"升级为"基于合约的验证"，从而显著提高 sprint 的可复现性和可维护性。

### 8.4 Prompt 工程的细节实践：bounded context 与 summary extraction

institute-one 的 `prompts.py` 展示了 Prompt 三明治的具体实现细节，其中两个设计尤其值得 CDS4WorldCup 借鉴：**bounded context** 和 **summary extraction**。

**Bounded Context 设计**：
```python
def previous_steps_block(results: list[tuple[str, str]], budget_chars: int = 8000) -> str:
    """results: [(title, summary)]. Bounded context from earlier steps."""
    if not results:
        return ""
    parts = ["## 前序步骤结论（摘要）"]
    per = max(500, budget_chars // max(len(results), 1))
    for title, summary in results:
        s = (summary or "").strip()
        if len(s) > per:
            s = s[:per] + "…"
        parts.append(f"### {title}\n{s}")
    block = "\n\n".join(parts)
    return block[:budget_chars]
```

**关键设计点**：
- **总预算控制**：默认 8000 字符，防止 context 爆炸
- **公平分配**：每个前序步骤平均分配预算
- **硬性截断**：超出预算的部分直接截断，添加省略号
- **最终保护**：整个 block 再次截断到 budget_chars

**Summary Extraction 设计**：
```python
def extract_summary(text: str, cap: int = 800) -> str:
    """Pull the 核心结论 section if present, else the head of the text."""
    marker_hits = [m for m in ("## 核心结论", "# 核心结论", "核心结论") if m in text]
    if marker_hits:
        seg = text.split(marker_hits[0], 1)[1]
        for stop in ("\n## ", "\n# "):
            if stop in seg:
                seg = seg.split(stop, 1)[0]
        return seg.strip()[:cap]
    return text.strip()[:cap]
```

**关键设计点**：
- **智能定位**：优先提取"核心结论"部分
- **多级 marker**：支持多种标题格式
- **边界识别**：遇到下一个标题即停止
- **兜底策略**：无 marker 时提取文本头部

**对 CDS4WorldCup 的启示**：当前项目的 MiMo sprint 在处理多步骤任务时，容易出现"context 爆炸"问题。例如：
- Settlement 任务需要读取所有已完成的 Match Context 文件
- Path Card Audit 需要读取所有球队的 Path Card
- Cognitive Audit 需要读取整个赛季的所有产出

可以借鉴 bounded context 和 summary extraction 的设计：

1. **在 `src/utils/prompt_builder.py` 中实现**：
   - `bounded_context(files: list[Path], budget_chars: int = 8000) -> str`
   - `extract_key_section(file: Path, section_title: str = "核心结论") -> str`

2. **在 MiMo prompt 中应用**：
   ```
   ## 前序任务摘要（预算 8000 字符）
   {bounded_context(previous_task_outputs)}

   ## 当前任务
   {current_task_description}
   ```

3. **标准化输出格式**：
   - 每个任务输出必须包含"## 核心结论"部分
   - 后续任务自动提取该部分作为 context

**战略意义**：bounded context 和 summary extraction 的核心价值在于"在有限的 context 窗口内传递最关键的信息"。institute-one 通过这两个设计实现了"多步骤工作流中每一步都能获得前序步骤的关键信息，而不会因为 context 爆炸而失败"。这对 CDS4WorldCup 的 MiMo sprint 尤其重要，因为世界杯赛季会产生大量文件（48 支球队的 Path Card、64 场比赛的 Match Context、多次 Settlement 报告等），如果不加控制地全部加载到 context 中，会迅速超出模型的 context 窗口限制。引入 bounded context 后，可以确保每个任务都能获得"足够但不过量"的前序信息，从而在"信息完整性"和"context 可控性"之间找到最佳平衡点。

### 8.5 测试驱动的工作流验证：从单元测试到集成测试

institute-one 的测试套件展示了一种"从单元测试到集成测试"的完整验证策略，这对 CDS4WorldCup 如何验证 MiMo sprint 的端到端正确性具有重要借鉴意义。

**测试层次结构**：
1. **单元测试**：验证单个函数的正确性（如 `test_add_topic_dedups_by_hash`）
2. **集成测试**：验证多个模块协作的正确性（如 `test_tick_drives_board_to_completed_on_echo`）
3. **端到端测试**：验证完整工作流的正确性（如从 topic 添加到 board 完成的全流程）

**关键测试模式**：
```python
async def test_tick_drives_board_to_completed_on_echo():
    # 1. 准备初始状态
    await whiteboard.add_topic("宏观利率走向", "美联储下一步会怎么走？", source="test")
    board_id = await whiteboard.kickoff()

    # 2. 驱动状态机
    for _ in range(20):
        await whiteboard.tick()
        await _drain_bg()  # 等待后台任务
        board = await whiteboard.get_board(board_id)
        if board["status"] != "active":
            break

    # 3. 验证最终状态
    assert board["status"] == "completed"
    assert all(c["status"] == "completed" for c in cards)

    # 4. 验证副作用
    events = await bus.replay(0, types=["whiteboard.board_completed"])
    assert len([e for e in events if e.ref_id == board_id]) == 1

    # 5. 验证文件系统
    digest = Path(session["workspace_dir"]) / "_board.md"
    assert digest.is_file()
    assert "宏观利率走向" in digest.read_text()
```

**对 CDS4WorldCup 的启示**：当前项目缺乏对 MiMo sprint 的自动化验证机制。可以借鉴 institute-one 的测试模式：

1. **创建 `tests/sprint/` 目录**：存放所有 sprint 相关的测试
2. **定义测试基类**：
   ```python
   class SprintTestBase:
       async def setup_sprint_env(self):
           # 准备干净的 data/ops/ 环境
           # 加载测试数据
           # 配置 echo executor

       async def drive_sprint_to_completion(self, task_type: str, max_rounds: int = 20):
           # 驱动 sprint 直到完成或超时

       async def verify_final_state(self, task_id: str):
           # 验证任务状态、输出文件、事件日志
   ```

3. **为每种标准任务类型创建测试**：
   - `test_path_card_audit_sprint()`
   - `test_match_context_candidate_sprint()`
   - `test_settlement_sprint()`

4. **验证关键属性**：
   - 任务状态转换正确（pending → running → completed）
   - 输出文件存在且格式正确
   - 事件日志记录完整
   - 文件系统副作用符合预期

**实施建议**：
```python
# tests/sprint/test_path_card_audit.py
async def test_path_card_audit_sprint():
    # 1. 准备环境
    await setup_sprint_env()
    await setup_test_teams_data()  # 创建 48 支球队的测试数据

    # 2. 提交任务
    task_id = await submit_task("path_card_audit", parameters={})

    # 3. 驱动 sprint
    await drive_sprint_to_completion(task_id, max_rounds=20)

    # 4. 验证最终状态
    task = await get_task(task_id)
    assert task["status"] == "completed"

    # 5. 验证输出
    output_file = Path(task["output_file"])
    assert output_file.exists()
    content = output_file.read_text()
    assert "夺冠概率" in content
    assert "来源等级" in content

    # 6. 验证事件
    events = await get_events(ref_id=task_id)
    assert any(e["type"] == "task.completed" for e in events)
```

**战略意义**：测试驱动的工作流验证的核心价值在于"将 sprint 的正确性验证从人工检查转变为自动化测试"。institute-one 通过完整的测试套件实现了"每次代码变更都可以在几分钟内验证整个系统的正确性"，这对 CDS4WorldCup 的 MiMo sprint 迭代至关重要。当前项目的 MiMo sprint 缺乏自动化验证，每次修改 prompt、任务逻辑或数据结构后，都需要人工启动一次完整的 sprint 来验证正确性，这不仅消耗时间，更重要的是无法建立"快速反馈循环"。引入自动化测试后，可以在每次修改后立即验证 sprint 的端到端正确性，从而显著提高迭代速度和系统可靠性。

### 8.6 运维成熟度与可观测性：从日志到健康检查

institute-one 展示了一种"从日志到健康检查"的完整运维成熟度体系，这对 CDS4WorldCup 如何监控 MiMo sprint 的运行状态具有重要借鉴意义。

**运维工具链**：
1. **日志管理**：`~/.institute-one/logs/server.log`，结构化日志
2. **备份机制**：夜间 SQLite 备份到 `~/.institute-one/backups/`（03:00–05:00 SGT）
3. **健康检查**：`POST /api/vault/doctor` 报告 vault drift
4. **状态监控**：`GET /api/tasks/queue` 查看队列状态
5. **维护模式**：`admin_state` key `maintenance` 暂停所有新任务

**关键设计点**：
- **Vault doctor**：对比 ledger vs 磁盘，报告 clean/conflict/missing/drifted 数量
- **Orphan recovery**：重启时自动恢复孤儿任务
- **Quota walls**：per-CLI rate-limit signatures 解析，持久化 cooldowns
- **One CLI = one task**：per-hand mutex，防止并发冲突

**对 CDS4WorldCup 的启示**：当前项目的 MiMo sprint 缺乏系统的运维工具链。可以借鉴 institute-one 的模式：

1. **创建 `scripts/sprint_health.py`**：
   ```python
   def check_sprint_health():
       # 检查 task_queue.json 状态
       # 检查 campaign_state.json 一致性
       # 检查 data/ops/ 目录结构
       # 检查 wiki/ 批注完整性
       # 返回健康报告
   ```

2. **创建 `scripts/sprint_backup.py`**：
   ```python
   def backup_sprint_state():
       # 备份 task_queue.json
       # 备份 campaign_state.json
       # 备份 data/ops/candidate/
       # 备份 data/ops/mimo_outputs/
       # 保存到 data/backups/{date}/
   ```

3. **创建 `scripts/sprint_orphan_recovery.py`**：
   ```python
   def recover_orphan_tasks():
       # 扫描 task_queue.json 中 running 状态的任务
       # 检查 started_at 是否超期
       # 超期任务标记为 stalled
       # 允许下一轮 sprint 重新认领
   ```

4. **在 `docs/ops/mimo-season-campaign.md` 中定义运维流程**：
   - Sprint 启动前：运行 `sprint_health.py` 检查环境
   - Sprint 结束后：运行 `sprint_backup.py` 备份状态
   - Sprint 异常时：运行 `sprint_orphan_recovery.py` 恢复孤儿任务

**实施建议**：
```bash
# Sprint 启动前
python3 scripts/sprint_health.py
# 输出：
# ✅ task_queue.json: 3 pending, 0 running, 5 completed
# ✅ campaign_state.json: consistent
# ⚠️  data/ops/candidate/: 2 files missing source_level
# ✅ wiki/: all pages have recent memo annotations

# Sprint 结束后
python3 scripts/sprint_backup.py
# 输出：
# ✅ Backed up to data/backups/2026-06-12/
#    - task_queue.json
#    - campaign_state.json
#    - candidate/ (15 files)
#    - mimo_outputs/ (8 files)

# Sprint 异常时
python3 scripts/sprint_orphan_recovery.py
# 输出：
# ⚠️  Found 2 orphan tasks (running > 24h)
#    - task_abc123: Path Card Audit (started 2026-06-11 10:00)
#    - task_def456: Match Context Candidate (started 2026-06-11 12:00)
# ✅ Marked as stalled, ready for re-claim
```

**战略意义**：运维成熟度与可观测性的核心价值在于"将 sprint 的运行状态从黑盒转变为白盒"。institute-one 通过完整的运维工具链实现了"任何时候都能准确知道系统状态，任何异常都能快速定位和恢复"，这对 CDS4WorldCup 的 MiMo sprint 长期运行至关重要。当前项目的 MiMo sprint 缺乏系统的运维支持，每次 sprint 的状态分散在多个 JSON 文件和 Markdown 批注中，难以快速评估整体健康状况。引入运维工具链后，可以建立"健康检查 → 状态备份 → 异常恢复"的完整运维闭环，从而显著提高 sprint 的可靠性和可维护性。更重要的是，这些运维工具本身也可以成为 MiMo sprint 的一部分——例如，每周自动运行一次 `sprint_health.py` 并生成健康报告，作为 Cognitive Audit 的输入。

---

## 9. 综合结论与战略建议

institute-one 对 CDS4WorldCup 的借鉴价值不仅在于具体的技术机制，更在于其背后的**设计哲学**：将不确定性隔离在边界内，让可恢复性成为默认属性，将隐性约束显性化，将验证成本降至零。这些哲学在 CDS4WorldCup 的约束条件下需要被转译为 Markdown 和 JSON 语境下的等价实践。

**核心借鉴路径**：
1. **短期（本周）**：实施 Prompt 三明治标准化 + task_queue 状态机
2. **中期（下周）**：实施 VaultWriter 安全规则 + 事件批注 + 任务 JSON 模板
3. **长期（赛季中期）**：实施角色配置化 + 跟随机制 + 运维工具链

**关键成功因素**：
- **合约优先**：先定义共享的数据结构和接口，再实施具体机制
- **测试驱动**：每种机制都有对应的自动化测试，确保正确性
- **渐进式引入**：从零依赖、零架构改动的机制开始，验证后再进入下一阶段
- **运维闭环**：每种机制都有对应的健康检查和恢复工具

**最终目标**：建立一种"AI-first 的知识生成基础设施"，使得 CDS4WorldCup 的 MiMo sprint 能够像 institute-one 的 vibe-coding 工作流一样，实现"用 AI 管理 AI"的闭环，从而在 2026 FIFA 世界杯赛季中持续产出高质量、可校准的路径分析结果。

---

## 8. 深度代码分析补充（kimi-k2.5 追加）

> **作者**: kimi-k2.5  
> **时间**: 2026-06-12  
> **分析深度**: 代码级实现细节

### 8.1 Executor 的并发控制模型

institute-one 的 `executor.py` 实现了一个精密的并发控制层，其核心设计值得深入理解：

**双层锁机制**：
- **全局信号量**（`asyncio.Semaphore`，默认 3）：控制整体并发度，防止系统过载
- **Per-hand 互斥锁**（`dict[str, asyncio.Lock]`）：每个 CLI hand 一次只能执行一个任务，避免同一 CLI 实例的竞态

这种设计的精妙之处在于**资源隔离**——全局信号量保护系统资源，per-hand 锁保护外部 CLI 工具的状态完整性。CDS4WorldCup 当前虽然没有多 hand 场景，但这种分层锁的思维可以应用于：
- 如果未来同时运行多个 MiMo 实例，可以用类似机制避免对同一文件的并发写入
- 对 `task_queue.json` 的读写操作可以视为"单 hand"场景，用文件级锁保护

**条件认领惯用法的实现细节**：
```python
claimed = await db.execute(
    "UPDATE tasks SET status='running', hand=?, model=?, started_at=? WHERE id=? AND status='queued'",
    (hand.name, model, bus.now_iso(), task_id),
)
if claimed == 0:  # cancelled while queued
    return await get_task(task_id)
```

关键点在于**利用数据库的 rowcount 返回值**判断是否真的"抢到了"任务。这种"compare-and-swap"模式在 JSON 文件场景下的等价实现是：
1. 读取时记录 `version` 字段
2. 写回时检查 `version` 是否匹配
3. 不匹配则放弃当前操作（冲突解决策略）

### 8.2 Scheduler 的容错设计哲学

`scheduler.py` 中的 `@metered` 装饰器体现了**防御性编程**的核心原则：

```python
def metered(name: str, *, gated: bool = False):
    def deco(fn):
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs):
            try:
                if gated and await get_maintenance():
                    return  # 维护模式下跳过
                t0 = time.monotonic()
                await fn(*args, **kwargs)
                # 日志记录...
            except Exception:  # noqa: BLE001 - scheduler jobs must never raise
                log.exception("job %s failed", name)
        return wrapper
    return deco
```

**关键洞察**：
- `BLE001` 注释明确说明这是**有意为之的裸异常捕获**
- 调度器任务**绝对不能抛出异常**，否则会杀死整个调度器
- 这与 CDS4WorldCup 的 MiMo sprint 容错需求高度契合：单个任务失败不应中断整个 sprint

**Janitor 任务的启示**：
institute-one 的 janitor 不仅做清理，还负责：
1. **僵尸工作流检测**：标记 stuck >6h 的 workflow runs
2. **过期 topic 清理**：14 天 pending 的 topic pool 条目过期
3. **临时文件清理**：7 天以上的 adhoc workspaces
4. **夜间备份**：在 03:00-05:00 SGT 窗口执行 DB 备份

CDS4WorldCup 可以在 sprint 结束时运行类似的"清理审计"：
- 扫描 `task_queue.json` 中的 stalled 任务
- 清理过期的临时文件
- 生成 sprint 执行摘要

### 8.3 VaultWriter 的 Hash Ledger 机制

`vault/writer.py` 的五条规则中，**hash ledger** 是最精妙的设计：

```python
async def write_note(self, relpath, frontmatter, body, *, artifact_kind, artifact_id):
    # ... 前置检查 ...
    row = await db.query_one("SELECT sha256, state FROM vault_index WHERE path = ?", (rel,))
    
    if row and new_sha == row["sha256"] and target.exists():
        return rel  # 规则 (d): 未变更则跳过
    
    if row and target.exists():
        disk_sha = _sha_file(target)
        if disk_sha is not None and disk_sha != row["sha256"]:
            # 规则 (c): 检测到人类编辑，写旁支文件
            alt_rel = str(p.parent / f"{p.stem} (institute update {work_date()}){p.suffix}")
            _atomic_write(self._root / alt_rel, content)
            await db.execute("UPDATE vault_index SET state='conflict' ...")
```

**设计原理**：
- `vault_index` 表记录的是"最后一次由系统写入时的 SHA256"
- 如果磁盘文件的 SHA 与 ledger 不一致 → 说明人类编辑过 → **绝不覆盖**
- 这种设计实现了**人类与 AI 的协作边界保护**

**CDS4WorldCup 的轻量实现方案**：
```python
# src/utils/vault_writer.py 伪代码
import hashlib
import json
from pathlib import Path

class SimpleVaultWriter:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.ledger_path = base_dir / ".ledger.jsonl"
    
    def _get_ledger_sha(self, relpath: str) -> str | None:
        """从 JSONL ledger 中读取最后一次记录的 SHA"""
        if not self.ledger_path.exists():
            return None
        # 读取最后一行匹配的 path 记录
        ...
    
    def write(self, relpath: str, content: str) -> str:
        target = self.base_dir / relpath
        new_sha = hashlib.sha256(content.encode()).hexdigest()
        ledger_sha = self._get_ledger_sha(relpath)
        
        if target.exists() and ledger_sha:
            disk_sha = hashlib.sha256(target.read_bytes()).hexdigest()
            if disk_sha != ledger_sha:
                # 人类编辑检测，写旁支
                alt_path = target.parent / f"{target.stem} (mimo update {date}){target.suffix}"
                alt_path.write_text(content)
                self._append_ledger(relpath, new_sha, "conflict")
                return str(alt_path)
        
        # 原子写入
        tmp = target.parent / f".tmp.{target.name}"
        tmp.write_text(content)
        tmp.replace(target)
        self._append_ledger(relpath, new_sha, "clean")
        return str(target)
```

### 8.4 Event Bus 的持久化设计

`bus.py` 实现了**内存 + 持久化**的双层事件系统：

```python
async def emit(type, ref_kind, ref_id, payload):
    # 1. 持久化到 events 表
    event_id = await db.insert("INSERT INTO events ...")
    event = Event(...)
    
    # 2. 推送到内存订阅者（SSE）
    for q in _subscribers:
        try:
            q.put_nowait(event)
        except asyncio.QueueFull:
            pass  # 慢消费者丢弃，cursor 端点可恢复
    
    # 3. 调用注册的处理器
    for prefix, handler in _handlers:
        if event.type.startswith(prefix):
            try:
                await handler(event)
            except Exception:
                log.exception("handler failed")  # 绝不中断 emitter
```

**关键设计决策**：
- **events 表是真相源**，SSE 只是实时投影
- **慢消费者被丢弃**，但可以通过 `replay(since=...)` API 恢复
- **处理器异常被捕获**，单个 handler 失败不影响其他 handler

**CDS4WorldCup 的 JSONL 等价实现**：
```python
# data/ops/events.jsonl 示例
{"id": 1, "type": "task.started", "ref_kind": "task", "ref_id": "task-001", "payload": {...}, "created_at": "2026-06-12T10:00:00"}
{"id": 2, "type": "task.completed", "ref_kind": "task", "ref_id": "task-001", "payload": {...}, "created_at": "2026-06-12T10:30:00"}
```

### 8.5 Prompt 工程的契约思维

`prompts.py` 展示了**prompt 作为行为契约**的工程实践：

```python
CITATION_MANDATE = """\
【引用规范】所有事实性论断必须给出来源（链接、报告名或数据出处）。无法核实的内容必须明确标注「未经核实」。
区分事实与观点：观点用「我认为/判断」开头。数字给出时间点。禁止编造数据。\
"""

FILE_DELIVERABLE = """\
【交付规范】把完整成果写入工作目录下的文件 {filename}（Markdown，中文为主）。\
写完后只回复一行：DONE: {filename}\
"""
```

**设计原则**：
1. **Prompt 是产品形态**，不是可随意重构的辅助文本
2. **Never paraphrase existing prompt strings**（CLAUDE.md 硬规则）
3. **措辞漂移会导致输出分布偏移**

**CDS4WorldCup 的具体建议**：

```python
# src/utils/prompt_builder.py 建议结构

# 常量定义：直接复制总控文档中的纪律表述，不做改写
SOURCE_POLICY_BLOCK = """\
【来源纪律】
- Green Source（官方数据、权威报告）→ 可作为事实输入
- Yellow Source（媒体报道、分析师观点）→ 需交叉验证
- Red Source（社交媒体、匿名消息）→ 仅作 baseline 参考
"""

PATH_CARD_CONTEXT_BLOCK = """\
【路径卡上下文】
当前分析的路径卡：{path_card_id}
路径描述：{path_description}
关键因子：{key_factors}
"""

def build_mimo_prompt(
    role: str,
    task: str,
    path_card_id: str | None = None,
    output_file: str | None = None,
) -> str:
    """构建标准化的 MiMo prompt"""
    parts = [
        date_anchor(),  # 时间锚点
        f"【角色】{ROLE_PERSONAS[role]}",  # 人格块
    ]
    
    if path_card_id:
        parts.append(PATH_CARD_CONTEXT_BLOCK.format(...))  # 上下文块
    
    parts.extend([
        f"【任务】{task}",
        SOURCE_POLICY_BLOCK,  # 引用规范
    ])
    
    if output_file:
        parts.append(FILE_DELIVERABLE.format(filename=output_file))
    
    return "\n\n".join(parts)
```

### 8.6 Workflows 的变量替换与上下文传递

`workflows.py` 中的工作流引擎实现了**步骤间的上下文传递**：

```python
# 变量替换
prompt = substitute_variables(step.get("prompt", ""), variables)

# 前序步骤的摘要传递（有界上下文）
full_prompt = build_analyst_prompt(
    analyst, prompt,
    context_blocks=[previous_steps_block(prior)],  # 只传递摘要，不传递全文
    output_file=step.get("output_file"),
)
```

**`previous_steps_block` 的实现**（有界上下文的关键）：
```python
def previous_steps_block(results: list[tuple[str, str]], budget_chars: int = 8000):
    """results: [(title, summary)]. Bounded context from earlier steps."""
    if not results:
        return ""
    parts = ["## 前序步骤结论（摘要）"]
    per = max(500, budget_chars // max(len(results), 1))  # 每个步骤的预算
    for title, summary in results:
        s = (summary or "").strip()
        if len(s) > per:
            s = s[:per] + "…"
        parts.append(f"### {title}\n{s}")
    return "\n\n".join(parts)[:budget_chars]
```

**启示**：
- 不传递前序步骤的全文，只传递**摘要**，控制上下文窗口
- 每个步骤的摘要是通过 `extract_summary()` 从输出文件中提取的
- CDS4WorldCup 可以在工作流模板中采用类似机制，避免 MiMo 的上下文被无限膨胀

### 8.7 分析师角色的配置化设计

`catalog/analysts.json` 的结构展示了**角色即配置**的理念：

```json
{
  "id": "macro-analyst",
  "name": "宏观分析师",
  "name_en": "Macro Analyst",
  "category": "macro",
  "emoji": "🌏",
  "focus": "宏观经济与流动性分析师，覆盖中美欧增长、通胀与货币财政",
  "persona": "你以数据为锚：增长、通胀、就业、利率、汇率、流动性...",
  "hand": null,
  "model": null
}
```

**设计洞察**：
- `focus` 和 `persona` 分离：focus 是功能描述，persona 是行为约束
- `hand` 和 `model` 可为 null，表示使用默认值
- emoji 和 category 用于 UI 展示（虽然 CDS4WorldCup 没有 UI，但可用于日志/批注）

**CDS4WorldCup 的角色设计建议**：

```json
// data/ops/roles/path-analyst.json
{
  "id": "path-analyst",
  "name": "路径分析师",
  "focus": "负责夺冠路径的结构化推演与缺口识别",
  "persona": "你以路径空间方法论为核心工具。你的分析必须：1) 明确列出所有可能路径；2) 量化每条路径的概率分布；3) 识别关键决策节点；4) 标注不确定性来源。你避免单一预测，而是呈现概率化的路径集合。",
  "prompt_blocks": ["date_anchor", "source_policy", "path_space_primer"]
}
```

### 8.8 综合评估与实施建议（更新）

基于代码级分析，对原有优先级进行微调：

**P1 保持**（零依赖，立即可做）：
1. **Prompt Builder**：直接复用 `prompts.py` 的结构，但用纯 Python 实现
2. **Task Queue 状态机**：借鉴条件认领惯用法，用 `version` 字段实现乐观锁

**P2 细化**（建议拆分为两个阶段）：
- **P2a（高优先级）**：VaultWriter 安全写入规则——`candidate/` 和 `mimo_outputs/` 的并发保护是真实风险点
- **P2b（中优先级）**：Events JSONL + 工作流模板——需要更多设计讨论

**新增 P1.5**（代码分析发现的高价值点）：
- **有界上下文传递**：在任务拆分时，前序步骤只传递摘要而非全文，这对 MiMo 的长程 sprint 尤为重要
- **Sprint 结束时的 Janitor 模式**：清理 stalled 任务、生成执行摘要、归档临时文件

**不建议引入的机制（补充）**：
- **Lazy import 模式**：institute-one 在 scheduler jobs 中使用懒加载来隔离故障域，但 CDS4WorldCup 没有常驻进程，此模式不适用
- **Session workspace 隔离**：institute-one 每个 workflow run 有独立 workspace，CDS4WorldCup 的文件结构已经通过目录组织实现了类似隔离

---

> [!memo] 2026-06-12 深度代码分析补充完成
>
> 作者：kimi-k2.5  
> 分析范围：executor.py、scheduler.py、vault/writer.py、bus.py、prompts.py、workflows.py、analysts.json、research.json  
> 核心发现：institute-one 的设计精髓在于**边界隔离**（并发锁、异常捕获、人类编辑保护）和**可恢复性**（条件认领、ledger 校验、孤儿恢复），这些原则在纯文件/JSON 环境下有等价实现路径。
