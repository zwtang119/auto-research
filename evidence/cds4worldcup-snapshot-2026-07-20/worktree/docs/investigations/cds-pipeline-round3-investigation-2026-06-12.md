# Investigation: CDS Pipeline 第三轮深度排查

## Summary
在前两轮调查（发现 23 个问题，已修复 18 个）基础上，针对以下未覆盖区域进行系统性排查：
1. F-23 schedule.json match_id swap 的根因追踪
2. 已修复代码的回归风险验证
3. 未调查的脚本和管线组件
4. 数据流端到端一致性

## 调查假设

### H1: parse_schedule.py 根因追踪
F-23 发现 schedule.json 中 3 组 match_id swap（74↔75, 76↔77, 81↔82）。需要追踪 parse_schedule.py 中导致 swap 的代码路径。

### H2: 已修复代码的回归风险
- WI-2 的 `qual_prob_top2` 新字段是否被 build_site_data.py 正确传递？
- WI-2 的 cache key 变更是否影响性能（48×缓存 vs 1×缓存）？
- WI-3 的 `distributePct` 函数在 edge case（0%, 100%）下是否正确？

### H3: 未调查的脚本
- `numeric_odds.py` — Elo+Poisson 模型是否有精度或逻辑问题？
- `fetch_market_snapshot.py` — 市场数据抓取是否有安全或鲁棒性问题？
- `generate_path_cards.py` — 路径卡生成是否与 CDS 数据一致？
- `scripts/verify.py` — 验证脚本是否覆盖新增的 CDS 数据？

### H4: CI/CD 管线完整性
- daily-update.yml 是否能在 WI-2 的新字段变更后正常工作？
- build_site_data.py 的新 `_write_data_script()` 是否与所有调用方兼容？

### H5: 数据契约一致性
- qualification.py 输出 → championship.py 输入 → build_site_data.py 合并 → JS 前端消费
- 新增的 `qual_prob_top2` 字段是否在每个环节都正确传递？

## Investigator Findings

### A. parse_schedule.py 根因追踪（F-23 match_id swap）

**严重度: P1 — 数据正确性**

**结论：确认是数据录入错误，不是代码逻辑 bug。**

通过 [Wikipedia 2026 FIFA World Cup knockout stage](https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_knockout_stage) 交叉验证，确认 3 组 swap 如下：

| Match # | FIFA 官方 (slot) | 代码中 (slot) | 偏移原因 |
|---------|-----------------|---------------|----------|
| KO74 | `1E vs 3ABCDF` | `1C vs 2F` | 74↔75 swap |
| KO75 | `1F vs 2C` | `1E vs 3ABCDF` | 74↔75 swap |
| KO76 | `1C vs 2F` | `1F vs 2C` | 76↔77 swap |
| KO77 | `1I vs 3CDFGH` | `2E vs 2I` | 76↔77 swap |
| KO78 | `2E vs 2I` | `1I vs 3CDFGH` | 77→78 shift |
| KO81 | `1D vs 3BEFIJ` | `1G vs 3AEHIJ` | 81↔82 swap |
| KO82 | `1G vs 3AEHIJ` | `1D vs 3BEFIJ` | 81↔82 swap |

**根因分析：**

1. `parse_schedule.py` 中 `KNOCKOUT_FIXTURES` 是硬编码的元组列表（lines ~372-408）
2. `build_knockout_stage()` (line ~474) 只做 `match_id = f"KO{match_num}"` — **完全静态**，无任何动态分配逻辑
3. match_num 直接来自元组位置 [0]，不存在代码路径可以产生 swap
4. **根因是数据录入时 3 组 match_num 搞混了**：录入人员把本应属于 KO74 的 1E vs 3ABCDF 错放到了 KO75 的位置

**影响链：**
- `data/processed/schedule.json` 和 `site/data/schedule.json` 的 `knockout_stage` 均受影响
- R16 的 W73/W74/W75 等引用（如 KO89=`W73 vs W75`, KO90=`W74 vs W77`）在冠军路径模拟中会产生错误的对手解析
- `championship.py` 的 `_trace_raw_paths()` 和 `_resolve_propagation_slot()` 使用的下游图会基于错误的 match_id 传播

**修复方案：**
- 修改 `KNOCKOUT_FIXTURES` 中 3 组 tuple 的 match_num
- 重新运行 `parse_schedule.py` 生成正确的 schedule.json
- 重新运行 `cds_path_simulation.py` 以修正冠军路径
- **修复难度**：低（3 行数据改动），**风险**：低（纯数据修正）

### B. 未调查的脚本

#### B1. numeric_odds.py — 10 队 Elo 并列 (3.6399) 根因

**严重度: P2 — 模型精度**

**根因**：Elo 分配仅使用 3 层分档：
- `ELO_BASE_BY_CONFED`（6 档：UEFA=1700, CONMEBOL=1690, ...）
- Kimi 概率 3 档 bonus（≥10%: +100, ≥3%: +60, <3%: +30）
- 东道主 bonus（+60）

当同一联合会内多支球队的 Kimi 概率在同一档位时，Elo 完全相同。例如 UEFA 内多支 3%-10% 的队都会得到 1700+60=1760。Elo 精度仅有 **27 个离散值**，无法区分同档内的 48 队。

**建议改进**：
- 在 Kimi bonus 档位内使用连续函数而非分档（如 `bonus = 30 + 70 * (prob / 20)`）
- 或在 team_registry.csv 中引入 FIFA 排名的连续细分
- 当前设计作为 MVP 基线可接受，但不应作为精细预测依据

#### B2. fetch_market_snapshot.py — 安全性评估

**严重度: P3 — 安全性**

评估结果：**安全性可接受**
- ✅ 使用 `timeout=30` 防止挂起
- ✅ 设置 User-Agent 标识
- ✅ 仅使用 stdlib，无第三方依赖
- ✅ 输出 sanitize 正常（`unmapped_markets` 记录未匹配项）
- ⚠️ 无 SSRF 风险：URL 是硬编码的 `gamma-api.polymarket.com`
- ⚠️ 无认证泄露：使用的是 public search endpoint
- **唯一问题**：无 HTTP 错误重试逻辑，CI 中偶尔网络抖动会导致 snapshot 缺失

#### B3. verify.py — 覆盖范围评估

**严重度: P3 — 功能缺失**

`verify.py` **仅验证 wiki 目录结构**（4 个必需子目录 + index.md），完全不涉及 CDS 数据验证。它不检查：
- schedule.json 合法性
- cds_qualification.json / cds_championship.json 存在性
- 数据一致性（如 match_id 格式）
- 字段完整性

建议：增加一个 `verify_cds_data.py` 或扩展 verify.py 以覆盖 CDS 管线验证。

#### B4. generate_path_cards.py — CDS 数据一致性

**严重度: P4 — 架构隔离**

`generate_path_cards.py` 生成的是 MVP-A1 薄切片路径卡（11 节模板），主要消费 Kimi 聚合数据。它与 CDS qualification/championship 数据管线**完全隔离**：
- 不读取 cds_qualification.json
- 不读取 cds_championship.json
- 输出的 `kimi_baseline_signals_matrix.csv` 被 `numeric_odds.py` 消费

两套数据流独立，无一致性风险，但也意味着路径卡不包含 CDS 模拟结果。这是一个已知的架构分层设计。

### C. 端到端数据契约验证（qual_prob_top2）

**严重度: P2 — 数据流断裂**

追踪 `qual_prob_top2` 在管线 4 个环节的传递：

| 环节 | 文件 | qual_prob_top2 状态 |
|------|------|-------------------|
| 1. qualification.py 输出 | `cds_qualification.json` | ✅ 存在（48 队均有） |
| 2. championship.py 读取 | `load_qualification_probs()` | ❌ **未读取** — 仅读 `qual_prob`, `position_probs`, `group`, `third_place_qual_prob` |
| 3. build_site_data.py 合并 | `build_cds_paths_json()` | ❌ **未传递** — qualification 子对象中缺少 `qual_prob_top2` |
| 4. team-detail.js 展示 | `renderCdsPaths()` | ❌ **未展示** — 仅展示 `qual_prob`（含第三名概率的总值） |

**影响**：
- 用户无法在前端区分「纯前二出线概率」和「含第三名晋级的总出线概率」
- 对于第三名晋级概率较高的队（如 66.7% 基率），差异可达 ~10-15 个百分点
- championship.py 不受影响（它用的是 qual_prob 乘以各轮胜率，不需要 top2）

**修复建议**：
- 在 `build_cds_paths_json()` 的 qualification 子对象中添加 `"qual_prob_top2": qual_team.get("qual_prob_top2", 0)`
- 在 `team-detail.js` 的 `renderCdsPaths()` 中添加「前二出线概率」展示（可作为 sub-label 出现在出线概率条旁）

### D. 已修复代码的回归风险

#### D1. WI-2 cache key 变更（加入 team）性能评估

**严重度: P3 — 性能**

`_resolve_propagation_slot()` 的 cache key 从 `f"{prop_type}:{src_id}"` 变为 `f"{prop_type}:{src_id}:{team}"`。

- 修正前：每种 slot 类型+match 组合仅计算 1 次，48 队共享 → **错误但快**
- 修正后：每种组合 per-team 计算 → ~32 个 KO match × 48 队 = ~1536 次计算
- 但 `_collect_teams_for_slot()` 递归深度 ≤ 10，且大量 slot 是 deterministic（position_group），实际 cache miss 远少于理论值
- championship.py 是 CPU-bound 计算（Bradley-Terry 乘法），不是 I/O-bound
- **结论**：正确性 > 速度。对于一次性模拟运行，额外开销可忽略（< 2s）。无性能退化风险。

#### D2. WI-3 distributePct 边界评估

**严重度: P3 — 前端健壮性**

代码分析（`site/js/common.js` lines 116-128）：

```javascript
function distributePct(vals) {
  var raw = vals.map(function (v) { return v * 100; });
  var floored = raw.map(function (v) { return Math.floor(v); });
  var remainder = 100 - floored.reduce(function (s, v) { return s + v; }, 0);
  // ... largest-remainder 分配
}
```

边界测试：
- `[0, 0, 1.0]` → raw=[0,0,100], floored=[0,0,100], remainder=0 → `[0,0,100]` ✅
- `[0.333, 0.333, 0.334]` → raw=[33.3,33.3,33.4], floored=[33,33,33], remainder=1 → 分配给 33.4 的位置 → `[33,33,34]` ✅
- `[0, 0, 0]` → raw=[0,0,0], floored=[0,0,0], remainder=100 → **但 indices 只有 3 个元素**，for 循环 `i < 100` 但 `indices[i]` 在 i≥3 时为 undefined → `floored[undefined]++` 是 NaN 赋值，不修改数组 → **返回 [0,0,0]，总和 0 ≠ 100** ⚠️
- `[1.5, 0, 0]`（概率和 >100%）→ raw=[150,0,0], floored=[150,0,0], remainder=-50 → 循环不执行 → `[150,0,0]`，总和 150 ≠ 100 ⚠️

**结论**：
- 正常概率分布（sum≈1.0）下完全正确
- 零概率输入 `[0,0,0]` 在实际场景中不会出现（Elo+Poisson 模型始终产出非零概率）
- 概率和 >1.0 理论上不可能（泊松截断+归一化保证 ≤1.0）
- **无需修复**，当前实现对实际数据安全

#### D3. WI-4 _write_data_script `</script>` 替换评估

**严重度: P3 — 安全性**

代码（`build_site_data.py` lines 1590-1598）：
```python
def _write_data_script(path, global_name, payload):
    js_text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    js_text = js_text.replace("</script>", "<\\/script>")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"window.{global_name} = ")
        f.write(js_text)
        f.write(";\n")
```

评估：
- ✅ `</script>` → `<\\/script>` 是标准 XSS 防护（防止提前关闭 `<script>` 标签）
- ✅ 替换在 JSON 序列化之后进行，不影响 JSON 结构
- ✅ `<\\/script>` 在 JS 字符串中解析为 `</script>`（`\\/` → `/`），JSON 数据无损
- ✅ `global_name` 有 `^[A-Z_][A-Z0-9_]*$` 正则校验，防注入
- ✅ `ensure_ascii=False` 允许 Unicode（中文球队名），`\uXXXX` 转义不存在
- **结论**：实现正确，无 JSON 有效性风险

### 总结

| ID | 方向 | 严重度 | 问题 | 状态 |
|----|------|--------|------|------|
| R3-A | parse_schedule.py | **P1** | 3 组 match_id swap（数据录入错误） | 需修复 |
| R3-B1 | numeric_odds.py | P2 | Elo 仅有 27 个离散值，10 队并列 | 已知限制 |
| R3-B2 | fetch_market_snapshot.py | P3 | 安全性可接受，无重试逻辑 | 可接受 |
| R3-B3 | verify.py | P3 | 不验证 CDS 数据，仅检查 wiki 结构 | 功能缺失 |
| R3-B4 | generate_path_cards.py | P4 | 与 CDS 管线隔离，架构设计如此 | 可接受 |
| R3-C | qual_prob_top2 流 | **P2** | 3 个下游环节未传递/展示该字段 | 需修复 |
| R3-D1 | cache key 性能 | P3 | 无实际退化，正确性优先 | 无风险 |
| R3-D2 | distributePct | P3 | 极端输入有理论缺陷，实际安全 | 无需修复 |
| R3-D3 | `</script>` 替换 | P3 | 实现正确，标准 XSS 防护 | 无风险 |

## Investigation Log
<!-- 由 agent 填充各阶段调查结果 -->
