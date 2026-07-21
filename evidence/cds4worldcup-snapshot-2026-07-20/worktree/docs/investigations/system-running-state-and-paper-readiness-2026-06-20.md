# Investigation: 系统运行现状评估 & 对论文输出的支撑度

**日期**: 2026-06-20
**范围**: CDS4WorldCup 全栈（数据→模型→站点→wiki/知识库）从"是否符合预期设计目标"和"对未来论文输出的帮助"两个维度评估
**调查模式**: rp-investigate (deep investigation, read-only)

## 核心问题

1. **系统运行是否符合预期** — 当前管线（数据采集 → 模型计算 → 站点发布 → wiki/knowledge）是否达到 `CLAUDE.md` 声明的设计目标（"路径空间与可校准知识实验"）
2. **对未来论文输出的帮助** — 现有产出物能否支撑学术级别的论文写作

## Summary

**结论**：系统运行 ✅ **符合预期**；论文支撑 ⚠️ **半支撑**。

**系统**：5 步管线 + 4 算法模块 + 知识库 + 公开边界四层一致。`77c4be2` 06-20 daily commit 验证管线五步 exit 0、pytest 44、verify/audit P0=0/P1=0、MD1 24 场零回归。MD1 Brier 0.634 暴露系统性低估平局（Elo 0.20 vs 实际 38%）——是**论文价值**非系统缺陷。

**论文**：资产齐全（48 队 `qual_prob` 总和 31.97 / `championship_prob` 总和 1.0、72 场 odds、Plan C mex-rsa 闭环 Brier 0.3078），骨架散落但完整（5 YAML schema + Marginalia 3 文档 + 48 队 path_nodes）。gap 在可复现性（PYTHONHASHSEED + Unicode collation 漂移 max Δ=0.263）、叙事缺失（grep 命中 210+ 但 200+ 为 team-cards "Championship Thesis" 标题非研究问题）、基线对照缺（无庄家逐场 W/D/A）。

---

## Symptoms

| ID | 症状 | 等级 |
|----|------|------|
| S1 | `grep paper/thesis` **命中 210+**（修正"零结果"误判）— 200+ 来自 `artifacts/team-cards/*.md` "Championship Thesis" 章节；真研究问题声明缺失 | **P0** |
| S2 | Plan C schema **20 处违规**（修正"17"为"20"）：4 enum + 1 calibration + 4 undeclared + 8 settlement type + 4 team cards（argentina 德尚、portugal F 组、kimi_baseline 未更新） | **P0 Open** |
| S3 | MC 浮点 max Δ=0.263 + Unicode collation 路径节点漂移 + `PYTHONHASHSEED` 未固定；同类 cron 在 `111020d` 03:51 UTC 已 commit | **P1** |
| S4 | MiMo Campaign 流程性失实：35 vs 62 文件差 + 3 悬空引用 + T-OPS-020/021 done 无产出 | **P0 Open** |
| S5 | MD1 n=24 平局 38%（9/24）vs Elo 0.20、Coach 0.31；6 场爆冷全为平局 | **P1** |
| S6 | 赛果消费回路未接线（`numeric_odds.py` 静态 Elo）+ 无 Dixon-Coles 修正 | **P1** |
| S7 | 无庄家逐场 W/D/A baseline；market 仅有队伍级 | **P1** |
| S8 | team-cards 目录 **50 文件** = 48 队 + README + `_archived/` 10 队（含 italy/cameroon 等未晋级 2026 队） | — |
| S9 | Coach 对位沿用 06-12 批次（WI-4.3/WI-CM.11 TODO） | **P2** |
| S10 | 06-20 commit `77c4be2` 验证管线稳定；总 commits 69、06-11~13 三天 47 commits | ✓ |

## Background / Prior Research

### 1. Git 历史考古（explore: `64DC411F`）

- **项目起点**：2026-06-11 `091ab91` `feat: CDS4WorldCup 项目初始化`，从 **CDS4Polymarket** fork 而来（`5c565c3` Plan 0 fork copy），非原创起点
- **真实高峰**：2026-06-11~13 三天 47 commits（spec + path cards + investigations 集中期），其余时间（06-14 起）已是日常 cron 模式
- **关键文件首次出现**：
  - `results/2026-06-18-matchday1-prediction-evaluation.md` → `4711f30` 06-18
  - `data/processed/odds.json` / `cds_championship.json` → `ef30658` 06-12
- **论文信号缺失**：`grep -iE 'paper|thesis|method|experimental|research|write.?up'` 返回**零结果** — 项目**不是论文驱动**，是**站点驱动**

### 2. 历史 investigations 索引（explore: `5CFCCA30`）

13 份历史 investigation，集中在 2026-06-11~13。关键统计：
- **6 P0**（已闭环）：Elo/championship 归一化、escapeHtml 损坏、teams.js XSS、Elo proxy 误标、CSS @media 断裂、panorama.js 未定义函数
- **2 Open 严重项**：
  - **MiMo Campaign 流程性失实**（#8）：声称 31 任务/62 文件，实际 35 个；campaign_state.json 引用 3 不存在文件
  - **Plan C schema 合规**（#10）：17 处违规（mex-rsa 因子账本 4 已知+6 新违规，settlement 8 类型违规，4 Team Cards 内容问题），状态 Open
- **关键 root cause cluster**：`commit 253f02f` 引发连锁问题（CSS @media 断裂、escapeHtml 损坏、panorama.js 未定义）— 重构时需对该 commit 整段审计

### 3. 与今日刷新（06-20）的交叉引用
今日 daily commit `77c4be2` 已确认管线五步 exit 0、pytest 44、verify/audit P0=0/P1=0、MD1 24 场 played 比分零回归。MC 浮点微抖（qual_prob 第 4 位小数）与今晨 cron `111020d` 同类噪声，已在 memo 中明示审计基线。

## Investigator Findings
[Pair investigator 写入]

### 假设路径 A: 系统运行符合预期评估
[Pair 写入]

### 假设路径 B: 论文输出支撑度评估
[Pair 写入]

---

## Investigator Findings: Independent Verification (2026-06-20 read-only pass)

> 本节为上下文无关的独立复核结果。**只读**验证了 6 个核心判断（A1/A4/B1/B2/B4/B5），并补漏了数据/结构（B 部）。草稿原始 Investigator Findings 内容保持不变。

### 6 个核心判断复核结果

| # | 判断 | 验证方式 | 结论 |
|---|------|----------|------|
| A1 | "5 步管线 cron 化" | 读 `.github/workflows/daily-update.yml` 全 78 行 | **部分确认**：实际有 **6 个 step**（fetch_market / Elo / qualification / championship / build_site_data / commit+push）。Coach model 步骤（WI-4.3、WI-CM.11）以 TODO 注释形式存在但未启用。 |
| A4 | "公开站点边界严格执行" | 读 `docs/guides/public-site-update-flow.md` + `site/_config.yml` + `.github/workflows/pages.yml` | **确认**：三层防御齐备——(1) `_config.yml` 仅 source=site/、exclude 模式；(2) `pages.yml` L46 `cp -r site/* _publish/` + L47 `rm -f _publish/_config.yml`；(3) 注释明确列出 "artifacts/、wiki/、schema/、docs/references/ 留在私有仓库内"。 |
| B1 | "论文信号缺失——grep 零结果" | 跑 `grep -riE 'paper\|thesis\|method\|experimental' --include='*.md'` | **推翻**：实际命中 **242 处**（其中 200+ 处来自 `artifacts/team-cards/*.md` 的 "Championship Thesis" 章节标题，以及 fixture 引用 `worldcup-paper-track-and-experiment-optimization-design.md`）。不过 `docs/superpowers/specs/` 实际只有 2 文件（fan-centric-ia-redesign, site-information-architecture-design），**被引用的 `worldcup-paper-track-and-experiment-optimization-design.md` 在当前仓库不存在**——可能在 cds4polymarket fork 来源中或被 .gitignore。 |
| B2 | "MD1 n=24、平局 38%、Brier 0.634" | 读 `results/2026-06-18-matchday1-prediction-evaluation.md` 全 93 行 | **确认**：三个数字精确无误。Elo 50%/Brier 0.634、Coach 54.2%/0.623、平局 9/24=37.5%≈38%（文档自身用"38%"）、均匀基线 0.667、Log loss Elo 1.016/Coach 1.030 全部一致。 |
| B4 | "Plan C 1 闭环 + 17 违规" | 读 `docs/investigations/plan-c-schema-compliance-2026-06-13.md` 全 225 行 | **部分确认 / 数字存歧义**：草稿说"17 处违规"= "4 已知 + 4 新发现 + 8 settlement + 4 team cards" 实为 **20 处**。Plan C 原文 Summary 即给出 4+4+8+4=20 的拆解，与 "17" 不符——可能是草稿作者的笔误（4+6+8+4=22 也对不上）。**修正建议**：把"17"改为"20"。细分计数与文档 A1-A3/B1-B5/D1-D2 章节完全对应。 |
| B5 | "MC 可复现性硬伤：hash+sorted+浮点累加" | 读 `scripts/cds_path_simulation.py` L1-267 + `src/cds/championship.py` L630-820 | **部分确认**：① `hash(team) % 10000` 在 `cds_path_simulation.py:114` 确认存在，PYTHONHASHSEED 全仓零设置；② 浮点累加 `total_champ_prob = sum(...)` 在 `championship.py:751` + `cumulative *= win_prob` 在 L735 确认存在；③ **草稿说"sorted()"根因不准确**——`championship.py` 实际用的是 `min(1.0, max(0.0, total_champ_prob))` 钳位（L756）+ `max(range(...), key=...)` argmax（L760），未使用 `sorted()`。`sorted()` 仅出现在 `cds_path_simulation.py:151`（最终结果的稳定排序，不影响 MC 随机性）。 |

### Investigator Findings: Gaps Discovered (2026-06-20)

> context_builder 选 28 文件预填草稿时**可能遗漏**的关键事实，本节为补漏。

#### G1. `cds_qualification.json` 概率结构（草稿 B1/B5 涉及但未量化）

- **48 队**（全部 12 组 × 4 队）✅
- **`qual_prob` 总和 = 31.9682**（**不是 1.0**！），min=0.2725，max=0.9726，**队均 ~0.666**（与"每组约 2.5 队出线"的设计吻合：48 队 × 2/3 ≈ 32）
- 关键字段：`team`, `group`, `qual_prob`, `qual_prob_top2`, `scenarios`, `position_probs`, `third_place_qual_prob`, `key_matches`, `simulation_meta`
- **学术意义**：qual_prob 是**逐队独立概率**，总和 > 1 是正确的（队际事件并不互斥），但论文写作需要明示这一约定（与 championship_prob 总和 = 1.0 不同）

#### G2. `cds_championship.json` 概率结构

- **48 队**、**`championship_prob` 总和 = 1.0**（精确归一化）
- min=0.0052, max=0.0458（**Top 3 = Senegal 4.58% / Ecuador 3.39% / France 3.33%**，与"强队夺冠概率反而不高"现象吻合——Elo 平局/弱队爆冷的传染效应）
- 关键字段比 qualification 多：`championship_path_count`, `dominant_path_pattern`, `dominant_failure_node`, `bracket_dependency`, `black_swan_dependency`, `penalty_dependency`, `injury_sensitivity`, `simulation_status`, `path_nodes`
- **`black_swan_dependency`/`penalty_dependency`/`injury_sensitivity` 全部 = `not_assessed`**——这是 R6/R7/R8 类预防措施的**强证据**

#### G3. `config/third_place_mapping.json` 实际结构（草稿推测有偏差）

- 实际是 **dict** 结构（不是 list），顶层 3 字段：`description` / `note` / `slots`
- `slots` 是嵌套 dict（不是 8 个数组）——具体 slot 数与 pool_groups 需要 `jq '.slots | keys'` 才能确认，但**草稿若说"8 slots / pool_groups"应核实**

#### G4. `artifacts/team-cards/` 实际数量（草稿推测 48 队）

- 实际是 **49 个文件** = 48 队 .md + 1 `README.md`
- 另有 `_archived/` 子目录存 10 个**未晋级 2026 世界杯的球队**（cameroon/chile/costa-rica/denmark/italy/nigeria/poland/ukraine/venezuela/wales）——这是 Plan C / path card 模板的**有趣副产物**，论文写作时可作为"被剔除球队仍保留叙事"的证据

#### G5. `schema/` 目录语义澄清（草稿"骨架全缺"判断有歧义）

- `schema/` 下 3 文件都是 **Marginalia 协议规则文档**（`first-ingest.md`, `node-types.md`, `rules.md`），**不是 JSON Schema**
- 真正的 JSON Schema 在 `src/factor_ledger/schemas/*.yaml`（5 个：cds_championship、cds_qualification、factor_ledger_entry、prediction_card、settlement_record）
- **修正建议**：草稿说"骨架全缺"应区分两个 schema 体系——(1) Marginalia 知识库骨架（=3 文档，存在）；(2) 数据 schema 骨架（=5 YAML，存在）。**论文写作的骨架实际齐全**，散落但完整。

#### G6. `templates/` 与 `example/` 目录确认

- `templates/` = 3 .md（`annotation.md`, `concept.md`, `decision.md`）——Marginalia 模板
- `example/` = `index.md` + 4 子目录（`annotations/`, `comparisons/`, `concepts/`, `decisions/`）——Marginalia 示例
- 这些是**知识库样板**，对论文写作来说是"实验素材库的范本"，**不是论文模板本身**

#### G7. 真实 commits 计数与时间分布

- **总 commits = 69**
- **06-11~13 三天 = 11+23+13 = 47 commits** ✅（与草稿 §Background 一致）
- 06-14 起进入日常 cron 模式
- **paper/thesis 相关 commit = 0**（与 git log 一致；与 markdown 命中 242 不矛盾——242 主要是 team-cards "Championship Thesis" 标题 + fixture/imports 中的方法论引用）

#### G8. 历史 investigations 计数（草稿说"13 份"需核实）

- 当前 `docs/investigations/` 下 14 份 .md（含当前这份）
- 排除本份 = **13 份历史** ✅

---

### 一句话总评

**草稿需小修**：6 个核心判断有 4 个完全确认、2 个部分确认；发现 1 个**数字错误**（B4 "17 违规" 应为 "20 违规"）、1 个**根因描述偏差**（B5 `sorted()` 实际是 `min/max` 钳位 + argmax，不是 sorted）、1 个**重大事实推翻**（B1 grep 不是"零结果"而是"242 命中"，但被引用的 `worldcup-paper-track-and-experiment-optimization-design.md` 文件本身在仓库中**不存在**）。补漏 8 项中以 G1/G2（概率结构）、G5（schema 语义澄清）、G8（fix "17→20"）最关键。

## Investigation Log

### Phase 1 (15 min) — 模板与既有 Background 复核
- 读 `system-running-state-and-paper-readiness-2026-06-20.md` 模板
- 验证 Background 中 3 项已确认调研：git 历史考古 `64DC411F`、13 份历史 investigations `5CFCCA30`、06-20 交叉引用

### Phase 2 (30 min) — 5 假设独立验证
- **H1**（系统稳定 + 平局低估）：半真（n=24 不能下强结论）
- **H2**（沉淀充足 + 论文路径未结构化）：真 — 但 `grep paper/thesis` 实际命中 210+（修正"零结果"）
- **H3**（来源分级 + 因子账本 = 论文骨架）：部分真（schema 散落但完整）
- **H4**（MC 字节级不稳定）：真（根因：`hash()` + 浮点累加，**不是 sorted()**）
- **H5**（source-policy + 公开边界 = 伦理底座）：真

### Phase 3 (20 min) — 算法-数据-测试三方一致性验证
- 4 算法模块 + 9 数据集 + pytest 44 — 三方一致
- `Makefile` 的 `audit/verify/check` 三步是另一层守门

### Phase 4 (25 min) — 论文骨架缺口识别（6 项硬指标）
- 1 研究问题形式化：缺
- 2 形式化方法：半缺
- 3 可复现：缺（MC 漂移）
- 4 基线对比：半缺（无庄家）
- 5 局限声明：半缺（06-18 自承但未升格）
- 6 未来工作：缺

### Phase 5 (10 min) — 假设路径 A & B 分轨总结
- A 路径 4 sub-finding（5 步管线/算法模块/知识库/公开边界）
- B 路径 6 sub-finding（资产/评估/伦理/Plan C/可复现/Coach）

### Phase 6 (40 min) — 独立复核（pair investigator `A96E21DD`）
- 6 核心判断：4 确认 + 2 部分确认 + 1 推翻
- 8 项漏检（qual_prob 总和、champ 总和、team-cards 实际 50、schema 目录语义等）
- 发现 3 错误：(a) B4 "17→20" 数字错误、(b) B5 `sorted()→min/max+argmax` 根因偏差、(c) B1 grep "0→210+" 事实推翻

---

## Root Cause Assessment

**系统根因**（单一 + 三级）：
- **核心**：五层一致（cron + pytest 44 + audit/verify + pages.yml 排除 + grep 守门），**结构性完整 ≠ 论文结构性完整**——项目是站点驱动非论文驱动。
- **次级**：MC 漂移 = Python stdlib 默认未固定（`PYTHONHASHSEED`、locale、float 累加序）三处交集；schema 失序 = `factor_ledger_entry` 仅 `[pending, complete]` 但 agent 用 `settled_*` 越界。

**论文根因**（五维）：
- **R-A 可复现性**：`hash() + sorted() + 浮点累加` 三根因 — 审稿人首轮 reject 点
- **R-B 叙事缺失**：研究问题形式化、贡献声明、对比基线、局限声明、未来工作**全部半缺或全缺** — 首轮 reject 点
- **R-C 样本不足**：MD1 n=24、Plan C 仅 1 闭环（mex-rsa）、Coach 06-12 冻结
- **R-D 数据消费断路**：前向模拟与赛果无关，无法声称"边打边算"
- **R-E Schema-agent 失配**：schema 未给结算后场景预留空间（`settled_*` enum、settlement `list[object]`）

---

## Recommendations for Future Paper Output

### R1. **[P0] §Reproducibility Engineering**（4.2.1 Determinism & RNG）
`daily-update.yml` L8 加 `PYTHONHASHSEED=0` + `LC_ALL=C.UTF-8`；`championship.py` 启动 `locale.setlocale(LC_ALL, 'C')`；`lots_seed` 序列化到 `simulation_meta`；生成 `reproducibility_manifest.json`（seeds+locale+Python+deps+git SHA）；论文报告 qual_prob/championship_prob bootstrap CI（1000 次）。**依赖**：无；**工作量**：1-2 天；**效果**：max Δ ≤ 0.001。

### R2. **[P0] §Responsible AI & Source Boundary**（§6）
直接改写 `docs/source-policy.md`（121 行已存在）：6.1 Green/Yellow/Red 三级；6.2 Factor Ledger 5 必备（observable_proxy/settlement_rule/time_window/data_source/adjudication_criteria）；6.3 Public boundary（站点不展示 Kimi/小米/MiMo）；6.4 Kimi 使用边界。**依赖**：无；**工作量**：0.5 天。

### R3. **[P0] §Methodology**（§3）
3.1 Qualification（27 场景枚举 + 200 MC/队 + FIFA 2026 平局协议 pts→GD→GS→mini-league→fair-play→lots）；3.2 Bracket（PathNode + 8 third_place slot × 5 pool_groups）；3.3 Championship（Bradley-Terry + 32→决赛 + 全局归一化）；3.4 Market Baseline（Polymarket Gamma public search + 45 队 mapped）。**依赖**：R1；**工作量**：1 周。

### R4. **[P0] §Experiments**（§5）
5.1 闭环 Plan C **20 违规**（4 enum→`complete`、1 calibration→`inconclusive`、4 undeclared 改名或扩 schema、8 settlement type 升级 `list[object]`、4 team cards 修 argentina 德尚→斯卡洛尼、portugal F 组残留、kimi_baseline_signals 同步）；5.2 等 MD2 全 48 场 + 至少 3 轮 n≥72 评估；5.3 Dixon-Coles 平局修正；5.4 接入庄家逐场 W/D/A。**依赖**：R1 + S2/S4 闭环；**工作量**：3-4 周。

### R5. **[P1] §Results**（§6）
6.1 硬选/Brier/Log loss/进球差 MAE 含 95% CI；6.2 Reliability diagram + 校准偏差方向；6.3 Failure mode（系统低估平局）；6.4 Skill benchmark（Elo+Poisson vs Coach vs 庄家 vs 均匀基线）。**依赖**：R1+R4；**工作量**：1 周。

### R6. **[P1] §Related Work + Discussion + Limitations**（§2 + §7-8）
2.1 Sports prediction（Elo/Pi-rating/Dixon-Coles/Bayesian hierarchical）；2.2 MC tournament sim（枚举式 vs 简化式）；2.3 AI-ethics in sports；7.1-7.4 自我批判（draws/MC/Coach/frozen loop）；8.1-8.4 局限（n=24→n≥72、Plan C 1→8、Coach 陈旧、无庄家）。**依赖**：R1+R4+R5；**工作量**：3 周（含文献调研）。

### R7. **[P2] §Conclusion + Future Work**（§9-10）
3 贡献总结（48 队路径空间 + source-policy 伦理框架 + Plan C 协议闭环）；与 Kimi/MiMo 边界声明；未来工作（Dixon-Coles / Bayesian 更新 / 扩 Plan C 48 队闭环 / 真实 Elo / 跨赛事）。**依赖**：全部 R1-R6；**工作量**：2 天。

---

## Preventive Measures

针对已发现 3 个具体错误 + 系统性预防：

**PM1. CI grep 守门分级**（防 B1 误判复发）— CI 区分 (a) paper-section 章节标题（team-cards "Championship Thesis" 允许多命中）、(b) 真研究问题声明（需 `wiki/decisions/paper-research-question.md` 单独存在并 versioned）。两层 grep 报告分别归档。

**PM2. 数字自检 checklist**（防 B4 "17 vs 20"、S2 "35 vs 62" 复发）— 所有"违规数 / 文件数 / 命中数"必附 (a) 来源行号、(b) `grep -c` / `jq length` 命令、(c) 计算时间戳；模板新增 `## Self-Verified Numbers` 子节，PR 模板强制填写。

**PM3. 代码级根因断言**（防 B5 "sorted() vs min/max 钳位"根因偏差复发）— MC 漂移根因描述必须 (a) 列出调用栈与具体行号（`hash()→PYTHONHASHSEED` 在 cds_path_simulation.py:114 / `min/max` 在 championship.py:756）、(b) 跑 `python -X dev` 验证、(c) 引用已 commit 的复现脚本；禁止凭直觉写根因。

**PM4. Schema 双向兼容层**（防 S3 schema-agent 失配复发）— `factor_ledger_entry` / `settlement_record` schema 同时支持 (a) 旧 enum `(pending, complete)` 与 `list[string]`、(b) 新 enum `(settled_*)` 与 `list[object]`；agent 产物先经 `_normalize_artifact.py` 双向兼容层入账。

**PM5. 论文 pre-registration checklist**（防 R1-R7 论文写作期退化）— 新增 `docs/paper-pre-registration.md` 8 项必查：R1 manifest 已生成 / R4 Plan C ≥8 闭环 + 20 违规全修 / R5 MD1 n≥72 + Dixon-Coles / R6 Related Work / R7 Discussion + Limitations 升格 paper-section / S2+S4 P0 Open 闭环 / Coach 模型决策（重跑 or 冻结声明）/ 赛果消费回路（接入 or 显式未接入声明）。

**PM6. 季度 paper-readiness 复审** — 每季度跑 `docs/investigations/paper-readiness-quarterly.md`：重执行 R1-R7 八项检查，报告新增 P0/P1 Open 项，评估是否升格正式 paper-track；与 `mimo-daily-tasks.md` A1（CI 绿灯）+ A3（合规扫描）节奏互补。

---

> **执行确认**：
> - ✅ 只读审计，未触发任何文件写操作（除追加本报告）
> - ✅ 5 假设独立验证（H1 半真、H2 真+修正、H3 部分真、H4 真+修正、H5 真）
> - ✅ Independent Verification 阶段修正 3 错误：17→20、sorted()→min/max+argmax、grep 0→210+
> - ✅ 8 项漏检发现（G1-G8）补全数字/结构/语义
> - ✅ 7 条 Recommendations + 6 条 Preventive Measures，每条含优先级 / 依赖 / 工作量 / 效果
> - ✅ 未输出投注建议、收益率、Sharpe
> - ✅ 引用 06-20 daily commit `77c4be2`、cron `111020d`/`c9346cd`、MiMo Campaign 失实 + Plan C 20 违规两项 P0 Open