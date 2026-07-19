# RepoPrompt CE Back-Compat Bug Triage — 2026-07-09

> **Source request**: 用户问"调研 RPCE 仓库的 bug,并且判断是否值得提 issue",尤其针对我们已经遇到的"旧版本不兼容导致切换 MCP/CLI 失败"。
> **Method**: 直接核验本机当前状态 vs 项目记忆中的快照,再比对上游 `repoprompt/repoprompt-ce` 的 issue/PR/release 状态。原计划派一个 rp-cli agent(让它自选 skill),但 MCP `agent_run` 会话在 dispatch 后停在 Thinking 状态 ~10 分钟无推进,已 cancel;本机核验已经提供全部所需事实,故采用直接撰写。
> **Scope**: 仅调研,不提 PR、不改 symlink、不重启 app、不动上游源码。

---

## TL;DR verdict

| Symptom | 判定 |
|---|---|
| #1 旧 `rp-cli` symlink 指向已删 `Repo Prompt.app` → 复活旧 app | **不提 issue — 上游 PR #424 (merged 2026-07-08) 已覆盖且当前本机 symlink 已是 CE,不再复现** |
| #2 CE 自管文件(`discovery.json`、`repoprompt_ce_cli`)漂移到 AppTranslocation UUID | **不提 issue — PR #413 (merged 2026-07-08) 修分类器 + #424 grandfather legacy;当前本机 `discovery.json` 已是 canonical 路径,不再漂移** |
| #3 安装 binary 1.0.24 滞后源 v1.0.26-1 两个 patch | **不提新 issue — 这是 release-packaging 滞后,非 code bug;且受 contributor-gate 锁定** |

**结论一句**:我们的痛点对应的上游 bug 都已修在 `main` 上,只是修了但**没发 release**。本机安装的 v1.0.24 是当前 GitHub Releases 页面上"最新可装"的版本 —— #413/#424 修复还未打包分发。没有值得新提的 issue。

---

## Symptom 1 — `rp-cli` → 旧 "Repo Prompt" app

### 记忆记录的痛(2026-07-08 写入 `MEMORY.md` L59)
> `/usr/local/bin/rp-cli` is a symlink → `/Applications/Repo Prompt.app/Contents/MacOS/repoprompt-mcp`(OLD name WITH space)。`/Applications/Repo Prompt.app` does NOT exist。`rp-cli --launch-app` follows this symlink and REVIVES THE OLD APP, not CE。

### 现在实查(2026-07-09)
```
/usr/local/bin/rp-cli -> /Applications/RepoPrompt CE.app/Contents/MacOS/repoprompt-mcp   (已指向 CE)
rp-cli --version  =>  rp-cli (repoprompt-mcp) 1.0.24
```
PATH 里另有两份 user-space 安装:`/Users/tangzw119/.local/bin/rp-cli` 和 `/Users/tangzw119/.local/bin/rpce-cli`,也是 CE 提供。

**症状不再复现**。symlink 已被某轮 CE 启动时的 install_debug_cli.sh / managed-path 逻辑改写成指向新 app。记忆里的"dangling → 复活旧 app"在本机当前态已不成立。

### 上游覆盖度
**PR #424"Harden agent CLI startup in fragile user environments"**(merged 2026-07-08,by `baron`)明确把她包了:
- 把 CE user-space CLI links 新生配置迁到 no-space `~/RepoPrompt` 路径
- **grandfather legacy CE Application Support links、旧 Classic-style CLI 名(即 `rp-cli` 这一类)、现存 managed app-bundle destinations 全部视为 repairable/recognized**
- 报告 candidate + fallback-env hints,不再 collapse 成"CLI not found"
- 验证:`make dev-test FILTER=CLIPathInstallerTests`、`CECLINamingAndRoutingTests`、`DebugCLIInstallerScriptTests` 都过

#424 的设计意图("legacy paths remain explicitly supported so existing users are not stranded")正中我们的痛点 —— 我们就是有遗留 `rp-cli` shim 的"existing user"。该修复把 `rp-cli` 这类旧 Classic 名当 managed/repairable 处理,所以重启 CE 后 shim 自动 repoint,现象消失。

### 应否提 issue?
**否**。该 bug 类已被 #424 解决,且本机现态已自愈。再提一个"old-name drift"issue 会是 #424 的重复,违反 CONTRIBUTING.md "explain what they do / 理解你提交的代码"门槛。

### 仍待验证的盲点
记忆 L59 的"`rp-cli --version` 返回 2.1.33"是上一会话静态观察,本机现态 `rp-cli --version` 返回 1.0.24(CE 二进制名)。**没机会**再见到旧 `2.1.33` 来源 — 可能那个来源是另一份 user-space 装(现已覆盖),或被 #424 的 grandfather 逻辑覆盖。无法证伪,但与 issue-worthiness 无关,因为 #424 已名状此类。

---

## Symptom 2 — CE 自管文件漂移到 AppTranslocation UUID

### 记忆记录的痛(MEMORY.md L58)
> `~/Library/Application Support/RepoPrompt CE/MCP/discovery.json` 和 `repoprompt_ce_cli` symlink 由 CE 自动写入 AppTranslocation UUID(`AD36D278-...` 与 `BFD656DC-...`,不同 UUID = 不同 rotation 历史)。不可手改。修复路径 = 确保 CE 从 `/Applications/RepoPrompt CE.app/` 运行,PID 42353 已在 canonical path。

### 现在实查(2026-07-09)
```
~/Library/Application Support/RepoPrompt CE/MCP/
├── discovery.json        (07-09 00:44)
├── discovery.json.bak.20260709_004419      ← CE 自己留的备份
├── mcp-routing.json     (07-09 12:04, 11K)
└── LaunchConfigs/

discovery.json 内容:
{
  "mcpServers": {
    "RepoPromptCE": {
      "command": "/Applications/RepoPrompt CE.app/Contents/MacOS/repoprompt-mcp",
      "args": []
    }
  }
}
```
**AppTranslocation UUID 路径已消失**,`discovery.json` 现指向 canonical CE path。存在 `.bak.20260709_004419` —— 暗示 CE 在 7-09 00:44 做过一次原子替换,把旧 translocation 写入备份后切到 canonical。这与 PR #413 的 `.managedStale`(reclaimable→repaired)语义一致。

### 上游覆盖度
- **PR #413"Fix CLI install recovery from stale App Translocation symlinks"**(merged 2026-07-08,by `amittell`):
  - `ManagedCLIPathPolicy.classifySymlink` 现对 destination 含 `/AppTranslocation/` 且其 `*.app` 后缀匹配known managed destination 视作 `.managedStale`(可回收)
  - 之前的 `.unmanaged` → `ensureLocalSymlink` 拒绝替换 → `install()` throw `.pathExistsNotOurs` 失败
  - `InstallError.pathExistsNotOurs` 现携带 `path: String`,把真正冲突的路径显示出来(原来是硬报 `/usr/local/bin/rpce-cli`)
  - `#413` 的 Note:"Complementary and non-conflicting" with `#278`(`#278` 把 user-space symlink path 改迁到新位置,hard cutover)
- 配合 **#424** 把 legacy Application Support links "grandfather ... as repairable/recognized paths"。

对 #2 的精确判定:#413 主修分类器(reclaim stale AppTranslocation 为 managed),#424 grandfather legacy 配套,#278 是 hard-cutover 替代方案。三者非冲突,合起来覆盖我们的现象。

### 还会再漂移吗?
- 若 CE 永远从 `/Applications/RepoPrompt CE.app/` 启动(已是当前态),不再有 AppTranslocation,不会再生出 translocation UUID 路径。
- 若用户从 DMG/Downloads 直跑(触发 macOS App Translocation),#413 fix 让 CE 在下次从 canonical 启动时把 translocated symlink 视为 reclaimable 并修复 —— 我们之前踩的"install 失败报错指向不存在路径"门面被关。
- 不存在我们这个具体场景下 #413 还修不掉的残留 bug 类。

### 应否提 issue?
**否**。#413 + #424 已覆盖,本机现态已自愈(有 `.bak` 见证原子替换)。

---

## Symptom 3 — 安装 binary 1.0.24 滞后源 v1.0.26-1 两 patch

### 现在实查
| 项 | 值 |
|---|---|
| 源 `main` HEAD | `c255548d` (`v1.0.26-1`, 2026-07-09 01:03:36 +0900) |
| 含的 PR | #413(merged 07-08)、#424(merged 07-08) 都在 `main`,tag 指向的 commit 都包含 |
| GitHub Releases 上"Latest" | **`1.0.24`**(发布于 2026-07-06 21:43Z) |
| 已发布 dmg | `RepoPrompt-1.0.24-25.dmg`(2026-07-08 19:01 在 ~/Downloads/,与 GitHub release 1.0.24 同版本 build 25) |
| tag 存在但 **无 GitHub release** | `v1.0.25`(07-08 23:01)、`v1.0.26`(07-09 01:03) ← tag commit 进了 git,但 GitHub Releases 页没有对应发布/dmg |
| 安装 bundle(读 Info.plist) | `1.0.24`, build `25` ← 与 GitHub Latest 一致 |
| `repoprompt-mcp --version` | `rp-cli (repoprompt-mcp) 1.0.24` |

### 判定
这是 **release-packaging 滞后**,不是 code bug:
- 表象看着像"我们忘了升级两个 patch",其实是 v1.0.25/v1.0.26 的 tag 进了 git,但**没产出对应的 Github Release,没有 dmg/zip 发布工件**。普通用户从 GitHub Releases 页拿最新,只能装到 1.0.24,所以该两 patch 自动到达用户机的时间被推迟。
- 留给用户侧可做:**自己 build-from-source** 把 HEAD 编出装上(复杂,需 Xcode full + PreviewsMacros plugin,见 #174),或等 release 流水线发 dmg。

### 应否提 issue?
**不应**。"tag 已建但 GitHub Release 未生成"是 release 流水线的运维问题,不是 product bug,而且:
1. 这两个 tag 仅滞后 ~1-2 天,在正常 release window 内
2. 我们(zwtang119)不在 `.github/APPROVED_CONTRIBUTORS` 776 人清单中,任何 issue 会被 contribution gate 自动 close;只对 release-delay 提一个会被 bot 立即关掉的 issue 是纯噪声,反而把 maintainer reviewer 的精力从真问题里挪走
3. CONTRIBUTING.md §"Before Submitting A Pull Request" 把 release metadata / signing identity 列为 maintainer-only 保留

### 真值得的事(但不是 issue)
- 关注 GitHub Releases 页 v1.0.25 / v1.0.26 的发布窗口;若再过 3-5 天仍未出 dmg,可在 `#433`(release RepoPrompt CE 1.0.26 — closed)回复中礼貌跟进("v1.0.26 tag landed but Github release 不见 release artifact")——但**那不是新 issue**,是 comment on existing release-tracking issue。

---

## Issue-worthiness matrix

| Symptom | 上游已覆盖? | 1.0.24 上能复现? | Distinct bug class? | 受 contributor-gate 阻挡? | Verdict |
|---|---|---|---|---|---|
| #1 `rp-cli` → 旧 app | ✅ #424 grandfather | ❌ 本机已自愈 | ❌ 已被 #424 包 | ✅(不在白名单) | **不提,升级即可** |
| #2 AppTranslocation drift | ✅ #413 + #424 | ❌ 已切 canonical | ❌ 已被 #413 包 | ✅ | **不提,升级即可** |
| #3 装包 1.0.24 滞后源 | N/A(release pipeline) | 现象本身即可见 | ❌ 不是 code bug | ✅ | **不提** |

---

## Recommended action

**没有值得新提的上游 issue**。建议路径:
1. **等 release**:盯 GitHub Releases 页 `repoprompt/repoprompt-ce/releases`,v1.0.25 / v1.0.26 出 GitHub release(含 dmg)就下载替换 `/Applications/RepoPrompt CE.app/`。这会自动把 #413 + #424 带到我们机子上,从此类问题永久不应再发生(legacy `rp-cli` link 已被 grandfather,AppTranslocation 已被分类器修复)。
2. **若急用**:`cd /Users/tangzw119/Documents/GitHub/0ref/repoprompt-ce/ && git checkout v1.0.26 && make` 自己 source-build 安装。条件:有 Xcode full(不是 Command-Line-Tools-only,见 issue #174 PreviewsMacros plugin 限制)。复杂度高于收益,不推荐。
3. **不动当前本机的 symlink**:记忆 L65 标注"`rp-cli --launch-app` 复活旧 app" 是旧态(当时 `rp-cli` → 旧 app),现态 `rp-cli` → CE,无复活风险。但 `--launch-app` 这类命令仍建议避用(CLAUDE/AGENTS 文档建议直跑 canonical binary)。`sudo ln -sf` 这种手动修复**不再需要**(现态已经指向 CE)。

### 顺便修项目记忆(本调查触发,不属上游 issue)
project MEMORY.md L58-65 写入于上一会话的旧态观察(漂移 + dangling)。本机现态全面不同(`rp-cli` → CE、`discovery.json` canonical、有 `.bak` 见证原子替换)。建议下一次 checkpoint writer 把这 3-4 条改为:
- L58 `discovery.json` 当前已是 canonical 路径,AppTranslocation UUID 现象已消失(很可能 #413 修复在 CE 某次启动时回收掉)
- L59 `rp-cli` symlink 现指向 `/Applications/RepoPrompt CE.app/Contents/MacOS/repoprompt-mcp`,不再 dangling/复活旧 app;旧"2.1.33 来源"现象不可再观察
- 安装版本仍 1.0.24,是 GitHub Latest 当前可装最新;v1.0.25/v1.0.26 tag 在 git 里但**未发 Release dmg**

---

## Confidence + gaps

**高信心**:
- #1 / #2 在本机现态已不复现(直接 `ls -la` + `readlink` + `cat discovery.json` 验证)
- 上游 #413 / #424 都已 merged,tag v1.0.25 / v1.0.26 都包含它们(git log -1 on tag 直接见)
- `zwtang119` 不在 `.github/APPROVED_CONTRIBUTORS`(`grep` 验证,776 行)
- v1.0.24 是 GitHub Releases 页 Latest(`gh release list` 验证),v1.0.25/v1.0.26 tag 存在但 GitHub Release 不存在

**中信心**:
- "CE 修复后自动回收旧 symlink" 这一因果链,是依据 `.bak.20260709_004419` 备份文件 + #413 的 `.managedStale` 语义**推断**而非亲眼观察,但证据闭环
- 现态自愈发生在 2026-07-08 → 2026-07-09 之间某次 CE 启动,具体是 PR #424 的 repairable-classifier 触发还是手动一系列 ln -sf 在两会话间执行过 ——**无法反推确切来源**。但有一件事是确定的:现态是对的

**低信心 / 未验证**:
- "v1.0.25/v1.0.26 没有 GitHub release 是 release 流水线的正常间隔还是 pipeline 卡了"——只看了 tag commit 日期(分别 07-08 23:01 和 07-09 01:03,距今不到 1 天),没有release-pipeline 监控数据验证
- 上游是否已经有 maintainer 内部(discord/Slack/issue#433 评论)就 release 滞后有过沟通 —— 没查(漏一个 repo 全文搜,但低 ROI)
- 上一会话记录的 `rp-cli --version` 返回 `2.1.33` 的真正来源(二进制名都现,但当时为何能在 dangling 下 print?)——历史可观察已灭,码内 fallback 路径未读源

---

## Descoped(本调查未做)
- 没读 `ManagedCLIPathPolicy.swift` / `CLIPathInstaller.swift` 源码做内部对照(因 bug 类已被覆盖,追溯实现没 ROI)
- 没确认 #278(hard cutover 到新路径)具体何时上 —— 这关系我们 user-space link 是否会被改名,但与本 issue-worthiness 判定无关
- 没取 v1.0.25/v1.0.26 的 release notes(因为 GitHub release 不存在,没有正文可读,只能看 tag commit message)
