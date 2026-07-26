# Memo：CDS 引擎 bracket 编码有效性核验（2026-07-26）

> 执行：分析副本任务（MANIFEST 三级结构第三级）｜ 输入：证据快照内 `ef30658` 版 `cds_championship.json`（bundle 提取语义）+ 封存仓库 `923e23a` 已结算 `schedule.json` ｜ 输出：本 memo + 对照表（复算脚本见文末）

## 1. 问题

路径空间引擎（P3）的 bracket 编码（半区约束、KO slot 分配）是否结构正确？用户直觉："西班牙与法国同半区不可能决赛相遇"——核验引擎是否也如此编码，以及路径级预测的可靠性边界。

## 2. 结构核验：编码正确，占用预测不可靠

**(i) 半区约束编码正确**。两个实际半决赛对阵都出现在引擎优势路径结构中，且均从**被淘汰方**视角命中：

- France 优势路径：`…→ SF:Spain → Final:England`——实际半决赛正是 西班牙 2–0 法国 ✓
- England 优势路径：`…→ QF:Norway → SF:Argentina → Final:France`——实际 QF 挪威 1–2 英格兰 ✓、SF 阿根廷 2–1 英格兰 ✓（QF/SF 双命中）

**(ii) slot 占用错误 ≠ 编码错误**。France 的 QF 预测对手为 Netherlands，实际为 Morocco——但 Morocco 正是从 Netherlands 的 R32 slot 中胜出（KO76 荷兰 1–1 摩洛哥后晋级）。即：**slot 结构对，slot 里的队填错了**。同类：Spain R32 对手命中（Austria ✓），Ecuador/Norway 的互预测配对则完全未发生。

**(iii) 路径级预测不可靠（定量）**。R32 对手命中率 **5/32（15.6%）**；引擎 top-8 热门的优势路径在 R16 之后几乎全部失真（详见 §3 对照表）。引擎模态决赛预测为"英格兰 vs 法国"，实际为"西班牙 vs 阿根廷"——**任何"预测了决赛对阵"的表述都是错误的，论文禁用**。

**(iv) 数据注意**。点球大战胜场在 score 字段记为平局（KO74 德国 1–1 巴拉圭、KO76 荷兰 1–1 摩洛哥，负方实际出局）——路径对账时已人工确认晋级方；下游分析若按比分直读会误判。

## 3. 引擎 top-8 预测路径 vs 实际路径

| 队（引擎排名/概率） | R32 | R16 | QF | SF | F |
|---|---|---|---|---|---|
| Spain #1 0.0484 | Austria ✓ | ✗ Portugal | ✗ Belgium | ✗ France | ✗ Argentina |
| France #2 0.0482 | ✗ Sweden | ✗ Paraguay | ✗ Morocco | **Spain ✓** | ✗ Argentina |
| Argentina #3 0.0469 | ✗ Cape Verde | ✗ Egypt | ✗ Switzerland | ✗ England | ✗ Spain |
| Ecuador #4 0.0451 | ✗ Mexico（出局） | — | — | — | — |
| Norway #5 0.0429 | ✗ Côte d'Ivoire | ✗ Brazil | ✗ England（QF 出局） | — | — |
| Germany #6 0.0423 | ✗ Paraguay（出局） | — | — | — | — |
| Netherlands #7 0.0415 | ✗ Morocco（出局） | — | — | — | — |
| Brazil #8 0.0388 | ✗ Japan | Norway ✓（出局） | — | — | — |

（单元格 = 实际对手；✓ = 预测对手命中。"—" = 未进入该轮。England 虽非引擎 top-8，但其路径 QF:Norway ✓ + SF:Argentina ✓ 为全场最佳双命中，见 §2(i)。）

## 4. 对 Paper A 的含义（§5.2 / H3 素材）

1. **rank-vs-mass 分裂的结构性解释**：分裂不是 bracket 编码错误（编码经核验正确），而是**节点概率分配错误**——引擎给多数 KO 对阵的条件胜率接近 0.50（例：Czech vs Senegal win_prob 0.50），导致质量沿路径树近均匀扩散。这与 n=46 过度分散发现（93.5% 质量压出局队）机制一致，且给出了机制层解释：**bracket 约束收紧了"谁可能遇见谁"，但 0.5 化的节点概率放弃了"谁更可能赢"**。
2. **可用表述（安全）**："引擎的 bracket 编码经事后核验结构正确（两个半决赛对阵在其路径结构中可达），但路径级预测不可靠（R32 对手命中率 15.6%）——结构约束与概率分配的可靠性必须分开评估。"
3. **禁用表述**："预测了决赛/半决赛对阵"（模态决赛错误）；将半区规则知识作为命中证据（编码正确是建模义务，不是预测技能）。
4. **建议落位**：H3 的"枚举式路径模型的结构失败模式"案例增加本 memo 作为机制注脚；PIV `schema_status` 与本发现无联动（编码正确），联动点在 `path_nodes` 概率分配层。

## 5. 复算入口

输入版本：`ef30658:data/processed/cds_championship.json`（预测）+ `923e23a:data/processed/schedule.json`（实际，Green Source Wikipedia 已核验）。对照脚本逻辑：逐队提取 `path_nodes` 的 round→opponent 映射，与 schedule.json `knockout_stage` 已赛场次逐轮比对；命中判定 = 预测对手 == 实际对手（不比较比分）。本 memo 全部数字可由该逻辑一键复算（G2 闸门适用）。

## CHANGELOG

- 2026-07-26：建 memo；核验 bracket 编码（§2）；生成 top-8 对照表（§3）；R32 命中率 5/32；登记点球比分字段注意事项。
