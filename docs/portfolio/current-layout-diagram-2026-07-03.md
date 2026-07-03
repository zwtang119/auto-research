# AutoResearch 当前布局示意图 (2026-07-03)

> **状态**：rename 已落地。 本图用于二次审查。
> **查看方式**：本文档全部为 ASCII 视图，60 列宽。
> **配套**：`OBSOLETE.md` (root redirect), `rename-proposal-2026-07-03.md` (mapping), `restructure-blueprint-2026-07-03.md` (schema), `naming-audit-2026-07-03.md` (risk audit).

---

## 1. 全仓目录 60-列视图（执行后实际状态）

```
auto-research/                                            # 主仓根 (非 git repo)
├── README.md                  <-- 已 sed 更新
├── OBSOLETE.md                <-- 新写, 旧路径 redirect stub
├── docs/                      <-- 文档分层
│   ├── autoresearch/          <-- 框架知识
│   ├── compose/               <-- compose plan/spec/report
│   ├── investigations/        <-- paper-level 调研 (会下沉到 paper)
│   ├── portfolio/             <-- portfolio 级文档
│   │   ├── aliases.md             (aliases 映射表)
│   │   ├── data-contracts.md
│   │   ├── experiment-pitfalls.md
│   │   ├── project-index.md       (论文全表)
│   │   ├── configuration-audit.md
│   │   ├── rename-proposal-2026-07-03.md      (历史, EXECUTED)
│   │   ├── restructure-blueprint-2026-07-03.md
│   │   └── naming-audit-2026-07-03.md         (risk audit)
│   └── roadmaps/                  (跨论文路线图)
├── logs/                          <-- portfolio 级 logs (未动)
├── state/                         <-- portfolio 级 orchestrator state
├── papers/                        <-- ★ 新建顶层: ACTIVE papers
│   ├── p07-signal-fusion/
│   ├── p08-market-calibration/
│   ├── p12-judge-calibration/     <-- 当前主线, M1 已交付
│   └── p1p2-evidence-ledger/
├── legacy/                        <-- ★ 新建顶层: 历史/closed
│   ├── p07-legacy-init-2026-07/
│   ├── p08-legacy-init-2026-07/
│   ├── p11-closed-v5-mimo/       (git repo, history 保留)
│   ├── p11-closed-v5-minimax-m3/ (git repo, history 保留)
│   └── p11-legacy-snapshot-2026-07/  (non-git parent of P11)
└── victorchen96.github.io/        <-- 别人仓的 clone, 仅参考
```

---

## 2. 名空间映射（旧 → 新）

```
                       旧 (9 个路径)                          新
                       ─────────────                          ─────────────
   ACTIVE ────┬─►  p12-judge-calibration/                   papers/p12-judge-calibration/
              │   p1-p2-evidence-ledger/                    papers/p1p2-evidence-ledger/
              │   p1.2-market-calibration_minimax-m3/        papers/p08-market-calibration/
              │   p2.1-signal-fusion_minimax-m3/             papers/p07-signal-fusion/
              │
   CLOSED ────┼─►  p1.1-inner-monologue_minimax-m3/         legacy/p11-closed-v5-minimax-m3/
              │   p1.1-inner-monologue-mimo/                 legacy/p11-closed-v5-mimo/
              │   p1.1-inner-monologue/                      legacy/p11-legacy-snapshot-2026-07/
              │
   LEGACY ────┼─►  p1.2-market-calibration-mimo/             legacy/p08-legacy-init-2026-07/
              └   p2.1-signal-fusion-mimo/                   legacy/p07-legacy-init-2026-07/
```

**3 区分**: ACTIVE (在 `papers/`) / CLOSED (在 `legacy/`, 标 `closed-vN-`) / LEGACY (在 `legacy/`, 标 `legacy-…`)

---

## 3. papers/ 子树 (ACTIVE 论文层)

```
papers/
│
├─ p07-signal-fusion/                        P7 主线入口
│  ├─ CLAUDE.md                   (更新)
│  ├─ mimo-prompt.md              (更新)
│  ├─ README.md
│  ├─ MEMORY.md
│  ├─ state/
│  │  └─ io_spec.md               (更新)
│  ├─ logs/                       (work/orchestrator/heartbeat)
│  ├─ paper/                      (LaTeX + bib)
│  └─ wiki/
│     ├─ index.md                 (更新)
│     └─ decisions/
│        └─ 2026-07-03-evidence-input-configuration.md  (更新)
│
├─ p08-market-calibration/                   P8 主线入口
│  ├─ CLAUDE.md                   (更新)
│  ├─ mimo-prompt.md
│  ├─ README.md
│  ├─ MEMORY.md
│  ├─ state/
│  │  └─ io_spec.md               (更新)
│  ├─ logs/
│  └─ wiki/decisions/
│     └─ 2026-07-03-settlement-layer-configuration.md  (更新)
│
├─ p12-judge-calibration/                    ★ 当前主线 (M1 closed)
│  ├─ CLAUDE.md                   (更新)  ← 旧 CLAUDE.md? 见 #4 注释
│  ├─ claude-prompt.md            (更新, path 替换)
│  ├─ mimo-prompt.md              (更新)
│  ├─ README.md                   (更新)
│  ├─ state/
│  │  ├─ task_spec.md             (更新)
│  │  ├─ progress.json            (更新)
│  │  ├─ experiment_design.md     (更新, P11 path 已指 legacy/)
│  │  ├─ io_spec.md               (更新)
│  │  ├─ directions_tried.json
│  │  ├─ iteration_log.jsonl
│  │  └─ findings.jsonl
│  ├─ logs/                       (work/heartbeat/orchestrator)
│  ├─ paper/outline.md
│  ├─ wiki/index.md               (更新)
│  └─ experiments/
│     ├─ build_sample_manifest.py       (路径算术修: parent.parent)
│     ├─ test_build_sample_manifest.py  (路径算术修)
│     ├─ validate_manifest.sh           (注释修)
│     ├─ sample_manifest.jsonl          (450 rows, source_path = legacy/p11-…)
│     └─ sample_ids_ordered.json        (P12-001..P12-450)
│
└─ p1p2-evidence-ledger/                     概念主线
   ├─ CLAUDE.md                   (更新)
   ├─ mimo-prompt.md              (更新)
   ├─ README.md                   (更新)
   ├─ state/
   │  └─ progress.json            (更新)
   ├─ paper/outline.md            (更新)
   └─ wiki/
      ├─ index.md                 (更新)
      └─ concepts/layer-roles.md  (更新)
```

> #4 注释: p12-judge-calibration/ 没有独立 CLAUDE.md，但是是 README.md 的导航
> 项。p11-inner-monologue 也无 CLAUDE.md，因为其子目录 (legacy/) 是 closed
> 而 non-git parent 是 mix-bag。 这与 P7/P8 pattern 一致 — 加 CLAUDE.md 留给
> 下一个 milestone。

---

## 4. legacy/ 子树 (历史/closed)

```
legacy/
│
├─ p07-legacy-init-2026-07/             (旧 p2.1-signal-fusion-mimo/)
│  ├─ CLAUDE.md
│  ├─ mimo-prompt.md
│  ├─ MEMORY.md
│  ├─ state/
│  └─ logs/
│                                          ⚠️ 仅 init, 无实验数据
│
├─ p08-legacy-init-2026-07/             (旧 p1.2-market-calibration-mimo/)
│  ├─ CLAUDE.md
│  ├─ mimo-prompt.md
│  ├─ MEMORY.md
│  └─ state/
│                                          ⚠️ 仅 init, 无实验数据
│
├─ p11-closed-v5-mimo/                  (旧 p1.1-inner-monologue-mimo/)
│  ├─ .git/                            ← git 仓库, history 保留
│  ├─ CLAUDE.md
│  ├─ README.md
│  ├─ mimo-prompt.md
│  ├─ MEMORY.md
│  ├─ state/
│  ├─ logs/
│  ├─ wiki/concepts/mimo-model.md      (历史旧名, 故意保留)
│  ├─ paper/
│  └─ experiments/
│
├─ p11-closed-v5-minimax-m3/            (旧 p1.1-inner-monologue_minimax-m3/)
│  ├─ .git/                            ← git 仓库, history 保留
│  ├─ CLAUDE.md
│  ├─ README.md
│  ├─ claude-prompt.md
│  ├─ mimo-prompt.md
│  ├─ MEMORY.md
│  ├─ state/
│  │  ├─ progress.json      (status=closed_2026-07-03)
│  │  ├─ closure.md
│  │  ├─ checkpoint.md
│  │  ├─ h1-auditability/
│  │  ├─ h1-continuity/
│  │  └─ task_spec.md
│  ├─ logs/
│  ├─ experiments/
│  │  ├─ h5-emergence/
│  │  │  ├─ A/yaml/  (750 yaml, source of P12 manifest)
│  │  │  ├─ A1, A2b, C/, pilot/
│  │  │  ├─ analysis/
│  │  │  ├─ gold-calibration.json
│  │  │  └─ metadata.json
│  │  └─ ...
│  ├─ paper/
│  ├─ harness/                         (6 v5 scripts, 已修路径上轮)
│  ├─ wiki/
│  │  ├─ closure/
│  │  ├─ decisions/
│  │  └─ concepts/
│  └─ docs/superpowers/{plans,specs}
│
└─ p11-legacy-snapshot-2026-07/         (旧 p1.1-inner-monologue/, 非 git)
   ├─ CLAUDE.md                        (P11 parent snapshot)
   ├─ README.md
   ├─ MEMORY.md
   ├─ experiments/test/
   ├─ logs/{heartbeat,orchestrator,work}.jsonl
   ├─ scripts/
   │  ├─ inner_monologue_experiment.py
   │  ├─ llm_judge_scoring.py
   │  ├─ statistical_analysis.py
   │  └─ test_api.py  (有 2-vs-3-tuple pre-existing bug, 不在本次范围)
   ├─ state/
   ├─ wiki/{annotations,comparisons,concepts,decisions,index.md}
   └─ (无 .git — 父级 M1 bundle, 不可还原)
```

---

## 5. P12 M1 状态在论文树中的位置

```
papers/p12-judge-calibration/
│
├─ state/experiment_design.md       <-- § § § M1 预注册文档 (frozen)
│
├─ experiments/                     <-- ★ M1 全部交付物
│  ├─ sample_manifest.jsonl             450 rows, PIT-105 clean
│  ├─ sample_ids_ordered.json           P12-001..P12-450 (冻结)
│  ├─ build_sample_manifest.py          (parent.parent 路径算术, OK)
│  ├─ test_build_sample_manifest.py     9 unit tests
│  └─ validate_manifest.sh              io_spec §7.1/§7.2/§7.3 guard
│
├─ logs/{work,orchestrator,heartbeat}.jsonl        (框架 §4 + §7)
│
└─ state/
   ├─ progress.json                  (current_milestone=M2 ready)
   ├─ task_spec.md                   (M1 closed, M2 pending)
   ├─ io_spec.md                     (5 protocols frozen)
   ├─ directions_tried.json
   ├─ iteration_log.jsonl
   └─ findings.jsonl                 (M1 closing log line present)
```

---

## 6. cite-redirect 链路

```
读者 / 工具
    │
    ├─ 访问  p1.1-inner-monologue_*/      ──┐
    │                                       │
    ├─ 访问  p12-judge-calibration/        ──┤
    │                                       │
    └─ (其他旧路径)                       ──┤
                                            │
                                            ▼
                              OBSOLETE.md (auto-research 根目录)
                                            │
                                读 mapping table
                                            │
                                            ▼
                  papers/<N>-<topic>/     → 进 ACTIVE 论文
                  legacy/p<N>-<status>-/  → 进 CLOSED/LEGACY 论文
                                            │
                                            ▼
                            + docs/portfolio/aliases.md (alias 表)
```

---

## 7. 仓库层间 (论文 / 框架) 关系

```
                                    ┌───────────────────────┐
                                    │  framework/  (规划中)  │
                                    │  ────────────────     │
                                    │  skills/, prompts/,   │
                                    │  scripts/, schemas/,  │
                                    │  knowledge/,          │
                                    │  runbooks/            │
                                    └───────────▲───────────┘
                                                │
                                                │ (跨论文复用:
                                                │  paper-specific
                                                │  → 上抽 ≥ 2 论文)
                                                │
   ┌────────────────────────────────────────────┴─────────────────────────────┐
   │                            papers/                                      │
   │  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐            │
   │  │ p07-signal-fusion │ │ p08-market-calib. │ │ p12-judge-...   │ ...      │
   │  │   framework/     │  │   framework/     │  │  framework/     │          │
   │  │     (this-paper- │  │     (this-paper- │  │   (prompts/     │          │
   │  │      specific)   │  │      specific)   │  │    judge-...)   │          │
   │  └──────────────────┘  └──────────────────┘  └─────────────────┘            │
   └───────────────────────────────────────────────────────────────────────────┘
```

> 当前 (2026-07-03)：framework/ 顶层尚未创建；p07/p08/p12 各有 framework/
> 子目录但很多还是空的。Day 1 (执行时序) 会从 p12 抽出 judge-protocols.md
> 进 framework/prompts/，验证二态规则。

---

## 8. GitHub Pages (另仓, 当前未创建)

```
                  ┌─────────────────────────────┐
                  │  <owner>.github.io          │
                  │  ──────────────             │
                  │  delichen96.github.io       │  <-- 待用户在 GH 建仓
                  │  内容: mkdocs / hugo 站点   │
                  │  source: 不在 auto-research/│
                  └────▲────────────────────────┘
                       │ push (CI/CD build artifact)
                       │
   ┌───────────────────┴────────────────────────┐
   │  auto-research/website/                   │  <-- 暂无 (Day 1 加)
   │  ────────────                              │
   │  mkdocs.yml                                │
   │  content/{papers,p12.md,...}              │
   │  public/  (gitignored)                     │
   └────────────────────────────────────────────┘
```

> 当前: website/ 目录不存在；CI/CD 不存在；用户在 GH 尚未建 website 仓。
> 蓝图 (restructure-blueprint §5) 标注此为 "framework 仓外另起"。

---

## 9. cite-redirect 之外：根级 OBSOLETE.md 实例

```
auto-research/OBSOLETE.md
─────────────────────────
   自我描述:
     "This top-level layout was reorganized into the new schema on 2026-07-03"

   包含:
     - 9 行 old → new 映射表
     - 为什么不用 git mv (auto-research 自身非 git repo)
     - 向后兼容策略 (redirect stub 即可, 无 symlink)
     - 提醒 agent: 不要再写旧路径
```

---

## 10. 自检 — review 关注点

请重点确认以下 6 点（review 时可按此清单过一遍）：

- [ ] **Q1**: `papers/<N>-<topic>/` 与论文代号 (P7/P8/P11/P12/P1+P2) 视觉一致?
- [ ] **Q2**: `legacy/p11-closed-v5-{mimo,minimax-m3}/` 命名带有版本 + writer，是否能区分两种 closure?
- [ ] **Q3**: p12 主线树的 M1 交付物 (5 文件) 路径 OK?
- [ ] **Q4**: path 算术 (`P12_ROOT.parent.parent`) 在 build_sample_manifest.py 是否对?
- [ ] **Q5**: `OBSOLETE.md` 是否在仓根路径上对 agent 可见?
- [ ] **Q6**: framework/ 顶层还没建 (Day 1 才建), 这是否符合"先做实验"原则? (YAGNI 验证)

---

## 11. 关键事实数字 (落地后实测)

| 维度 | 数字 |
|---|---|
| 顶层子目录变化 (mv count) | 9 个目录移动 |
| sed 替换文件数 (active scope) | 31 个文档 + 3 个 runtime script |
| 顶层 docs/portfolio/ 新增 | naming-audit-2026-07-03.md |
| 顶层新增 | OBSOLETE.md |
| P12 unit tests 通过 | 9 / 9 |
| P12 manifest guard | OK |
| P12 manifest rows | 450 |
| Old-token hits in active scope (post-rename) | 0 |
| Old-token hits in legacy/ + OBSOLETE + 2 proposal | 38 (intentional) |
| Closed git repos preserved (.git intact) | 2 (mimo + minimax-m3) |
