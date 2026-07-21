# Championship Path Simulation Card: 波斯尼亚和黑塞哥维那 (Bosnia and Herzegovina)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `bosnia-and-herzegovina`

## 1. Team Profile

```yaml
team: 波斯尼亚和黑塞哥维那 (Bosnia and Herzegovina)
team_slug: bosnia-and-herzegovina
confederation: UEFA
group: B
tier: unassigned
tier_status: pending_data_gate
path_type: unassigned
path_type_status: unassigned
kimi_baseline_signals:
  - none_yet
source_status:
  green_sources: [public-football-knowledge]
  yellow_sources: []
  red_sources: []
  coverage: thin
```

波黑通过欧预赛附加赛获得 2026 世界杯参赛资格。这支球队处于黄金一代老去和新老交替的过渡期，2014 年世界杯是首次参赛经验（小组出局）。埃丁·哲科（Edin Džeko）虽然年事已高但仍是精神领袖和关键得分点。球队整体以身体对抗和直接进攻风格为主，技术精细度有限。B 组同组加拿大、卡塔尔、瑞士，瑞士是最大威胁，与加拿大争夺第二是现实目标。

## 2. Championship Thesis

> 如果波黑夺冠，最可能是因为哲科在最后一届世界杯中爆发了超越年龄的传奇表现（类似 2018 莫德里奇的壮举），球队的身体对抗优势在淘汰赛中将技术型对手拖入泥潭，且 B 组低消耗出线为淘汰赛储备了体能——用纯粹的意志力和身体优势完成了世界杯历史上最不可思议的奇迹之一。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 与世界级球队的硬实力差距 | base_strength_gap | 除少数球员外缺乏欧洲顶级联赛主力，整体实力有天花板 | vs 顶级对手的控球率和射门比 |
| 黄金一代老去，新生代未成长 | squad_depth | 哲科等核心球员年龄偏大，替补水平明显低于首发 | 核心球员的体能和替补上场后的场面 |
| 进攻创造力严重不足 | low_scoring_dependency | 进攻过于依赖哲科的终结和定位球，缺乏运动战创造力 | 场均 xG 和关键传球数 |
| 缺乏大赛淘汰赛经验 | psychological_pressure | 2014 小组出局是仅有的世界杯经验，淘汰赛经验为零 | 淘汰赛首场表现 |
| 防守端面对速度型攻击的脆弱性 | tactical_mismatch | 后防线速度不足，面对快速反击时可能暴露 | vs 速度型球队的失球数 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| B 组成功出线 | 小组赛 | 积分 ≥4 出线 | 小组未出线 |
| 哲科或替代者保持进球效率 | 小组赛 | 中锋位置小组赛进球 ≥2 | 中锋 0 球 |
| 防守纪律性验证 | 全赛程 | 场均失球 ≤1 | 场均失球 ≥2 |
| 新生代球员站出来 | 全赛程 | 至少 1 名 U25 球员进球或助攻 ≥2 | 新生代球员无贡献 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| 哲科传奇级最后一舞 | 老将在最后一届大赛中超常发挥的历史先例存在 | 是 | 哲科赛前进球率 |
| B 组瑞士以外对手相对可控 | 加拿大和卡塔尔提供拿分机会 | 是 | B 组积分分布 |
| 定位球在淘汰赛成为武器 | 波黑的身体优势在定位球中可能最大化 | 是 | 定位球进球占比 |
| 半区有利抽签 | 避免淘汰赛早期遭遇顶级对手 | 是 | 淘汰赛对阵表 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 4
conditions:
  - condition: B 组成功出线
    type: precursor
    observable_proxy: B 组积分
    settlement_rule: 积分 ≥4 出线
  - condition: 哲科或替代中锋淘汰赛进球 ≥2
    type: precursor
    observable_proxy: 中锋淘汰赛进球数
    settlement_rule: 淘汰赛进球 ≥2
  - condition: 防守端淘汰赛场均失球 ≤1
    type: precursor
    observable_proxy: 淘汰赛失球数
    settlement_rule: 淘汰赛场均失球 ≤1
  - condition: 半决赛前避免遭遇法国或阿根廷
    type: branch
    observable_proxy: 淘汰赛对阵表
    settlement_rule: 半决赛前不与法/阿交手
```

## 7. Path Simulation Notes

```yaml
simulation_status: not_run_yet
championship_path_count: null
dominant_path_pattern: null
dominant_failure_node: null
bracket_dependency: null
black_swan_dependency: null
penalty_dependency: null
injury_sensitivity: null
```

## 8. Factor Ledger Candidates

| factor_id | factor_name | relation | observable_proxy | settlement_rule | source |
|---|---|---|---|---|---|
| bih-physicality | 身体对抗强度 | precursor | 对抗成功率和定位球获得数 | 对抗成功率 ≥55% | public-football-knowledge |
| bih-dzeko-output | 哲科终结效率 | precursor | 哲科每 90 分钟进球数 | 小组赛+淘汰赛进球 ≥3 | public-football-knowledge |

## 9. Marginalia Notes

> [!memo] 2026-06-13 波黑数据覆盖较薄。哲科的年龄（40 岁）使他成为本届赛事可能年龄最大的参赛球员之一，这本身就是一个独特变量。新老交替的困境是结构性问题。
>
> 来源：公开足球知识
> 上下文：B 组分析
> 不进入 Factor Ledger 的原因：数据点有限，哲科年龄因素需赛中验证

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-12 | pre-tournament | 初始薄切片版本（Wikipedia draw 数据校正） | WI-0.2 |
| 2026-06-13 | pre-tournament | 深描版本：填充 §1-§6, §8, §11 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: 以 B 组第二或最佳第三名出线（与加拿大竞争，击败卡塔尔是必须完成的任务），16 强赛面对非顶级对手时依靠身体对抗和定位球。哲科的个人能力和经验在这一阶段可能制造惊喜。如果能进入 1/8 决赛，这已是波黑在世界杯上的历史性突破。

**最不可信叙事**: "波黑的身体对抗可以碾压一切技术型对手"——身体优势是真实的但在现代足球中不足以弥补技术、战术和个体能力的系统性差距。

**最值得赛中监控的信号**: (1) B 组 vs 瑞士和加拿大的场面数据；(2) 哲科的体能和进球产出；(3) 新生代球员的表现——如果 U25 球员站出来，波黑的竞争力将显著提升。

**如果夺冠，哪些赛前判断有价值**: (1) 哲科是本届赛事中年龄与影响力的最大变量——如果他在最后一届世界杯中超常发挥，这将是世界杯历史上最动人的故事之一；(2) B 组签运对波黑而言是相对有利的，与加拿大争夺第二的窗口存在；(3) 定位球和身体对抗在淘汰赛僵局中可能比预期更有效。
