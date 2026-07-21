# Mimo Goal 模式任务全景图

> **分析日期**：2026-06-13
> **基于**：项目现状 + task_queue + source-policy + 刚完成的 Goal A 经验

---

## 筛选标准

好的 Goal 任务有 4 个特征：
1. **停止条件可机器验证**（grep 通过、测试通过、文件存在、脚本 exit 0）
2. **不需要人类判断**（不需要区分"这算 Green 还是 Yellow Source"）
3. **边界明确**（改哪些文件、不改哪些文件）
4. **足够大**（值得 Goal 模式的自主循环，不值得手动一步步指导）

---

## 按优先级排列

### 🔴 高优先级（马上可以做）

#### Goal E：对手名称中文化

**为什么现在做**：Goal A 刚翻译了 trigger 模板，但对手名称还是英文（"输给 South Africa"）。
用户会看到"输给 South Africa → 出线危险"——半中半英，比全英文更别扭。

**停止条件**：
```
/goal site/data/cds-paths.json 中所有 qualification.scenarios[].trigger 里的
对手名称全部为中文（不含 "输给 [A-Z]" 这种模式），
championship.dominant_path_pattern 和 dominant_failure_node 中的对手名称也全部为中文，
python3 -m pytest tests/ -q 全部通过，
python3 scripts/build_site_data.py exit 0
```

**上下文**：
```
背景：Goal A 翻译了 trigger 模板（"输给 {team} → 出线危险"），
但 {team} 变量来自 team name，仍然是英文（如 "South Africa"）。
需要添加 team_name → 中文名映射。

中文名来源：data/processed/team_registry.csv 中应有中文名列，
或 data/processed/team_name_map.csv 中有映射。
如果都不存在，需要在 scripts/ 中新建映射。

需要翻译的位置：
1. qualification.py 中 scenario trigger 的对手名称
2. championship.py 中 dominant_path_pattern（如 "R32:Senegal → R16:Senegal"）
3. championship.py 中 dominant_failure_node（如 "Round Of 32 vs Senegal"）

约束：只改数据生成层，不改 site/js/。保持概率数字不变。
```

**预计时间**：20-30 分钟
**风险**：低。纯文本替换。

---

#### Goal F：公开数据禁词清洗

**为什么现在做**：交叉验证确认 baselines-data.js 的 description 字段含 ROI/PnL/Sharpe/仓位。
虽然 UI 不渲染，但数据文件是公开的。

**停止条件**：
```
/goal grep -rn "ROI\|PnL\|Sharpe\|仓位\|投注建议\|低估\|高估\|value bet" site/data/ 无命中，
python3 scripts/build_site_data.py exit 0，
python3 -m pytest tests/ -q 全部通过
```

**上下文**：
```
背景：site/data/baselines-data.js 的 description 字段包含 "ROI"、"PnL"、"Sharpe"、"仓位"。
虽然 UI 不渲染 description，但这些文件作为 <script> 标签加载到公开站点。

修复方式（二选一）：
a) 在 build_site_data.py 中删除公开 JSON 的 description 字段（如果前端不消费）
b) 在 build_site_data.py 中添加文本替换，将禁词替换为合规表述

约束：不改 site/js/。测试不能断 description 存在（如果选删除）。
```

**预计时间**：15-20 分钟
**风险**：极低。

---

#### Goal G：CSS 重复 media query 合并

**为什么现在做**：Trae 报告确认存在，纯技术债清理，无功能风险。

**停止条件**：
```
/goal site/css/portal.css 中只有一个 @media (max-width: 640px) 块
（grep -c "@media.*640px" site/css/portal.css 输出 1），
python3 -m http.server 启动后首页桌面端和移动端截图布局正常，
CSS 总行数减少
```

**上下文**：
```
背景：portal.css 有两个连续的 @media (max-width: 640px) 块（约 L1319 和 L1334 附近）。
需要将第二个块的内容合并到第一个中，删除第二个块的 @media 声明。

约束：只改 site/css/portal.css。不改变任何视觉行为——合并前后的渲染结果必须一致。
```

**预计时间**：10-15 分钟
**风险**：极低。纯合并，不改规则内容。

---

### 🟡 中优先级（可以做，但需人类先决定）

#### Goal H：Team Card 内容审计

**为什么适合 Goal**：48 张卡片，逐张检查。机械但量大。Goal 的独立验证者能防止"假装看了"。

**停止条件**：
```
/goal data/ops/candidate/full-48-audit-{日期}.csv 存在且非空，
包含全部 48 支球队的审计结果（team, has_green_source, obstacle_count,
placeholder_count, source_boundary_compliant 列），
data/ops/review_queue/full-48-audit-review-{日期}.md 存在且包含摘要统计
```

**上下文**：
```
审计 artifacts/team-cards/ 下全部 48 张球队卡片。
对每张卡片检查：
1. 是否有至少一个 Green Source 引用
2. obstacle 数量
3. placeholder 占位符数量（{{...}} 或 TODO）
4. source boundary 是否合规（无 Kimi/小米/MiMo 品牌泄露）

输出 CSV 到 data/ops/candidate/，审核报告到 data/ops/review_queue/。
只读操作，不修改任何文件。
```

**⚠️ 需要人类决定**：审计标准是否需要调整。

---

#### Goal I：Wiki 健康检查 + 修复

**为什么适合 Goal**：`scripts/audit.py` 已存在，结果可机器验证。

**停止条件**：
```
/goal python3 scripts/audit.py --root wiki/ 输出 issues 数组为空（或仅含已知的 P2 orphan 页面），
python3 scripts/verify.py --root wiki/ exit 0，
wiki/index.md 的最后修改时间为今天
```

**上下文**：
```
运行 scripts/audit.py 检查 wiki 健康状态。
修复发现的所有 P0/P1 问题（如缺少日期的批注、断链）。
P2 orphan 页面记录但不修（已知存在）。
在 wiki/index.md 添加今天的 memo 批注。
```

**⚠️ 需要人类决定**：wiki 修改需要 `APPROVE_FORMAL_MUTATION: wiki/`。

---

### 🟢 低优先级 / 长程

#### Goal J：Team Registry 重建提案（T005）

**停止条件**：
```
/goal data/ops/review_queue/ 中存在完整的 registry-rebuild formal-change-proposal，
包含：10 队移除列表、10 队新增列表、12 组重建对照表，
每个变更都有 Wikipedia 或 FIFA 来源标注，
proposal 通过 source_gap_scanner.py 的验证
```

**⚠️ 需要 `APPROVE_FORMAL_MUTATION`** 才能执行实际修改。

---

#### Goal K：Settlement 闭环验证

**停止条件**：
```
/goal A1 墨西哥 vs 南非 的 settlement_record 通过 schema 验证，
knowledge_update_log 和 protocol_failure_log 完整，
Brier 分数在合理范围 [0, 1]
```

---

## 执行建议

```
现在立刻跑（并行）：
  Goal E（对手名称中文）  ← 延续 Goal A 的翻译工作
  Goal F（禁词清洗）
  Goal G（CSS 合并）

人类审批后跑：
  Goal H（Team Card 审计）
  Goal I（Wiki 修复）

长程任务：
  Goal J（Registry 重建）  ← 等世界杯接近再推进
```

---

## 不适合 Goal 模式的任务

| 任务 | 为什么不适合 |
|------|------------|
| 来源分级判断（Green/Yellow/Red） | 需要人类判断"这个 Wikipedia 页面算不算 Green Source" |
| 赔率数据解读 | 涉及投注边界，source-policy 禁止 AI 自行判断 |
| Spec 设计 | 创意性工作，没有可机器验证的停止条件 |
| 首页文案优化 | 主观判断"这句中文通不通顺" |

---

## 新发现的 Goal

刚发现 Goal A 的翻译不完整——对手名称还是英文。建议作为 Goal E 立刻执行：

```
/goal site/data/cds-paths.json 中所有 trigger 里的对手名称全部为中文
（"输给 South Africa" → "输给 南非"），
dominant_path_pattern 和 dominant_failure_node 中的对手名称也全部为中文，
python3 -m pytest tests/ -q 全部通过，build_site_data.py exit 0

背景：Goal A 翻译了模板但没翻译 {team} 变量。对手名来自 team 字段，是英文。
需要添加 team_name → 中文名映射（可能在 team_registry.csv 或 team_name_map.csv 中）。
翻译位置：qualification.py 的 trigger、championship.py 的 dominant_path_pattern
和 dominant_failure_node。
约束：只改数据生成层。保持概率数字不变。
```
