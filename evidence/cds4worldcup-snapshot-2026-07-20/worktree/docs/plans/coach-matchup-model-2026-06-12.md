# 教练+球员对位模型：Phase 3 核心模块

> 替代 `player-matchup-model-2026-06-12.md`（key person overlay 方案，已 superseded）

## Goal

在 Phase 3 中实现教练决策+球员对位引擎+蒙特卡洛模拟的完整预测管线。LLM 担任教练角色选阵选人，数值模型基于 Transfermarkt 身价做位置对位评估，Poisson 模拟产出比赛概率分布。与现有 Kimi Agent 投票（WI-3.4）独立并列展示。

## Background

### 设计核心：LLM 做决策，数值做评估

```
LLM 教练的职责（决策）：
  ✅ 选阵型（4-3-3 / 4-4-2 / 3-5-2 等）
  ✅ 选首发 XI（给定阵型 + 26 人名单）
  ✅ 战术适配（对手高位压迫 → 我打防守反击）
  ❌ 不评估胜率——这是数值模型的事

对位引擎的职责（评估）：
  ✅ 身价 → 位置对位 → λ（期望进球率）
  ✅ Poisson 模拟 → 胜/平/负概率
  ❌ 不选阵型——这是教练的事
```

这个分工避免了 LLM 生成虚假概率的根本问题。LLM 做结构化推理（选人），数值模型做确定性计算（评估）。

### 数据可行性（已验证）

**Transfermarkt 48 队全量数据可获取**：

| 字段 | 可获取 | 模型需要 | 来源分级 |
|------|--------|---------|---------|
| 球员姓名 | ✅ 48/48 | ✅ | Yellow |
| 位置（GK/CB/LB/RB/DM/CM/AM/LW/RW/CF） | ✅ 48/48 | ✅ 关键 | Yellow |
| 身价（EUR） | ✅ 48/48 | ✅ 能力代理 | Yellow |
| 年龄 | ✅ 48/48 | ✅ 体能因素 | Yellow |
| 当前俱乐部 | ✅ 48/48 | ✅ 联赛修正 | Yellow |
| 总计 | ~1,248 条球员记录 | | |

身价作为能力代理已被学术研究验证（与球员能力 Pearson r ≈ 0.8+）。阿根廷全队 €807M vs 卡塔尔全队 €20M，直接映射对位强度。

**教练数据**：Soccerphile 已有 48 队教练完整列表（姓名、国籍、任职起始、上份工作）。阵型分布需从 FBref 历史比赛数据推导。

**阵型策略**：历史阵型分布采样（不用 LLM）。阿根廷最近 20 场 → `{4-3-3: 60%, 4-4-2: 30%, 3-5-2: 10%}` → 每次蒙特卡洛迭代从分布中采样。MVP 阶段可用预定义默认 + 少量手动验证。

### 身价→对位公式（log 变换）

Raw 身价比会极端扭曲（梅西 €20M vs 萨利巴 €65M → 0.24）。解决方案：

```python
# log 变换压缩极端值
ratio = log(attack_val + 1) / (log(attack_val + 1) + log(defend_val + 1))

# 效果：
#   姆巴佩 €180M vs 莫利纳 €25M → 0.61 (合理碾压，不夸张)
#   梅西 €20M vs 萨利巴 €65M → 0.42 (接近，防守方优)
```

V1 可追加年龄衰减和联赛修正。

### 现有管线对接点

**数据生产**：`scripts/numeric_odds.py:42-43` 输入 `schedule.json` + `team_registry.csv`，输出 `odds.json`（per-match predictions 数组）。教练模型复用同一 schema，`model` 字段标记为 `"coach_matchup"`。

**构建管线**：`scripts/build_site_data.py:1431-1440` 的 `main()` 顺序调用各 build 函数。新增 `build_coach_simulation_json()` 遵循相同模式：读 `data/processed/coach_simulation.json` → 返回 dict 或 None → 写 `site/data/coach-sim.json` + `coach-sim-data.js`。

**前端**：`site/js/panorama.js:194` 构建 `oddsMap[match_id]`，读取 `{ home_win, draw, away_win, confidence, expected_goals_home, expected_goals_away }`。教练模型数据可用相同 key 结构叠加或作为第二数据源。

**CI**：`.github/workflows/market-snapshot.yml` 的模式是 cron → 运行脚本 → diff-check → commit+push → 触发 pages.yml。教练模型脚本可加入同一 workflow 或独立 workflow。

**爬虫模式**：`scripts/fetch_market_snapshot.py` 使用 stdlib `urllib`（零第三方依赖），30s 超时，无 rate limiting。Transfermarkt 爬虫需遵循相同模式但加入请求间隔（Transfermarkt 反爬严格）。

### 来源分级约束

| 数据 | 来源 | 分级 | 约束 |
|------|------|------|------|
| Transfermarkt 身价/位置/年龄 | transfermarkt.com | Yellow | 需验证后才可进入 Green Source |
| 教练阵型分布（预定义） | 人工整理 | Green | |
| 教练阵型分布（FBref） | fbref.com | Yellow | |
| LLM 教练选人决策 | MiniMax-M3 | Red | 不可作为事实，只能参考 |
| 对位引擎输出 | 模型计算 | Red | 模型模拟输出，非事实 |
| Poisson 模拟概率 | 模型计算 | Red | 同上 |

所有前端展示必须标注来源分级 badge + "只能参考"标签。

### 成本估算

```
每场比赛蒙特卡洛 30 次迭代 × 每次迭代 2 次 LLM 调用（双方教练选人）
= 60 次 LLM 调用/场

每日 4-6 场比赛 → 240-360 次 LLM 调用/日
MiniMax-M3: ~¥3-5/日

对比原计划 Kimi Agent 投票: ~1,500 次/日, ~¥15/日
```

## Approach

### 架构：两阶段管线

```
PRE-COMPUTE（一次性，或阵容更新时重跑）
  Transfermarkt ──→ fetch_transfermarkt_squads.py
                    ↓ data/processed/transfermarkt_squads.json (48队 × ~26人)
  LLM 教练 ──────→ coach_simulation.py --phase=select-xi
                    ↓ data/processed/coach_formations.json (缓存 XI 选择)

SIMULATION（每日，不消耗 LLM）
  coach_simulation.py --phase=simulate
    1. schedule.json → 识别当日比赛
    2. 对每场比赛采样 N=20 次阵型对
    3. 查缓存 XI → 位置对位 → λ → Poisson 模拟
    4. 聚合：均值概率 + 阵型分布
    ↓ data/processed/coach_simulation.json
    ↓ build_site_data.py → site/data/coach-sim.json + coach-sim-data.js
    ↓ panorama.js + team-detail.js (前端)
```

**关键洞察**：XI 选择按 `(team, formation, opponent)` 维度缓存。赛前一次性预计算 ~430 次 LLM 调用；赛中每日仅对当天比赛的 4-6 队重选（~12-20 次调用）。模拟阶段（Monte Carlo）零 LLM。总成本 ~¥1/日（赛中），远低于 Kimi 方案的 ~¥15/日。

### Open Questions 解决方案

| 问题 | 决策 | 理由 |
|------|------|------|
| Transfermarkt 反爬 | `urllib` + 4s 间隔 + retry(3) + 手动 fallback 文件 | 项目零依赖约束；Playwright 违反此约束 |
| MVP 验证阈值 | 不同阵型对同一对队必须产出 ≥2pp 概率差异 | 低于 2pp 模型等效于噪声 |
| 阵型→位置映射 | **位置组聚合**（ATT vs DEF, MID vs MID）而非逐行对位 | 逐行对位（LW vs RB）依赖阵型且脆弱；组聚合稳健 |

### 对位引擎核心公式

```
λ 推导（不使用 Elo，完全基于球员身价）：

Step 1: 位置组价值聚合（log 变换）
  group_value(team, "ATT") = Σ log(player.market_value_eur + 1) for player in XI where position ∈ {CF, LW, RW}

Step 2: 攻防比率
  attack_ratio_home = att_home / (att_home + def_away)
  midfield_ratio = mid_home / (mid_home + mid_away)

Step 3: λ 计算
  λ_home = BASE_GOALS × (attack_ratio_home / 0.5) × (0.7 + 0.3 × midfield_ratio) × HOME_ADV
  λ_away = BASE_GOALS × (attack_ratio_away / 0.5) × (0.7 + 0.3 × (1 - midfield_ratio))

  BASE_GOALS=1.35, HOME_ADV=1.12（与 numeric_odds.py 一致）
  λ bounds: [0.3, 3.5]

Step 4: Poisson 目标矩阵 → 胜/平/负概率
```

---

## Work Items

### WI-CM.1 — 阵型-位置映射表

**Goal:** 定义 6 种常见阵型的位置结构和位置组归属
**Done when:** `config/formation_positions.json` 存在，含 6 种阵型（4-3-3, 4-4-2, 4-2-3-1, 3-5-2, 3-4-3, 5-3-2），每种有 11 个位置 + 4 个位置组计数，总和 = 11
**Key files:** 新建 `config/formation_positions.json`
**Dependencies:** 无
**Size:** S (1h)

### WI-CM.2 — 共享 Poisson 模块

**Goal:** 从 `numeric_odds.py` 提取 Poisson 模拟函数为可导入模块
**Done when:** `src/utils/poisson.py` 含 `poisson_prob()`, `simulate_goal_matrix()`, `normalize_probs()`；`numeric_odds.py` 改为 import 该模块；现有 7/7 测试全部通过且输出不变
**Key files:** 新建 `src/utils/poisson.py`, 修改 `scripts/numeric_odds.py:86-131`
**Dependencies:** 无
**Size:** S (2h)

### WI-CM.3 — 阵型分布数据库

**Goal:** 为 48 队定义历史阵型使用概率分布
**Done when:** `config/formation_distributions.json` 存在，21 deep team 有专属分布，27 thin-slice 用 default；每队概率和 = 1.0
**Key files:** 新建 `config/formation_distributions.json`
**Dependencies:** 无
**Size:** M (4h)

### WI-CM.4 — Transfermarkt 球队爬虫

**Goal:** 爬取 48 队完整阵容（姓名、位置、身价、年龄、俱乐部）
**Done when:** `scripts/fetch_transfermarkt_squads.py` 产出 `data/processed/transfermarkt_squads.json`，≥40/48 队成功，每队 ≥20 球员含有效 position_code 和 market_value_eur；手动抽检 5 队（阿根廷、法国、巴西、西班牙、日本）与 Transfermarkt 网站一致
**Key files:** 新建 `scripts/fetch_transfermarkt_squads.py`（~300 行），输出 `data/processed/transfermarkt_squads.json`
**Dependencies:** 无
**Size:** L (1d)
**Risk:** Transfermarkt 反爬（429/403）。缓解：4s 间隔 + retry(3) + 手动 fallback 文件
**Implementation note:** 实施者需：(1) 构建 48 队的 `verein_id` 映射（从 Transfermarkt URL 提取），(2) 确定页面 CSS 选择器（Transfermarkt 阵容表通常在 `table.items > tbody > tr` 中，位置在 `td.posrela > table > tr > td`，身价在 `td.rechts.hauptlink`）。
(3) 处理身价格式多样性（"€20m", "€20mil.", "£15m" → 统一转 EUR 整数）。这些是爬虫的核心实现细节，实施时应先用 `curl` 抓取 1-2 队页面验证选择器。

### WI-CM.5 — LLM 教练 XI 选择（对手感知 + 赛中更新）

**Goal:** LLM 为每队每种阵型 × 每个对手选择首发 XI，赛中每日根据赛况更新
**Done when:** `scripts/coach_simulation.py --phase=select-xi` 产出 `data/processed/coach_formations.json`；赛前 ≥400 有效 XI（48队 × ~3阵型 × ~3对手），赛中每日更新当天比赛的 XI；每个 XI 恰好 11 人且位置匹配阵型
**Key files:** 新建 `scripts/coach_simulation.py`，依赖 WI-3.1（`llm_client.py`）或内置最小 LLM 客户端
**Dependencies:** WI-CM.1, WI-CM.3, WI-CM.4
**Size:** L (1d)

**两阶段运行模式：**

| 阶段 | 时机 | LLM 调用 | 说明 |
|------|------|---------|------|
| 赛前预计算 | 一次性 | ~430（48队 × 3阵型 × 3对手） | 生成 baseline XI |
| 赛中每日 | 每日 | ~12-20（当天比赛的 4-6 队） | 根据赛况重选 XI |

**赛中更新的必要性**：小组赛每轮结果改变出线形势 → 教练策略随之变化：
- 已出线 → 轮换主力，备战淘汰赛
- 必须赢 → 全力出击，核心球员首发
- 关键球员受伤 → 调整阵容

**LLM prompt 上下文（赛中版）**：
```
输入：
  - 当前小组积分榜（你队 X 分，对手 Y 分）
  - 出线形势（"本场必须赢才能出线" / "已出线可轮换"）
  - 可用球员（26人 × 位置+身价，标注伤病/停赛）
  - 对手信息（预计阵型、核心球员）
  - 比赛：{formation} vs {opponent_formation}

输出：JSON { formation, starting_xi[], tactical_rationale, rotation_flag }
```

**Cost:** 赛前 ~¥0.9（一次性），赛中 ~¥0.1/日。总成本远低于 Kimi ¥15/日。
**LLM client fallback:** 如 WI-3.1 未就绪，在脚本内实现最小 OpenAI 兼容客户端（~60 行：`urllib.request` + JSON 解析 + retry），参照 `fetch_market_snapshot.py` 模式。API key 从 `MINIMAX_API_KEY` 环境变量读取。

### WI-CM.6 — 对位引擎 + 蒙特卡洛模拟

**Goal:** 基于身价位置对位计算 λ，Poisson 模拟产出比赛概率
**Done when:** `scripts/coach_simulation.py --phase=simulate` 产出 `data/processed/coach_simulation.json`，≥60/72 场小组赛有预测，概率和 = 1.0 ± 0.01；MVP 验证：阿根廷 vs 法国不同阵型对 ≥2pp 差异
**Key files:** `scripts/coach_simulation.py`（~450 行总计），依赖 `src/utils/poisson.py`
**Dependencies:** WI-CM.1, WI-CM.2, WI-CM.4, WI-CM.5
**Size:** XL (2d)

### WI-CM.7 — 构建管线集成

**Goal:** 教练模型数据接入 `build_site_data.py`
**Done when:** `build_coach_simulation_json()` 函数产出 `site/data/coach-sim.json` + `coach-sim-data.js`；通过 `_validate_public_text_boundary()` 检查；构建成功
**Key files:** 修改 `scripts/build_site_data.py:1431-1440`（main 函数）
**Dependencies:** WI-CM.6
**Size:** S (2h)
**Note:** 必须与 WI-CM.8 同一 commit

### WI-CM.8 — 前端集成

**Goal:** 全景图和球队详情页展示教练模型数据
**Done when:** `panorama.js` 加载 `coachMap[match_id]` 与 `oddsMap` 并列显示概率条；`team-detail.js` 展示阵型分布和示例 XI；所有数据标注 Red Source badge + "只能参考"；本地 HTTP server 验证渲染正常
**Key files:** 修改 `site/js/panorama.js:194`（数据加载）, `site/js/team-detail.js`, `site/css/portal.css`, `site/panorama.html`, `site/team.html`
**Dependencies:** WI-CM.7（同一 commit）
**Size:** L (1d)

### WI-CM.9 — 测试

**Goal:** 验证教练模型管线正确性
**Done when:** `tests/test_coach_simulation.py` 含 8+ 单元测试（Poisson 模块、对位计算、λ 边界、阵型采样、缺失数据降级、文本边界）；`tests/test_build_site_data.py` 新增 `test_build_coach_simulation_json()`；全部测试通过
**Key files:** 新建 `tests/test_coach_simulation.py`, 修改 `tests/test_build_site_data.py`
**Dependencies:** WI-CM.7, WI-CM.8
**Size:** M (4h)

### WI-CM.10 — Factor Ledger 条目

**Goal:** 为教练模型的主要对位信号生成 Factor YAML
**Done when:** 按 matchup signal 强度 Top 10 场比赛生成 factor YAML，遵循 `factor_ledger_entry.schema.yaml` 结构
**Key files:** `artifacts/fixtures/cds4polymarket/factor-ledger/` 新增文件
**Dependencies:** WI-CM.6
**Size:** M (3h)
**Note:** 可与 WI-CM.7~9 并行。**可推迟**：非核心功能，可在模型验证通过后再做

### WI-CM.11 — CI 集成

**Goal:** 教练模型加入每日更新 workflow
**Done when:** `daily-update.yml` 中 `numeric_odds.py` 之后添加 `coach_simulation.py --phase=simulate` 步骤（`continue-on-error: true`）；可选：biweekly XI 重选 workflow
**Key files:** 修改 `.github/workflows/daily-update.yml`（WI-4.3 产物），新建可选 `.github/workflows/coach-xi-selection.yml`
**Dependencies:** WI-CM.6
**Size:** S (2h)
**Note:** 依赖现有升级计划的 WI-4.3（daily-update.yml）先实施。**可推迟** — Tag + 文档

**Goal:** 标记教练模型完成
**Done when:** `git tag upgrade-phase-3-coach-model-done`；`wiki/index.md` 更新含教练模型页面；旧计划 `player-matchup-model-2026-06-12.md` 标记 superseded
**Dependencies:** WI-CM.9, WI-CM.11
**Size:** S (30min)

---

## 实施顺序

```
Phase A (基础，可并行):
  WI-CM.1 (阵型映射) ─┐
  WI-CM.2 (Poisson)  ─┤
  WI-CM.3 (阵型分布) ─┼──→ Phase B
  WI-CM.4 (TM 爬虫)  ─┘

Phase B (核心模型):
  WI-CM.5 (LLM XI 选择) ──→ WI-CM.6 (对位+MC)

Phase C (集成):
  WI-CM.7 (管线) ←atomic→ WI-CM.8 (前端) ──→ WI-CM.9 (测试)

Phase D (收尾):
  WI-CM.10 (Factor) — 与 Phase C 并行
  WI-CM.11 (CI) — Phase C 之后
  WI-CM.12 (Tag) — 最后
```

## 风险与缓解

| 风险 | 缓解 |
|------|------|
| Transfermarkt 403 批量失败 | 手动 fallback 文件 `transfermarkt_manual_override.json` |
| LLM XI 选择不一致（重跑不同） | temperature=0 + 缓存 + 仅手动触发重选 |
| 身价数据锦标赛期间过时 | weekly 重爬计划 |
| 教练模型与 Elo 模型高度相似 | 监控 Elo vs Coach 偏离度；如均值绝对差 <1pp 需调参数 |
| `coach_simulation.json` 过大 | 只 commit 构建后的 `site/data/coach-sim.json`（更小） |

## 成本

| 组件 | LLM 调用 | 成本 |
|------|---------|------|
| 初始 XI 选择 | ~144 次 | ¥0.3（一次性） |
| Biweekly 重选 | ~144 次 | ¥0.3/两周 |
| 每日模拟 | **0** | **¥0** |
| **总计运行时** | **0/日** | **¥0/日** |

对比 Kimi Agent 投票: ~1,500 次/日, ~¥15/日

### References

- `docs/plans/full-upgrade-2026-06-12.md` — 现有升级计划（Phase 0-4）
- `scripts/numeric_odds.py:90-139` — `compute_match_probs()` Poisson 模拟核心
- `scripts/fetch_market_snapshot.py:164-187` — 现有爬虫模式（urllib, 30s timeout）
- `scripts/build_site_data.py:1431-1440` — `main()` 构建编排
- `site/js/panorama.js:194` — `oddsMap[match_id]` 前端数据消费
- `.github/workflows/market-snapshot.yml:33` — CI daily update 模式
- `docs/source-policy.md` — 来源分级规则
- [Transfermarkt WC2026 参赛队](https://www.transfermarkt.com/weltmeisterschaft/teilnehmer/pokalwettbewerb/FIWC/saison_id/2025)
- [Soccerphile WC2026 教练列表](https://www.soccerphile.com/world-cup-2026/managers)
