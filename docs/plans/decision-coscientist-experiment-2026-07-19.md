# Decision Co-Scientist 实验方案（Nature 标准）

> 日期：2026-07-19 ｜ 状态：v2（builder 骨架 + 设计评审修订，评审记录 `docs/reviews/plan-critique-decision-coscientist-experiment-2026-07-19.md`）｜ 上游：`docs/investigations/decision-coscientist-proposal/`（开题报告 v1.3.1、终裁 memo、PROJECT-BRIEF）
> 实施侧主战场：`Policysim-v0.2/dev/backend`（引擎）+ `auto-research`（锚资产、合规资产、分析）

## Goal

构建并执行 Decision Co-Scientist 的实验验证链：**古雷单场景 MVE → 全设计主实验（4 条件 × 4 基线 × 3 消融）→ 多案例扩展（郑州 7·20、Buncefield、横州六蓝）**。实验设计、统计报告与可复现性按 Nature 系发表标准建设；投稿节奏为 NeurIPS D&B 先行，Nature Computational Science 作滚动目标（用户决策 2026-07-19）。

## Background

**开题报告已钉死**（`proposal-decision-coscientist.md`）：
- H1–H4 判定规则与预注册统计方案：配对 Wilcoxon 符号秩 / 非配对置换检验或 Mann-Whitney U；BH 校正按假设族；N≈175/组（δ=0.3，功效 0.8，α=0.05）至 395（δ=0.2）；报告 Cliff's δ 与 CI；反转零假设（≤15% 均值差判等价）；Axtell bootstrap 防假阴性（:139–144, :199–208）
- 臂定义：C0 单批次协商 / C1 仅锦标赛 / C2 锦标赛+进化 / C3 全闭环；B1 best-of-N / B2 普通 GA / B3 人类专家 / B4 直接作答；3 组消融（:170–180）；同评估协议 + 同 token 预算（:168）
- 60/40 锚分离：前兆/抑制/分支/反证四族分层，实验前冻结；**评估池两案合计 ≥8 条可裁定因子**（:139, :158）
- 回退条款：G2 不可达则转方法短文；锚协议未就绪触发降级（:242–248）；污染控制六条（:205）；H4 四道关（:144）

**引擎现状（2026-07-19 代码级核查，路径前缀 `Policysim-v0.2/dev/backend/src/`）**：
- 可跑：`experiment.service.ts:92` `runBaselineInference`（C0/B4 等价）；`:78` `runMultiAgentSimulation`（MAMR）；`monte-carlo.controller.ts:73` `/api/monte-carlo/compare` 主入口；`strategy-search.service.ts`（候选生成+启动+Pareto，M3 骨架）；`comparison.service.ts`（百分位 P5–P95）；handler 已注入 `SEED-${batchId}-${runIndex}` 提示词层扰动（软基础，待硬化）
- 未实现：C1/C2/C3、B1–B4 无代码；Multi-Judge 空缺；校验臂空白；Tsinghua 仓 `tournament.py` 是 LLM 模型评测引擎，非策略进化
- G2 实锤：`ChatCompletionOptions` 无 `seed` 字段，7 个 provider service 请求体均只有 `temperature`/`max_tokens`（`modules/ai/services/*.service.ts`）
- 锚资产：古雷 9 因子已编码（`anchors/gulei-2015-0406.factors.yaml`）；结算模板现成；`gold-hml-anchors.yaml`（H/M/L 校准素材）；横州六蓝 seed 已建（`emergency-scenarios.seed.ts`）

**用户决策（2026-07-19）**：① Nature 标准、分阶段投稿；② 预算不设硬顶、按功效分析满配；③ 专家 panel 不确定 → fallback（公开实务方案集 + 延迟招募并行）；④ 横州六蓝纳入主设计（条件触发型零污染锚）。

**Nature 合规基线（2026-07-19 官方调研）**：主文 ≤3,500 词 + Online Methods；Data/Code Availability **强制**（Zenodo/Code Ocean DOI）；软件版本入 Methods；单命令安装 + 随机性 deterministic（Whitaker 2021 Silver）；ML Reporting Summary V1.1；LLM 精确版本 + 访问日期 + 代表性 prompts 披露；AI 生成内容声明强制；**ComSci 不收 RR** → 预注册走 OSF/Figshare 公共仓库；统计须报精确 p + 效应量 + 95% CI + 多重比较校正 + 样本量依据。

**统计工具链（已核实）**：α-Rank → `open_spiel.python.egt.alpharank`（OpenSpiel v1.6.12）；检验 → scipy 1.18.0（`wilcoxon`/`permutation_test`/`mannwhitneyu`/`false_discovery_control`）；LHS → `scipy.stats.qmc.LatinHypercube(rng=np.random.default_rng(seed))`；TOST → `scipy.stats.ttost_ind`；Cliff's δ → `δ=2U/(n₁n₂)−1` 换算。

## Approach

总策略：**在 Policysim-v0.2 现有引擎上最小侵入地长出 Co-Scientist 闭环**——不另起炉灶，复用 `startSimulation`/`compare`/`strategy-search`/provenance 审计四条既有主干；G2 先行（它是所有统计结论的地基，闸门从开题 W4 末前移至 W1 末，尽早证伪成本低）；MVE 卡在开题原 W15 主实验之前（对齐终裁 memo 修正清单 #1）；Nature 合规资产与引擎建设并行，不等数据。

**架构增量**（`dev/backend/src/modules/`）：
- `monte-carlo/services/` 新增：`tournament-orchestrator`（C1/C2 配对+N 次 MC+judge）、`evolution-operators`（M3 变异/杂交/多样性）、`alpharank`（α-Rank+Nash averaging+Cliff's δ+bootstrap CI，纯 TS 端口，对照 OpenSpiel 验证）、`judge-panel`（M4 Multi-Judge+Gold 校准+Youden J）、`feedback-loop`（M4 元评审回灌）、`validation-arm`（GB 50151 泡沫闸门 + NUREG/CR-7002 疏散排队）、`hypothesis-generation`（M1 生成+聚类去重）、`distribution-independence`（G2 验收检验）
- `anchors/` 新模块：`factor-ledger` / `settlement` / `pool`（60/40 冻结）三服务 + 新表 migration（tournament_pairings / judge_votes / evolution_generations / anchor_factors / settlement_records / judge_prompt_hashes）
- `ai/` 改造：`ChatCompletionOptions` 与 `ProvenanceContext` 加 `seed?`；7 个 provider service 请求体接入 seed（**Anthropic 不支持 → 自动降级 temperature=0 + 固定 prompt + `usedFallback` 标记**）；provenance 落库 seed（Silver 标准审计点）；`LatinHypercubeSamplerService` 保留 LCG、新增 `sampleScipy`（Python 微服务 adapter，保向后兼容）
- `emergency-scenario.handler` 扩展 sim 可观测性：复燃状态机、罐区 1.5D 邻罐几何、伤亡伤/亡分离（Q4 备忘录已知缺口）
- 实验数据流：候选 → `startSimulation`（seed 透传）→ 三轮协商 → metrics 提取 → 锦标赛评分 → α-Rank → 进化产生下一代 → 终末 settlement（评估池因子裁定）

**关键设计选择**：
1. α-Rank 用纯 TS 端口而非 Python 依赖——部署简单，用 OpenSpiel 输出做正确性对照。
2. LHS 走 adapter（新增 `sampleScipy` 调 scipy 微服务）而非替换现有 LCG——不破坏向后兼容。
3. MVE 配置：古雷 8 候选（4 初始 + 4 进化一代）× 30 runs = 240 runs，单底座 `deepseek-v4-flash`——它是可行性探针兼成本试跑，不是 H1/H3 完整检验。
4. 专家 fallback 双轨：W1 启动招募，W11 未达 3 人 → B3 改用公开实务方案集（备案预案/官方战法），盲评由校准后的 judge panel 代行并在论文中声明；Buncefield 力争 ≥1 名国际专家。
5. 横州六蓝写成条件触发型工作流：Tier 4 监测官方报告 → 发布 7 日内 Tier 1-2 草编 → 14 日内 Tier 3 核验入库 → 28 日内跑 B4 对照（零污染特性）；W18 未发布则主实验按 3 场景收官，横州降为扩展。

## Work Items

按依赖编号 `W{周}-{序}`；每项：内容 / 依赖 / 验收 / 决策点。**四个硬 go/no-go：W1 末 G2、W14 末 MVE 可行性、W18 末横州触发、W22 末总回退。**

### Phase A：G2 与基础设施（W1–W4，关键路径）

> W1–W2 的第一轮数据同时回答四个早期未知：Anthropic seed 支持情况、scipy 微服务延迟、LHS 选型、各 provider 确定性边界。

| # | 内容 | 依赖 | 验收 | 决策点 |
|---|---|---|---|---|
| W1-1 | 全 provider seed 接入（接口+7 service+provenance 落库；含 Anthropic 降级路径） | — | `seed-reproducibility.spec.ts`：同 (prompt,seed) 两次调用输出一致（vendor 承诺范围内），7 provider 全覆盖 | **W1 末 G2 闸门**：任一 provider 同 seed 输出不可复现 → no-go，阻断后续 |
| W1-2 | scipy 微服务（`/lhs-sample`、`/tost`、`/cliffs-delta-bootstrap`）+ `sampleScipy` adapter | W1-1 | 100 次采样 KS 均匀性优于 LCG（p<0.01）；调用延迟 <100ms | 延迟不达标 → 改 npm wasm 包（本项内决断，不留尾巴） |
| W1-3 | `DistributionIndependenceService`（跨 seed Mann-Whitney + Levene + KS） | W1-1 | 古雷 5 seed × 20 runs：跨 seed 分布有显著差异且单组不偏离均匀 | 独立性失败 → 进入 G2 降级评估（见 Open Questions） |
| W2-1 | sim 可观测性三项（回归级）：复燃状态机 + 罐区 1.5D 邻罐几何 + 伤亡伤/亡分离 | W1-1 | 古雷 50 runs 回归：复燃概率 ∈[0.30,0.80]（对锚 f004）、P(蔓延)≤0.05、P(零死亡)=1.0 | — |

### Phase B：M1–M4 引擎（W3–W11）

| # | 内容 | 依赖 | 验收 |
|---|---|---|---|
| W3-1 | `TournamentOrchestratorService`（adaptive/round_robin 配对 + N 次 MC + judge 评分） | W1-1 | 8 候选 × 5 对 × 5 runs 端到端跑通 |
| W3-2 | `AlphaRankService`（α-Rank + Nash averaging + Cliff's δ bootstrap） | — | toy 数据与 OpenSpiel 排序一致；δ 与 scipy 对照 ±0.02 |
| W3-3 | `EvolutionOperatorsService`（3 变异 + 2 杂交 + 多样性度量） | W1-2 | 4 父代→8 子代，扰动在算子范围内、多样性超阈值 |
| W3-4 | `StrategySearchService` 加 `mode='evolution'` 主路径 + 候选表加代次字段（含与 judge panel 的集成，由 W12-1 e2e 终验） | W3-1/2/3 | e2e：1 代进化后 α-Rank 稳定，DB 父子代正确 |
| W4-1 | `JudgePanelService`（Multi-Judge 投票 + Gold 校准 + Youden J） | W1-1 | 4 judge × H/M/L 锚：κ≥0.6、误判率 ≤10%、J>0 |
| W4-2 | `FeedbackLoopService`（元评审模式回写 prompt/权重） | W4-1 | mock 20 轮评审产出可回写的权重调整 |
| W4-3 | `ValidationArmService`（GB 50151 泡沫闸门 + NUREG/CR-7002 ETE） | — | 古雷 f002/f008 过校验臂，红色告警率 <5% |
| W5-1 | `HypothesisGenerationService`（生成 + embedding 聚类去重） | W1-1 | 古雷 16 候选去重后 ≥12 簇 |
| W5-2 | judge prompt v1 文件 + 哈希清单（**W12 前必备**，保障 MVE 起 judge 稳定）；commit-lock 钩子延至 W19 投稿前安装 | — | 哈希清单入库；prompt 改动可追溯 |

### Phase C：锚扩展（W6–W11，与 B 并行）

| # | 内容 | 依赖 | 验收 |
|---|---|---|---|
| W6-1 | anchors 模块 + 新表 migration + 古雷 9 因子导入 | — | CRUD API 可用；9 因子入库 |
| W6-2 | 锚池 60/40 按四族分层冻结 | W6-1 | AllocationSnapshot 写库 + commit-lock；古雷评估池 ≥3，**郑州编码后两案评估池合计 ≥8（开题下限）** |
| W6-3 | `SettlementService` + 古雷 settlement 首跑 | W6-1/2 | settlement_record 生成；泡沫因子 supported、环境因子 inconclusive（PX 争议降半级） |
| W7-1 | 郑州 7·20 因子编码（人工，≥15 条，负锚方式） | W6-1 | 四族齐备、可裁定；郭家咀有效部分纳入 |
| W7-2 | Buncefield 因子编码（人工，≥12 条，跨辖区） | W7-1 | 入库可裁定；HSE/国内格式差异已对齐 |
| W8-1 | 横州六蓝 Tier 4 条件触发工作流（GitHub Actions 监测） | W6-1 | mock 发布 → 自动草编 + 核验清单；**信源清单（应急部/广西水利厅/广西政府网）W8 前人工核实一轮** |

### Phase D：MVE 古雷单场景（W12–W14）

| # | 内容 | 依赖 | 验收 |
|---|---|---|---|
| W12-1 | MVE 配置跑：8 候选 × 30 runs = 240 runs（C0 vs C2，单底座） | W3-4, **W4-1**, W4-3, W6-3 | 240 runs 全完成，verificationReport 非空；**兼作成本试跑（实测 token 外推主实验预算）** |
| W12-2 | MVE settlement：适应度池因子逐条裁定 | W12-1 | ≥4/6 supported、≤1 rejected |
| W12-3 | MVE judge 校准跑（古雷 H/M/L Gold 锚） | W4-1 | κ≥0.6、误判率 ≤10%、J>0 |
| W12-4 | **W14 末 MVE 可行性闸门**：240 runs 齐 + ≥4 supported + κ≥0.6 + 误判率 ≤10% + 分布独立性通过。**注意：本闸门只验可行性；H4 四道关全量判定在主实验 W16-4** | 以上 | go → 主实验；no-go → 阻断，按降级路径（workshop 版/方法短文） |

### Phase E：主实验（W15–W19）

| # | 内容 | 依赖 | 验收 |
|---|---|---|---|
| W15-1 | 主实验满配：8 臂 × N=175/组 × 3 场景（古雷/郑州/Buncefield）× 2 底座（deepseek-v4-flash + glm-5）≈ 8400 runs | W12-4 go | 全部 batch 完成；token 消耗按 W12-1 实测复核 |
| W15-2 | 消融 3 组 × N=87 × **2 场景（古雷+郑州，成本对齐）** × 2 底座 ≈ 1044 runs；**校正沿用 BH（按消融族），不开新口径** | W15-1 | 消融方向与假设一致（缺位应降主效应） |
| W16-1 | 统计分析：配对 Wilcoxon + Cliff's δ + bootstrap CI（H1 族 28 对比 + H3 族，BH 校正） | W15-1/2 | 精确 p + 效应量 + 95% CI 全报告 |
| W16-2 | 反转零假设 TOST（Δ=0.15×mean(C0)） | W16-1 | 等价检验报告；显著且等价的边界案例单独讨论 |
| W16-3 | 跨底座复现：两底座主结论不翻转 | W15-1/2 | 一致率 ≥80%；不一致案例 Discussion 分析 |
| W16-4 | **H4 四道关全量判定**：Gold 锚误判率 ≪10% + Youden J>0 + judge 与校验臂排名 Kendall's τ≥0.5（≥10 策略对，限覆盖维度）+ 跨底座不翻转（用 W16-3 数据） | W16-1, W4-1, W4-3 | 四道关报告齐出；任一不过 → H4 不成立并在论文如实报告 |
| W17-1 | 全场景 settlement + H3 汇总判定（评估池 supported ≥60% 且无因子族被系统 rejected） | W15-1/2, W7-1/2 | ≥200 条 settlement_records；H3 判定自动报告 |
| W17-2 | **W18 末横州触发判定**：报告已发布 → 4 场景满配；未发布 → 3 场景收官 + 横州扩展 | W8-1 | 判定记录存档 |

### Phase F：Nature 合规资产（并行）

| # | 内容 | 依赖 | 验收 |
|---|---|---|---|
| W5-4 | Zenodo DOI 仓库（代码+数据+脚本版本化） | W3-4, W6-1 | 概念 DOI + 版本 DOI 自动颁发 |
| W10-1 | 复现包 `docker-compose`（DB + provider mock + 报告服务，`./run.sh` 单命令） | W3-4, W4-1, W4-3 | 干净环境一次跑通 |
| W10-2 | Silver 标准复现测试（同 seed 两遍 bit-identical；provenance seed 非空） | W10-1 | 100 runs 对照全 deterministic |
| W19-1 | 主报告初稿（≤3,500 词 + ≤6 display + ≤10 Extended Data） | W15–W18 | 字数/结构合规 |
| W19-2 | 引用核验 + Data/Code Availability 声明 | W19-1 | 全部 DOI 核验通过 |
| W19-3 | 合规文档 sprint：ML Reporting Summary V1.1 + LLM 披露包（版本+访问日期+代表性 prompts ≥5）+ AI 生成内容声明 | W15-1 数据齐 | 三项文档符合官方 schema 与政策 |

### Phase G：投稿（W20–W22）

| # | 内容 | 依赖 | 验收 |
|---|---|---|---|
| W20-1 | NeurIPS D&B 稿件（含 benchmark 资产提交） | W19-1/2/3 | 格式+checklist 合规 |
| W20-2 | ComSci 滚动稿件（Article 模板 + Online Methods + reporting summary） | W20-1 反馈 | Nature reporting standards 全填 |
| W22-1 | **W22 末总检查**：对照回退条款（评审不过/G2 不可达/横州未发布）执行降级 | 全部 | 投稿状态明确 |

**关键路径**：W1-1 →（W1-2/W1-3）+ W2-1 + W3-1→W3-4 + W4-x + W6-x → W12 MVE → W15 主实验 → W16/17 分析 → W19 成稿 → W20 投稿。锚扩展（C）与合规资产（F）全程并行。

## Open Questions

- **G2 降级的最终形态**（W1 末若触发）：temperature=0 + 固定 prompt + 诚实声明独立性假设部分失效，p 值降为参考——此形态投 D&B 还是直接转方法短文？（倾向前者，W1 末定）
- **横州六蓝报告发布时间**：不可控；W18 触发判定已内置，信源核实已写入 W8-1。
- **judge panel 规模**（3 vs 5 模型）：W4-1 先用 3；若 κ 在边界（0.5–0.6）波动，扩到 5 的边际成本待 MVE 数据回答。

## References

- 开题报告：`docs/investigations/decision-coscientist-proposal/proposal-decision-coscientist.md`（H1–H4 与统计 :139–208；进度回退 :240–248）
- 终裁 memo：`docs/investigations/decision-coscientist-proposal/topic-eval-top-journal-2026-07-19.md`（修正清单 #1 MVE）
- 锚资产：`docs/investigations/decision-coscientist-proposal/anchors/`（古雷 9 因子、结算模板、锚池流水线）
- 设计评审：`docs/reviews/plan-critique-decision-coscientist-experiment-2026-07-19.md`（已折入：依赖补全、闸门正名、口径统一、裁剪合并）
- 引擎：`Policysim-v0.2/dev/backend/src/modules/{experiment,monte-carlo,ai}/`（改造点见 Background）
- Nature 合规：https://www.nature.com/natcomputsci/content ｜ /editorial-policies/reporting-standards ｜ ML checklist V1.1 ｜ Computational tools guidelines ｜ NMI 2024-08 LLM 披露 ｜ Whitaker 2021 Silver 标准
- 工具链：OpenSpiel v1.6.12 https://github.com/google-deepmind/open_spiel ｜ SciPy 1.18.0 https://docs.scipy.org/doc/scipy/reference/
- 兄弟仓库资产：`cds4worldcup` 结算 schema 三件套；`cds4polymarket/ab-test` 实验治理 SOP + forecast-ledger schema（leakage_risk 字段）
