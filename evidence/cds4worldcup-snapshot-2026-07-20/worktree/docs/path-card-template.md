# Championship Path Simulation Card Template

> **用途**: CDS4WorldCup2026 MVP-A1 48 队薄切片夺冠路径推演卡模板；也可扩展为 4 队深描质检卡。
> **原则**: 不问“这队会不会夺冠”，而问“如果它夺冠，世界必须怎样变化”。
> **分类约束**: MVP-A1 阶段不固定最终 `path_type`；只记录 `path_signals` 和 `path_type_status`，等待 MVP-A2 数据派生分类。

---

## 1. Team Profile

```yaml
team:
team_slug:
confederation:
group:
tier: unassigned
tier_status: pending_data_gate
path_type: unassigned
path_type_status: unassigned
path_signals:
  -
source_status:
  green_sources:
  yellow_sources:
  red_sources:
  coverage: sufficient / partial / thin / missing
```

简述球队当前基本面、公开强弱定位和本卡使用的数据来源。数据不足时直接标注 `thin` / `missing`，不要靠叙事补齐。

## 2. Championship Thesis

一句话说明该队夺冠故事：

> 如果 `<team>` 夺冠，最可能是因为 `<核心路径逻辑>`，并且 `<关键阻力>` 被 `<机制>` 破解。

## 3. Primary Obstacles

列出 3-7 个最大阻力。

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
|  |  |  |  |

类型可选：

- `base_strength_gap`
- `bracket_strength`
- `squad_depth`
- `injury_risk`
- `travel_fatigue`
- `tactical_mismatch`
- `psychological_pressure`
- `low_scoring_dependency`
- `penalty_dependency`
- `favorite_collision`

## 4. Required Breakthroughs

列出该队若要夺冠必须完成的突破。

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
|  |  |  |  |

## 5. Black Swan Helpers

列出该队需要或高度受益的黑天鹅助力。

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| 热门队伤病 | 降低半区强度 | 是 |  |
| 红牌 / VAR | 单场方差放大 | 是 |  |
| 点球大战聚集 | 把实力差距转为心理/门将优势 | 是 |  |
| 天气 / 场地异常 | 放大环境适应差异 | 是 |  |

## 6. Miracle Package

最小奇迹包：该队夺冠至少需要哪些条件同时成立？

```yaml
minimum_conditions_count:
conditions:
  - condition:
    type:
    observable_proxy:
    settlement_rule:
```

## 7. Path Simulation Notes

记录 Markov / Monte Carlo 路径层输出。MVP-A1 阶段可以为空或标记 `not_run_yet`。

```yaml
simulation_status: not_run_yet
championship_path_count:
dominant_path_pattern:
dominant_failure_node:
bracket_dependency:
black_swan_dependency:
penalty_dependency:
injury_sensitivity:
```

## 8. Factor Ledger Candidates

只放可判定候选因子。

| factor_id | factor_name | relation | observable_proxy | settlement_rule | source |
|---|---|---|---|---|---|
|  |  | precursor / inhibitor / branch / counter_signal |  |  |  |

## 9. Marginalia Notes

保留不可判定但有语义价值的内容。

```markdown
> [!memo] YYYY-MM-DD <note>
>
> 来源：
> 上下文：
> 不进入 Factor Ledger 的原因：
```

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
|  | pre-tournament | 初始版本 |  |

## 11. Current Interpretation

用 2-4 段自然语言总结：

- 这队夺冠的最可信路径。
- 最不可信的叙事。
- 最值得赛中监控的 3 个信号。
- 如果该队最终夺冠，哪些赛前判断会被证明有价值。
