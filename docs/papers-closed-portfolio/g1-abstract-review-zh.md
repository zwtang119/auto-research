# G1 — PA-Degrades-Fidelity 摘要 — 6 人评审

> 生成于 2026-07-05T02:08:48Z by `/tmp/run_g1_review.py`。  
> **通过条件（G1）**：R1 + R3 ≥ 5.5 in 5 人评审  
> 5 个 Paratera 评审 + 1 个 minimaxi.com 交叉验证（PIT-107 satisfied）

## 1. 评审组

| # | 角色 | 提供方 | 模型 ID | 分数 | 绑定弱点 |
|---|---------|----------|----------|-------|------------------|
| R1 | R1 实验主义者（方法学严谨） | paratera | `deepseek-v4-pro` | 4.0 | 主观保真度 inter-judge agreement 接近随机（ρ=0.19），破坏了核心效应的可靠性以及「4 judge 复现能排除 judge-specific artifact」的声称。 |
| R2 | R2 理论家（概念贡献） | paratera | `kimi-k2.5` | 5.0 | 反方向效应有趣但「结构化推理有 trade-offs」理论新颖度有限；标签泄露偏差是方法修正而非理论贡献。 |
| R3 | R3 应用（实际有用性） | paratera | `MiniMax-M3` | 单一石化场景限制了部署的可推广性，且标签盲 judge 对照增加了成本，对大多数团队没有明确的 ROI。 |
| R4 | R4 怀疑论者（假阳性猎手） | paratera | `deepseek-v4-flash` | 2.0 | 主观保真度接近随机的 inter-judge agreement（ρ=0.19）使 t-test 无效；显著结果可能是 artifact。 |
| R5 | R5 系统（工程质量） | paratera | `qwen3.5-122b-a10b` | 6.0 | state progress.json 引用缺少 version hash，相较证据表其它位置提供的显式 experiment log path，降低了长期可复现性。 |
| R6 | R6 交叉验证（R6 新增：minimaxi.com MiniMax-M3，独立提供方） | minimaxi | `MiniMax-M3` | 5.0 | 「约 0.4 分」放大声称无法直接从引用的 Cliff's δ 值推导；27% DeepSeek 解析失败与未处理的差异性 attrition 威胁反方向发现。 |

## 2. 汇总

- 中位：**4.5**
- 平均：4.33
- 最大：6.0（anti-inflation 上限 ≤ 7.0）

## 3. G1 gate 判定

- R1（实验主义者）分数：**4.0**（G1 阈值：≥ 5.5）
- R3（应用）分数：**4.0**（G1 阈值：≥ 5.5）

### **G1 FAILED** — 放弃作为独立；保留为 P11 workshop 支柱

R1=4.0，R3=4.0 —— 至少一个 < 5.5。Per first-principles §87：「如失败则放弃作为独立；保留为 P11 workshop 支柱」。PA-degrades-fidelity 发现将并入 P11 workshop 论文（per investigation Rank 3，14 天硬截止）而非作为顶刊摘要提交。

## 4. R6 交叉验证注记（NEW 模式）

R6（minimaxi.com MiniMax-M3，独立提供方）评 5.0。Paratera 中位 4.0；R6 偏差 +1.0。R6 偏差 ≥ 1.0 表明跨提供方偏差信号，与先前的观察一致（joint outline 评审：R6=4.0, R3=3.0；+1.0 偏差）。

## 5. 详细绑定弱点（每位评审一条）

- **R1 实验主义者**（`deepseek-v4-pro`，分 4.0）：主观保真度 inter-judge agreement 接近随机（ρ=0.19），破坏了核心效应的可靠性以及「4 judge 复现能排除 judge-specific artifact」的声称。
- **R2 理论家**（`kimi-k2.5`，分 5.0）：反方向效应有趣但「结构化推理有 trade-offs」理论新颖度有限；标签泄露偏差是方法修正而非理论贡献。
- **R3 应用**（`MiniMax-M3`，分 4.0）：单一石化场景限制了部署的可推广性，且标签盲 judge 对照增加了成本，对大多数团队没有明确的 ROI。
- **R4 怀疑论者**（`deepseek-v4-flash`，分 2.0）：主观保真度接近随机的 inter-judge agreement（ρ=0.19）使 t-test 无效；显著结果可能是 artifact。
- **R5 系统**（`qwen3.5-122b-a10b`，分 6.0）：state progress.json 引用缺少 version hash，相较证据表其它位置提供的显式 experiment log path，降低了长期可复现性。
- **R6 交叉验证**（minimaxi.com `MiniMax-M3`，分 5.0）：「约 0.4 分」放大声称无法直接从引用的 Cliff's δ 值推导；27% DeepSeek 解析失败与未处理的差异性 attrition 威胁反方向发现。

---

## 6. R7 交叉验证（OpenRouter gpt-oss-120b，2026-07-05）

R7（OpenRouter gpt-oss-120b，第 4 个独立提供方）评 **4.0**：「发现基于单一场景且 inter-judge agreement 低，限制了对更广适用性的信心。」

7 人评审重新汇总：[4.0, 5.0, 4.0, 2.0, 6.0, 5.0, 4.0]，中位 4.0，平均 4.29。

跨提供方偏差表：

| 提供方 | 模型 | 分数 | vs Paratera 中位（4.0） |
|----------|-------|-------|--------------------------|
| paratera | deepseek-v4-pro (R1) | 4.0 | 0.0 |
| paratera | kimi-k2.5 (R2) | 5.0 | +1.0 |
| paratera | MiniMax-M3 (R3) | 4.0 | 0.0 |
| paratera | deepseek-v4-flash (R4) | 2.0 | -2.0 |
| paratera | qwen3.5-122b-a10b (R5) | 6.0 | +2.0 |
| minimaxi | MiniMax-M3 (R6) | 5.0 | **+1.0** |
| openrouter | gpt-oss-120b (R7) | 4.0 | 0.0 |

**G1 在 7 人评审重新汇总下仍 FAILED**（R1=4, R3=4 均 < 5.5；R7=4）。Per first-principles §87：放弃作为独立；保留为 P11 workshop 支柱。

**跨提供方模式**：3 个 OpenRouter 独立模型 ID（R3 paratera MiniMax-M3 / R6 minimaxi MiniMax-M3 / R7 openrouter gpt-oss-120b）在「同一任务」上给出 3 个不同分数——确认 joint outline 与 G1 评审中观察到的跨提供方 review-bias 信号。同一个 model_id（MiniMax-M3）在不同提供方（paratera vs minimaxi）下给出 4.0 vs 5.0；不同 model_id 在同一任务上给出 2.0-6.0 跨度。Review-bias 单位是提供方 + model_id 组合，而非单独的 model_id。
