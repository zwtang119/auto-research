# MANIFEST 增补：时间戳锚定与封存破口披露

> 日期：2026-07-25 ｜ 性质：对 `cds4worldcup-snapshot-2026-07-20/MANIFEST.md` 的增补，不替代原件 ｜ 执行：Kimi Work agent（用户授权，只读源仓库 + GitHub 设置项变更，零 commit）

## 1. 本日执行的保全动作（均为 GitHub 设置/导出，未触碰 git 历史）

| 动作 | 结果 |
|---|---|
| Actions 运行记录保留期 90 → 400 天 | 已生效（API 确认 `{"days":400,"maximum_allowed_days":400}`）。覆盖至 ~2027-08-29，保住 148 条服务端记录活过审稿周期 |
| 导出全部 Actions 运行记录 | `github-actions-runs-export-2026-07-25.json`（148 条，2026-06-11T06:28:03Z → 2026-07-25T06:19:21Z）。`created_at` 为 GitHub 服务端生成，作者无写权限 |
| 全量 SHA-256 校验和 | `CHECKSUMS-sha256-2026-07-25.txt`（bundle + MANIFEST + 导出件 + worktree 822 文件逐字节） |
| 停用每日定时 workflow | `Daily CDS Update`、`Market Snapshot` → `disabled_manually`（设置项，非 commit）。每日 bot 对封存仓库的自动写入就此止血；CI / Deploy Pages（push 触发）保留 |
| 导出 GitHub Events API | `github-events-export-2026-07-25.json`（61 条 PushEvent，2026-06-25→07-25）。独立于 Actions 的第二套服务端记录；6-11 的推送事件已自然老化消失，特此备注 |
| 证据截图 18 张 + 中文索引 | `screenshots/`（A 时效性 6、B 内容性 7、C 公开面 3、D 阴性 1 + `截图索引.csv`）。定位为展示件/旁证，与导出 JSON 交叉印证；全部含 URL 栏、原始 PNG |
| Wayback 首个存档 | 触发并确认：`web.archive.org/web/20260725075343/`（本站史上首个第三方存档，内容为 6-15 冻结版首页） |
| Branch protection 开启 | main：禁 force-push + 禁删除 + 强制线性历史 + 对管理员同效。历史改写在服务端被禁止，普通 push 不受影响 |
| Gmail 通知邮件证据 | 14 封 GitHub 通知（zwtang119@gmail.com），**8 封为 6 月记录**（6-11×3、6-13×2、6-18×2、6-20）。Google 服务器时间戳，为目前唯一回溯到 6 月的第三方平台证据；E2（6-11 14:28）与 Actions 记录（06:28:03Z）同分钟互证 |
| **时间锚（已完成）** | 2026-07-25 18:12–18:13 UTC：① OpenTimestamps 双日历提交（a.pool + b.pool，收据 `ots-receipt-*.ots`，锚定哈希 `525e6301…b14df`，待比特币确认后升级）；② FreeTSA RFC 3161 锚定（`evidence-freetsa.tsr`，serial 0x067B81C2，Status: Granted）。注：被锚哈希对应锚定时刻的 CHECKSUMS 版本；此后追加使清单哈希变更（当前 `19f7a9e4…c501`），后续重大增补后应重新锚定 |

## 2. 封存破口披露（主动声明，供论文 Data Availability 引用）

MANIFEST（2026-07-20）声明封存仓库"零读写封存"。实际情况：封存于次日起被持续打破，披露如下——

1. **每日自动化提交（2026-07-21 → 07-25，10 个 commit）**：github-actions bot 每日重建 `cds_championship.json` 等管线文件（概率漂移）。属系统原设计，非人工干预；已于本日停用（见 §1）。
2. **结算提交改写（2026-07-19/20）**：本地未推送的 `e8d74aab` 被 amend 为 `923e23a` 后推送。差异仅限每日自动生成的 site 数据（14 文件 2618/2618 行）。**MANIFEST 原定论文引用锚 `e8d74aa` 从未推送至 GitHub（API 验证返回 422），引用锚必须改为 `923e23a`**——两者除上述生成文件外逐字节相同，`e8d74aab` 本体封存于 bundle。
3. **MIGRATED 指针提交（2026-07-25，`9bd5a2d`）**：纯文档新增（2 个 MIGRATED.md），未触碰任何数据/结果文件。注：该提交的 CI 与 Deploy Pages 运行均 failed（原因待查，与证据链无关）。
4. **联邦迁移尾批（2026-07-25 16:24，`c7b18cb`）**：World Cup 场景模板迁出至 CDS-ontologyKB（删 2 个模板文件 + MIGRATED 指针 + CHANGELOG 0.4.1 + .gitignore/wiki 更新）。CI 与 Deploy Pages 均 failed（Gmail 失败通知 16:24 互证；根因 = build_site_data 扫描到非球队卡 .md）。公开站点继续服务 6-15 构建版（未受部署失败影响，客观上维持赛前展示）。

**封存终态确认（2026-08-02 核验）**：HEAD = `c7b18cb`（一周无新提交，已稳定）；工作区干净，仅 1 个已知未跟踪文件（`docs/investigations/system-running-state-and-paper-readiness-2026-06-20.md`，已含于本快照 worktree 并在原 MANIFEST 标注证据等级）；LICENSE 仍在（用户曾决意删除，2026-07-25 15:28 被恢复，删除决定顺延至投稿转公开时处置）；两个每日 workflow 已停用、branch protection 生效——封存由服务端强制维持。

**已发布历史经 bundle 对账：零重写。** 快照记录的 origin/main（`62b8c99`）为当前 main 的祖先。

## 3. 独立网页存档核查（阴性结果，须写入论文证据声明）

2026-07-25 核查，以下第三方存档源**均无**本站赛前记录：

- Wayback Machine（CDX ×3 + availability API ×2）✗
- archive.today ✗
- Common Crawl `CC-MAIN-2026-25`（爬取窗口 2026-06-05→06-18，覆盖开赛日）✗

含义：不存在"赛前第三方网页存档"；赛前存在性证据依赖 GitHub 服务端运行记录（§1，400 天保留期内可在线核验）+ 本增补的事后锚定链。信任结构与 OSF 预注册相同（信任平台而非作者）。

## 4. 论文主张 → 证据锚点对照表

| 论文主张 | 证据 artifact | 锚定 commit | 备注 |
|---|---|---|---|
| kimi 公众信号头号热门西班牙（23.82）、前五覆盖四强全部 | `site/data/homepage.json` 的 `public_model_crowd`（自 `0ff58a7` 起逐字节冻结至今） | `0ff58a7`（2026-06-13） | 源数据 `data/raw/kimi/kimi_300_unpacked/`（metadata 2026-06-05）；聚合层 21/21 复算已验证；基准率论证见缺口分析，仅作描述 |
| CDS 引擎夺冠预测（赛前版西班牙 #1, 0.0484） | `data/processed/cds_championship.json` | `ef30658`（2026-06-12） | ⚠️ 必须同时披露 `875748b` 归一化修正（6-12/13，头号热门变为塞内加尔）；隐藏修正史将构成选择性报告 |
| 路径卡与 kimi signals 开赛前入库 | `artifacts/team-cards/` 等 | `2915511`（2026-06-11，开赛日） | 当日 11 个 commit，Actions 记录 06-11T06:28Z 起 |
| 小组赛结算 | `results/2026-07-08-*.md` 等 | `ca0e3ff`（2026-07-08） | Green Source Wikipedia 核验 |
| 夺冠 46 队结算 | `results/2026-07-18-cds-championship-knockout-settlement.md` | `923e23a`（2026-07-19） | 引用锚自此 commit（替代 `e8d74aa`） |

**固化策略：固化全部，而非单个"压中" commit。** bundle 的单一 SHA-256 即固化全量历史（含 `875748b` 修正史）；论文通过上表按 commit 引用具体版本。只固化"压中"版本会在方法论审查时构成致命的选择性固化嫌疑。

## 5. 待办（用户决策中）

- [ ] OpenTimestamps / RFC 3161 TSA 锚定 `CHECKSUMS-sha256-2026-07-25.txt`（哈希已备好，用户考虑中）
- [ ] 公开渠道广播 bundle SHA-256（Gist / X，一分钟）
- [ ] Zenodo 归档提前（原计划 W8-1）：上传 bundle + worktree + 本目录，获取 CERN DOI 时间锚
- [ ] 投稿时：仓库转公开 → Software Heritage save + Zenodo-GitHub 集成
- [ ] 调查 `9bd5a2d` 的 CI / Deploy Pages 失败原因（与证据无关，站点维护项）
