# 清华 1023 / 1025 实验与全项目 Token 清洁交付：执行计划

日期：2026-10-27｜阶段：计划定稿，已补详细清单与包级并行排程；Mid-flow、一次设计审查及保真检查完成｜本轮仅规划，不实施、不 commit/push。

## 1. Goal

向 `policysim-research-Tsinghua` 交付可直接使用的 1023、1025 **修复／补测后完整生成与评分主集**、完整中文分析报告、完整实际运行脚本及离线复算材料；另交付全部清华实验 token 估算的逐调用公开输入、已知小计、情景总估算和未知范围。不能只交原始失败数据、缺口附录或让读者自行拼接。公开包不含运行金额、凭据或个人隐私；保留研究材料与模型正文中的政策／企业经济数值（用户Mid-flow已确认）。

采用薄发布层：等待并消费现有最终收口、补测、统计／报告和 token 任务的正式交接，不重建其执行管线，不打断任务，不用新设快照级别绕过 final gate。本轮唯一正式交付为本文。

### 路径与来源约定

- `A`：`/Users/tangzw119/Documents/GitHub/auto-research`；`P`：`/Users/tangzw119/Documents/GitHub/policysim-research-Tsinghua`。绝对路径仅用于私有计划，不得进入公开包。
- `W=A/analysis/tsinghua-baseline-audit-20261022`；`D=W/D-dna-ablation-20261023`；`F=A/analysis/tsinghua-factorial-ablation-20261025`；`S=F/supplementary-scoring-20261027`。
- `T1=A/analysis/token-imputation-audit-20261026`；`T2=A/analysis/token-final-readiness-20261026`；`T3=A/analysis/token-1023-append-20261027`。
- `C=A/analysis/tsinghua-clean-release-20261027`：未来独占发布工作区，本轮不创建。
- `E23=P/experiments/mc-2026-10-23`；`E25=P/experiments/mc-2026-10-25`；`T=P/docs/token-estimates-2026-10-27`（用户已确认；不改共享索引）。
- **Green Source**：直接核查的文件、代码及计算事实。**Red Source**：模型生成、评分和估算；交付时绑定实际冻结 source/code/policy SHA256，不代表现实政策效应。

## 2. Background：调查时点与交接依赖

以下不是发布验收；状态变化以所属执行者正式交接后直接核验为准，不扫描 latest 猜终态。

| 分支 | 已直接核查的事实（Green Source） | 依赖／不能推出的结论 |
|---|---|---|
| 1023 | canonical每样本每评委唯一采用，630网格显式left join；旧导出不完整、provisional。两例最小YAML恢复获批，但非最终验收 | 消费dna-final-20261027最终验收、两期正式统计、630 JSON/HTML/PDF及中文汇总；v12监控630/pending空不是停写凭据 |
| 1025 | 原r2 dataset直接读取为360生成、A355/B351有效；builder要求原task call ID与input hash。较新STATUS记录13有效补测＋1135格式侧车＝14/14、侧车1080/1080 | 核验原release和补测总验收交接；STATUS的PASS只是上游声明，本轮未实跑总验收。补齐不恢复原预注册完整性 |
| token | 旧safe-ledger直接逐行计数12263：may4319、benchmark3446、1023 3231、1025 1267。保留7765、supersede旧4498 | 等T3交接和1025全资源冻结；T2 gate恒NO-GO，尚缺生产完成、scope/adoption等审批，不能改True解锁 |
| 目标仓 | 五月为experiments/mc-YYYY-MM-DD，四件套和raw-data/evaluation/analysis/reports；历史归档与当前研究源版脚本不同 | 按五月命名，二月模板作元数据／命令参考；不改历史，不用当前脚本冒充实际版本 |

证据入口：`W/report-adapter-prep-20261026/INTERFACE.md:9-35,43-64`；`W/minimax-yaml-recovery-20261027/REPORT.md:3-35`；`A/docs/plans/tsinghua-dna-final-closeout-2026-10-27.md:7-34`；`F/scripts/build_factorial_dataset.py:8-65`；`S/STATUS.md:3-12`；`F/terminal-acceptance-20261026/HANDOFF.md:48-56`；`T2/README.md:20-38`；`P/experiments/mc-2026-05-05/README.md:65-100`；`P/wiki/annotations/current-state.md:16-31`。

直接复核记录（2026-10-27，主执行者）：旧账计数如上；T1 ZIP含金额表，不能原包公开。已证伪探针“T3目录不存在”：直接exists及目录树确认source.zip/source-manifest.json/append1023.py等在新增，不据此称已完成。1025旧“403 STOP／12未发”已被较新STATUS覆盖，不再安排重复补测；本任务仍不授权发API。另已直接读取新增`A/docs/plans/token-1025-append-2026-10-27.md:5-21`：1025 replacement和1023缺usage核查由另一任务负责；本发布层等待其统一包，不重复实现源提取／接入。`A/docs/investigations/token-1023-handoff-confirmation-2026-10-27.md:5-7,26-36`提供转达复核和限定范围交接声明，本轮未重跑该包，不把文档声明升级为本次独立验收。其他会话分析、两个论文wiki及legacy子模块改动不触碰。

## 3. Approach

### 3.1 唯一默认主集与目录

已确认采用 `adopted-v1` 吸收经核验的技术替代、已批准恢复和补测，作为raw-data、evaluation、主表、报告和默认CLI的唯一主集；`legacy-protocol-view/`保留原协议清洁输入和独立结果，不能自动回退或覆盖原值。所有表绑定release_view与policy hash。主报告展示采用主集，附一页采用／差异简表及legacy链接；原协议全表留legacy目录。

- **1023硬目标**：630生成、1890唯一且主指标有效的采用评分；历史630对照输入随包，两期统计1260样本槽。无GT，不虚构GT目录／字段。
- **1025硬目标**：360生成、1080唯一有效采用评分；13补测及1135侧车逐条来源闭合，原14缺失留痕。
- 缺行占位、not_adopted_missing或provisional不能冒充完整主集。采用政策版本化，不按分数高低选择。

E23/E25沿五月四件套；1025以八个完整条件名扩展两条件层级，README明示扩展。包间不互相import：

```text
README.md  PLAN.md  METHODOLOGY.md  VALIDATION.md  CHANGELOG.md
config/                   发布配置、无秘密在线示例
materials/  protocol/     实际运行材料／协议的清洁冻结副本
raw-data/{condition}/{model}/{enterprise}/run_XXX.yaml
evaluation/               默认adopted评分、逐judge完整解析对象
analysis/                 dataset、CSV、codebook、statistics、诊断、full_output
reports/                  中文主报告md/html/pdf、阅读指南、图表、index.html
  04-single-reports/       630或360份JSON/HTML/PDF，合计990份三格式
provenance/               sources、adoption、transformations、semantic-events
legacy-protocol-view/     原协议清洁输入／评价／主表／统计，独立复算
scripts/                  reproduce.py、verify_release.py、run_experiment.py
  runtime/  statistics/   实际模块闭包与冻结算术副本
tests/  environment/      测试、依赖锁、平台、字体及许可
release-manifest.json  RELEASE.sha256
```

E23另含历史630及judge映射；E25另含360行设计manifest、60份summary（以交接核验为准）。manifest列包内产物relative_path/bytes/sha256但不包含自身，外层RELEASE.sha256绑定manifest，避免循环哈希。所有引用包内闭合。

T包括四件套／报告／环境／测试／manifest，以及：

- `inputs/resource-records.jsonl`：全部已知逐调用／attempt安全字段；
- `inputs/{shared-meters,estimator-features,calibration,orchestrator-anchors}.jsonl`：共享计量、长度、校准、210编排锚点；
- `analysis/{active-ledger.csv,master-table.csv,coverage.json,scenarios.csv,adopted-subset.csv}`；
- `provenance/{sources.jsonl,supersedes.json,superseded-index.csv,scope-registry.json}`、`estimators.yaml`及复算脚本。

首页同时给已知小计、S0–S4情景总估算、unknown范围／原因，不把估算写成账单实测总量。

#### 3.1.1 详细交付核对表

以下是交付目标，不是现有文件存在性或验收结论。评分数量指唯一有效采用槽，不要求一槽必须拆成一个文件；报告数量按文件核对。源码／资产具体成员由获准交接后的dependency-inventory逐项列定。

| 公共交付族（E23/E25各一套） | 必交内容／验收依据 |
|---|---|
| 根文档 | README、PLAN、METHODOLOGY、VALIDATION、CHANGELOG；实际设计／执行差异、采用政策、复算与限制 |
| 默认采用数据 | raw-data、evaluation、dataset、CSV、codebook；adopted-v1直接可用，不要求读者自行拼接 |
| 原协议追溯 | legacy-protocol-view中的清洁输入／评分／主表／统计；原值、缺失和独立复算保留 |
| 来源及变换 | sources/adoption/transformations/semantic-events；每槽original/selected引用、物理调用、政策和hash闭合 |
| 运行资产与脚本 | 实际版本config/materials/protocol、run_experiment及完整runtime；只新run、不含凭据或历史金额 |
| 离线工具与环境 | reproduce/verify_release、统计／报告生成器、tests、依赖锁／安装材料、平台／字体／Chromium及许可 |
| 中文主报告与阅读入口 | summary.md/html/pdf、阅读指南、图表、reports/index.html；主报告一页差异简表＋legacy链接 |
| 发行与验证 | VALIDATION记实际数据／隐私／搬迁复算／视觉状态；release-manifest及RELEASE.sha256最后绑定全部产物 |

| 包／编号 | 专属交付 | 完成门槛 |
|---|---|---|
| E23-1 | 630生成＋1890评分、技术替代与GLM继承解析 | 设计键完整、每judge唯一且主指标有效；原／替调用均可追溯 |
| E23-2 | 两例MiniMax恢复原／选对象、overlay与批准证明 | 仅批准两键、hash联合匹配、恢复不增调用／行数 |
| E23-3 | 历史630清洁对照输入及judge角色映射、两期1260槽 | 包内自包含；保留original_judge及历史scores所有已有非None值 |
| E23-4 | 原协议／恢复版统计、分模型／ALL、有效数／差值／区间／重采样数、诊断及token摘要 | 原loader等价及原bootstrap；不作DNA因果归因 |
| E23-5 | 630份JSON＋630份HTML＋630份PDF | 完整允许公开的prompt／生成轮次／响应／评分／来源，PDF省略reasoning声明明确 |
| E25-1 | 360设计manifest、360生成full_history/final及hash、60份summary及依赖 | 数量及拓扑以正式交接逐项核验，不只数文件 |
| E25-2 | 1080采用评分及14失效槽闭合登记、配置替代审计 | 13补测＋1135格式恢复；原失败／所有真实attempt留痕，不伪造原task ID |
| E25-3 | 原协议／adopted／排除1135三分析、完整对比及Shapley、missingness/cell-n和长度／轮次／测量诊断 | adopted仅描述性区间；原协议及排除1135的B完整设计NA边界保留 |
| E25-4 | 360份JSON＋360份HTML＋360份PDF及token摘要 | 完整历史、三judge、采用来源及事后补测标签齐全 |

两个实验合计990个生成样本、2970个唯一有效采用评分槽、**2970份单样本报告文件**（990×3）；另有主报告／图表／指南。历史630对照不重复算作新增990样本或新增单样本报告要求。

| Token包交付族 | 必交内容 |
|---|---|
| 范围及逐资源输入 | scope-registry、resource-records；正式／pilot／失败／替代／补测全已知记录，历史缺计量部分明确unknown/N/A |
| 完整估算依赖 | shared-meters、estimator-features、calibration、210条orchestrator-anchors、estimators.yaml、S0–S4输入／公式／版本 |
| 机器表与追溯 | active-ledger、master-table、coverage、scenarios、adopted-subset；sources/supersedes/superseded-index，实测与填补互斥 |
| 文档与报告 | 四件套、CHANGELOG、字段五态／reasoning口径、中文summary.md/html/pdf、阅读入口；已知小计／情景估算／未知范围分列 |
| 复算与发行 | 离线reproduce/verify_release、tests、environment、release-manifest/RELEASE.sha256；不含在线实验runtime |

**私有交接材料（只留C、不进P）**：政策／handoff、captures/input-lock、dependency-inventory、source-bindings、字段／脱敏／数值等价核验、实际命令和exit/code/input hash、视觉检查范围、三包publication-receipt。公共验证结论只投影允许字段，不公开原敏感ZIP／journal。

### 3.2 交接、薄CLI与状态所有权

`C/scripts/release.py`为同步CLI，不建服务或数据库；inspect/build/verify支持`--package 1023|1025|tokens`，inspect/verify另支持`--package all`汇总。单包build输出到`builds/<build-id>/<package>/`，同一build-id的公共policy／工具登记由协调者先固定；允许独立进程在互斥包工作区并行。publish仅支持三包总门禁并由协调者调用，不授权提前发布单包。`inspect(handoffs,policy)`查依赖；`build(...,new_output)`构建；`verify(staging)`验收；`publish(staging,targets)`落位。成功0、校验阻断2、运行错误1；缺交接只WAITING，不恢复任务。实验状态由原执行者拥有。

每包独立状态：`WAITING_HANDOFF → INPUTS_PINNED → PRIVATE_VERIFIED → PUBLIC_PROJECTED → REPRODUCED → RELEASED`；失败BLOCKED附reason_code、对象引用、last_successful_stage。状态表示已通过的里程碑，不禁止独立产物重叠构建；未集齐该包产物不能前移。某包WAITING不阻塞其他包。视觉另列unconfirmed/pass/fail，总体完成须三包齐全。

`handoffs/{1023,1025,token-1023,token-other}.json`最小契约（token-1023/token-other归入tokens包核验）：schema_version/component/owner、source_manifest_sha256、scope_document_sha256、completion_evidence_refs、adoption_evidence_refs、owner_attestation_ref、capture_started_at/finished_at、late_changes_policy。实际上游文件名可不同，由inspect显式映射，不强迫上游重建接口。W1中的adoption证明针对上游已批准采用集；W5-b再与W3-a/W4-a公开映射逐项对应，不要求上游等待发布报告或反向依赖W5-b。

- 等正式交接再捕获；完成、退出码／接受策略、停写／无补跑、scope/adoption按原gate真实核验。声明不冒充独立证明，不手改gate/provisional或伪造父审批。
- C根政策／公共工具版本／总台账／publication-receipt由协调者单写；`C/builds/<build-id>/{1023,1025,tokens}/`分包独占锁及输出，不用全C长时锁串行化三包。子任务只写获分配文件族或批次目录；各包负责人汇总，不能共同追加同一manifest／日志。不碰实验锁。白名单先列后读；双遍枚举文件集合、hash、symlink目标相同，锁定第一遍字节；变化立即BLOCKED。双遍稳定不是原子停写证明。
- 各包工作区的`captures/`、`private/`、任务／验证记录与`public/`候选严格分离；只有`public/`可映射到E23/E25/T。CLI的`--staging`指私有构建工作区，由工具显式定位其public候选，禁止整目录发布或将私有核验产物纳入公共manifest。
- 同handoff hash复用已验证捕获，新hash新build；目标存在拒绝覆盖。中断保留.incomplete与诊断，新目录全量重建；不设计断点续构，无完成标记不得发布。
- 目标同文件系统staging逐包验收后原子rename；三个目录不假装跨目录事务。总receipt列每包hash/状态，三包齐全才RELEASED（本次不改共享索引）；中途失败记录部分落位，不自动删除／覆盖，交用户裁定恢复。

### 3.3 1023：消费closeout，保持原算术

数据流：上游final capture／authority／1890原采用与恢复双视图 → 本包交接核验／原协议验证 → 采用集与清洁输入固定。此后loader/pipeline双路复算及两期1260槽统计、630样本报告、脚本／环境可按§4并行；主报告结果等统计，token摘要最后回填，全部产物完成后才最终全链验收→E23。上游closeout计划的W1–W3是产源，不与本文工作项混同，不再做独立实验收口。

`C/scripts/assemble_1023.py`负责布局适配，不改W/D：

1. 显式630×3judge网格；canonical_key由condition/model/enterprise/run_id/judge结构重建。GLM继承链按authority和逐键采用映射解析，禁累加6目录或按最新文件猜权威。
2. 核schema/snapshot/generation_inventory、gate_provenance/selection_pinning、disposition的`logical_key|path|sha256`及parent_review；原／选调用、input/content/evaluation hash联合匹配。key_derived_unpinned按原门禁处置，不自升可信。
3. tech01保留原／替hash和物理／逻辑差额；原失败／终态未知诊断留痕。恢复只允许两批准键，policy=minimax-two-case-yaml-recovery-v1，manifest SHA256=`f7832c64b3a852654b634116c180a9a6564a0f7a6d673a23f6fbaf98557e991a`。closeout已应用则核验不再应用，禁止双恢复、glob采用、扩容错parser；恢复不增调用／行数。
4. 原解析对象不改，legacy两例scores={}仍NA。GLM24项／空解析协议零、非None error（含空串）、已有部分维度／全None保持原loader语义，不新增25项或五维筛样。
5. 历史原judge=glm-5.1-coding保留，仅统计副本显式映射glm-5.1并保存original_judge。历史B额外overall_score必须参与原loader对所有已有非None scores.values()求均值，不能删为五维。

统计：NumPy标量保留至原三位舍入，双方有效才算双判官；差值**无DNA−有DNA**。`SeedSequence(20261023).spawn(2)`两期独立PCG64；MAMR同批三企业同index、SASR企业格内抽样；NA留原35槽；格／模型等权；10000次、9900有效阈值、线性percentile。恢复主集格格35有效时pooled=格等权，直接证明不制造额外审批；原协议缺失如有口径实差，沿上游真实裁定与hash绑定gate，不绕过。四组×四指标格均值／loader派生列零失配，抽样索引hash和正式统计一致。

Green Source：`W/statistics-prep-20261026/README.md:35-70`；`W/historical-acceptance-20261027/formal630-basis.md:27-40`；`A/docs/plans/tsinghua-dna-final-closeout-2026-10-27.md:20-34`。

### 3.4 1025：原集验证后应用补测，不伪造身份

数据流：原manifest/raw/full_history/score/journal → 本包原release复核 → 14失效槽与补测／1135证明 → adopted360×3及清洁输入固定。三视图分析、360样本报告、脚本／环境分流推进；主报告结果等分析，token摘要最后回填，全部完成后最终全链验收→E25，不等1023报告才启动。

`C/scripts/assemble_1025.py`先复算原dataset，核event930 replacement-config-v1，旧物理调用不采用但留资源账。补测独立物理ID，不能改成原task call ID或启用synthetic_measurements=True绕过builder。逐槽匹配design_key/judge/full_history/input hash、实际messages、模型／route和授权attempt，只按授权规则选择，不选最高／最新。模型／评委／输入不符BLOCKED，另批新测量政策，本任务不发API。

逐judge保留original_protocol_value、original_analysis_value、selected_value、selection_kind、physical_call_id、original_ref/selected_ref、input_sha256、policy_id/sha256、transformation_ref。1135仅经核验format_repaired，原protocol=null，不增请求。重新计算合成B（双方有效才有值），更新audit但不抹原失效。

优先保持 `analyze(dataset,distribution=None)` 数值函数不变，在返回值外包装 `analysis_context={release_view,measurement_policy_sha256,posthoc_completion,preregistered_complete_design}`。发布副本仅把diagnostics中的费用输入索引和costs/budget_ledger输出依赖裁掉（原实现直接索引dataset['costs']，见`F/scripts/analyze_factorial.py:127-130`），并改写write_analysis的费用说明；不补假零、不改数值函数。私有原分析→公共分析只比较白名单统计字段，公共复算→随包公共结果再全量精确比较。若确需改签名，仅改发布副本，write_analysis/reproduce/测试同批。

- 原协议完整设计estimate/SD/CI仍NA；available-case九格等权、全部主移除差／简单效应／交互及Shapley由冻结输入复算，不转引自评数字。
- adopted每指标360有效则复用原块bootstrap：模型内replicate整块、八臂及三企业同抽，原seed/draw hash不变；称**补测后完整采用集描述性区间**，preregistered_complete_design=false。数值齐全不恢复预注册完整性。
- 排除1135敏感性：B完整设计NA，仅available-case点值；A按实际覆盖，不连带置NA。
- 保留原LIMITATIONS语义，长度／轮次为post-treatment诊断不调整；不写显著／等价／最优，不以Shapley替代主差或硬加不相加归属。旧全面review未通过不能改写。

Green Source：`F/scripts/build_factorial_dataset.py:8-65`；`F/scripts/analyze_factorial.py:95-177`；`S/STATUS.md:5-11`；`F/terminal-acceptance-20261026/REVIEW-STATUS.md:1-18`。

### 3.5 公共采用、canonical接口

`provenance/adoption.jsonl`为clean-adoption-v1：sample_key/design_key、judge、release_view、selection_kind（original/technical_replacement/supplementary/format_repaired）、original_ref/selected_ref（source_id/path/hash）、physical_call_id、input_sha256、policy_id/sha256、transformation_ref；每样本每judge恰一行，原／补测不同时计入。

1023 canonical保留schema_version、canonical_key/sample_key、condition/model/enterprise/run_id/judge、snapshot_sha256、input/evaluation/call/manifest source、adoption/original_evaluation、response source、reasoning/raw presence、provisional；v2保留gate_provenance/selection_pinning/disposition、audit.parent_review/capture_failures/generation_inventory；消费evaluation_differences为分类权威，不用已废duplicate_differences、不重做上游分类（`W/report-adapter-prep-20261026/INTERFACE.md:45-63`）。路径／敏感metadata投影，私有原gate证据不原样公开；公共证明绑定公共manifest并关联私有原hash，标明范围，脱敏字节不能冒称仍有原hash。

1025保留manifest/raw/summary/call/score/snapshot/coverage关系，scoring_view唯一full_history，protocol_result/protocol_value/analysis_value不混称；新增采用层不改原对象schema。

### 3.6 Token：replacement、全资源账与五态

`C/scripts/export_tokens.py`消费T3及1025 replacement任务的冻结交接／统一表，只做公开投影与独立复算，不扫描活动源、不接管资源接入。以旧safe-ledger的may4319＋benchmark3446＝7765行为历史保留基准，1023/1025旧4498行必须退出active、仅留superseded。若已交接统一replacement包已完成替换，就验证不再替换；否则仅组装尚未替换的分区。T3交整张active-ledger时先拆分目标分区，不能整表追加历史／1025两遍。五月ORCH-MEAN保留Red Source/item1-v1身份。

资源scope至少formal/pilot/technical/config-invalidated/supplementary/benchmark/historical-estimate/unclassified；**scope与正式采用是两轴**。失败、配置替代、补测全部真实attempt留账；格式恢复无新调用。scope_registry列“全部清华实验”的范围、包、排除、未知，不按目录猜全集。unclassified保留并阻断“分类全集完成”。

身份：1023 canonical source_path／manifest确认realpath别名组转public source_id；1025 experiment＋run＋完整attempt-qualified call_id＋attempt，dependency_ids保留父attempt，不截字符串。fingerprint仅诊断；同源pending→completed是状态修订不增调用；同run重复complete幂等、冲突拒绝；跨run同call_id或真实不同attempt分计。prepared/pending/complete与HTTP发送分列；1023无journal是not-applicable，不是零发送；无provider收据仍unknown。

**五态保留**：measured / reconstructed-imputed / partial / not-applicable / unknown。字段各有value/state/coverage/basis；聚合分known/missing/partial/invalid及known_subtotal，invalid不转0、缺失null不补0。

原生prompt/completion/total/reasoning原值＋field_pointer保留；reasoning_accounting_mode=unknown，reasoning不加total；completion−reasoning只arithmetic_difference，不标实测visible；reasoning=0不代表无思考，缺total不强造measured。主表按experiment/stage/provider/model/arm/scope列records/physical_calls/calls_state/basis/provider_provenance、四字段及visible的value/coverage/state、estimator_id/version和notes。

公开输入必须含共享MAMR meter语义组／重复投影关系、原Unicode长度及模板组成、校准样本／系数／公式版本、210编排锚点逐记录计量、S0–S4输入、benchmark逐结果、1023/1025全部已知资源逐调用／attempt。不能从汇总表复算同一汇总表；脱敏正文不代替原长度重测。情景分区明确，实测与填补互斥不双算。

T2旧gate代码恒NO-GO（`T2/readiness.py:213-224`），不等待它自动PASS、不改布尔、不旁路。**交接阻断项**：T3／1025 replacement所属协调者须提供另行批准的版本化验证入口及completion/scope/adoption证明，交接明确verifier路径／code hash／输入schema／批准人及原始证据hash；C只执行并核验，不补实现或代签。没有此交接就WAITING，即使已知小计可算也不先发布。全部已知资源和估算可完整交付，但不冒称账单级最终实测总量；known-subtotals不是未完成交接的许可。

Green Source：`T2/README.md:20-38`；`A/docs/investigations/token-readiness-recheck-2026-10-26.md:10-24`；`A/docs/plans/token-1023-append-2026-10-27.md:6-17`。

### 3.7 公开白名单、隐私与hash边界

`C/scripts/public_projection.py`按schema白名单导出，不搬原ZIP／journal再批量删字段；先审dependency-inventory后复制资产。运行金额、余额、预算、预留、费率、key／片段／key hash、认证header/cookie、账户标识、个人信息／个人路径均禁公开；配置只保留环境变量名。按已确认范围保留研究经济数值，仍逐字段扫描materials中的凭据、个人信息和运行费用；豁免须基于语义类别，不得整目录放行。

脱敏登记字段／文本位置、rule_id、original_sha256/public_sha256及数量，不保存被删秘密值；扫描只报文件／字段位置。不将敏感字串塞进负例日志或报告。如因凭据或隐私必须改写正文，公开文本为派生物，不能宣称actual prompt逐字相同或重测长等价；以原长度特征复算token，原件私有核验。第三方材料／字体无再分发权则解决许可，不能盲复制后称自包含。

公共semantic event含event_id/source_event_id/source_sha256、event_type、call_id、dependency_ids、request_ref/response_ref、status/validity和token字段；正文由清洁raw/score/summary引用闭合。公共链重新计算public_prev_sha256/public_event_sha256；原journal head只作provenance，不能冒称公共链就是原链。

`C/builds/<build-id>/<package>/private/source-bindings.jsonl`保存本包私有原路径／hash→public_id及字段对应，不进P；以下表中的“各包private”均指C内私有工作区，不是公开包目录。分两层验收：私有核验原字节→公开保留字段／采用选择；公开独立核验投影输入→主表／统计／报告。公众能复算公开数据，不能独立验证未公开原件；manifest完整性不等于真实性签名。

### 3.8 完整脚本、依赖闭包与报告

三包reproduce.py离线验证→建表→统计→报告，verify_release.py只读检查；仅E23/E25有run_experiment.py在线生成／评分／协调入口，T只含token离线工具和依赖，不复制实验runtime。runtime包含**实际执行版本**全部本地import、恢复／journal／调度模块、prompt模板、材料、协议、配置和报告生成器；不能只有wrapper或离线分析，不以目标仓六月脚本替代当时版本。

在线只写使用者指定的新run目录，存在即拒绝；凭据与运行控制由使用者提供，不带历史或默认金额；缺必要配置发送前失败。发布验收仅mock，不发实验API；mock核messages、request hash、参数、省略max_tokens及恢复依赖。去敏改变请求语义就标不等价。离线不导入副作用worker、不读凭据；socket禁网加外部网络隔离，不单靠monkeypatch冒称断网。禁python -O、关闭pyc、全新输出不覆盖原件。

environment包含实际核验的Python/package锁、平台、离线wheelhouse或明确预备安装材料及hash、可再分发字体／许可、Chromium渲染依赖。`F/frozen/environment.json:1-9`是历史依据，不照抄版本宣称已安装。准备可安装公开依赖，最终断网；原根不可访问、空HOME、无凭据、任意cwd和搬迁路径均须成功。包间无隐式依赖。

报告消费上游成果清洁重建，不另造分析管线。采用集及清洁内容固定即可分批构建单样本报告，与总体统计并行；方法／局限先写，主报告数字和结论等正式机器结果。token摘要最后回填时随各实验包带上复算该摘要所需的安全输入及公式／版本，不从T跨包import；须重渲染受影响主报告；回填后再做隐私终检、完整搬迁断网复算和最终manifest，不能复用回填前的全链PASS。中文主报告含摘要、设计／执行差异、采用政策、完整覆盖、主结果和全部补充对比、分模型、长度／轮次／测量诊断、token、局限与复算来源。1023不改原论文主检验、不作DNA因果归因；1025标事后补测与pilot边界。数字从包内机器结果生成，表图绑定view/policy hash。

单样本JSON/HTML含实际prompt、全部生成轮次、可见响应、完整评委判断／理由、原／选值和修复标签；reasoning默认HTML折叠，JSON保留允许字段，PDF明示未收录reasoning正文。全部990样本均输出JSON、HTML、PDF，另有实验及token中文主报告。沿预检Chromium路线，换包内字体后重验，不引未验证渲染器。

机器核数量、关联、分页、替换字符、越界／异常空白页；PDF双文本引擎核可见正文。人工逐页查1023三类型、1025八臂及所有修复／补测样张，全量缩略图记录查看范围。不实际看图则visual_status=unconfirmed，可交“内容完成、视觉待验”但不能称完整视觉PASS；页数实测、不发明压页合同。依据：`A/docs/plans/tsinghua-dna-final-closeout-2026-10-27.md:20-34`；`A/docs/reviews/tsinghua-report-visual-preflight-2026-10-27.md:5-31`（Green Source）。

## 4. Work Items 与逐文件影响

以下全部为**未来实施**；本轮不创建C、不写P、不运行这些命令。每次分析增补记录C/CHANGELOG.md（内容、来源、时间、执行者）。

### 4.1 工作项：保留W0–W9，按包／产物拆依赖

`p`表示1023、1025或tokens；同编号的分包实例独立完成，不设置“三包全部完成Wn后才能进入Wn+1”的屏障。W6按输入／输出文件族推进，不是W3–W5全部结束后的统一阶段。

| 项 | Goal | Done when | Key files | Dependencies | Size |
|---|---|---|---|---|---|
| W0 | 固化已确认政策 | §6结论、授权范围、schema／白名单／公私hash语义及工具版本固定，不重问偏好 | C/release-policy.json、公共工具版本登记 | 本计划§6 | S |
| W1-p | 三包各自交接／捕获 | 对应完成／scope／gate证据通过，双遍input-lock一致；tokens另有上游批准的版本化verifier及证明 | C/handoffs/*、各包captures/input-lock.json | W0＋本包正式交接，不等其他包 | M/包 |
| W2-common | 公共契约及工具 | 投影／采用／验证接口、结果schema、合成安全测试固定版本；不读取活动数据 | C/scripts公共工具、C/tests | W0；可在等待W1时完成 | M |
| W2-p | 本包白名单／运行闭包 | 列全获准源码／资产／许可／依赖及hash，无禁读路径或未解析引用 | 各包dependency-inventory.json | W1-p、W2-common | M/包 |
| W3-a | 固定1023采用集 | 630/1890有效唯一、历史630及两期1260槽、overlay幂等、原loader零失配；输出版本化采用映射 | assemble_1023.py、采用／历史输入 | W1-1023、W2-1023 | L |
| W3-b | 1023正式统计 | 清洁输入与私有基准等价；原协议／恢复统计、抽样hash及诊断齐全 | E23 analysis、机器结果 | W3-a、W6-1023输入族 | L |
| W4-a | 固定1025采用集 | 360/1080有效唯一、14槽来源闭合，补测／1135不伪造身份；输出版本化采用映射 | assemble_1025.py、采用／设计输入 | W1-1025、W2-1025 | L |
| W4-b | 1025正式三视图分析 | 原协议／adopted／排除1135语义及数值通过，费用诊断适配不改算术 | E25 analysis、机器结果 | W4-a、W6-1025输入族 | L |
| W5-a | 全资源token与估算 | 复核上游replacement守恒；全已知资源、五态／coverage／S0–S4输入→表复算，不重复接入 | export_tokens.py、T inputs/analysis | W1-tokens、W2-tokens、对应W6输入投影；不等实验报告／统计 | L |
| W5-b | token正式采用子集 | 两个最终采用映射与资源身份关联，scope和adoption两轴独立，导出版本化摘要 | T adopted-subset及实验token摘要 | W5-a、W3-a／W4-a及其公共采用映射核验 | M |
| W6-p | 分文件族清洁投影／核验 | 就绪输入逐族投影，保留字段／脱敏／引用／hash核验后供下游；全部报告及回填完成再全包隐私终检 | public_projection.py、verify_private_public.py、包内数据／private映射 | 输入族依本包采用／资源输入；输出族依其产出；终检依W8报告／回填 | L/包 |
| W7-p | 脚本／环境／生成器 | 实际模块闭包、mock请求等价、依赖安装及隔离夹具通过；数据就绪后可先做统计级搬迁测试 | 三包scripts/tests/environment；在线runtime仅E23/E25 | W2-p；数据测试等本包W6输入，准备工作不等W3-b/W4-b/W5-b | L/包 |
| W8-s | 实验样本报告 | 1023的630与1025的360各JSON/HTML/PDF，批次无缺漏／重复，内容与视觉状态记录 | 各包单样本报告及batch-index | 本包采用／清洁内容固定、W7对应生成器可用；不等总体统计或token | L |
| W8-m | 主报告及非结果文档 | 方法／局限可先写；结果表图等W3-b/W4-b/W5，机器结果绑定view/policy hash，主报告md/html/pdf齐 | 三包summary、图表、指南／索引 | 模板依W0/W2；结果依本包正式统计，token报告另等W5-b | L |
| W8-t | token摘要最后回填 | 将W5-b冻结摘要及包内复算所需安全输入／公式写入两实验analysis／主报告，重渲染受影响产物，记录摘要及采用映射hash | E23/E25 token摘要与主报告 | W5-b＋各实验W8-m；不阻塞此前统计／样本报告 | M |
| W8-v | 每包最终全链验收 | 全部文件含token回填完成，W6终检、完整搬迁断网复算及报告内容检查通过；如实列视觉状态 | 各包verification、复算／视觉记录 | 本包W7、W8-s（实验包）、W8-m、W8-t（实验包）、W6终检 | L/包 |
| W9 | 清单、单写落位与总交接 | 三包W8-v齐全后定稿manifest/RELEASE hash、验hash；协调者逐包原子落位并写总receipt，索引不变 | release.py、targets.json、publication-receipt.json | 三包W8-v及W0授权；落位只单写者 | M |

### 4.2 串并行DAG与关键收口

```text
W0 → W2-common（公共契约／工具；可与等待交接重叠）
 ├─ W1-1023 → W2-1023 → W3-a → W6输入 ┬→ W3-b统计 → W8-m结果 ─┐
 │                                    └→ W8-s样本报告 ────────┤
 │              W2-1023 → W7脚本／环境／生成器 ────────────────┤
 ├─ W1-1025 → W2-1025 → W4-a → W6输入 ┬→ W4-b三视图 → W8-m ──┤
 │                                    └→ W8-s样本报告 ────────┤
 │              W2-1025 → W7脚本／环境／生成器 ────────────────┤
 └─ W1-tokens → W2-tokens → W6输入／W5-a资源账与估算 ─┐        │
       W3-a/W4-a公共采用映射 ────────────────────────┴→ W5-b │
       W5-b → token主报告；实验摘要W8-t回填／重渲染 ────────────┘
各包最终产物齐 → 本包W6终检 → 本包W8-v全链复算／验证
三包W8-v齐 → W9最终manifest/hash → 单写者落位 → 总receipt
```

DAG只展示主要数据依赖；W2-p还依W2-common，样本报告依本包生成器，完整约束以§4.1为准。采用映射只依采用集和公共身份核验，**不依主报告或token摘要**，避免循环。

| 必须串行 | 可重叠／并行 | 不可省略的边界 |
|---|---|---|
| 公共政策／接口固定→正式构建 | 等交接时做合成夹具、CLI、安全测试 | 未交接不消费活动源或构建正式包 |
| 本包交接→核验捕获→原协议验证→采用固定 | 三包独立交接，先就绪先推进 | 1023不等1025，实验输入构建不等token |
| 采用固定→正式统计→主报告结果 | 同时做样本报告、脚本／环境、非结果文档；报告分批渲染／检查 | 样本报告需清洁内容及生成器固定；不提前写结果结论 |
| 两实验采用映射→W5-b→实验token回填 | W5-a资源账／估算不等采用映射；实验统计／样本不等W5 | token验证证明仍是外部硬门禁，不由并发或发布层绕过 |
| 最终回填／重渲染→全包终检→全链复算 | 三包在隔离目录各自验收 | 回填前测试仅中间验证，不作为最终REPRODUCED |
| 三包验收→最终manifest/hash→落位→总receipt | 最终验收前各自产物可持续准备 | 冻结后任何文件变动均使相关验收／hash失效；W9单写 |

### 4.3 写入归属与有界资源并发

采用“三条包级流水线＋公共工具／集成负责人”的职责划分，不等于本轮启动代理或授权无限并发。实施时一个执行者可以承担多种职责；只有任务另获委派授权才创建子代理。

- 协调者独占C根policy、公共工具版本、总台账、CHANGELOG汇总及W9；包负责人独占本包工作区及汇总记录。并发执行者各写独立任务记录，由协调者逐条并入C/CHANGELOG.md，保留内容、来源、时间、执行者，不共同追加同一文件。
- 公共工具先冻结code hash，再供各包使用；必须改版则登记受影响包／文件族并重验，拒绝静默混用版本。仅身份／路径不同的包输入可共享同一工具版本，不能共享可变缓存或输出目录。
- 990样本按稳定sample_key预分互斥批次；每批独占输出及记录，不重复写index/summary/manifest。包负责人核集合恰好覆盖630／360，再单写合并索引；生成器或清洁内容变更须重建受影响批次。
- JSON／HTML完成一批即可渲染并检查该批PDF；bootstrap、Chromium、搬迁复算的并发上限先测CPU／内存／I/O余量，再记录配置和实际峰值，重型任务使用统一资源配额，不启动990个Chromium。不得影响既有实验／补测／统计／token任务，不启停或修改其进程；资源不足时降低本发布任务并发。
- 预计最大可消除等待是旧全局W5→W6→W7→W8屏障；上游正式交接／token批准证明不可加速绕过。未测耗时与资源占用前，不承诺倍数或完成时间。

### 4.4 逐文件影响

| 文件族 | 未来改动与契约 |
|---|---|
| C/README.md、CHANGELOG.md、release-policy.json、handoffs/*、builds/<build-id>/{1023,1025,tokens}/* | 根元数据协调者单写；分包captures/input-lock、inventory、任务／批次记录及验证输出独占；不修改D/F/T1–T3 |
| C/scripts/{release,assemble_1023,assemble_1025,export_tokens,public_projection,verify_private_public}.py | 薄同步CLI／纯适配层，职责见§3；测试先行 |
| C/tests/{test_adoption,test_projection,test_tokens,test_release}.py | 覆盖§5负例；各包verification独立记录实际命令／exit／代码及输入hash，协调者汇总C/verification.json，不共享追加 |
| 各包private/source-bindings.jsonl、dependency-inventory.json | 按包／文件族核公私字段对应及许可／import闭包，私有映射禁止进P |
| E23/E25四件套、config/materials/protocol | 新增清洁副本；不改P根protocol/materials/config |
| E23/E25 raw-data/evaluation/provenance/legacy-protocol-view | 新增采用主集、原协议、源／变换／采用登记；禁止原ZIP或任意源码目录整包复制 |
| E23 analysis | 无GT CSV／码本、历史映射及两期输入、原协议与恢复统计、comparison-tables、token摘要 |
| E25 manifest/summaries/analysis | 360设计、summary、双dataset、三分析、missingness/cell-n、token摘要；数值函数保留，外包装context |
| 三包scripts/tests/environment/reports | 各包完整离线工具，E23/E25另有完整在线runtime；锁／许可、全部报告，批次独占输出、索引单写；先inventory再复制 |
| T inputs/analysis/provenance/estimators.yaml | §3.6安全逐记录、完整估算依赖、supersedes、coverage、scope、采用子集 |
| 三包release-manifest.json、RELEASE.sha256 | 最后生成、不循环hash；公开路径只相对包根 |
| P/experiments/10-EXPERIMENTS.md及wiki入口 | 本次明确不改；各包README及reports/index.html提供包内入口 |

## 5. 验收、风险及失败边界

### 5.1 硬Go/No-Go

- 不读写封存cds4worldcup；evidence只读；不读.env／凭据／SECRETS／旧PROGRESS原文。不修改高引用区、实验源／冻结protocol／journal，不清账，不启停进程，不补发／重评／重跑API，不接管T3。
- 任一缺交接（本包WAITING_HANDOFF）、hash／身份冲突、缺采用槽／无效主指标、未获真实gate证明、隐私命中、包外依赖→本包阻断，不阻止其他包独立准备／验收，但任一包未过均禁止总体发布。不得手改证据迎合PASS，不以快照级别、只填行数、缺口附件降级满足目标。
- 完成定义：E23 630/1890、E25 360/1080；默认数据／统计／报告同adopted-v1；原值／恢复／补测身份清楚；token全已交接已知资源及估算输入齐全、unknown不当0；公开无禁项、搬迁断网复算；没有未授权改动。视觉未确认只能报告对应条件状态。
- 迟到输入／新补跑生成新release和supersedes，不修改已发布版。回退只停止引用新包，保留历史；任何删除先列清单请示，不以“新增即可删”推定授权。

### 5.2 必测正反例

1. 六路径别名只计一物理文件；同fingerprint不同响应计二；跨run同call_id计二；完整父attempt不截断。
2. pending→complete不增物理行；重复相同complete幂等、冲突拒绝；缺usage=null，not-applicable不写成零发送。
3. 五态不丢partial；reasoning不叠加、mode不确定化、算术差额不变measured visible；情景和实测不重复计数。
4. 旧4498 active重现／T3整表重复追加失败；保留7765身份／数值／估算版本不变；格式恢复零新增调用。
5. canonical缺judge／重复／多余／缺槽拒绝；overlay键同但任一input/call/content hash异即拒；已应用overlay不再应用。
6. 1023历史额外overall_score参与均值，judge映射不改原值，NumPy舍入、NA／零、partial覆盖沿原语义；必要格NA不得强出区间。
7. 补测未授权attempt、异模型／judge／messages／full_history即拒；不伪造原call ID，不启synthetic bypass。
8. adopted完整不改原协议NA或preregistered_complete_design；排除1135的B完整设计NA；八格多项式夹具验证差值符号／交互／Shapley，不只同函数自比。
9. gate/provisional篡改、审批hash不符、缺handoff、源双遍增删／变更、symlink越界／循环、..／绝对路径／外部import均拒。
10. 合成嵌套金额／headers秘密／个人路径及压缩附件泄漏必须拦截；只报位置不回显值。重算公开事件链，不能以原head冒充。
11. 目标存在拒绝覆盖，中断无完成标记拒发布；分包落位中途失败不生成总完成receipt。
12. 隐藏A、搬迁、空HOME、无凭据、外部断网后，CSV／规范JSON／抽样hash／统计数值确定一致；在线mock不发API；缺控制参数发送前失败。
13. 一个包WAITING时，其他已交接包可构建／验证但publish all拒绝；W5-a不要求实验报告，W5-b缺任一最终采用映射则拒绝完整采用子集。
14. 报告批次缺键／重键／跨批重叠、JSON/HTML/PDF缺格式、旧版生成器／内容hash混入均拒绝；总集合恰为630／360，不只比文件数。
15. 两执行者竞争同一包级汇总文件／同一批次或根共享文件时独占检查拒绝；不同包或本包已分配的互斥文件族／批次可并发。公共工具改版未重验、policy／采用／token摘要版本混用拒绝。
16. token回填或重渲染后复用旧终检／复算／manifest的PASS应失效；有任何待回填、incomplete或未消费输出的批次不能进入最终REPRODUCED。

### 5.3 未来验收命令契约

以下接口**尚未实现、未运行**。每包最终产物（含实验token摘要）齐全后，在包根执行；输出必须不存在：

```sh
python3 -B scripts/verify_release.py --package . --content-only
python3 -B -m unittest discover -s tests -p 'test_*.py'
python3 -B scripts/reproduce.py --package . --output ./reproduced-check
python3 -B scripts/verify_release.py --package . --content-only --compare-reproduction ./reproduced-check
```

由外层验证环境实际禁网、隐藏A、清空凭据，搬迁至另一绝对路径重跑。三包可在各自隔离目录及配额内并行。数据／规范JSON／数值精确比较；HTML/PDF按内容／版面合同，不要求含生成时间的PDF字节一致。构建期统计级测试及报告批次检查只登记中间结果，不替代这里的全链验收。复算输出留在验收副本或私有目录，不能被收入公开manifest；`--content-only`只验最终内容／引用及复算，不要求尚未生成的发行清单；W9定稿后不带此选项再只读复验manifest完整性，模式须写入验证记录。

C根的单包接口（以1023为例；1025、tokens换相应包名和独占输出，可独立执行，不需等此命令链完成）：

```sh
python3 -B scripts/release.py inspect --package 1023 --handoffs handoffs --policy release-policy.json
python3 -B -m unittest discover -s tests -p 'test_*.py'
python3 -B scripts/release.py build --package 1023 --handoffs handoffs --policy release-policy.json --output builds/check-01/1023
python3 -B scripts/release.py verify --package 1023 --staging builds/check-01/1023 --content-only
```

以上是本包最终内容验收、尚未定稿发行清单的命令合同；`--content-only`不豁免任何数据／隐私／报告／交接门禁，不把缺token回填的中间产物当作final内容验收成功；各文件族可按§4分工提前产出，最终build只汇集已核验的同版本产物，不重复上游实验／统计接入。公共测试由工具负责人运行，包内测试由包负责人运行，避免并发改共享测试输出。

三包全链验收通过后，协调者执行最终门禁与落位；`verify --package all --finalize-manifests`仅在三包W8-v证明有效且文件集合不再变化时生成最终manifest/hash，再只读验证完整性，成功后允许publish。该选项写最终清单，除此以外verify只读；失败不生成发布成功标记。构建期验收与发行清单校验分层，避免“生成manifest才能验收／验收后才能生成manifest”的循环：

```sh
python3 -B scripts/release.py inspect --package all --handoffs handoffs --policy release-policy.json
python3 -B scripts/release.py verify --package all --staging builds/check-01 --finalize-manifests
python3 -B scripts/release.py verify --package all --staging builds/check-01
python3 -B scripts/release.py publish --package all --staging builds/check-01 --targets targets.json
```

publish再次只读核对三包最终验收／hash及目标不存在，不重生成任何报告。targets仅允许E23/E25/T，共享索引不在授权写入范围。verify输出每gate实际结果、计数／有效数／view／policy hash、工具版本、输入／代码hash、退出码、视觉范围及未完成项。无源目录写入或真实API是验收项，不只口头承诺。

### 5.4 风险与处置

| 风险 | 处置 |
|---|---|
| 上游延期或STATUS与冻结件不符 | WAITING／BLOCKED，交还原owner，不重复补测、不猜最终路径 |
| 采用版被误读为原协议 | 新policy/schema/view，原协议保留；1025描述性区间显式事后标签 |
| 隐私脱敏破坏正文／逐字复现 | 研究经济数值已明确保留；必要隐私脱敏记录公私hash与原长度特征，降低逐字复现声明不篡改原件 |
| 旧脚本外部依赖／输出费用 | inventory闭包、发布副本最小适配、私有数值核验与公开投影分层 |
| token范围／历史发送无法证明全集 | scope排除／未知明示，全已知资源＋估算，不称最终账单；不借标签绕过交接 |
| PDF体量／视觉未闭合 | 已确定全990三格式；复用上游产物、按页验收，状态如实不发明页数合同 |
| 多包部分落位／共享索引冲突 | 每包原子、总receipt，保留诊断待裁定；不自动删包或覆盖别人工作 |
| 并发写冲突／工具版本漂移／批次漏重 | 根单写、分包／批次独占、code/policy/content hash锁定；集合核验，改版重验 |
| bootstrap／Chromium争抢现有任务资源 | 先测资源余量、有界并发及独立临时目录；只降低本发布并发，不控制现有任务 |

## 6. Open Questions／已确认的Mid-flow决策

用户于2026-10-27回复“四项均按推荐”；此前超时已按约停止，答复后才恢复审查。四项固定：

1. 修复／补测后的adopted-v1为唯一默认主集；主报告一页采用／差异简表＋legacy链接，原协议全表保留于legacy目录。
2. 删除账户／API运行金额、预算／费率等；保留研究材料与模型正文中的政策／企业经济数值，不把研究内容误判成运行费用。
3. 全990样本全部JSON＋HTML＋PDF，另交两实验及全项目token中文主报告。
4. T=`P/docs/token-estimates-2026-10-27`；私有映射只留C；不改实验追踪表、wiki或其他共享索引。

无剩余用户偏好问题。实施依赖仍有：1023 closeout、补测与token统一包正式交接，以及token版本化验证入口／审批证明（§3.6）；缺交接就等待，出现新API／替换路线等实质缺口另请示。

## 7. References 与规划保真记录

主要证据已在各节以path:line引用；执行时读取绑定版本，不将动态行号代替hash。补充入口：`A/docs/plans/tsinghua-dna-ablation-2026-10-23.md:115-125`；`A/docs/plans/tsinghua-factorial-ablation-evaluation-2026-10-25.md`；`A/docs/plans/tsinghua-dna-ablation-report-adapter-2026-10-26.md`；`P/experiments/EXPERIMENT-TEMPLATE.md`；`P/experiments/10-EXPERIMENTS.md`；`T1/estimators.yaml`及共享计量／估算输入工具。以上只作只读规格，不复制含费用文档原文。

### 7.1 完整规划基线coverage ledger

已完整读取1469行Oracle导出（按当前splitlines复核），Generated Plan之后三路有效结果为规划基线，另一路并发限流失败、没有有效计划，未重试。下表合并全部可执行骨架；冲突显式纠偏，不静默丢失。工具原输出不是事实，具体断言经主执行者直接复核才纳入。

| 基线支持内容 | 本计划落位／直接核验与纠偏 |
|---|---|
| targeted发布层、目录、双视图、字段／状态／生命周期 | §1、§3.1–3.5；保留可执行接口与所有权，不重建上游 |
| 1023 canonical／继承／tech01／overlay／历史身份／原loader／两期bootstrap | §3.3、§5.2；直接读INTERFACE、statistics README、formal630及closeout；历史overall_score不删，完整格权重不虚构新审批 |
| 1025原builder身份、14槽、protocol／analysis双层、块bootstrap／Shapley／限制 | §3.4、§5.2；直接读builder/analyze及STATUS。纠偏：独立补测ID不可伪造；优先外包装context，不强改数值函数签名 |
| token replacement、scope、物理身份、状态更新、五态、估算与公开输入 | §3.6；直接csv计数及T2 README，保留partial；不能只发逐行usage却漏共享meter／校准／长度／210锚点／S0–S4 |
| snapshot-frozen旁路final gate（一路建议） | **拒绝**：与完整终局交付及原门禁冲突；§1、§3.2、§5.1等待真实交接，不绕check_release、不把provisional主集发布 |
| 一路仍以1025采用后CI全NA、1135只附录 | **纠偏**：直接analyze源码完整才bootstrap；§3.4采用完整可给独立描述性区间，原协议NA不改；敏感性B仍NA |
| 新STATUS与旧403未发叙述冲突、T3不存在探针 | §2直接读STATUS:7-11确认新覆盖声明但未代替验收；直接exists／目录证伪T3不存在，不接管／重复跑 |
| 隐私／原hash链／事件投影／两层验收／禁读 | §3.7、§5.1–5.2；直接ZIP目录核金额表；不公开原archive/journal，不将公私hash混称，不给材料默认豁免 |
| 完整运行源码、依赖锁、断网、报告／PDF／视觉 | §3.8、§4、§5.3；纠偏“只拷分析脚本／不拷runtime”不满足完整脚本；实际模块闭包必须随包，版本安装需实核 |
| 文件影响、工作项Done when/Deps/Size、负例、命令、原子边界、风险回退 | §4–5；保留所有支持项但不复制三套重复命名；回退不默认删除；跨包非全局原子 |
| token目录／主报告对照／金额／全量PDF／索引授权 | §6四项已获用户确认，不同Oracle目录建议以实际裁定为准 |

### 7.2 设计审查与最终状态

一次design审查已完成，内部记录：`A/docs/reviews/tsinghua-clean-release-critique-2026-10-27.md:11-22`。主执行者直接复核确认三项：T2/readiness.py:213-224恒NO-GO、F/analyze_factorial.py:127-130直接索引费用诊断、原W7/W8报告依赖倒置；分别在§3.6、§3.4、§4修正。确认漏列evaluation_differences（INTERFACE.md:50），已补§3.5；删断点续构和token在线runtime。无新增审查轮次，未实施。原定稿时直接检查：29处带行号引用的路径和范围有效，Markdown代码围栏配对，无TODO/TBD占位；三路有效基线覆盖及拒绝／纠偏见§7.1。Oracle导出1469行，SHA256=`0729a9fb75bac91cf8ad778455914c73523d32f944d4e231b7ab4c91714b17e0`；吸收后仅清理该本次导出，不动其他会话文件。计划定稿不代表发布门禁已通过；未来命令未运行。

### 7.3 本轮清单与排程优化（2026-10-27）

用户已同意详细交付清单及串并行评估，本轮仅将其写回本文。§3.1.1列全三个公开包与私有交接材料，保留990样本三格式、2970采用槽及历史630不重复计数的边界；§3.2、§4改为独立交接／分包里程碑、token资源账与采用子集两阶段、采用后统计／样本报告／环境并行，最后回填与全链收口；§5补单包CLI、三包总门禁及批次／版本／写冲突负例。

本轮直接检查：29处path:line引用的路径／行范围有效；按§4.1拆开W6输入、输出与终检后，34节点依赖图拓扑排序通过，无循环，1023统计不依1025或token、W5-a不依实验采用映射、样本报告不依token的断言均通过；数量算术与Markdown格式检查通过。这是计划一致性检查，不是实现测试。

此前一次design审查及直接源码复核结论仍有效，未新增代理／Oracle轮次，也未重跑上游验证。此次依赖检查针对计划文本，不代表任何动态交接或发布验收通过；未来C／目标包未由本轮创建，未运行API、实验、补测、统计或token任务，未commit/push。


## 8. 分期实施授权与本轮执行（2026-10-27）

用户在计划定稿后明确授权逐步实施，指定1025已完成，其他实验由用户另行通知启动。因此本轮只执行W0/W1-1025/W2-1025/W4/W6-1025/W7-1025/W8-1025及1025单包W9；1023与全项目token流水线不启动。该最新授权覆盖§3.2／§4／§5中“三包齐全才落位”的批次限制，仅允许本包全部验收后单包落位，总体仍非RELEASED。

保留其余全部数据／隐私／身份／自包含复算门禁；不因用户说明完成而跳过直接核验。W5-b全项目采用子集及全项目token摘要不由本轮执行；1025报告可单列本实验已交接原生usage小计／缺失，不冒称完成全项目情景估算，不启动其上游任务。将来全项目摘要补入时须版本化重发并重新验收，不能修改本轮封存版。

PRIMARY_GOAL为1025清洁交付，阶段Deliver；完成标准及实际进度、变换、命令与hash记录在`analysis/tsinghua-clean-release-20261027/README.md`、`CHANGELOG.md`及各任务记录。源实验与上游交接只读；只新增目标`experiments/mc-2026-10-25/`，不改共享wiki／追踪表，不commit/push。发现目标仓已有wiki未提交修改，已记录私有基线且不触碰。


### 8.1 后续范围更新：1023同时开启（2026-10-27）

用户随后明确通知1023实验已完毕并要求按计划交付清洁版。该更新增量开启1023，不取消已进行的1025；两个实验各自核验、构建、验收及单包落位，均不等待全项目token包。1023须先直接核验最终closeout／两期统计／630报告正式交接，保留所有本包数据／身份／隐私／复算门禁。全项目token及其余实验仍等待用户通知；不调用API或重启上游，不改共享索引，不commit/push。

本轮五项执行范围：①1025数据核验与三视图复算；②1025完整runtime／资产；③1025报告；④1023正式交接门禁→清洁包构建（先门禁再分工）；⑤协调者独立验收／集成／两包分别落位。各项输出目录互斥，报告／bootstrap／Chromium共享有界资源配额，不增加无界重型并发。


### 8.2 三线并行实施更新（2026-10-27）

用户现明确授权并要求1023、1025与token统计并行推进。此前§8/§8.1“全项目token未开启／等待”的限定不再适用于当前执行。恢复§4.1分包DAG：1023正式交接／独立工具准备、1025报告／集成验收、token全资源统计与清洁投影同时执行；真实门禁仅阻断依赖它的节点，不造成全局串行屏障。不重跑实验/API，不接管其他活动源，不改上游批准。1023当前父统计脚本绑定冲突仍需合格版本化承接，不能以并行要求绕过；无依赖的契约/合成测试/环境准备继续。

并行文件所有权：1023=`C/1023-work/`，token=`C/token-work/`，1025报告=`C/report-work/`，1025集成=`C/integration-work/`；各写独立任务记录，协调者汇总根日志及最终单写落位。1025数据统计/runtime已交接，只读消费。token W5-a不等待两实验报告或统计；W5-b仅相关采用join等待相应版本化映射。实验主报告W8-t最终消费已交接token安全摘要/复算输入，重渲染受影响主报告，再做本包终检；不重建未受影响的360单样本报告。已完成阶段验证保留，不能冒称含未来摘要的全链PASS。包间无“所有Wn齐才做Wn+1”的屏障，最终按实际依赖及本包门禁判定可落位状态，不因并行降低断言。


### 8.3 1025独立先交付授权（2026-10-27）

用户明确同意：“1025独立先交付，全项目token摘要后续版本化增补；其余验收标准不变。”并已转发token原owner补交接要求。此条仅覆盖§8.2对本次1025发行必须等待全项目W5-b／W8-t的依赖，不取消三线并行、不改变1023/token各自真实门禁。1025本次定义为独立版：完整采用数据、三视图统计、360样本三格式、中文主报告、实际runtime及离线复算材料；token仅保留已交接本实验native usage的明确范围／缺失，不声称全项目资源统计或S0–S4完成。全项目token摘要作为未来新版本增补，保留本次版本，不原位覆盖。

需要显式版本化发布契约、主报告与指南、验证器／相关负例：取消本次独立版对全项目W8-t的阻断必须引用本用户授权，不能把未交摘要标成COMPLETE或冒充正式统计。未知不归零、reasoning不叠加、物理attempt等计量语义不变。主报告缺图修复、完整依赖引用／隐私扫描、第三方分发许可／source条件、明确预备环境与断网搬迁全链复算、最终manifest及只读复验仍必须通过；visual_status如实列unconfirmed，不冒称视觉PASS。仅本包通过后由协调者单写新增目标experiments/mc-2026-10-25，不等1023/token，无共享索引／wiki写入，无commit/push。


### 8.4 执行独立交付更新（2026-10-27）

用户明确要求执行交付或各项目独立交付，仅遇实质障碍再报；并告知token原owner需求已实现、1023原owner正在最后复查。按包并行恢复并先直接核验新交接，不复述旧缺口、不设三包总等待。1025沿§8.3独立版；依§3.8已允许的明确固定预备安装环境路线，在新版本白名单不捆绑尚缺分发材料的第三方报告二进制（PyMuPDF wheel、Chromium/FFmpeg ZIP），保留全部旧候选与研究数据/报告/运行源码，提供官方取得URL/hash、环境锁/安装脚本并真实预备后断网验收；不删除旧件、不擅改license、不假称portable。分发是否闭合按实际分发文件与适用条件逐项核验，不能以泛化法务担忧无限阻断。各包实际通过后协调者单写落位并逐包receipt，不commit/push、不改共享索引。token新正式交接及1023新superseding先核hash/code/input/真实执行，不以用户转达替代核验，也不把永久无未来重跑的不可证要求扩大为新增门禁。实质审批/证据不足精确报告；常规路径/环境/打包由执行方解决。


### 8.5 协调状态附录：原会话并行恢复与消费续核（2026-10-27）

本节仅登记当前执行状态及证据等级，不新增授权，不修改§8.2–8.4或旧历史。三原session已恢复互斥并行，继续各守原工作区；不设全局等待屏障。

- **token**：本线本次直接核26条证据、5组closure共24文件条目，原只读verifier返回`VERIFIED_WAITING_APPROVAL / exit2 / ready=false`（Green Source：`A/analysis/tsinghua-clean-release-20261027/token-work/consumption-recheck-20261027-01/verification.json:1`、`REPORT.md:1`）。本次用户转达协调者已直接执行同目录`verify_record.py`得exit0，并阅读REPORT、接受仅记录完整性范围；此exit0不是生产批准或统计PASS。现有v1没有exit0 acceptance；另版v2＋绑定最终code/schema/input/policy/evidence的原owner批准仍为实质阻断，W5-a未执行。不代签、不填JSON解锁，不把准备PASS冒充统计PASS，不等待实验报告。
- **1023**：新承接已存在于`A/analysis/tsinghua-baseline-audit-20261022/dna-final-20261027/parent-statistics-superseding-20261027-01/`，旧“尚无承接”仅属历史时点。兄弟目前仅预览自报W1捕获通过，协调者尚未直接复核，故仅记**代理进展待核**，不标Green、不写已完成或已确认INPUTS_PINNED；新承接不自动批准token join。
- **1025**：V6仍在验收，尚未发行；沿§8.3独立交付，不因token待批重新阻断，也不将候选验收进展写为RELEASED。
- **保护／目标**：本次用户转达，在独立target核验后，协调者已直接重算10/10保护hash一致、三个目标目录均不存在；本状态记录者未重复目标核验，不将转达冒充自身直接计算。`legacy/p11-closed-v5-minimax-m3` dirty及两论文wiki既有改动未触碰。

本轮变动仅为C根README／CHANGELOG与本状态附录的追加，不改旧sealed token接口、上游、其他工作目录或目标仓；无commit/push／实验API。状态同步后停写，无新增用户同意请求。


### 8.6 首版交付落位更新（2026-10-27）

用户明确要求首版优先交付、不再等待原完整发行审计，并授权本执行者为唯一目标 writer 执行实际落位。1025 负责人已停写 V6 候选（`analysis/tsinghua-clean-release-20261027/integration-work/package-standalone-v6/`，后台终态）；源无最终 manifest、stage manifest 非整树，本次仅生成 transport inventory/hash（5365 文件，770458151 bytes，manifest sha256 `8c1f4695…1cedc`）用于复制一致性，不依赖不存在的 final manifest，不做额外审计/扫描/统计/环境/测试。经目标不存在与 10 保护 hash 快查、dry-run 预检后，仅新增落位 `experiments/mc-2026-10-25/`（完整复制源目录内容含 `FIRST-DELIVERY.md`，不含上级；三二进制已由 owner 排除），独占创建不覆盖，写后逐项同字节复核、baseline 前后 10/10 全同，私有 receipt（sha256 `5a108dc5…cc50`）存于 `coordinator-checks/independent-delivery-20261027/`。

首版状态如实标注：FIRST_DELIVERY/INCOMPLETE，安全终检未完成、最终 acceptance NOT_RUN；用户允许交付但不标 PASS——原完整门禁未做，不冒 PASS，已有隐私清洁不撤回，不将 INCOMPLETE 标 PASS。无 commit/push、不改 wiki/共享索引。本轮变动仅为本节、C 根 README/CHANGELOG 与执行者目录 CHANGELOG 追加；落位完成后停写。
