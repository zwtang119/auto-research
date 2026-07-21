# Investigation: Kimi Agent Reason 数据丢失 — 根因分析与连锁影响

> **日期**: 2026-06-11
> **状态**: ✅ 已修复并验证

## Summary

`generate_path_cards.py` 的 `group_kimi_by_team()` 用 CSV champion 列的中文队名（"阿根廷"）作为字典 key，但查找时用英文名（"Argentina"），导致 21 队 §9 Marginalia 全部为空，300 条 Kimi agent reason 全部丢失。聚合概率不受影响（独立的查找路径）。两个 path signal 类型成为死代码。另有一处潜在的 f-string bug。

## Symptoms

- 所有 21 队路径卡的 §9 Marginalia 显示"无 Kimi agent 预测数据"
- 西班牙（62 票 Kimi 预测）、阿根廷（55 票）、法国、巴西、德国等强队也不例外
- §2 正确引用 Kimi 聚合概率（如 "Kimi 聚合概率: 23.82%（62 票）"），但 §9 没有 agent reason 摘要
- `kimi_baseline_signals_matrix.csv` 中 `broad_faction_support` 和 `cross_faction_consensus` 信号从未出现

## Root Cause

**直接原因**：`scripts/generate_path_cards.py` 中两处代码使用了不同的队名语言。

```
L46-49: group_kimi_by_team() 按 CSV champion 列分组
         → 字典 key = 中文名（"西班牙"、"阿根廷"、"法国"...）

L78:     kimi_by_team.get(en, [])
         → en = team["en_name"] = 英文名（"Spain"、"Argentina"、"France"）
         → 永远匹配不上 → kimi_agents = []
```

**证据**：

| 查找方式 | "阿根廷" key 的 agent 数 | "Argentina" key 的 agent 数 |
|----------|------------------------|---------------------------|
| 中文 key | 55 条 | N/A |
| 英文 key | N/A | 0 条 |
| 西班牙/Spain | 62 条 / 0 条 | |

**为何聚合概率没受影响**：

L55-63 `get_team_aggregation()` 同时检查 `team_zh` 和 `team_en`，所以 `kimi_prob` 和 `kimi_votes` 正常工作。两条数据路径使用了不同的查找逻辑。

## Blast Radius

### 直接受影响

| # | 产出 | 影响 | 严重度 |
|---|------|------|--------|
| 1 | 21 队 §9 Marginalia | 300 条 agent reason 全部丢失，显示为"无 Kimi agent 预测数据" | 🔴 高 |
| 2 | `broad_faction_support` signal | 死代码：`len(kimi_agents) > 20` 永远为 False（实际 0） | 🟡 中 |
| 3 | `cross_faction_consensus` signal | 死代码：`len(factions_seen) >= 5` 永远为 False（空 set） | 🟡 中 |
| 4 | `kimi_baseline_signals_matrix.csv` | 48 行中 `kimi_baseline_signals` 列只出现 `high_kimi_probability`、`kimi_longshot` 和 `none`，从不出现 `broad_faction_support` 或 `cross_faction_consensus` | 🟡 中 |

### 连锁影响：21 队深描

深描 commit（`1104f8e`）在填写 §2-§6 和 §11 时，保留了 §9 的原有内容。由于 §9 已因 Bug 显示"无 Kimi agent 预测数据"，深描版本继承了错误状态。

**影响**：深描 21 队（如 argentina.md、spain.md、turkey.md）的 §9 全部为空，即使这些队有大量 Kimi agent reason 可供摘要。

### 前端数据层传播（Oracle 盲点验证）

`build_site_data.py` 读取 `kimi_baseline_signals_matrix.csv`（L163），将其 `kimi_baseline_signals` 字段写入 `site/data/teams.json`（L204）。因此死信号传播到了 GitHub Pages 前端数据层。

`site/data/teams.json` 信号分布：

| 信号 | 出现次数 |
|------|--------|
| `none` | 30（27 non-Kimi + 3 中间概率）|
| `kimi_longshot` | 15 |
| `high_kimi_probability` | 3 |
| `broad_faction_support` | **0**（死代码）|
| `cross_faction_consensus` | **0**（死代码）|

`site/data/meta.json` 的 `kimi_coverage` 统计正确（21/27），不受此 Bug 影响。

### 确认不受影响

| 产出 | 原因 |
|------|------|
| `kimi_probability`（§1/§2/§11） | `get_team_aggregation()` 用双重 zh/en 检查 |
| `has_kimi` 标志 | 基于 `team_registry.csv` 的 `coverage_status`，非查找结果 |
| README 覆盖图标（✅/📋） | 基于 `has_kimi` 标志 |
| `high_kimi_probability` signal | 基于 `kimi_prob`（聚合路径） |
| `kimi_longshot` signal | 同上 |
| `generate_codability_annotation_pack.py` | 按 `faction` 分组，不涉及 champion 列 |
| `audit.py` / `verify.py` | 不处理队名 |
| `kimi_reason_sample_30.csv` | 非本脚本生成 |

## Secondary Findings

### 1. `team_name_map.csv` 是死产物

该文件在 MVP-0 数据门控期间创建（commit `dc99dba`），明确目的是建立中文↔英文队名映射。`mvp0-data-gate-report.md` 写道：

> "team_name_map.csv 已建立映射"

但**没有任何 Python 脚本 import 或读取这个文件**。它被创建来解决这个问题，却从未被使用。

### 2. 潜在 f-string Bug（L218）

```python
# L218 — 缺少 f 前缀
lines.append("> [!memo] {TODAY} Kimi reason 暂作为 Red Source / 候选线索保留。")
```

当前不可达（因为 `kimi_agents` 永远为空，该分支不执行），但如果修复 Bug #1 后不修此处，将输出字面文本 `{TODAY}` 而非日期值。

### 3. 前端数据层传播

`build_site_data.py` 消费 `kimi_baseline_signals_matrix.csv`，将死信号传播到 `site/data/teams.json`。GitHub Pages 展示层从未显示 `broad_faction_support` 或 `cross_faction_consensus`。

### 4. 信号命名的语义风险

`kimi_baseline_signals` 字段中 `broad_faction_support` 和 `cross_faction_consensus` 是有价值的分析维度（派别覆盖广度和跨派别共识），但因 Bug 从未生效。如果未来做 Plan A2 路径分类，需要意识到这两个维度目前完全缺失。

## Encoding Safety Verification

修复前已验证中文队名的字节级匹配：

```python
# 21 个 champion 值全部存在于 team_registry.csv 的 zh_name 列中
# 无 Unicode 异常（无 BOM、无 NBSP、无全角空格）
champions - zh_names == set()  # 空集，零缺失
```

**结论：`get(zh, [])` 修复安全，无编码风险。**

## Recommended Fix

### Fix 1：修正查找键（最小改动）

`scripts/generate_path_cards.py` L78，将英文名查找改为中文名查找：

```python
# 当前（Bug）：
kimi_agents = kimi_by_team.get(en, [])

# 修复：
kimi_agents = kimi_by_team.get(zh, [])
```

`zh` 在 L70 已经定义为 `team["zh_name"]`，与 `group_kimi_by_team()` 的字典 key 完全一致。

### Fix 2：修正 f-string（同步修复）

L218 添加 `f` 前缀：

```python
# 当前（Bug）：
lines.append("> [!memo] {TODAY} Kimi reason 暂作为 Red Source / 候选线索保留。")

# 修复：
lines.append(f"> [!memo] {TODAY} Kimi reason 暂作为 Red Source / 候选线索保留。")
```

### Fix 3：增量更新策略（关键）

⚠️ **不要全量重跑 `generate_path_cards.py`！** 全量重跑会覆盖 21 队的深描内容（§2-§6, §11），这些是 commit `1104f8e` 手工填充的。

**推荐方案：增量 §9 补丁**

```python
# 只更新 §9，保留其他 section 的深描内容
def patch_section_9(card_path, kimi_agents, kimi_prob):
    text = card_path.read_text(encoding="utf-8")
    s9_start = text.index("## 9. Marginalia Notes")
    s10_start = text.index("## 10. Update Log")
    new_s9 = build_section_9(kimi_agents, kimi_prob)
    patched = text[:s9_start] + new_s9 + "\n\n" + text[s10_start:]
    card_path.write_text(patched, encoding="utf-8")
```

然后单独更新：
- `kimi_baseline_signals_matrix.csv`（补充 `broad_faction_support` 和 `cross_faction_consensus`）
- 重跑 `build_site_data.py` 更新 `site/data/teams.json`

### Fix 3-alt：全量重跑（不推荐）

如果选择全量重跑 `generate_path_cards.py`，需要后续重新执行 21 队深描。

修复后重新执行 `python3 scripts/generate_path_cards.py`，将正确生成：
- 21 队 §9 包含 agent reason 摘要和派别分布
- `broad_faction_support` 和 `cross_faction_consensus` 信号正常出现
- `kimi_baseline_signals_matrix.csv` 更新

### Fix 4：更新深描 21 队

重跑后 21 队路径卡将回到薄切片状态（§2-§6 和 §11 的深描内容会被覆盖）。需要重新执行深描，或采用增量更新策略只更新 §9。

## Known Gaps（非 Bug，但需记录）

### top3 列未被处理

`group_kimi_by_team()` 仅按 `champion` 分组。`top3` 列（如 "西班牙|法国|英格兰"）从未被解析。一个预测 "挪威夺冠、阿根廷 top3" 的 agent 对阿根廷卡无任何贡献。这是设计简化，不是 Bug，但影响 48 队路径卡的 top3 覆盖度。

### kimi_reason_sample_30.csv 有同类风险

该文件的 `champion` 列也使用中文名。未来如果有脚本按英文队名查找此文件的 champion 列，会遇到完全相同的 Bug。

## Preventive Measures

1. **统一队名查找**：创建共享的 `team_name_resolver` 工具函数，所有脚本通过同一接口做中文↔英文↔slug 转换。`team_name_map.csv` 应作为该函数的数据源。
2. **单元测试**：为 `group_kimi_by_team()` 和 `generate_card()` 添加测试，验证中文名查找能匹配到正确的 agent。
3. **数据门控断言**：在脚本中加入断言，如 `assert len(kimi_by_team) > 0, "No agents grouped by team"`，防止类似问题静默通过。
4. **CI 集成检查**：在 CI 中添加检查步骤，验证 Kimi 覆盖的 21 队 §9 不为空。
5. **`team_name_map.csv` 激活**：将其纳入至少一个脚本的 import 链，或明确标注为"参考文档"避免误以为在用。
6. **构建脚本检查**：`build_site_data.py` 应在构建时验证信号完整性，如 `assert 'broad_faction_support' in all_signals`。

## Investigation Log

### Phase 1 - Bug 确认
**Hypothesis:** champion 列中英文不匹配导致查找失败
**Findings:** 已确认。CSV champion 列用中文，脚本用英文查找
**Evidence:** `kimi_agent_inventory.csv` champion 列 = 中文; `generate_path_cards.py:78` = `kimi_by_team.get(en, [])`; 运行验证: 中文 key "阿根廷" 有 55 条记录，英文 "Argentina" 查找返回 0
**Conclusion:** Confirmed

### Phase 2 - Blast Radius 验证
**Hypothesis:** Bug 只影响 §9，不影响聚合概率和基础信号
**Findings:** 确认。`get_team_aggregation()` 有独立的 zh/en 双重检查。`has_kimi` 基于 coverage_status 而非查找结果
**Evidence:** spain.md §2 显示 "Kimi 聚合概率: 23.82%（62 票）"（正确），§9 显示 "无 Kimi agent 预测数据"（Bug）
**Conclusion:** Confirmed — blast radius 精确限定在 agent-level 数据路径

### Phase 3 - 死信号验证
**Hypothesis:** `broad_faction_support` 和 `cross_faction_consensus` 从未出现在任何输出中
**Findings:** grep 搜索 `kimi_baseline_signals_matrix.csv` 确认 0 次出现
**Evidence:** `grep -c "broad_faction_support\|cross_faction_consensus" data/processed/kimi_baseline_signals_matrix.csv` = 0
**Conclusion:** Confirmed — 两个信号类型为死代码

### Phase 4 - 类似问题排查
**Hypothesis:** 其他脚本可能存在类似的中文/英文队名不匹配
**Findings:** `generate_codability_annotation_pack.py` 按 `faction`（英文标识）分组，不存在此问题。`audit.py` 不处理队名。`team_name_map.csv` 从未被任何脚本引用。
**Evidence:** `grep -rn "team_name_map" scripts/` 无结果
**Conclusion:** 无类似问题，但 `team_name_map.csv` 是死产物
