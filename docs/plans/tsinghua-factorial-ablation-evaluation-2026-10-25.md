# 1025独立八条件消融研究计划

日期：2026-10-25｜版本：`factorial-design-v3.1-20261025`｜状态：唯一权威设计；研究问题已裁定，文档准备完成；实现仍为v2，当前未ready。

## 1. Summary — Goal

开展同期 SA/MA × SR/MR × DNA/NoDNA 八臂探索性研究：3生成模型×3企业×5重复，每臂45份，共360份企业级输出。同期 MAMR_DNA 复刻五月内容协议，SASR使用五月原SASR；SAMR采用S2（自身上一轮已接受全文回灌，无摘要调用）；MASR为沿SASR同请求的无交流负对照。不增加45份桥接。组件移除差及交互为主，精确Shapley为补充。

本文是唯一权威v3.1；历史审计中的S1、桥接等候选已由用户最终裁定取代。现有实现和32项离线测试属于v2，不能据此宣称v3.1 ready。本轮只修订主计划、预算、交接及CHANGELOG。

## 2. Background — 基准、证据与状态

Green Source：用户2026-10-25最终裁定；静态审计见 `F/MAY-PROTOCOL-AUDIT.md:18-100`；前次v3整合直接读取 `F/frozen/original/generate_experiments.py.txt:45-224`，确认SASR/MAMR原措辞、竞争摘要、Jaccard与信息流。下文 F 均指 `analysis/tsinghua-factorial-ablation-20261025`。五月内容基准commit为 `545faac7d42247f8b32167779480bb9c9ac517e1`；源码身份不等于逐请求历史服务确证。

本次使用当前同期服务，执行时间及服务版本与五月可能不同，结果解释限于本次冻结服务条件。

### 2.1 准确模型与路由（已知，不待用户提供ID）

Green Source：`F/MAY-PROTOCOL-AUDIT.md:55-68` 已有路由审计；这里使用其准确ID，不重新读取或操作1023。

| 角色 | Provider | model ID |
|---|---|---|
| GPT-OSS生成/摘要 | OpenRouter | `openai/gpt-oss-120b` |
| DeepSeek生成/摘要 | OpenRouter | `deepseek/deepseek-v4-flash` |
| Qwen生成/摘要 | Paratera | `Qwen3.5-122B-A10B` |
| A | Paratera | `GLM-5.1` |
| B-Kimi | OpenRouter | `moonshotai/kimi-k2.5` |
| B-MiniMax | Paratera | `MiniMax-M2.7` |

现有config/source-manifest仍含旧角色及未解决ID字段，后续需按本表修正并重新冻结；不是研究设计待裁定。原材料、40变体、one-shot、本体及测量模板已有静态资产，须绑定五月来源和实际哈希，不能把当前v2配置当v3.1。

### 2.2 数据流与边界

冻结资产/配置 → immutable manifest → 条件依赖图 → coordinator → 单发worker → 原子journal → 内容接受/Jaccard → MAMR共同摘要或SAMR自身全文 → raw全历史 → full_history主评分 → 严格有效性审计 → manifest左连接 → 差值/交互/Shapley。

配置→manifest是唯一随机分配阶段；响应有效性与内容追加分开；评分协议值与分析值分开；统计按固定设计键和九格等权，不按完成顺序加权。全历史评分、任务措辞、轮数、压缩、追加机会与计算量均可能随处理绑定，识别的是处理包效应，不能称纯agent数量或纯认知机制。

## 3. Design — Approach

### 3.1 范围与冻结

F已存在且有v2离线实现；本次不修改运行代码/配置，不发API，不读runs或封存库，不操作1023。审计文档保留为历史证据。后续实现采用新的v3.1 protocol hash，不复用v2实验目录或结果；所有资产增补记录来源、时间、执行者及哈希。

### 3.2 八臂、最小措辞差异及内容协议

令a=MA、r=MR、d=DNA，八臂各45份。

| 条件 | 内容定义与最小必要改变 | 正式生成/摘要调用 |
|---|---|---:|
| SASR_DNA | 五月原SASR单轮任务、五属性 | 45/0 |
| SASR_NoDNA | 原SASR只删除五属性行 | 45/0 |
| MASR_DNA | 三企业调度分组，无交流；每企业请求与SASR_DNA同变体完全相同 | 45/0 |
| MASR_NoDNA | 同上，只删除五属性行 | 45/0 |
| SAMR_DNA | 原MAMR最小改为单智能体三轮；上一轮自身已接受决策全文回灌；删除编排摘要 | 135/0 |
| SAMR_NoDNA | 同上，只删除五属性行 | 135/0 |
| MAMR_DNA | 五月原MAMR三轮、三企业共同竞争摘要、完整五属性 | 135/30 |
| MAMR_NoDNA | 原MAMR只删除五属性行 | 135/30 |

**模板与必要diff：**

- 政策、企业身份、one-shot、40变体原文及顺序/空白保留。DNA只控制技术路线、规模、供应链策略、安全合规禀赋、标准跟随策略五行；身份保留，NoDNA不代表没有预训练企业知识。
- SASR保留“请直接输出你的分析，包含一阶、二阶、三阶效应。”；MASR逐请求与对应SASR相同，独立采样，不复用响应。
- MAMR保留原首轮“多智能体多轮博弈”、决策层、策略决策/理由/预期效应；后续保留竞争态势、调整策略及“新发现的效应”，不改成长篇完整重述任务。
- SAMR仅将“多智能体多轮博弈”替换为“单智能体多轮推演”；“上一轮竞争态势摘要：”替换为“上一轮自身决策文本：”；“请基于新的竞争态势，调整你的策略决策。”替换为“请基于上一轮自身决策文本，调整你的策略决策。”。其余原MAMR要求保留；不得新增长任务。
- SAMR第2/3轮仅注入自身紧邻上一轮已接受全文，不截800字符，不摘要、不注入更早轮或他企业正文；Jaccard仍查自身全部前轮。记录全文hash及来源call。
- 后续在`protocol-diff.md`逐臂登记必要变更及逐字diff；这些是新增臂，不冒称五月已有SAMR/MASR。SASR与MAMR原任务措辞差异是既定处理包的一部分。

**共同摘要（仅MAMR）：** 同一生成模型，无状态调用；固定LANDSPACE→SPACETIMETECH→ISPACE顺序，保留中文名+ID标题、每企业Python字符串前800字符及五月原竞争摘要模板（策略立场、冲突互补、市场格局、200字以内）。不改为中性状态摘要，不硬截输出，不因超过200字重抽。等待本轮三企业全部接受后，生成一次摘要供下一轮三企业共同消费；同轮互不可见。两次摘要，无第3轮后摘要。

**请求参数：** 全部生成、摘要及A/B评分均省略`max_tokens`、`max_completion_tokens`及其他输出cap，温度0.7；保留原messages及准确model ID，不新增API seed、工具或reasoning强度。验收须检查实际SDK请求kwargs及序列化body确实无输出cap，不能只检查配置，也不能以null或SDK默认注入替代省略。相对五月静态参数，本次仅调整为省略输出cap、采用下述并发配额和600秒客户端timeout。

**Jaccard：** 原空白split/set、空并集0；MR候选与自身全部已接受前轮的最大相似度≥0.4，最多追加2次，累计原提醒“注意：请避免重复之前的分析角度。”，不重抽变体。最后允许候选正文可用即接受；追加技术失败则本轮缺失，不回退先前候选。SR不触发。内容追加不是技术重试。

技术调用沿现有单发实现作为工程默认，成功不重复发，pending不重发；这不是消融因子或用户必须裁定的新流程，不新增技术重试实现。

### 3.3 Manifest、类型与随机化

现有 `F/scripts/design.py`，使用不可变 record/dataclass 风格类型，与同步 Python 脚本结构一致：

- `ConditionSpec`：`condition_id, agent_mode, round_count, dna_present`；仅上述八值。
- `TaskSpec`：稳定任务身份、角色、依赖、provider/model、优先入队序、请求输入哈希。
- `Manifest`：完整实验设计与资产/运行环境哈希，prepare 创建，后续只读。

接口形状：

- `build_manifest(config) → manifest`：同步；配置、资产或键校验失败即终止。
- 新组件不修改任何现有公共 API，无外部调用点迁移。

随机化固定为15个 `model×replicate` 完整块：

1. `random.Random(20261025)` 生成块排列及每块八条件排列。
2. 独立 `random.Random(20261026)` 为每个 `model×replicate×enterprise×round` 分配 framework/context。
3. 八条件共享对应变体；SR 只使用 round 1。
4. 固定 Python 版本，manifest 保存实际变体文本、组合、排列、版本和 SHA-256。
5. 内容尝试不消费 RNG；恢复不重新抽样。

并行下 `execution_order` 定义为**准入/入队顺序，不保证完成顺序**。每个模型按全局块排列在该模型上的投影依次激活块；最多一个生成块活跃。一个块的生成/摘要全部终态后可激活下一块，评分尾部不阻塞生成块释放；“单模型一个块”指生成模型角色，评分仍按实际provider/model共享配额。

### 3.4 Coordinator、worker 与公平调度

现有 `F/scripts/coordinator.py`；其可变状态由单协调器线程独占：

`manifest, dependency_graph, ready_queues, in_flight, completed, blocked, concurrency_version, reservations`。

worker 采用同进程有界线程池，只执行一次同步 SDK 请求，无自动重试、无共享状态写入、无 SDK 全局 monkeypatch。worker 的 client 在线程内创建/使用并在关闭时释放。

**接口调整：**

| 组件 | 早期接口 | 保留的接口职责 |
|---|---|---|
| generator | `generate_unit(spec, unit, request_fn) → records` | 拆为同步 `initialize_unit(...) → state`、`advance(state, durable_result) → tasks/records`；均由 coordinator 调用 |
| journal | `request(call_id, dependencies, body) → response` | 拆为协调器 `prepare/mark_pending/complete` 和 worker `request(...) → response`；worker 不写 journal |
| runner | `prepare/generate/score/audit/analyze` | 子命令保持；`generate` 默认启动生成与评分重叠流水，`score` 仅处理未派发且依赖已满足的评分 |

拆分避免同步 `generate_unit` 占据 worker 后等待下游请求造成线程池死锁。现有调用链涉及 `run_factorial.py`、`coordinator.py`、`generate_factorial.py`、`score_factorial.py`。

**调度规则：**

- 初始配额：global=6、per-model=2；Paratera provider至少4（建议4），OpenRouter=3。Qwen与GLM各须支持至少2路独立就绪调用并发。
- 当Qwen和GLM各有2项独立ready任务且global/provider/model均有额度时，允许2+2同时准入；不得用统一provider=3将其串行化。依赖屏障和单模型活跃块约束照常遵守，没有ready任务时不承诺并发。MiniMax继续参与公平调度，不为维持2+2而饥饿等待；2+2不是永久专属槽。
- model 配额按实际 `(provider, model_id)` 计数；同模型用于生成、摘要和评分时共享限额。
- 所有请求共用配额；provider 限额可能先于 global 限额生效。
- 条件没有优先级、专属配额或限流。
- 同时就绪按 manifest 顺序入队；后续就绪按协调器接收的持久化完成事件入队，事件序号记录。
- 在满足配额的候选中选 FIFO 最早项；因某 provider 无额度可扫描后项，不能阻塞其他 provider。
- 生成/摘要队列与评分队列分开；评分按完整full_history冻结顺序，三个评委固定 A、B-Kimi、B-MiniMax 顺序入队。
- 当某 provider 存在可派发评分且当前没有该 provider 的评分在途，其下一个可用槽优先交评分；反向规则保障生成/摘要。双方均为零时按记录的交替位选择；其余槽按两队头最早入队序派发。该规则在初始配额下为双方各保底一个可用槽，并避免永久抢占。
- 全局层先在存在配额可用候选的两类中按保底/交替规则选择类别，再在该类别扫描FIFO最早可派发项；provider/model层也应用同一保底规则。缺配额的队头不阻挡其他可用provider。降至global/provider/model单槽时采用双方交替，不要求不可实现的同时保底；交替位持久化于snapshot。
- 每个 call 保存 `concurrency_version`、global/provider/model 的 `in_flight_at_dispatch` 和实际 provider/model。

并发参数仅在独立 smoke 中确定后冻结；正式运行中仅允许预先声明的降并发操作：停止新派发，排空在途，原子记录旧值、新值、原因、时间后恢复。429 本身不触发重发。

### 3.5 Journal、失败、STOP 与恢复

保留请求状态：

`prepared → pending → completed | transport_error`

响应有效性独立枚举：

`usable | empty | provider_error | tool_response`

`transport_error` 的响应有效性为 null，另存原因；`completed` 不等于可用。

**执行顺序：**

1. 配额及预算预留检查。
2. coordinator 原子持久化实际 body、依赖、fingerprint、预留和 `prepared`。
3. 原子写入 `pending` 后交 worker；任何写失败均不发送。
4. worker 返回结果事件。
5. coordinator 先落盘完整响应/错误，再推进内容状态或派发消费者。

`pending` 写入后、物理发送前崩溃仍视为不确定请求，禁止自动重发；选择保守留缺失而非冒险重复收费。

**失败传播完整规则：**

- SDK/外围自动技术重试关闭。
- provider error，包括非空正文伴随 `finish_reason=error`、空正文、工具响应、超时：保存并记缺失，不替代、不补样。
- 429：`transport_error`，`reason_code=rate_limited`，不重发。
- 非空 `length` 正文可用但标截断，不续写、不因格式重抽。
- SAMR 失败只阻断该企业后续；MAMR 第1/2轮任一企业失败阻断其后续共同摘要及消费者。
- 摘要失败阻断全部消费者；MAMR 第3轮一个企业失败不撤销其他 final。
- Jaccard 追加失败使本轮缺失；final 缺失不派评分。
- 普通已确认失败允许无依赖任务继续；认证失败、预算触发、journal 损坏停止全局新派发并排空在途。

STOP 同样停止新派发、排空在途、落盘后退出，不取消已发送请求。客户端SDK timeout固定600秒，并在实际client构造处验收；它约束SDK连接/读写等阶段等待，具体语义随冻结SDK核对，不等于请求或整次运行严格600秒总墙钟deadline。外层runner/工具不得以480秒先终止；外层等待须容纳SDK阶段等待与排空落盘，不新增复杂超时流程。journal 写失败时保留可恢复的在内存结果并尝试恢复写入；无法持久化的请求保留 `pending`，不得声称已安全归档。

**任务级状态另设：**

`waiting | ready | in_flight | succeeded | failed | blocked | not_dispatched`

终止报告为全部未执行任务提供原因：

`dependency_missing, upstream_failed, rate_limited, budget_exhausted, provider_unavailable, auth_failed, journal_corrupt, queued_not_dispatched`。

`not_dispatched` 是本次执行终态，后续恢复可继续；物理已失败或不确定请求不可重试。

**恢复优先级：**

- immutable manifest → journal 权威记录 → snapshot 调度缓存。
- snapshot 每次派发/完成/配额变更后原子写，空闲时每5秒写。
- snapshot 保存队列、在途 ID、完成集合、并发版本、预留账、各层公平调度交替位和 journal 序号；并发变更另追加 `concurrency-versions.jsonl`，审计生成 `blocked-tasks.json`。
- journal以单调event_seq记录队列准入、持久化响应完成、活跃块切换、预算暂停/显式恢复、并发版本及派发承诺；各层公平交替位仅在派发承诺耐久写入pending时翻转。版本日志是这些事件的派生视图，采用同一event_seq，重放以journal为准。snapshot过期时从其最后序号重放事件，恢复准入序、交替位、块状态和预留账；事件或版本不一致停止派发。
- snapshot 过期可由 journal 重建；请求哈希不符、journal 损坏或遗留 `pending` 阻止恢复派发。
- 已完成且指纹一致只离线回放；重复完成事件按 `call_id` 幂等处理，冲突事件报错。
- 单 run 使用独占锁，异常退出和正常退出均关闭线程池/client 并释放锁。

### 3.6 预算预留与调用量

Red Source／`factorial-budget-v3.1-20261025`：以下为S2拓扑推算，非实测。全部请求省略输出cap；旧token数仅为费用情景假设，不能据此约束实际输出或保证金额上限，仍需当前价格、计费语义与在途预留。预算详见F/BUDGET-ESTIMATE-20261025.md。

| 正式阶段 | OpenRouter | Paratera | 合计 |
|---|---:|---:|---:|
| 企业生成 | 480 | 240 | 720 |
| MAMR摘要 | 40 | 20 | 60 |
| A | 0 | 360 | 360 |
| B-Kimi | 360 | 0 | 360 |
| B-MiniMax | 0 | 360 | 360 |
| 基础 | **880** | **980** | **1860** |
| 最大内容追加 | 480 | 240 | 720 |
| 逻辑调用上限 | **1360** | **1220** | **2580** |

每生成模型240生成+20摘要。GPT-OSS一重复八臂小试：48生成+4摘要+72评分=124，追加≤48，总≤172；OpenRouter76+最多48，Paratera48。正式加小试：OpenRouter956/1484、Paratera1028/1268，共1984基础/2752满追加。不加桥接或额外评分view。失败可能减少实际调用。

费用公式`C=Σ n(I×p_in+O×p_out)/10^6`。沿既有列表价及明确token假设，OpenRouter含小试无追加基本/偏高5.365380/10.12932752美元，满追加5.820180/10.83283856美元；用户称1023 OpenRouter仅花约4美元（Green Source：2026-10-25用户经验，未独立账单核验，本轮不读1023运行），仅作历史参考；不得按调用数盲推本次同成本。建议OpenRouter 10美元工作预留，原20美元降为可选宽裕额；均非执行授权或费用上限保证。旧约5.37–10.83美元仍仅为token情景，不是输出cap约束。Paratera实际价目未知，只给按模型的可核价公式；旧600元算例不作为报价或预留结论。用户已确认成本可控，余项为环境与预算落实。

派发沿现有预算机制：已知累计费用+未结算预留+在途预留+新请求预留不得超过授权阈值；usage/cost未知保留null和预留，不按0释放。预留不足全局停止新派发并排空，生成budget_exhausted清单；排空不静默重启，显式恢复只派从未发送任务。已知费用、账户变化、未知费用分列。缺口为max(0,小试费用+正式选定情景+余量−可用余额)；实时价格/余额未核验，不声称已硬封顶。

### 3.7 评分、持久化与覆盖

评分继承五月全历史内容与模板；有效性边界保留前次评审修正，见 `docs/reviews/tsinghua-factorial-ablation-review-2026-10-25.md:16-25`。

指定末轮接受且完整历史落盘后触发主评分：

- SR 指定 round1；MR 指定 round3，不能回退。
- raw与full_history输入哈希写入成功后才能创建三个评分任务；MAMR可在单企业round3接受后评分，不必等待另两企业final，因同轮互不可见且最终正文不会再变。
- A=`GLM-5.1`；B=`moonshotai/kimi-k2.5`、`MiniMax-M2.7`，provider见§2.1。
- 评分适配器将SR的一轮、MR全部三轮已接受正文以五月原分隔符 `\n\n---\n\n` 拼接为combined_output；主scoring_view=full_history，依赖及input_sha256覆盖全部轮次。缺任一轮不评分、不回退final或部分历史；不传条件/DNA标签、摘要及日志。
- A 主指标 SO+TO；B次指标为两评委维度均值的等权均值，不用模型自报overall。
- 冻结评分函数若内部调用传输，必须通过显式 request callback 接入 journal；不得用并发全局 monkeypatch。

有效性：

- 保存 `protocol_value` 协议值及独立 `analysis_value`。B协议值复刻旧建表：每评委非空维度均值先Python round(x,3)，再双评委均值round(x,3)；分析层仅用通过严格有效性检查的原始维度数值，不做中间舍入，两评委原始均值等权平均。二者字段及报表分列，不混称五月原值。A空解析的协议0与分析NA亦分开。
- A：非空可解析 judgments，ID 为本体内唯一 ID，`appeared` 严格布尔；部分覆盖可用并标注。空、重复、未知 ID、类型异常、技术失败为 NA。
- B：按已有非空维度均值；非空分数须为非 bool 的有限数值且在1–5。任一异常或全空使该评委 NA；两评委均有效才算总 B。
- 不补分、不修复、不重评；报告条目和维度覆盖组成。部分judgments计数不是完整本体覆盖下的零；部分维度均值可能改变测量组成，不额外要求全本体/全维度完整来筛样。
- final/full 字符长度、轮次、摘要长度、tokens、缺失率必报。长度是处理后变量，不能靠回归宣称纯机制。
- `full_history`是唯一主评分；本次不增加final-only诊断调用。不截断或长度匹配删样，不以每千字符得分代替主指标。

v3.1须更新schema/protocol版本，明确与既有v2分离，不迁移或混用旧数据。必填字段缺失直接拒绝；未知 usage/cost 用 JSON null，统计 NA 序列化为 null 并附原因。

| 对象 | 必需字段 |
|---|---|
| manifest | `experiment_id, protocol_hash, model, replicate, condition_id, enterprise, block_id, variant_by_round, execution_order`，另含冻结资产、路由、环境、并发版本 |
| raw | `responses, combined_output, token_usage, schema_version, dna_present, round_count, final_output, final_sha256, full_history_sha256, call_ids, summary_ids, status` |
| summary | `summary_id, source_call_ids, source_text_sha256, input_char_counts, text, consumer_call_ids` |
| call | `call_id, request_hash, dependency_ids, status, response, usage, cost, response_validity, reason_code`及派发并发元数据 |
| score | `scoring_view, input_sha256, protocol_result, protocol_value, analysis_value, audit_flags, judge_call_id` |
| snapshot | journal序号、队列、在途、完成集合、并发版本、预留账 |
| coverage | 预期数、final生成数、评分响应数、指标有效数、审计完整数及原因分布 |

`call_id` 包含条件、生成模型、重复、企业或batch、轮次、角色、内容尝试序号；评分另含 judge 身份和 scoring view。哈希覆盖实际请求、路由及依赖。成本按唯一物理 call 求和，raw token 汇总仅作描述。

数据集从 manifest 左连接，正式固定360行；smoke 固定24行且目录隔离。额外键、重复键或未知资产报审计失败。

### 3.8 归因、交互与精度

令 \(\mu_{ard}\) 为每模型×企业内五重复均值，再对九格等权平均。

索引顺序固定为 `(a=MA, r=MR, d=DNA)`，0为低水平、1为高水平：

| µ | 条件 | µ | 条件 |
|---|---|---|---|
| 000 | SASR_NoDNA | 001 | SASR_DNA |
| 010 | SAMR_NoDNA | 011 | SAMR_DNA |
| 100 | MASR_NoDNA | 101 | MASR_DNA |
| 110 | MAMR_NoDNA | 111 | MAMR_DNA |

#### 头条主表

| 指标 | 定义 |
|---|---|
| 移除跨企业信息组织 | \(C_A=\mu_{111}-\mu_{011}\) |
| 移除多轮 | \(C_R=\mu_{111}-\mu_{101}\) |
| 移除显式五属性 | \(C_D=\mu_{111}-\mu_{110}\) |
| DNA 调节共同信息差值 | \(I_{AD\mid R=1}=(\mu_{111}-\mu_{011})-(\mu_{110}-\mu_{010})\) |
| DNA 调节轮次差值 | \(I_{RD\mid A=1}=(\mu_{111}-\mu_{101})-(\mu_{110}-\mu_{100})\) |
| DNA 条件下 A×R | \(I_{AR\mid D=1}=\mu_{111}-\mu_{011}-\mu_{101}+\mu_{001}\) |

三个 \(C\) 是同一全状态附近的移除差，含重叠交互，**互不加总**，其和不等于 \(\mu_{111}-\mu_{000}\)。

同时报告 `I_AR|D=0 = µ110−µ010−µ100+µ000`，三重交互为 `I_AR|D=1−I_AR|D=0`。四架构各自DNA差值全部报告，避免只选MAMR结果。

保留七效应（统一采用原量纲差值/差中之差，不作±1回归系数缩放）：

- DNA、Round、Agent 主效应：分别在其他两因子水平上平均的一阶差。
- A×R、A×D、R×D：在剩余因子上平均的二阶差。
- A×R×D：三阶差。

上述三个局部二阶交互分别等于对应平均二阶交互加三阶交互的一半。两 DNA 水平分别报告：

- `MAMR−SAMR`、`MASR−SASR`；
- `SAMR−SASR`、`MAMR−MASR`。

若 SR 负对照期望差为零，Agent 主效应是跨 DNA 平均 MR 差的一半，A×R 是该 MR 差；不是两份独立机制证据。

#### Shapley 补充表

三玩家 \(N=\{A,R,D\}\)，八联盟的值取对应条件均值，\(v(\varnothing)=\mu_{000}\)：

\[
\phi_i=\sum_{S\subseteq N\setminus\{i\}}
\frac{|S|!(2-|S|)!}{3!}\,[v(S\cup\{i\})-v(S)].
\]

精确枚举；权重按联盟大小为 \(1/3,1/6,1/3\)。无需新评分/API。

- \(\phi_A+\phi_R+\phi_D=\mu_{111}-\mu_{000}\)。
- 负值不裁剪，默认不报百分比。
- 与主差值表相邻呈现，明确“补充归因”，不能替代头条。
- 它分摊所定义处理包的增量，不产生纯机制因果解释。

#### 缺失与 bootstrap

统一按模型内完整replicate块重采样，以保留八臂匹配变体及MAMR三企业依赖；模型、企业不是可互换总体抽样单位。

- 对每个指标，360值全有效才给完整设计估计与区间。
- 有缺失则完整分析置 NA；另报 available-case：每模型×企业对有效重复取均值，九格仍等权。
- 必要格全缺失时相应对比 NA；任一联盟必要格不可估时完整 Shapley 向量 NA，不重分权。
- 每指标输出条件×模型×企业的有效重复数n（0–5）、观察均值及缺失原因。available-case对比/Shapley单列，基于观察到的重复，不等同完整设计估计；有点估计时仍不报告主区间。
- model 内有放回抽五个 replicate 块，八条件与三企业同时移动。
- 10,000次，PCG64 seed `20261027`；每次 draw 同时计算全部差值、交互与 Shapley。
- 报 bootstrap SD、2.5/97.5百分位线性插值区间，不筛选“可计算重抽”。

**Red Source／`precision-v3.1-20261025`**：

\[
SE\approx\sqrt{\sum_m s_m^2/(9\times5)}
\]

其中 \(s_m^2\) 是模型内块级对比方差，仅描述量级，不保证覆盖或功效。扩量须另按实质差异尺度、目标半宽及保留块结构的模拟制定，不能追加到显著。

设计内部限制明确为：八标签六种可见策略、每模型五块、MAMR 内容 cluster、模型/企业/政策推广范围有限。所有 DNA 差值方向统一为有DNA减无DNA。

## 4. File-by-file impact — 下一步代码差异

本轮修改唯一主计划、F/BUDGET-ESTIMATE-20261025.md、F/HANDOFF.md顶端和F/CHANGELOG.md；F/MAY-PROTOCOL-AUDIT.md及旧验收报告原样保留为历史证据。以下是后续实现任务，不代表本轮已执行。

| 文件/模块 | 必要差异 | 验收 |
|---|---|---|
| config/factorial.yaml、scripts/design.py | 修正三生成模型/评委ID；v3.1、五月commit、S2、省略全部输出cap、full_history；移除旧未决ID | 360键/15块，新hash；旧协议拒绝混用 |
| design.py prompt、protocol-diff.md | 原SASR/MAMR模板；SAMR仅列明必要措辞替换；MASR沿SASR；NoDNA只五行 | 五月黄金请求及逐臂diff |
| scripts/generate_factorial.py | 删除SAMR摘要节点，上一轮自身接受全文依赖；恢复MAMR原摘要/标题 | 720生成+60摘要；无同轮/跨企业泄漏 |
| scripts/score_factorial.py、build_factorial_dataset.py、protocol/schema-v1.json | 主full_history及省略输出cap；全历史hash/依赖；B旧round(3)协议与无中间舍入分析层分离 | 完整历史缺失、严格NA、双评委及舍入fixture |
| scripts/coordinator.py、journal.py、worker.py、production.py、run_factorial.py | 沿既有并行/单发恢复；实际SDK请求省略输出cap，评分触发绑定完整历史，落实600秒客户端timeout及预算情景语义 | SDK mock实际body；成功零重发、pending阻断；公平/预算恢复 |
| frozen/source-manifest.json及独立golden fixtures | 绑定五月blob/哈希；清理旧未决状态，保留原始资产证据 | 独立纯函数fixture与实际新请求逐字比较 |
| scripts/test_w123.py、test_w45.py、test_production.py、test_w6.py、verify_factorial.py | 替换旧中性prompt/自摘要/最终轮/阶段cap/调用数断言，保留有效工程统计测试 | v3.1离线结果独立记录，不能沿用旧32/32 |
| config/budget.yaml、config/concurrency.yaml及环境记录 | 落实当前价目/额度、token预留、SDK省略cap、600秒timeout与global=6、per-model=2、Paratera≥4（建议4）/OpenRouter=3配额 | 环境预算闭合后才进入小试 |

统计analyze的差值/交互/Shapley和同draw设计保留，仅适配v3.1协议及主view。运行产物仍限定F下独立run目录，拒绝符号链接逃逸/异manifest目录复用；本次不读写runs。

## 5. Work Items、黄金对照与闸门

### 5.1 实施次序

W0：本次v3.1文档整合。W1：绑定五月静态来源、修正配置/模型/协议hash。W2：实现原模板及S2信息流。W3：主full_history及B双层聚合。W4：落实SDK省略输出cap、600秒timeout、2+2就绪准入及既有并行journal/预算/schema。W5：黄金对照及工程/统计离线回归。W6：环境与预算落实后独立小试（124+最多48）。W7：正式360份（1860+最多720）。W8：离线审计与报告。后续代码工作须完成后重新冻结，不把预算输入缺失当代码差异已完成。

### 5.2 离线必验（黄金对照）

1. 从五月静态源码/已审计字节提取纯模板与常量，不执行旧main/API；fixture独立于新builder，固定framework/context和上一轮内容。MAMR_DNA 3企业×40变体×3轮=360个黄金情境；原SASR_DNA 3×40=120。比完整messages、空白/尾换行；参数按本版请求规格验证；八臂共(4×1+4×3)×40×3=1920情境逐项diff，DNA仅五行，SASR/MASR同请求。
2. SAMR仅上述3项措辞替换与自身紧邻上一轮已接受全文，无摘要调用/截断/新任务；MAMR原三源标题、800字符、摘要模板/完整输出、轮间屏障及一对多依赖hash。Jaccard全部自身前轮、阈值边界、提醒累计、追加不耗RNG。
3. 拓扑正式720+60+1080=1860，追加≤720；小试48+4+72=124，追加≤48；合计1984/2752，按实际provider/model复核供应商分配。
4. 主full_history原分隔符、全部轮依赖/input hash、A/B实际messages与五月fixture相同；生成/摘要/A/B实际SDK kwargs及序列化body均无max_tokens、max_completion_tokens等输出cap，client timeout=600且无外层480秒提前终止；SDK阶段超时与总墙钟分列；缺轮不回退。A空解析protocol0/analysisNA；B部分维度、非法/bool/非有限值、两评委缺一、Python round(3)中间舍入与无中间舍入分析分列。
5. 增加离线准入验收：Qwen/GLM各2项独立ready且额度可用时同时2+2准入；无ready不强派；Paratera≥4、OpenRouter=3、global=6、per-model=2，实际同model跨角色合并计数，MiniMax不饥饿。保留并行乱序屏障、共享provider/model配额、每模型单活跃块、公平与单槽交替、STOP排空；prepared/pending/响应落盘前后故障；completed零重发、pending阻止恢复、snapshot落后重建、重复事件幂等。重建后派发顺序/并发版本/预留账须等于不中断基准，覆盖预算暂停显式恢复及降并发。
6. 追加失败、摘要失败、MAMR第三轮部分成功、429/auth/预算/journal错误逐项验失败传播；不新增技术重试测试框架或实现流程。
7. 人工八格验证差值符号、不可加性、交互、Shapley守恒/负值、同draw bootstrap及缺失九格等权；额外/重复键、未知资产/模型、目录逃逸拒绝。

离线验收在非runs临时区且禁网；本次未运行旧测试，避免生成运行产物。后续verify/audit/analyze仍要求零网络。覆盖、条件×并发度/版本/provider分布用于诊断，不据事后平衡删样。

### 5.3 Go/No-Go与当前状态

| 闸门 | Go判据 | 当前 |
|---|---|---|
| G0 | v3.1资产/正确ID/原文diff/来源hash落实 | ID与设计已知，配置未修订 |
| G1 | v3.1黄金对照、工程和统计回归通过并冻结 | 未完成；32/32仅v2旧验收 |
| G2 | 当前价格/余额/额度、实际SDK省略输出cap、600秒timeout语义及外层等待、并发配额与预算可执行 | 环境/预算待落实 |
| G3 | 独立小试依赖/评分/费用可追溯，并发参数冻结 | 未执行 |
| G4 | 具体正式manifest执行授权 | 本次仅文档准备 |
| G5 | 360预期键终态、覆盖/缺失/统计交付齐全 | 未执行 |

### 5.4 Open Questions — 研究设计已全部裁定

不再询问模型ID、SAMR方案、SASR/MAMR措辞、MASR、桥接、主评分、重复数或技术重试。剩余外部输入仅环境可用性（SDK省略输出cap、600秒timeout及外层等待、账户配额）与预算落实（最新价格、余额、预留和具体执行授权）；内部待办是按§4修正实现并完成§5.2验收。当前未ready，文档批准不自动发API。

### 5.5 交付包

v3.1冻结协议与manifest、逐指标条件×模型×企业n/观察均值/缺失原因、360键覆盖、原始轨迹、SAMR全文来源及MAMR摘要依赖、唯一物理请求/并发版本/预留结算账、三评委protocol/analysis分层结果、主差值与交互/简单效应、Shapley补充、共享draw区间或NA、长度/用量诊断及处理包可识别性限制。

## 6. Tradeoffs、风险与验证样例

- **八标签六种可见策略**：SASR/MASR的同prompt负对照被保留以检查采样与调度差异，不把其不显著当等价证据。MA效应包括跨企业信息、压缩比例和共享摘要噪声；MR效应包括后续推理、摘要和内容追加机会。
- **SAMR全文回灌**：采用S2，正式减少180次摘要调用；A差值同时移除跨企业信息、压缩及编排者，不能解释为只改变agent数量。
- **精度**：每模型5个块、全设计15个块；每条件45条不是45个独立MAMR批次。定位探索性pilot，不预先保证小交互可检出。
- **并行**：优先减少墙钟时间，不能承诺几倍加速；配额、共享provider、摘要屏障决定实际吞吐。独立目录不能隔离共享账户限流；实施前确认独立可用额度，若与其他任务共享账户则使用明确分配给1025的剩余额度，避免抢占。
- **恢复**：snapshot是缓存，journal是证据；不确定请求保留缺失，不以自动重发换完整率。回退为停止新入口、排空在途并保留产物，不删除证据或迁移其他实验。

统计离线验收以合成函数 `v(a,r,d)=10+2a+3r+5d+6ar+4ad+8rd+12ard` 为例：八格按000/001/010/011/100/101/110/111为10/15/13/26/12/21/21/50；组件移除为24/29/29，总提升40；`I_AD|R=1=16`、`I_RD|A=1=20`、`I_AR|D=1=18`、`I_AR|D=0=6`、三阶12；Shapley为11/14/15，和40。另验证常数函数全零、单一主效应、纯二阶/三阶协同、负贡献不裁剪、标签置换、缺失九格不重加权以及逐draw守恒。合成数据仅为验收样例，不是模型实验结果。

## 7. References与修订核验

- Green Source：用户2026-10-25最终裁定及本轮最新经验；本文件v3.1为唯一执行设计。
- Green Source：F/MAY-PROTOCOL-AUDIT.md:55-100（模型/协议）、:172-215（S2数量/token情景），为历史审计，其候选选择不是现行指令；F/frozen/original/generate_experiments.py.txt:45-224（前次v3整合直接核对原任务/摘要/Jaccard）。
- Green Source：CLAUDE.md:62-69、AGENTS.md:14-31（来源与复核纪律）；前次v2评审仅保留有效并行、恢复、缺失统计约束。
- Red Source：factorial-design-v3.1-20261025及factorial-budget-v3.1-20261025为设计/费用情景，不是模型实测效果。

本轮依据用户最新经验更新请求参数、并发、timeout及预算口径，直接核对四文档一致性；既有调用数及token费用情景保留，历史审计与v2验收不作为当前执行规格。

## 8. 当前实施状态

v2曾记录32/32离线通过（历史记录见F/HANDOFF.md及CHANGELOG），仅证明旧实现内部验收，不能证明五月内容等价或v3.1可运行。现有实现需完成§4差异及§5黄金验收；本次未改实现/配置，未运行实验。主计划与预算已整合v3.1，HANDOFF顶端标记当前状态，历史审计原样保留。
