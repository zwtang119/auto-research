# AutoResearch 仓库结构重构蓝图（草案 2026-07-03）

> **Status**: 用户审批前的草案（Diagram-led review）。不动代码、不动路径，仅做 *schema 设计*。
>
> **本稿针对**：`docs/portfolio/rename-proposal-2026-07-03.md` §9 之后追加的「框架型 monorepo」讨论。
>
> **核心结论**：
> 1. auto-research/ 改为 **单仓 monorepo**，框架 + 全部论文同居一仓。
> 2. `framework/` 采用 **二态混合**：paper-agnostic 顶层 + paper-specific 子仓。
> 3. **GitHub Pages 分离**到独立仓（建议名 `<owner>.github.io`，复用当前 clone 的 `victorchen96.github.io` 改名）。
>
> **本文目录**：
> - §1 三仓位关系图
> - §2 auto-research/ 详细目录树（ASCII tree）
> - §3 `framework/` 二态展开图
> - §4 `papers/<N>/` 标准骨架（每篇论文都照这个长）
> - §5 `website/` 与独立 website 仓的关系
> - §6 文件迁移矩阵（旧 → 新）
> - §7 schema 命名约定（formal）
> - §8 docs/ 与 state/ 简化表
> - §9 三日执行时序
> - §10 Open questions（请回复）

---

## 1. 三仓位关系图

```
                    ┌────────────────────────────────────┐
                    │   <owner>.github.io  (website 仓)  │
                    │   ─────────────────────────────    │
                    │   单一目的: 挂 GitHub Pages        │
                    │   内容: hugo / mkdocs 站点源       │
                    └──────────────▲─────┬───────────────┘
                                   │ push
                                   │ (CI/CD: website → site)
   ┌───────────────────────────┐   │     ┌─────────────────────────┐
   │  framework/ (skill/       │   │     │   papers/<N>/           │
   │  schemas/prompts/scripts  │───┼────►│   framework/(paper-     │
   │  knowledge/runbooks)      │   │     │   specific extensions) │
   │                           │   │     │                         │
   │  papers/<N>/  ────────────┼───┼────►│   state/ + experiments/ │
   │   ├─ p07-signal-fusion    │   │     │   + paper/ + logs/     │
   │   ├─ p08-market-calibr…   │   │     └─────────────────────────┘
   │   ├─ p11-inner-monologue  │   │
   │   ├─ p12-judge-calibr…    │   │
   │   └─ p1p2-evidence-ledger │   │
   │                           │   │
   │  docs/  state/  logs/     │   │
   │  website/                 │───┘
   │  CLAUDE.md / README.md    │
   └───────────────────────────┘
              本仓: auto-research  (单仓)
```

---

## 2. auto-research/ 详细目录树（顶层）

```
auto-research/                                     # 主仓根
│
├── README.md                                      # 仓门面: 导航 + 当前主线 + last-updated
├── CLAUDE.md                                      # agent 协作规约
├── AGENTS.md                                      # 子 agent / 多 agent 协议
├── CHANGELOG.md                                   # 仓级变更日志 (semver 风格)
├── LICENSE
├── .gitignore
│
├── framework/                                     # 跨论文可复用层 (二态混合)
│   ├── README.md
│   ├── skills/                                    # 框架级 skill (Deli_AutoResearch 等)
│   ├── prompts/                                   # 通用 prompt template (judge, survey-gen, …)
│   ├── scripts/                                   # 跨论文工具 (api_client / evaluator / …)
│   ├── schemas/                                   # data-contracts / pitfalls / portfolio/
│   ├── knowledge/                                 # 框架级 wiki + decision logs
│   └── runbooks/                                  # 操作 SOP (start paper, close paper, …)
│
├── papers/                                        # 论文层 (每篇一个子目录)
│   ├── README.md                                  # 全部论文总表 (代号 + status + link)
│   ├── p07-signal-fusion/                         # ACTIVE 主线入口
│   ├── p08-market-calibration/                    # ACTIVE
│   ├── p11-inner-monologue/                       # CLOSED (主版本 + mimo 副)
│   ├── p12-judge-calibration/                     # ACTIVE
│   └── p1p2-evidence-ledger/                      # CONCEPT 概念主线
│
├── docs/                                          # portfolio-level docs (扁)
│   ├── README.md
│   ├── aliases.md                                 # 论文代号表
│   ├── project-index.md                           # 论文全表
│   └── rename-history.md                          # 旧→新迁移历史
│
├── state/                                         # portfolio-level state (orchestrator)
│   ├── progress.json
│   ├── directions_tried.json
│   ├── findings.jsonl
│   └── iteration_log.jsonl
│
├── logs/                                          # portfolio-level logs
│   ├── work.jsonl
│   ├── orchestrator.jsonl
│   └── heartbeat.jsonl
│
└── website/                                       # 网站源 (不出仓, 用于构建)
    ├── README.md
    ├── mkdocs.yml (或 hugo.yaml)
    ├── content/                                   # 论文摘要 + 历程
    │   ├── papers/
    │   │   ├── p07.md
    │   │   ├── p08.md
    │   │   ├── p11.md
    │   │   ├── p12.md
    │   │   └── p1p2.md
    │   └── blog/
    └── public/                                    # gitignored 构建产物
```

---

## 3. `framework/` 二态展开图

```
framework/                                         # paper-agnostic (跨论文)
├── skills/
│   ├── deli-autoresearch-framework/              # 现有 SKILL.md 镜像
│   ├── judge-protocols/                          # 通用 5-protocol judge specs
│   ├── paper-closing/                            # 通用 paper-closure runbook
│   ├── result-tabulation/                        # 跨论文结果表生成
│   └── …
├── prompts/
│   ├── judges/                                   # 通用 judge prompt template
│   ├── survey-gen/                               # 综述生成 prompt
│   └── …
├── scripts/
│   ├── api_client.py                             # 跨论文 LLM 客户端
│   ├── hashing.py                                # sha12 / sha256 utilities
│   ├── normalize_yaml.py                         # yaml loader
│   └── …
├── schemas/
│   ├── data-contracts.md                         # data-contracts / pitfalls / portfolio/
│   ├── paper-state.md                            # 论文级 state 字段约定
│   ├── review-rubrics.md                         # 五人 review 评分定义
│   └── …
├── knowledge/
│   ├── auto-research-history.md                  # 框架演进
│   └── …
└── runbooks/
    ├── start-paper.md                            # 新论文三步走
    ├── close-paper.md                            # 论文收口 14-step
    ├── rollback-paper.md
    └── …

↑↑↑ paper-agnostic (4 仓级 + 共享) ↑↑↑


papers/<N>/framework/                              # paper-specific 扩展 (二态)
├── prompts/                                      # 这篇论文独特的 prompt
├── scripts/                                      # 这篇论文独特的脚本
└── schemas/                                      # 这篇论文独特的 schema

↓ 提炼路径（后续可上抽到 framework/）:
   papers/p12/framework/prompts/judge-protocols.md
     ─── (当 ≥2 论文需要该 prompt 时) ───► framework/prompts/judges/

```

**二态规则的文字版**：
1. **初始态**：先放 `papers/<N>/framework/<x>/`，**默认**所有新论文的独有物在 paper-specific 目录。
2. **晋升**：同一物被 ≥2 篇论文复用，才晋升到 `framework/<x>/`。
3. **不可逆**：晋升后不再回到 paper-specific（避免双份维护漂移）。

---

## 4. `papers/<N>/` 标准骨架（每篇论文都这样长）

```
papers/<N>-<topic>/                                # 例: p12-judge-calibration
├── README.md                                      # 论文一句话+里程碑+最新 status
├── plan.md                                        # 论文设计 + hypothesis + roadmap
│
├── state/                                         # 论文级 state (框架 §4)
│   ├── task_spec.md
│   ├── progress.json
│   ├── experiment_design.md                       # 预注册 (PIT-006)
│   ├── findings.jsonl
│   ├── directions_tried.json
│   ├── iteration_log.jsonl
│   └── writer.json                                # 写入者 (e.g. minimax-m3)
│
├── logs/                                          # 论文级 logs
│   ├── work.jsonl
│   ├── orchestrator.jsonl
│   └── heartbeat.jsonl
│
├── experiments/                                   # 数据 + 实验输出
│   ├── sample_manifest.jsonl                      # 输入样本清单
│   ├── sample_ids_ordered.json                    # 冻结执行顺序
│   ├── build_sample_manifest.py                  # 样本构建脚本
│   ├── test_build_sample_manifest.py
│   ├── validate_manifest.sh
│   ├── leakage_reproduction.json                  # M2 输出
│   └── …
│
├── paper/                                         # LaTeX + bib
│   ├── main.tex
│   ├── main.bib
│   └── figures/
│
├── framework/                                     # paper-specific 二态扩展
│   ├── prompts/
│   │   └── <judge|generator|...>-<variant>.md
│   ├── scripts/
│   │   └── <paper-specific-script>.py
│   └── schemas/
│       └── <paper-specific-schema>.md
│
└── archive/                                       # 旧版本 / 关闭副本
    ├── closed-v5-minimax-m3/                      # 例: P11 m3 实现关档
    └── closed-v5-mimo/                            # 例: P11 mimo 实现关档
```

---

## 5. `website/` 与独立 website 仓的关系

```
auto-research/website/                             # 在主仓内
    │
    ├── content/    (mkdocs markdown)
    ├── mkdocs.yml
    └── build artifact → out/

        │ gh-deploy / manual push
        ▼

<owner>.github.io/                                  # 独立 website 仓
    ├── index.md
    ├── papers/                                    # 直接接受从主仓 content 推来的内容
    └── …                                          # site 配置 (.nojekyll / theme / assets)
```

**关系规则**：
- `website/` 在主仓内，**不允许直接 push 到 Pages**。产物经过 `mkdocs build` 后由 CI/CD 推到 website 仓。
- website 仓是**独立 GitHub 仓**，仅接受 build 后的产物（无需 docs/framework/knowledge/...噪音）。

**重要前置**：`<owner>.github.io` 的 GitHub Pages 命名规则是 *账号锁定的*。clone 别人的 `victorchen96.github.io` 推到你的账号**不会自动启用 Pages**。需要你：
1. 在 GitHub 上建一个新仓 `<你的用户名>.github.io`（任意前缀，只要匹配账号）。
2. 在那个新仓的 Settings → Pages 设 source 为 main 分支。
3. `victorchen96.github.io/` 这个本地目录**只是参考资料**，不要再 push 到该仓。

---

## 6. 文件迁移矩阵（旧 → 新）

| 当前路径 | 新路径 | 备注 |
|---|---|---|
| `p1.1-inner-monologue/` | `papers/p11-inner-monologue/legacy-snapshot-2026-07/` | parent（无 git），仅 M1 snapshot |
| `p1.1-inner-monologue-mimo/` | `papers/p11-inner-monologue/archive/closed-v5-mimo/` | git repo, history 保 |
| `p1.1-inner-monologue_minimax-m3/` | `papers/p11-inner-monologue/archive/closed-v5-minimax-m3/` | git repo, history 保 |
| `p1.2-market-calibration_minimax-m3/` | `papers/p08-market-calibration/` | active, 改名 |
| `p1.2-market-calibration-mimo/` | `papers/p08-market-calibration/archive/legacy-init-2026-07/` | legacy |
| `p2.1-signal-fusion_minimax-m3/` | `papers/p07-signal-fusion/` | active, 改名 |
| `p2.1-signal-fusion-mimo/` | `papers/p07-signal-fusion/archive/legacy-init-2026-07/` | legacy |
| `p1-p2-evidence-ledger/` | `papers/p1p2-evidence-ledger/` | active, 改名 + slash 调整 |
| `p12-judge-calibration/` | `papers/p12-judge-calibration/` | active, 改名 |
| `docs/aliases.md` | `docs/aliases.md` (扁平, 留 portfolio/docs) | 不改 |
| `docs/portfolio/aliases.md` | `docs/aliases.md` | 提级 (palette/portfolio 子目录散掉) |
| `docs/portfolio/project-index.md` | `docs/project-index.md` | 同上 |
| `framework/schemas/experiment-pitfalls.md` | `framework/schemas/experiment-pitfalls.md` | 归类 |
| `framework/schemas/data-contracts.md` | `framework/schemas/data-contracts.md` | 归类 |
| `docs/portfolio/configuration-audit.md` | `docs/configuration-audit.md` | 提级 |
| `docs/portfolio/rename-proposal-2026-07-03.md` | `docs/rename-proposal-2026-07-03.md` | 提级 |
| `docs/autoresearch/` | `framework/knowledge/` | 归类 |
| `docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md` | `papers/README.md` + `docs/roadmap.md` | 拆 |
| `docs/investigations/p11-inner-monologue-paper-readiness-2026-07-03.md` | `papers/p11-inner-monologue/investigations/p11-paper-readiness-2026-07-03.md` | 下沉到论文 |
| `state/` | `state/` (留在 portfolio root) | 不动 |
| `logs/` | `logs/` (留在 portfolio root) | 不动 |
| `topic5-research-directions.md` | `archive/topic5-research-directions-2026-07.md` | 历史 |
| `victorchen96.github.io/` | 不动 (参考资料, 不进 auto-research 仓) | — |
| `policysim-research-Tsinghua/` (外) | `framework/scripts/external/policysim-vendored/` (将来) 或 git submodule | Phase 2 follow-up |

合计 **43** 个被影响的 script 引用需同步迁移（详见 `rename-proposal-2026-07-03.md` §6 grep 命令）。

---

## 7. schema 命名约定（formal）

```
论文目录:                          p<N>{-<topic>}/
                                  N ∈ {1, 2, 7, 8, 11, 12, p1p2}
                                  topic: lowercase, hyphenated, ≤ 30 chars

论文状态后缀:                     (no suffix)            # ACTIVE
                                  legacy-init-YYYY-MM/   # initialized, inactive
                                  closed-v<N>-{agent}/   # CLOSED with version + agent
                                  legacy-snapshot-YYYY-MM/  # non-versioned mix

框架状态后缀:                     (no suffix)            # active framework
                                  experimental/          # WIP
                                  deprecated-YYYY-MM/    # 已弃用

框架分层:                         framework/{skills,prompts,scripts,schemas,knowledge,runbooks}/
                                  papers/<N>/framework/{prompts,scripts,schemas}/    # 二态扩展

file 类型约定:                    *.md       # docs
                                  *.json     # manifest / state
                                  *.jsonl    # append-only log
                                  *.yaml     # config
                                  *.py       # script
                                  *.sh       # shell script
                                  *.tex / *.bib  # paper

sample id:                        <exp_id>-<NNN>           # 例: P12-001
protocol run id:                  R-<exp_id>-<protocol>-<NNN>   # 例: R-P12-leaked-001
```

---

## 8. docs/ 与 state/ 简化对照表

| 旧 | 新 | 理由 |
|---|---|---|
| docs/portfolio/ 6 文件 | docs/ 4 文件 + framework/schemas/ 2 文件 | 扁平化，区分 portfolio 文档与框架 schema |
| docs/autoresearch/ | framework/knowledge/ | autor-search = 框架知识源 |
| docs/roadmaps/ | papers/README.md (内含) + docs/roadmap.md | roadmap 跨论文与单论文两层 |
| docs/investigations/ | papers/<N>/investigations/ | investigation 总是 paper-specific |
| state/ | state/ + papers/<N>/state/ | portfolio-state 与 paper-state 两者并存 |
| logs/ | logs/ + papers/<N>/logs/ | 同上 |

---

## 9. 三日执行时序

```
═══════════════════════════════════════════════════════════════
Day 0  (今晚 4-6 小时动手量)
═══════════════════════════════════════════════════════════════

00:00 ┌─ 0a. 在 GitHub 新建 website 仓
00:20 │     <owner>.github.io (你的用户名锁定的命名, 例 chenvictor.github.io)
00:40 │     验证 Pages 能启用 → 显示默认 home
00:50 └─ 0b. 本地 git clone 新仓到独立目录
        (留作 website 仓主目录, 不与 auto-research 混)

01:00 ┌─ 1a. 本地 auto-research/ 重排: 创建 framework/ + papers/ + docs/ + website/ 空结构
01:30 │     (不移动 paper 子目录, 先创建空骨架)
01:50 ├─ 1b. git init (auto-research/ 当前不是 git repo)
02:10 │     .gitignore + LICENSE + CLAUDE.md + AGENTS.md + README.md 首版
02:30 └─ 1c. 第一个 commit + push to new repo auto-research-framework
        (新仓名: <owner>/auto-research)

02:45 ┌─ 2a. 移 p12-judge-calibration/ → papers/p12-judge-calibration/
03:15 │     (含其 experiments/* + state/* + paper/ + logs/)
03:30 ├─ 2b. 修 43 个脚本引用 (build_sample_manifest.py 等)
03:50 │     用 sed + 人工校验所有 PIT-105 验证
04:00 ├─ 2c. 写 papers/p12-judge-calibration/framework/prompts/judge-protocols.md
04:15 └─ 2d. 验证: bash papers/p12-judge-calibration/experiments/validate_manifest.sh
        + python -m unittest → 全绿

═══════════════════════════════════════════════════════════════
Day 1  (明天 4-6 小时)
═══════════════════════════════════════════════════════════════

00:00 ┌─ 3a. 移 P11 三子目录 → papers/p11-inner-monologue/ (含 archive/closed-v5-{mimo,minimax-m3})
01:30 │     在 archive/closed-v5-*/ 下保留 git 子仓
        └  (这俩是 git 仓, 直接做 nested-repo + OBSOLETE.md)
02:00 ├─ 3b. 移 P7, P8, p1p2 三个子目录
03:00 ├─ 3c. 在 p1.1-inner-monologue/ 旧位置写 OBSOLETE.md (无 history 路径)
03:15 ├─ 3d. 提级 docs/* (扁平化), 移 docs/portfolio/* → docs/ + framework/schemas/
04:00 ├─ 3e. 写 website/content/papers/{p07,p08,p11,p12,p1p2}.md 摘要 (5 papers)
05:00 └─ 3f. mkdocs build 验证 website/ → out/ 产物
05:30 commit #2 (Day 1 batch)

═══════════════════════════════════════════════════════════════
Day 2  (后天 启动 P12 M2)
═══════════════════════════════════════════════════════════════

00:00 ┌─ 4a. 启动 P12 M2: leaked baseline run
01:00 ├─ 4b. 第一次 milestone-driven commit (M2 leaky reproduction)
02:00 ├─ 4c. website/content/p12.md 更新进度
03:00 └─ 4d. commit #3 (M2 closed)

═══════════════════════════════════════════════════════════════
Ongoing (持续)
═══════════════════════════════════════════════════════════════

  * website 仓 CI/CD: auto-research→ website→ GitHub Pages
  * 每篇论文 milestone commit
  * papers/<N>/framework/<x>/ 提取依赖 ≥ 2 篇 → 上抽 framework/
```

---

## 10. Open questions（请回答）

| # | 问题 | 选项 |
|---|---|---|
| Q1 | 单仓 vs 多仓: 确认 **单仓 monorepo** 方向 OK 吗？ | ✓/✗ |
| Q2 | `framework/` 二态混合 vs 全顶层: 确认 **二态混合** (paper-specific 先放, ≥2 复用上抽)? | ✓/✗ |
| Q3 | website 仓起点: 用 `<owner>.github.io` 还是另起一个非用户名锁定的仓?<br>建议: `<owner>.github.io` (GitHub Pages 唯一命名约定, 无 alternative) | ✓/✗ |
| Q4 | 你倾向的 `<owner>.github.io` 仓名? 三个候选:<br>  (a) `chenvictor.github.io` (你名字倒着读 - 同行惯例)<br>  (b) `delichen96.github.io` (姓名缩写)<br>  (c) 其他 (告诉我) | (a) / (b) / (c) |
| Q5 | `p1-p2-evidence-ledger` → `p1p2-evidence-ledger` 还是保持连字符? | 合并 / 保持 |
| Q6 | 大 P 命名 vs 小 p 命名: `p07-` 还是 `P07-`? 仓库名惯例是小写, 路径选小写 | 小写 `p07-` / 大写 `P07-` |
| Q7 | `state/` + `logs/` 在 portfolio 与 paper 双重存在, 旧的 portfolio 与 paper 交叉读取需要 sanitize 吗? | 双套保留 / 只保留 paper/ 下 |
| Q8 | 是否同时启动 `git init` + push (今晚就推到新建仓)? 我倾向 **是**, 否则 Day 1 整段重排风险高 | 是 / 否 |
| Q9 | P12 M2 现在可以启动吗? 还是先把仓型重构完成再启动实验? | 先重构 → 再 M2 / 并行 |

---

## 附：自查

| 项 | 是否解决 |
|---|---|
| 框架 vs 单论文区分 | ✅ framework/ 顶层 vs papers/ 论文层 |
| 论文代号一致 (P7 = papers/p07-) | ✅ |
| active vs closed 在路径上可读 | ✅ |
| 单一概念单一字面量 | ✅ |
| framework 二态混合 | ✅ |
| website 与主仓分离 | ✅ |
| 旧路径兼容 (OBSOLETE.md) | ✅ |
| cross-paper state 全局可见 (portfolio/state) | ✅ |
| paper-specific state 独立 (papers/<N>/state) | ✅ |
| ≤ 5 large files/iter + ≤ 300 lines/file | 待执行时验证 |
| 站点构建产物不入主仓 | ✅ public/ gitignored |
