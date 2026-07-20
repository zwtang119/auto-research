# Decision Co-Scientist 实验方案（Nature 标准）

> 日期：2026-07-19 ｜ 状态：v2.1（2026-07-19 外科手术式修订：F5 settleability 切割 + F1 宽类轨道 + F2 决策行动锚源 + F4 硬约束 + F6 采集基础设施）｜ 项目已关闭（2026-07-19 用户决策；本方案为最终交付物，未执行。若未来重启，以此为执行蓝图）｜ 评审记录 `docs/reviews/plan-critique-decision-coscientist-experiment-2026-07-19.md` ｜ 上游：`docs/investigations/decision-coscientist-proposal/`（开题报告 v1.4、终裁 memo、PROJECT-BRIEF）
> 实施侧主战场：`Policysim-v0.2/dev/backend`（引擎）+ `auto-research`（锚资产、合规资产、分析）

## Goal

构建并执行 Decision Co-Scientist 的实验验证链：**古雷单场景 MVE → 全设计主实验（4 条件 × 4 基线 × 3 消融）→ 多案例扩展（郑州 7·20、Buncefield、横州六蓝；**叠加 1 条宽类（H3 旁证 N≥60）**）**。实验设计、统计报告与可复现性按 Nature 系发表标准建设；投稿节奏为 NeurIPS D&B 先行，Nature Computational Science 作滚动目标（用户决策 2026-07-19）。锚数据集定位（按 F5 切割）：**首个可结算（settleable）的灾害决策因子集**——因子=带判定规则、阈值区间、反证信号、盲评字段、来源分级的可裁定断言，与 disaster knowledge graph 描述性三元组（如 LLM4TyphoonKG）显式区分。

## Background

**开题报告已钉死**（`proposal-decision-coscientist.md`）：
- H1–H4 判定规则与预注册统计方案：配对 Wilcoxon 符号秩 / 非配对置换检验或 Mann-Whitney U；BH 校正按假设族；N≈175/组（δ=0.3，功效 0.8，α=0.05）至 395（δ=0.2）；报告 Cliff's δ 与 CI；反转零假设（≤15% 均值差判等价）；Axtell bootstrap 防假阴性（:139–144, :199–208）
- 臂定义：C0 单批次协商 / C1 仅锦标赛 / C2 锦标赛+进化 / C3 全闭环；B1 best-of-N / B2 普通 GA / B3 人类专家 / B4 直接作答；3 组消融（:170–180）；同评估协议 + 同 token 预算（:168）
- 60/40 锚分离：前兆/抑制/分支/反证四族分层，实验前冻结；**评估池两深案合计 ≥8 条可裁定因子 + 宽类评估池 N≥60（H3 旁证）**（:139, :158, :169）。**决策行动锚源（2026-07-19 实测可用）**：官方调查 + mem.gov.cn 国家防总响应通告（`/xw/yjyw/` 2018-01 起静态 HTML 123 页归档、`/xw/yjglbgzdt/` 2020-07 起 88 页）+ 省厅（yjgl.gd.gov.cn 2020–2025、yjt.fujian.gov.cn 2019 起、yjt.zj.gov.cn 境内直连可爬）+ JMA 防灾信息 XML（Digital Typhoon 2012–2026，CC BY 4.0）+ IFRC GO API field-report（5,107 条含 `actions_taken`，中国 69 事件多为 GDACS 自动同步）+ NWS api.weather.gov CAP 预警 + NTSB CAROL + CSB 报告全本（BP Texas City）。
- 回退条款：G2 不可达则转方法短文；锚协议未就绪触发降级（:242–248）；污染控制六条（:205）；H4 四道关（:144）。**行动锚采集三条硬约束**（2026-07-19 实测后补入）：(a) **2018 断档**——国家防总响应通告归档仅 2018-01 起，2018 年前无官方机读记录；(b) **历史预警报文无机读存档**——中国气象历史预警报文（含中央气象台台风公报）无机器可读历史，策略生成不得假设其可回填；(c) **ReliefWeb appname**——ReliefWeb API 自 2025-11 起需 appname 预审批（未审批返回 410），不作为隐式可用源；以上三条为采集准入门坎，违反的锚行不入因子库。

**引擎现状（2026-07-19 代码级核查，路径前缀 `Policysim-v0.2/dev/backend/src/`）**：
- 可跑：`experiment.service.ts:92` `runBaselineInference`（C0/B4 等价）；`:78` `runMultiAgentSimulation`（MAMR）；`monte-carlo.controller.ts:73` `/api/monte-carlo/compare` 主入口；`strategy-search.service.ts`（候选生成+启动+Pareto，M3 骨架）；`comparison.service.ts`（百分位 P5–P95）；handler 已注入 `SEED-${batchId}-${runIndex}` 提示词层扰动（软基础，待硬化）
- 未实现：C1/C2/C3、B1–B4 无代码；Multi-Judge 空缺；校验臂空白；Tsinghua 仓 `tournament.py` 是 LLM 模型评测引擎，非策略进化
- G2 实锤：`ChatCompletionOptions` 无 `seed` 字段，7 个 provider service 请求体均只有 `temperature`/`max_tokens`（`modules/ai/services/*.service.ts`）
- 锚资产：古雷 9 因子已编码（`anchors/gulei-2015-0406.factors.yaml`）；结算模板现成；`gold-hml-anchors.yaml`（H/M/L 校准素材）；横州六蓝 seed 已建（`emergency-scenarios.seed.ts`）。**指定锚 2026-07-19 实测存活**：郑州 7·20 PDF（https://www.mem.gov.cn/gk/sgcc/tbzdsgdcbg/202201/P020220121639049697767.pdf ）、古雷 4·6 HTML（https://yjt.fj.gov.cn/zwgk/sgxxgk_gb/sgdcbg/202501/t20250102_6601366.htm ）；**Buncefield** HSE 官方直链 404，改用英国国家档案馆 webarchive 归档（`buncefieldinvestigation.gov.uk`）+ FABIG 镜像（Vol.1 https://www.fabig.com/media/tpuaseey/buncefield-incident-miib-final-report-volume-1-dec2008.pdf ；Vol.2 https://www.fabig.com/media/jkvgpiv3/buncefield-incident-miib-final-report-volume-2-dec2008.pdf ，Crown copyright 非商用）。

**用户决策（2026-07-19）**：① Nature 标准、分阶段投稿；② 预算不设硬顶、按功效分析满配；③ 专家 panel 不确定 → fallback（公开实务方案集 + 延迟招募并行）；④ 横州六蓝纳入主设计（条件触发型零污染锚）。

**Nature 合规基线（2026-07-19 官方调研）**：主文 ≤3,500 词 + Online Methods；Data/Code Availability **强制**（Zenodo/Code Ocean DOI）；软件版本入 Methods；单命令安装 + 随机性 deterministic（Whitaker 2021 Silver）；ML Reporting Summary V1.1；LLM 精确版本 + 访问日期 + 代表性 prompts 披露；AI 生成内容声明强制；**ComSci 不收 RR** → 预注册走 OSF/Figshare 公共仓库；统计须报精确 p + 效应量 + 95% CI + 多重比较校正 + 样本量依据。

**统计工具链（已核实）**：α-Rank → `open_spiel.python.egt.alpharank`（OpenSpiel v1.6.12）；检验 → scipy 1.18.0（`wilcoxon`/`permutation_test`/`mannwhitneyu`/`false_discovery_control`）；LHS → `scipy.stats.qmc.LatinHypercube(rng=np.random.default_rng(seed))`；TOST → `scipy.stats.ttost_ind`；Cliff's δ → `δ=2U/(n₁n₂)−1` 换算。

## Approach

总策略：**在 Policysim-v0.2 现有引擎上最小侵入地长出 Co-Scientist 闭环**——不另起炉灶，复用 `startSimulation`/`compare`/`strategy-search`/provenance 审计四条既有主干；G2 先行（它是所有统计结论的地基，闸门从开题 W4 末前移至 W1 末，尽早证伪成本低）；MVE 卡在开题原 W15 主实验之前（对齐终裁 memo 修正清单 #1）；Nature 合规资产与引擎建设并行，不等数据。

**架构增量**（`dev/backend/src/modules/`）：
- `monte-carlo/services/` 新增：`tournament-orchestrator`（C1/C2 配对+N 次 MC+judge）、`evolution-operators`（M3 变异/杂交/多样性）、`alpharank`（α-Rank+Nash averaging+Cliff's δ+bootstrap CI，纯 TS 端口，对照 OpenSpiel 验证）、`judge-panel`（M4 Multi-Judge+Gold 校准+Youden J）、`feedback-loop`（M4 元评审回灌）、`validation-arm`（GB 50151 泡沫闸门 + NUREG/CR-7002 疏散排队）、`hypothesis-generation`（M1 生成+聚类去重）、`distribution-independence`（G2 验收检验）
- `anchors/` 新模块：`factor-ledger` / `settlement` / `pool`（60/40 冻结）三服务 + 新表 migration（tournament_pairings / judge_votes / evolution_generations / anchor_factors / settlement_records / judge_prompt_hashes）；`anchor_factors` 表 contract 增 `settlement_rule`（判定规则+阈值区间+反证信号）与 `origin` 枚举（`historical_record` / `ifrc_go` / `nws_cap` / `ntsb` / `csb` / `ibtracs_cma` / `usgs_fdsn` / `digital_typhoon` 等），settleability 是入库硬约束
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
| W1-4 | **前瞻锚采集基础设施**（境内直连，mem.gov.cn `/xw/yjyw/` + `/xw/yjglbgzdt/` + 浙/闽/粤省厅 `/col/col1229565103/index.html` 模板 + JMA 防灾信息 XML，**采集走境内直连、勿挂 VPN**；按 F6 估算 1–2 天） | — | 各源 cron 抓取 → 原始 HTML/XML 入仓 → 解析为 `decision_actions[]` 行；省厅反爬策略：polite crawling（UA+速率限制+白名单时间窗） | 抓取失败 → 启用媒体源兜底（公开报道行动回填），并在论文附注声明 |
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
| W6-2 | 锚池 60/40 按四族分层冻结（**含宽类预留配额**） | W6-1 | AllocationSnapshot 写库 + commit-lock；古雷评估池 ≥3，**郑州编码后两深案评估池合计 ≥8（开题下限）**；**宽类（台风首选/地震备选）评估池 N≥60，仅作 H3 旁证，不入 H1/H2 主设计与统计方案** |
| W6-3 | `SettlementService` + 古雷 settlement 首跑（**calibration_status 注释按 F5 明确「可结算性」要件**） | W6-1/2 | settlement_record 生成；泡沫因子 supported、环境因子 inconclusive（PX 争议降半级）；因子入库须满足 settleable 五要件（判定规则+阈值区间+反证信号+盲评字段+来源分级） |
| W7-1 | 郑州 7·20 因子编码（人工，≥15 条，负锚方式） | W6-1 | 四族齐备、可裁定；郭家咀有效部分纳入 |
| W7-2 | Buncefield 因子编码（人工，≥12 条，跨辖区） | W7-1 | 入库可裁定；Crown copyright 非商用已声明（FABIG 镜像 + 国家档案馆 webarchive 归档，**非商用许可**）；六源中最贴应急指挥决策 |
| W7-3 | **宽类锚采集与编码**（台风首选/地震备选，**限 2020+ 事件以覆盖省级响应时间线**） | W6-1, W1-4 | 台风：IBTrACS v04r01 bulk（https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/ ，免 key）+ 内置 CMA 序列（替代原站 tcdata.typhoon.org.cn，**非商用 + WAF 拦脚本**）+ 省级响应通告（F2）+ EM-DAT 后果拼接；地震备选：USGS FDSN（https://earthquake.usgs.gov/fdsnws/event/1/ ，免 key，PAGER 警级 + ShakeMap）；评估池 N≥60、factor-eval 入库 | 宽类因子机判一致性 κ<0.5 → 降级为生成侧素材（不入评估池，不参与 H3 旁证）；2020 前事件因 2018 断档+历史预警报文无机读存档，**采样须避开** |
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
| W16-1 | 统计分析：配对 Wilcoxon + Cliff's δ + bootstrap CI（H1 族 28 对比 + H3 族，BH 校正）；**H3 旁证由宽类 N≥60 提供统计强化层（不参与 H1/H2 主设计与统计方案）** | W15-1/2 | 精确 p + 效应量 + 95% CI 全报告；宽类 pre-registered 分析计划存档（OSF/Figshare） |
| W16-2 | 反转零假设 TOST（Δ=0.15×mean(C0)） | W16-1 | 等价检验报告；显著且等价的边界案例单独讨论 |
| W16-3 | 跨底座复现：两底座主结论不翻转 | W15-1/2 | 一致率 ≥80%；不一致案例 Discussion 分析 |
| W16-4 | **H4 四道关全量判定**：Gold 锚误判率 ≪10% + Youden J>0 + judge 与校验臂排名 Kendall's τ≥0.5（≥10 策略对，限覆盖维度）+ 跨底座不翻转（用 W16-3 数据） | W16-1, W4-1, W4-3 | 四道关报告齐出；任一不过 → H4 不成立并在论文如实报告 |
| W17-1 | 全场景 settlement + H3 汇总判定（**深案评估池 supported ≥60% 且无因子族被系统 rejected；宽类评估池 supported ≥60% 且 N≥60**） | W15-1/2, W7-1/2/3 | ≥200 条 settlement_records；H3 判定自动报告 |
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
| W22-1 | **W22 末总检查**：对照回退条款（评审不过/G2 不可达/横州未发布）执行降级；**外加采集与锚域降级**——CMA 非商用风险（仅用 IBTrACS 内置 CMA 序列，不触原站 WAF）；省厅爬取合规（polite crawling + 白名单时间窗 + User-Agent 声明）；IFRC GO 中国覆盖薄（GDACS 自动同步条目兜底+媒体源）；ReliefWeb appname 不确定（提前申请 appname 或不依赖作主源）；宽类机判一致性不达标（W7-3 降级为生成侧素材、不入 H3 旁证）；专家核验工时瓶颈（宽类优先机器可判裁定规则） | 全部 | 投稿状态明确 |

**关键路径**：W1-1 →（W1-2/W1-3）+ W2-1 + W3-1→W3-4 + W4-x + W6-x → W12 MVE → W15 主实验 → W16/17 分析 → W19 成稿 → W20 投稿。锚扩展（C）与合规资产（F）全程并行。

## Open Questions

- **G2 降级的最终形态**（W1 末若触发）：temperature=0 + 固定 prompt + 诚实声明独立性假设部分失效，p 值降为参考——此形态投 D&B 还是直接转方法短文？（倾向前者，W1 末定）
- **横州六蓝报告发布时间**：不可控；W18 触发判定已内置，信源核实已写入 W8-1。
- **judge panel 规模**（3 vs 5 模型）：W4-1 先用 3；若 κ 在边界（0.5–0.6）波动，扩到 5 的边际成本待 MVE 数据回答。
- **宽类轨道激活/降级判定**：W7-3 末若宽类因子机判 κ<0.5 → 降级为生成侧素材（不参与 H3 旁证）；若 N<60 → 缩窄覆盖年份+地震备选补量；触发条件进入 W22-1 总回退。
- **标度测量层（二期工作包，G2 之后启动，不动 MVE 第一优先）**：100–200 受控配置扫描，自变量=judge 噪声 / Youden J / 协调结构 / 模型能力 / 灾种；验证协议=held-out + 跨底座离样本。范式参照 arXiv:2512.08296 *Towards a Science of Scaling Agent Systems*（180 配置 × 1.5 万 runs + 标度律），**本项目差异点=真实世界真值锚**。**灾种 3–4 个、每个凑齐参数/行动/后果三层锚**；深案层扩至 3–4 封顶（古雷+郑州+1–2 国外对照：US 众院《A Failure of Initiative》[Katrina] 与 CSB West Fertilizer 首选，全文已 2026-07-19 实测存活、公有领域，依据 `anchor-authenticity-and-corpus-2026-07-19.md`）。**venue 映射**：NeurIPS D&B 现状已够；Nature ComSci = 3–4 深 + 2 宽 + 标度层 + 前瞻锚 1–2 季；主刊需前瞻命中或外部复现 >1 年。本项在 G2 + MVE 全部通过之后启动，不进 W1–W22 关键路径。

## References

- 开题报告：`docs/investigations/decision-coscientist-proposal/proposal-decision-coscientist.md` v1.4（H1–H4 与统计 :139–208；宽类轨道 §5.1 :169；行动锚源清单 §4 M5 :160；风险 8 :241；进度回退 :240–248）
- 终裁 memo：`docs/investigations/decision-coscientist-proposal/topic-eval-top-journal-2026-07-19.md`（修正清单 #1 MVE）
- 锚资产：`docs/investigations/decision-coscientist-proposal/anchors/`（古雷 9 因子、结算模板、锚池流水线）
- 设计评审：`docs/reviews/plan-critique-decision-coscientist-experiment-2026-07-19.md`（已折入：依赖补全、闸门正名、口径统一、裁剪合并）
- 引擎：`Policysim-v0.2/dev/backend/src/modules/{experiment,monte-carlo,ai}/`（改造点见 Background）
- 数据可行性附件：`docs/investigations/decision-coscientist-proposal/source-inventory-2026-07-19.md`（含 §8/§9 两轮网络复测；最终网络指引：**采集走境内直连，勿挂 VPN**）
- Nature 合规：https://www.nature.com/natcomputsci/content ｜ /editorial-policies/reporting-standards ｜ ML checklist V1.1 ｜ Computational tools guidelines ｜ NMI 2024-08 LLM 披露 ｜ Whitaker 2021 Silver 标准
- 工具链：OpenSpiel v1.6.12 https://github.com/google-deepmind/open_spiel ｜ SciPy 1.18.0 https://docs.scipy.org/doc/scipy/reference/
- 宽类锚源：IBTrACS v04r01 https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/ ｜ USGS FDSN https://earthquake.usgs.gov/fdsnws/event/1/ ｜ JMA 防灾信息 XML（Digital Typhoon，2012–2026，CC BY 4.0）
- 兄弟仓库资产：`cds4worldcup` 结算 schema 三件套；`cds4polymarket/ab-test` 实验治理 SOP + forecast-ledger schema（leakage_risk 字段）

## 2026-07-19 修订记录

v2 → v2.1，按 `revision-brief-2026-07-19.md` 外科手术式修订，正文骨架与既有结论（含 H1/H2 主设计与统计方案、预算/功效核心）未动。

- **F5 settleability 切割**：Goal 与 Background 按 F5 统一表述——定位「首个可结算（settleable）的灾害决策因子集」，与 disaster knowledge graph 描述性三元组（如 LLM4TyphoonKG）显式区分；`anchor_factors` 表 contract 增 settleable 五要件（判定规则+阈值区间+反证信号+盲评字段+来源分级）作为入库硬约束，W6-3 settlement 验收标注「可结算性」要件。
- **F1 宽类轨道**：Goal 叠加「1 条宽类（H3 旁证 N≥60）」；Background 评估池口径由「两案合计 ≥8」升级为「两深案合计 ≥8 + 宽类 N≥60（仅 H3 旁证，不入 H1/H2 主设计与统计方案）」；新增 W7-3 宽类锚采集与编码工作包（台风首选：IBTrACS v04r01 + 内置 CMA 序列 + 省级响应通告 + EM-DAT；地震备选：USGS FDSN；限 2020+ 事件以覆盖省级响应时间线）；W16-1 / W17-1 验收补 H3 宽类旁证表述；Open Questions 补「宽类激活/降级判定」。
- **F2 决策行动锚源**：Background 补 mem.gov.cn / 省厅（浙闽粤）/ JMA 防灾信息 XML / IFRC GO API `actions_taken` / NWS CAP / NTSB CAROL / CSB 报告全本清单；新增 W1-4 前瞻锚采集基础设施（境内直连 mem.gov.cn+省厅+JMA XML，按 F6 估算 1–2 天，含省厅反爬策略 polite crawling+白名单时间窗）。
- **F4 硬约束**：Background 补 2018 断档 / 历史预警报文无机读存档 / ReliefWeb appname 三条采集准入门坎；W7-2 Buncefield 验收按 F4① 修正（HSE 官方直链 404 改用英国国家档案馆 webarchive 归档 + FABIG 镜像 Vol.1/Vol.2 URL，Crown copyright 非商用声明）；Background 指定锚实测存活补郑州 7·20 PDF + 古雷 4·6 HTML + Buncefield 镜像 URL。
- **F6 采集基础设施 + 对策**：W1-4 写入境内直连 mem.gov.cn/省厅爬取基础设施；W22-1 总回退扩「采集与锚域降级」六条（CMA 非商用走 IBTrACS 内置 CMA 序列、省厅爬取合规 polite crawling、IFRC GO 中国覆盖薄走 GDACS 同步条目兜底+媒体源、ReliefWeb appname 提前申请或不依赖主源、宽类机判 κ<0.5 降级为生成侧素材、专家核验工时瓶颈走机器可判裁定规则优先）。
- **References**：补 source-inventory-2026-07-19.md、IBTrACS v04r01、USGS FDSN、JMA Digital Typhoon；开题报告版本标注 v1.4。
- **F8 三层证据结构与二期工作包**：Open Questions 追加「标度测量层 100–200 配置（G2 之后启动，不动 MVE 第一优先）」条目——自变量=judge 噪声 / Youden J / 协调结构 / 模型能力 / 灾种，验证协议=held-out + 跨底座离样本；范式参照 arXiv:2512.08296 *Towards a Science of Scaling Agent Systems*（180 配置 × 1.5 万 runs + 标度律），本项目差异点=真实世界真值锚；**灾种 3–4 个 × 三层锚（参数/行动/后果）**；深案 3–4 封顶含 1–2 国外对照（US 众院《A Failure of Initiative》[Katrina] + CSB West Fertilizer 首选）；宽类 ≥120（台风+地震双宽类 × N≥60）；venue 映射 NeurIPS D&B / Nature ComSci / 主刊三档。本轮不开新版本号（保持 v2.1）。
