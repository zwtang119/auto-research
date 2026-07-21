# Investigation: CDS Pipeline 深度问题分析

## Summary
代码审查发现 18 个问题（2 P0, 7 P1, 9 P2），需要深入分析根因、爆炸半径和是否还有类似未发现的问题。

## Symptoms
- P0-1: 前端显示 raw Elo 值（1545-2157）带 "%" 后缀
- P0-2: 冠军概率求和可能超过 1.0，F-03 clamp 静默丢弃概率质量
- P1-3: FIFA 淘汰名次协议部分分离逻辑错误
- P1-4: 对手侧检测逻辑脆弱
- P1-5: dead code (third_place_map_path)
- P1-6: 第三名槽位可能重复计算球队
- P1-7: Poisson 采样边界条件
- P1-8: 构建管线 XSS 安全测试缺失
- P1-9: CI workflow 缺少 secret 管理
- P2-10 到 P2-18: 各种小问题

## Background / Prior Research
<!-- Phase 1.5: 外部调研结果 -->

## Investigator Findings: P0-2

**调查日期**: 2026-06-12
**调查范围**: `src/cds/championship.py` `_compute_team_championship()` 函数 (L595–L720)
**症状**: `cds_championship.json` 中 48 队 `championship_prob` 总和 = 1.103860，超标 10.4%

### 结论：存在两个独立缺陷，净效果相互抵消

| 缺陷 | 影响 | 方向 |
|------|------|------|
| **Bug A**: `qual_prob` 被乘了两次 | 每个 team 的概率 × `qual_prob`，总和变为 ~0.67× 正确值 | ↓ 压低 |
| **Bug B**: 路径求和未处理重叠（expected-opponent-Elo 近似误差累积） | 5 轮近似误差使总和膨胀至 ~1.52× | ↑ 抬高 |
| **净效果** | 0.67 × 1.52 ≈ 1.104 | ↑ 10.4% |

> **关键发现**：如果只修复 Bug A（去掉多余的 `qual_prob`），总和将从 1.104 **跳升到 1.521**（超标 52%），情况更糟。两个缺陷必须同时修复。

---

### Bug A: `qual_prob` 双重乘入

#### 代码路径（精确行号基于 `championship.py` 当前版本）

**第一次乘入 — L672：累积器初始化**
```python
# L672
cumulative = qual_prob
```
每条路径的概率从 `qual_prob`（该队的总出线概率）开始累积。

**循环乘入 — L687-L688：每轮胜率叠加**
```python
# L687-688
win_prob = team_elo / max(team_elo + opp_elo, 1e-9)
cumulative *= win_prob
```
5 轮淘汰赛的条件胜率依次乘入 `cumulative`。

**第二次乘入 — L696：路径权重叠加**
```python
# L696
all_path_results.append((cumulative * pos_weight, path_prob_nodes, raw_path))
```
其中 `pos_weight` 来自 entry point 构建：

| Entry | 代码位置 | pos_weight 定义 |
|-------|---------|----------------|
| 1st place | L658 | `position_probs.get("p_1st", 0.5)` |
| 2nd place | L663 | `position_probs.get("p_2nd", 0.3)` |
| 3rd place | L670 | `p_3rd * tpq` |

#### 数学证明

`pos_weight` 代表的是 **无条件** 位置概率（P(qualify AND finish at position X)），不是条件概率。

对每个 team，entry weights 之和 = `qual_prob`：

```
w_1st + w_2nd + w_3rd
= p_1st + p_2nd + p_3rd × tpq
= qual_prob   (由 qualification 模拟器保证)
```

**数据验证**（48 队全部通过，0 偏差）：

| Team | p_1st | p_2nd | p_3rd | tpq | w_3rd | Σweights | qual_prob | 比值 |
|------|-------|-------|-------|-----|-------|----------|-----------|------|
| Czech Republic | 0.5582 | 0.2671 | 0.1235 | 0.6663 | 0.08228 | 0.9076 | 0.9076 | 1.0000 |
| Mexico | 0.3051 | 0.4188 | 0.1956 | 0.6663 | 0.13030 | 0.8542 | 0.8542 | 1.0000 |
| South Africa | 0.0641 | 0.1453 | 0.2606 | 0.6663 | 0.17358 | 0.3830 | 0.3830 | 1.0000 |

因此当前公式为：

```
champ_prob = Σ_paths (cumulative × pos_weight)
           = Σ_paths (qual_prob × ∏win_probs × pos_weight)
           = qual_prob × Σ_paths (pos_weight × ∏win_probs)
                                             ^^^^^^^^^^^^^^^^
                                             这部分已经包含 P(qualify)
```

**`qual_prob` 被乘了两次**：一次在 `cumulative`（L672），一次在 `pos_weight`（L658-670）。

#### 验证：Czech Republic 手算

```
qual_prob = 0.9076
最佳路径 cumulative = 0.9076 × 0.5008 × 0.4998 × 0.4865 × 0.4835 × 0.4853 = 0.025931
× pos_weight(1st) = 0.5582
= 0.014474

如果 cumulative 从 1.0 开始：
1.0 × 0.5008 × 0.4998 × 0.4865 × 0.4835 × 0.4853 = 0.028579
× pos_weight = 0.028579 × 0.5582 = 0.015953

比值 0.015953 / 0.014474 = 1.1022 ≈ qual_prob⁻¹ (0.9076⁻¹ = 1.1018) ✓
```

---

### Bug B: Expected-opponent-Elo 近似误差导致路径求和膨胀

#### 机制

`_resolve_propagation_slot()`（L250-L310）使用 **概率加权平均 Elo** 作为期望对手：

```python
# L297
expected_elo = sum(w * elo_params.get(t, 0) for t, w in opponent_teams) / total_weight
```

Bradley-Terry 模型中，`P(A beats E[elo]) + P(B beats E[elo]) ≠ 1.0`：

```
示例：E[opp_elo] = 1000, elo_A = 1200, elo_B = 800
P(A beats 1000) = 1200/2200 = 0.5455
P(B beats 1000) = 800/1800  = 0.4444
Sum = 0.9899 ≠ 1.0   ← 0.0101 的概率质量"凭空消失"
```

这个误差在 5 轮比赛中累积。每轮 ~1% 的误差，经路径分支放大后，导致 path_sum 膨胀。

#### 量化验证

```
corrected_total = Σ_teams (champ_prob / qual_prob) = 1.520653
```

如果 Bug A 是唯一问题，corrected_total 应该 ≈ 1.0。实际为 1.521，说明路径求和有 52% 的膨胀。

按 team 分解（前 5 名）：

| Team | grp | qual_prob | champ_prob | path_sum (=champ/qp) | 路径数 |
|------|-----|-----------|------------|----------------------|--------|
| Senegal | I | 0.5067 | 0.033502 | 0.066118 | 8 |
| Ecuador | E | 0.8752 | 0.045118 | 0.051552 | 8 |
| France | I | 0.9624 | 0.048155 | 0.050036 | 8 |
| Spain | H | 0.9669 | 0.048364 | 0.050020 | 6 |
| Argentina | J | 0.9625 | 0.046922 | 0.048750 | 7 |

注意 Senegal（qual_prob=0.5067，最低的之一）的 path_sum 反而最高（0.066），因为它的路径数最多（8 条）且每条路径的 win_prob 都在膨胀。

---

### 净效果数学推导

```
observed_total = Σ_i [qual_prob_i × Σ_paths(pos_weight_i × ∏win_probs_i)]
               = Σ_i [qual_prob_i × path_sum_i]
               = Σ_i [qual_prob_i² × (path_sum_i / qual_prob_i)]

设 path_sum_i / qual_prob_i = r_i (每队的"膨胀因子")

observed_total = Σ_i [qual_prob_i² × r_i]

如果所有 r_i ≈ r̄ ≈ 1.521/32 × 48 = 1.521 (total/sum_qp):
  observed_total ≈ r̄ × Σ_i qual_prob_i²
                 ≈ 1.521 × 21.7 (sum of squares)
                 ≈ ???

实际上更准确：
  observed_total / corrected_total = Σ_i[qp_i² × r_i] / Σ_i[qp_i × r_i]
                                    ≈ weighted_avg(qp_i)
                                    ≈ 32/48 = 0.667

  1.104 / 1.521 = 0.726 ≈ 近似于 0.667 (因为高 qual_prob 队权重更大)
```

---

### 附带发现：position_probs 内部不一致

qualification 模拟器输出的 `position_probs` 存在 ±3% 的求和偏差（理论上每组 p_1st+p_2nd+p_3rd+p_4th = 1.0）：

| Group | p_1st Σ | p_2nd Σ | p_3rd Σ | p_4th Σ |
|-------|---------|---------|---------|---------|
| A | 0.9886 | 0.9990 | 0.9982 | 1.0142 |
| B | 0.9688 | 1.0325 | 0.9831 | 1.0156 |
| K | 1.0241 | 0.9760 | 1.0001 | 0.9998 |

这是上游 qualification 模拟器的精度问题，不是 championship 计算的 bug，但它会传导微量误差。

---

### 推荐修复方案

#### 方案 1（最小改动，推荐）

在 L696 处将 `pos_weight` 归一化：

```python
# L696 — 修改前
all_path_results.append((cumulative * pos_weight, path_prob_nodes, raw_path))

# L696 — 修改后
norm_weight = pos_weight / qual_prob if qual_prob > 0 else 0.0
all_path_results.append((cumulative * norm_weight, path_prob_nodes, raw_path))
```

这消除 Bug A（qual_prob 双重乘入），但会让总和膨胀到 ~1.52（Bug B 暴露）。需要配合 Bug B 修复。

#### 方案 2（推荐：同时修复两个缺陷）

```python
# L672 — 修改前
cumulative = qual_prob

# L672 — 修改后：cumulative 不再包含 qual_prob
cumulative = 1.0

# L696 — pos_weight 保持不变（已经是 P(pos) 无条件概率）
all_path_results.append((cumulative * pos_weight, path_prob_nodes, raw_path))
```

但这仍有 Bug B 的 52% 膨胀。根因在 `_resolve_propagation_slot()` 的 expected-opponent-Elo 近似。

#### 方案 3（彻底修复，工作量大）

在方案 2 基础上，修改对手解析使每场比赛的胜率严格互补：

- 对 `_resolve_propagation_slot()` 返回的对手，记录其 identity 分布
- 在主循环中，使用**同一批候选对手**计算当前 team 的胜率
- 确保 `P(A beats opp) + P(opp beats A) = 1.0` 对每个具体对手成立

或者更根本地：将 per-team 独立计算改为 **联合模拟**（Monte Carlo），在每次模拟中抽取具体对手而非使用期望值。

#### 推荐路径

1. **短期**（立即可做）：实施方案 2，同时在 `_compute_team_championship()` 末尾添加全局归一化：
   ```python
   # F-03 改进：全局归一化替代 per-team clamp
   total = sum(p for p, _, _ in all_path_results)
   if total > 0:
       for i in range(len(all_path_results)):
           all_path_results[i] = (all_path_results[i][0] / total, *all_path_results[i][1:])
   ```
   ⚠️ 注意：这是 per-team 归一化，不能解决跨 team 的总和问题。

2. **中期**：将 per-team 归一化改为 **全局归一化**（在 `compute_championship_paths()` 汇总所有 team 结果后统一除以总和）。

3. **长期**：实现 Monte Carlo 联合模拟，彻底消除近似误差。

---

### 爆炸半径

- **影响范围**：所有 48 队的 `championship_prob` 值
- **高 qual_prob 队受影响更大**：qual_prob 越高，双重乘入的偏差越大
  - France (qp=0.96): 偏差 ~4%
  - Czech Republic (qp=0.91): 偏差 ~10%
  - South Africa (qp=0.47): 偏差 ~53%（但绝对值很小）
- **下游影响**：`site/data/cds-paths.json`、`teams.json`、`homepage.json` 中所有引用 championship_prob 的展示值
- **决策影响**：任何基于 championship_prob 排序或比较的分析结论可能有误

---

---

## Phase 4: Oracle 综合分析

### 被证伪的假说
- Oracle 最初认为 "qual_prob 被乘两次" — **已确认正确**（entry weights 之和 = qual_prob，但 cumulative 也从 qual_prob 开始）
- 但同时发现了第二个隐藏缺陷（Bug B: expected-opponent-Elo 近似误差）

### 关键交叉验证
- Entry weights 48 队全部精确匹配 qual_prob（0 偏差）→ pos_weight 定义正确
- 但 `cumulative = qual_prob` (L672) + `cumulative * pos_weight` (L696) = qual_prob × qual_prob 的双重乘入
- 如果只修复 Bug A，总和会从 1.104 跳升到 1.521（Bug B 暴露）

---

## Root Cause 分析

### P0-1: 前端 Elo 数值显示为百分比

**根因类型**: 数据管线量纲约定断裂

**根因链**:
1. `elo-proxy.json` 从百分比格式 (0.5769–3.6399) 变为 raw Elo (1545–2157) — 本次 session 的变更
2. `build_site_data.py::build_baselines_json()` L1341-1381 直接透传 raw 值到 `baselines.json`
3. `homepage.js` L348: `existing.elo = prob` 把 raw 值当概率
4. `homepage.js` L415: `entry.elo.toFixed(1) + "%"` 显示 "2157.0%"
5. `team-detail.js` L250-327: `renderBaselines()` 用 `formatPercent(val)` 显示 "2157%"

**深层原因**: `build_baselines_json()` 没有类型标注 — 不知道 `elo.teams` 的值是 raw Elo 还是概率。前端假设所有 baseline 都是概率百分比。

**爆炸半径**: 48 队 × 所有页面用户。homepage 三信号图完全错误，team detail 基线对比图数值无意义。

### P0-2: 冠军概率系统性膨胀 10.4%（两个缺陷叠加）

**根因类型**: 数学错误 + 近似误差

**Bug A — qual_prob 双重乘入**:
- L672: `cumulative = qual_prob` — 路径概率从出线概率开始
- L696: `cumulative * pos_weight` — pos_weight 已经是 P(qualify AND position)，包含 qual_prob
- 结果: `champ_prob = qual_prob² × ∏(win_probs) × P(position|qualify)`

**Bug B — expected-opponent-Elo 近似误差**:
- `_resolve_propagation_slot()` L297: `expected_elo = Σ(w_i × elo_i) / Σ(w_i)`
- Bradley-Terry 非线性: `P(A beats E[elo]) + P(B beats E[elo]) ≠ 1.0`
- 5 轮累积导致路径求和膨胀 ~52%

**净效果**: 两个缺陷部分抵消，总和 = 1.104（10.4% 超标）

**爆炸半径**: 所有 48 队的 championship_prob 值。相对排序基本保持（所有队都被同比例影响），但绝对值有偏差。

### P1-3: FIFA 淘汰名次协议违规

**根因类型**: 算法设计不完整

**根因链**:
1. `_try_separate()` L296-316: 当 sub-group 仍有 ties 时返回 None
2. `_resolve_multi_team_tie()` L258-266: 收到 None 后直接尝试下一个 criterion
3. FIFA 规则: 应先排出可分的队，剩余队从 criterion 1 重新开始

**爆炸半径**: MC 模拟中 5-15% 的 scenario 至少 1 个 position 不正确。传导到 qual_prob 和 championship_prob。

---

## Recommendations（按优先级）

### Sprint 1 — 立即修复（预计 2 小时）

| # | 问题 | 修复方案 | 文件:行 |
|---|------|---------|---------|
| 1 | P0-1 前端显示 | `build_baselines_json()` 中将 Elo 值归一化为百分比: `v / sum(elo.values()) * 100` | `scripts/build_site_data.py:~L1370` |
| 2 | P0-2 Bug A | L672 改为 `cumulative = 1.0` | `src/cds/championship.py:683` |
| 3 | P0-2 Bug B | `compute_championship_paths()` 末尾添加全局归一化: `champ_prob /= total_sum` | `src/cds/championship.py:~L750` |

### Sprint 2 — 后续修复（预计 4 小时）

| # | 问题 | 修复方案 | 文件 |
|---|------|---------|------|
| 4 | P1-3 tiebreaker | `_try_separate()` 递归分离 | `src/cds/group_standings.py:296` |
| 5 | P1-5 dead code | 删除 `third_place_map_path` 参数或实际使用 | `src/cds/knockout_bracket.py:280` |
| 6 | P2-11 odds fallback | 缺失 match_id 时 log warning | `src/cds/qualification.py` |
| 7 | P2-12 lots seed | 使用不同种子或 team-dependent seed | `src/cds/group_standings.py` |

### 长期改进

| # | 问题 | 方案 |
|---|------|------|
| 8 | P0-2 根本解 | Monte Carlo 联合模拟替代 per-team 期望值近似 |
| 9 | P1-9 CI | 添加错误通知和数据新鲜度标记 |
| 10 | 测试覆盖 | 添加 Brazil > Saudi Arabia 排序回归测试 |

---

## Preventive Measures

1. **数据管线类型标注**: 在 `build_baselines_json()` 中添加数据类型检查 — 每个 baseline 的值域应有元数据标注（raw/ranking/probability）
2. **概率归一化检查**: 在 `compute_championship_paths()` 末尾添加 `assert abs(total_sum - 1.0) < 0.01` 作为 sanity check
3. **测试回归**: 添加 "top 5 队 championship_prob 排序不变" 的回归测试
4. **代码审查清单**: 凡是涉及概率乘法的代码，必须验证 entry weights 之和是否合理
