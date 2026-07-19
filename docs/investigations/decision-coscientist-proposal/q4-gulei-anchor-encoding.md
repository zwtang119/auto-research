# Q4：古雷「4·6」因子锚编码探针（G3）——Factor Ledger schema 灾害域适配性评估

> 状态：完成（试编码 9 条因子落盘）
> 日期：2026-07-19
> 产物：`anchors/gulei-2015-0406.factors.yaml`（9 条因子）、`anchors/settlement_record.template.disaster.yaml`（灾害域适配版 settlement 模板）
> 主要一手来源：福建省应急管理厅《腾龙芳烃（漳州）有限公司"4·6"爆炸着火重大事故调查报告》（fetch 成功，全文取得）；财新 2015-04-07；香港商报 2015-04-09；PolicySim seed `gulei-petrochemical`

---

## 1. 探针概述

G3 探针问题：为体育域（世界杯）设计的 Factor Ledger schema 能否编码灾害域因子？
方法：对古雷「4·6」事故试编码 9 条因子，覆盖全部四种 `event_relation`
（precursor×2、suppressor×2、branch×2、counter_signal×3），每条因子同时满足双挂钩：
(a) 推演侧可观测（事件链节点/干预维度/metricProfile 指标）；(b) 历史侧可锚定
（官方调查报告/媒体/工程规范中的数值化锚）。编码全程记录 schema 不适配点，
不硬塞。

**编码结果：9/9 条因子完成编码并全部进入 `calibration_status: tracking`，无一条因
schema 结构性障碍而失败。** 但 7 处适配点需要 fork 级改动（见 §4）。

---

## 2. 编码因子清单

| ID | relation | 一句话 |
|---|---|---|
| f001 | precursor | 开车引料液击→焊口断裂→炉膛引爆是事故链前兆（推演路径实例化率 ≥0.70/0.85 vs 报告确认的直接原因链） |
| f002 | suppressor | 大规模泡沫供给抑制控制时间（工程下限 ≈37t vs 历史锚 [850,1467]t，推演 P50∈[37,1500]） |
| f003 | counter_signal | 终控 56h 落在烧尽上界窗口 [50,80]h，反证"强攻快速扑灭"叙事 |
| f004 | branch | 初控后复燃分支（历史 3 次复燃+1 次迟发起火，每罐复燃率 ≈0.67，推演条件概率 ∈[0.3,0.8]） |
| f005 | branch | 第四罐（609）起火触发疏散升级 immediate_3km（升级比例 ≥0.80，完成率锚 0.97） |
| f006 | suppressor | 邻罐冷却（1.5D 判据）实现零蔓延（历史新增点燃罐=0，推演 P(蔓延)≤0.05） |
| f007 | counter_signal | 极低伤亡（6 伤 13 观 0 亡）否定"大火必高伤亡"先验，机制=非聚集时段+快速疏散（反事实 ≥3×） |
| f008 | precursor | 3km 立即疏散是零死亡的前置因子（29096 人、完成率 ≈0.97，推演 P50≥0.90 且 T90≤6h） |
| f009 | counter_signal | 官方监测环境零检出否定"PX 爆炸必致污染"公众先验（推演 P50≤1.0km²） |

---

## 3. schema 逐字段适配判定

### 3.1 factor_ledger_entry.schema.yaml

| 字段 | 判定 | 理由 |
|---|---|---|
| factor_id | ✅ 直接可用 | 命名约定 `gulei-2015-fNNN` 平滑替换 `wc2026-...` |
| match_id | 🟡 需改语义 | 复用承载事件 ID 无技术障碍，但 "Match identifier" 语义错位；fork 建议改名 `event_id`（向后兼容） |
| origin | 🟡 需改枚举 | 三枚举 `[cds_generated, kimi_derived, human_seeded]` 无"从历史记录播种"语义。本次全部因子实为 `historical_record`（从事后调查报告/媒体反向播种），暂以 `human_seeded` 兜底。**这是最重要的枚举缺口**：rubric §7 对 origin 有差异化规则，historical_record 需要自己的规则（如：必须声明锚值来源 tier、必须盲评） |
| event_relation | ✅ 直接可用 | 四种关系全部自然落地，无遗漏亦无冗余。灾害域甚至让 branch/counter_signal 比在体育域更自然（复燃、疏散升级、反叙事都是一等公民） |
| direction | 🟡 需改语义 | 体育域指向单一输赢结局；灾害域无单一终值。本次用约定 `increases_/decreases_<metric_key>`（metric_key 取自 seed `metricProfile.aiField`）解决，建议 fork 收编为正式约定 |
| observable_proxy | ✅ 直接可用 | 双挂钩写法（推演侧+历史侧）天然适配 |
| quantified_threshold | ✅ 直接可用 | 9/9 条完成数值化；灾害域反而更依赖数值化（工程闸门给的区间很硬） |
| settlement_rule | 🟡 需改语义 | 体育域："赛后证据→三态"；灾害域证据是**多口径区间**、判定对象是**推演分布**。统一改写为百分位区间语言（锚区间∩[P25,P75]→supported；落 [P5,P95] 外→rejected；口径/机制不可对齐→inconclusive）。三态裁定逻辑本身零改动可用 |
| counter_signal | ✅ 直接可用 | 灾害域反信号同样自然（证伪机制、时序反转、锚值失真） |
| data_sources | 🟡 需新增配套 | 扁平 list[string] 可用，但灾害域证据力分级是刚需（官方调查报告 / 媒体 / 工程规范 / seed 设计包络）。本次以 ID 前缀（official_/media_/eng_/seed_）临时承载，建议 source_ledger 增加 `reliability tier` 字段 |
| adjudicator.required_independence | ✅ 直接可用 | rubric §5 规则原样适用 |
| adjudicator（整体） | 🔴 需新增字段 | 灾害域因子**从结局反推**，专家裁定必须隐去结局，schema 无 `blinded` / `outcome_visibility` 字段。本次暂塞入 required_independence 字符串，属硬塞边缘，fork 必须收编 |
| calibration_status | ✅ 直接可用 | 四态枚举原样适用 |
| adjudication_evidence | ✅ 直接可用 | optional 槽位适配裁定证据 |

### 3.2 settlement_record.schema.yaml

| 字段 | 判定 | 理由 |
|---|---|---|
| match_id / task_type | 🟡 需改语义 | → event_id；task_type → `disaster_response_distribution` |
| result | 🟡 需改语义 | "官方比分"→"历史锚值表"：每锚带 value/interval + basis（口径）+ source + tier。灾害域没有单一终值，有的是多口径锚集合 |
| scores.brier / log_loss | 🔴 不可用，需替换 | 单事件灾害回溯无"对单一类别结局的事前概率预测"，两分数**数学上不可算**。替换为 `percentile_hit[]`（逐锚百分位命中）、`interval_coverage_P25_P75/P5_P95`、`anchor_distance_iqr`、`baseline_difference`（vs 工程夹逼基线）。已落盘适配模板 |
| scores.baseline_difference | ✅ 语义保留 | 基线从"FIFA 排名逻辑模型"换成"GB 50151 闸门/烧尽上界工程夹逼"，槽位语义不变 |
| factor_updates | ✅ 直接可用 | supported/rejected/inconclusive 三列表原样适用 |
| protocol_failures | ✅ 直接可用 | 本次编码已预见至少 3 条候选 pf（见 §4.2） |
| review_notes | ✅ 直接可用 | — |
| （新增）adjudication_meta | 🔴 需新增 | panel_size / blinded / outcome_visibility / inconclusive_rate_policy，见适配模板 |

**汇总：17 个判定项中，直接可用 9 项，需改枚举/语义 6 项，需新增字段 2 项。**

---

## 4. 编码过程中的难点

### 4.1 找不到数值化锚（历史侧缺口）

- **f005 疏散升级时序因果**：官方报告只确认"累计转移安置 29096 人"与 609 罐 4/8 11:05
  起火两个事实，**未将疏散命令与 609 起火显式挂钩**。"第四罐爆燃→3km 紧急疏散"
  的因果链仅见于媒体（香港商报 2015-04-09）。锚值有，因果挂钩是 media 级。
- **f008 疏散完成率分母**：完成率 ≈0.97 依赖"3km 范围人口 ≈3.0 万"的基数推断，
  该基数无任何一手来源。分子（29096）是 official 级，分母是推断——完成率锚
  整体只能算 derived 级。
- **f009 环境口径**："没有发现辖区环境污染"中"辖区"的空间范围、检出指标
  （PX/苯系物/石油烃）、检出限均未定义，且单一官方来源、PX 争议背景，
  证据等级应降半级。
- **罐容数据**：3×10000m³+1×20000m³ 不见于官方调查报告正文（报告只列罐号与
  介质），来自媒体/Q3 调研。f002 的工程下限 9.2t/罐 依赖 1 万 m³ 假设。
- **口径冲突**（编码时发现，非阻塞但必须写区间）：泡沫 650t（媒体，早期到位）/
  850t（seed 注释引 chenan 档案，桶装调拨）/1467t（官方报告，总调运）；
  人员 1169+120（官方）vs 1417（seed 设计上限）；车辆 269（官方）vs 322（seed）。
  **历史锚必须写成区间而非点值——这恰好印证了百分位区间 settlement 的必要性。**

### 4.2 推演侧观测不到（sim 侧缺口）

- **f006 的 1.5D 邻罐几何判据**：seed 场景无罐区拓扑/几何，"距燃烧罐 1.5 倍直径
  内的邻罐"在推演中无可观测对应物。只能退化为"点燃罐集合是否超出初始 4 罐"
  的粗粒度观测。→ 候选 protocol failure（类型：observable_proxy_not_in_sim）。
- **f004 的复燃机制条件**：复燃的触发机制（泡沫层破坏+残液高温+阵风）在 seed
  事件链中无状态变量；只有 `gas_explosion` 节点概率 0.6 可勉强挂钩复燃事件本身。
  且 seed 无"初控-复燃"两阶段状态机，f003 的"首控 21.7h vs 终控 56.0h"双口径
  也无法对齐。→ 这是**本次编码发现的最大 sim 侧结构性缺口**。
- **f007 的伤/亡分离**：`casualty_estimate` 是单一数值，不区分受伤/留观/死亡，
  而历史锚的精髓恰在"6 伤 13 观 0 亡"的结构。→ 候选 protocol failure。

### 4.3 inconclusive 风险排序

1. **f009（环境零检出）——最高风险**：单一官方来源 + 政治敏感（PX 公众争议）+
   口径未定义，三条 inconclusive 触发条件占两条半。编码时已在 settlement_rule
   中显式写明降级路径。
2. **f005（疏散升级时序）**：时序因果单一媒体来源；若再核查发现疏散令早于
   609 起火，因子直接 rejected 而非 inconclusive——风险性质是"被证伪"而非"无证据"。
3. **f006（零蔓延）**：风险不在证据而在 sim 侧几何缺失。
4. 其余因子（f001/f002/f003/f004/f007/f008）均有官方报告直接锚值 + 推演指标
   直接对应，inconclusive 风险低。

---

## 5. 探针判决

### 判决：**需适配**（三档中的中档），不触发方向降级

**不是"直接可用"**：origin 枚举缺 historical_record、direction 缺指标载体、
settlement 缺百分位语言、brier/log_loss 数学上不可算、盲评无字段承载——
五处不动 fork 就无法正式运行。

**更不是"不可用"（kill 条件未触发）**，判据：
1. 9/9 因子完成编码，四种 event_relation 全部自然落地，无一条因 schema 结构
   性障碍失败；
2. 三态裁定、置信度 0-10、独立性要求、修订协议（rubric §3-§8）**零改动适用**；
3. 灾害域的核心差异（无单一终值、证据多口径）被"分布百分位∩锚区间"的
   settlement 语言消化，不需要推翻 schema 的数据模型，只需改字段语义；
4. 编码暴露的缺口（复燃状态机、罐区几何、伤亡分离）全是 **sim 侧**缺口，
   不是 ledger schema 的缺陷——它们限制的是 PolicySim 的可裁定因子范围，
   恰恰是 Factor Ledger 应该诊断出的东西（protocol_failures 机制设计正确）。

### fork 改动清单（最小集）

1. `origin` 枚举增加 `historical_record`，并在 rubric §7 增加其规则
   （必须声明锚值 tier；必须盲评）；
2. `direction` 约定收编：`increases_/decreases_<metric_key>`；
3. `settlement_rule` 收编百分位区间语言（supported/rejected/inconclusive 三态
   的分布-区间映射模板）；
4. `settlement_record.scores` 替换为 percentile_hit / interval_coverage /
   anchor_distance_iqr / baseline_difference（工程夹逼基线），brier/log_loss
   置 null 保留槽位（已落盘模板）；
5. `adjudicator` 增加 `blinded` / `outcome_visibility` 字段；
6. `match_id` 语义泛化为 event_id（键名可保留以兼容校验器）；
7. source_ledger 增加 reliability tier（official/media/eng/seed/derived）。

---

## 6. 对专家盲评协议的建议

### 6.1 人员与独立性

- **≥3 名专家**，建议构成：化工安全 1 + 消防战术 1 + 应急管理 1（可加仿真/建模 1 人
  处理 f002/f003 的工程闸门与分布判读）；
- 专家不得是因子作者（rubric §5 原样适用）；本次编码人（research-engineer）
  不进入 panel，只做证据包准备；
- 专家互盲（独立裁定后再允许讨论分歧项），逐因子记录 confidence_0_10。

### 6.2 隐去结局（灾害域特有，必须两轮）

灾害域因子从历史结局反推，若专家先见结局再评阈值，裁定退化为事后合理化。建议两轮：

- **Round 1（盲评阈值）**：给专家去标识化场景卡——"2015 年某沿海石化园区 PX 装置
  爆炸，4 个储罐燃烧"（隐去古雷/腾龙/漳州地名，隐去 56h、29096 人、0 死亡等
  终值）+ 9 条因子的 quantified_threshold/settlement_rule。专家只判断：
  阈值区间是否合理？settlement_rule 的三态映射是否可执行？
- **Round 2（揭盲裁定）**：给出完整锚值表（含来源 tier），专家按冻结的
  settlement_rule 裁定 supported/rejected/inconclusive，打 confidence_0_10。
- `adjudication_meta.outcome_visibility: hidden_until_threshold_review` 记入
  settlement_record。

### 6.3 匹配粒度（在本批因子上的具体定义）

粒度不能一刀切，按因子类型分三档：

- **anchor 类（f002 泡沫、f003 时间、f008 疏散率）**：粒度=**区间重叠**。
  历史锚区间与推演 [P25,P75] 重叠 ≥50% 判 supported。点值匹配禁止——
  泡沫 850 vs 1467 的口径差本身就说明点值无意义。
- **branch 类（f004 复燃、f005 疏散升级）**：粒度=**事件级**，非时间级。
  复燃裁定看次数与条件概率（3 次复燃、每罐率 0.67 ∈ [0.3,0.8]），
  时间对齐允许 **±12h 窗口**（609 起火 T+40.1h 类事件不苛求小时级复现）；
  疏散升级看"新增罐事件→升级决策"的因果响应比例（≥0.80），不看升级的具体时刻。
- **counter_signal 类（f003 反叙事、f007 伤亡、f009 环境）**：粒度=**分布形态级**。
  只判推演 P50 是否落在因子指定的窗口内（如 f003 P50∈[40,80]h），
  外加机制检验（f007 的反事实 ≥3× 对照）；不要求分布形状匹配。

统一口径规则：每条因子裁定前，专家须先确认"历史锚的口径"（首控/终控、
调运/消耗、伤/亡/留观）与推演统计量对齐——f003 的 21.7h vs 56.0h 已经证明，
**口径不对齐是灾害域 inconclusive 的第一来源**。

### 6.4 inconclusive 率政策

rubric §6 三档（<30% 正常 / 30–70% 监控逐条记录 / >70% 连续 5 事件触发设计评审）
原样沿用，"match" 读作 "event"。本批 9 条因子的预期 inconclusive 率
（f009 几乎确定、f005/f006 各约五成）≈ 11–33%，落在正常到监控的下沿——
如果实测远超此区间，说明 sim 侧缺口（复燃状态机、罐区几何）比评估更严重，
应优先补 sim 而非改 ledger。

---

## 7. 数据缺口清单（需后续补齐）

1. 3km 范围人口基数（f008 分母）——无任何一手来源；
2. 泡沫实际喷施消耗量 vs 调运量（f002；官方报告确认泡沫站远程控制失效、
   给水压力不足，喷施量可能显著低于 1467t）；
3. 疏散命令下达时刻及其与 609 起火的先后（f005 时序因果）；
4. 罐容 3×1万+1×2万 m³ 的官方文件确认（f002 工程下限的分母）；
5. 环境监测的指标、点位、检出限明细（f009 口径）；
6. sim 侧：初控-复燃两阶段状态机、罐区几何（1.5D）、casualty 伤/亡分离——
   三项均为 PolicySim 增强项，非 ledger 缺陷。
