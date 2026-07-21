# 球员对位博弈建模方案：Phase 3 新增模块

> ⚠️ **SUPERSEDED** — 本计划已被 [`docs/plans/coach-matchup-model-2026-06-12.md`](coach-matchup-model-2026-06-12.md) 替代。
> 教练+球员对位模型是本方案的完整演化版本（从 key person overlay 升级为 LLM 教练 + 位置对位引擎 + 蒙特卡洛）。

## Goal

在现有升级计划的 Phase 3 中新增球员对位博弈模型（Player Matchup Model），作为 Kimi 多 Agent 投票之外的独立预测信号。利用现有数据提取 key person 依赖度分析（V0），并为获取外部数据后的完整位置对位模型（V1）预留接口。

## Background

### 项目当前数据基础

**队级别数据（已有）**：
- `data/processed/team_registry.csv` — 48 队基本信息
- `data/processed/kimi_baseline_signals_matrix.csv` — 21 队 Kimi 概率
- `data/processed/market_public_snapshot.json` — Polymarket 市场赔率
- `data/processed/schedule.json` — 完整赛程（72 场小组赛 + 淘汰赛）
- `artifacts/team-cards/*.md` — 47 队路径卡（含质性球员描述）

**球员级别数据（现状）**：
- `artifacts/team-cards/` 中顶级球队（阿根廷、法国、巴西等）在叙事中提到 3-6 名球员，包含质性描述（体能、射门、伤病风险等），但零结构化数据
- `data/processed/kimi_reason_sample_30.csv` 中 ~53 个独立球员名字被提及，~15 个有市场身价（散落在中文叙述中，非结构化）
- **零位置数据、零职业生涯统计、零阵容名册、零物理属性的结构化记录**
- `data/ops/mimo_outputs/fifa-debug-2026-06-12.html` — FIFA 网站空 HTML 壳（JS 动态加载，无可用数据）

### 球员建模的 CDS 映射

| CDS 概念 | 球员模型对应 | 数据现状 |
|----------|-------------|---------|
| Factor | 球员属性（速度、射门、传球等） | ❌ 仅有质性描述 |
| Factor Ledger | 球员属性 YAML + 来源标注 | ❌ 不存在 |
| Path Space | 对位 → 模拟 → 概率分布 | ❌ 无属性数据无法计算 |
| Obstacle | 球员伤病/停赛 → λ 下降 | ⚠️ 可从叙事中提取（Red Source） |
| Key Person | 去掉后球队期望进球下降最多的人 | ✅ 可从现有数据识别 |
| Marginalia | 球员状态标注 | ❌ 不存在 |

### 可参考的外部模式（cds4polymarket 预研）

- Arena 多 Agent 辩论模式（`arena.ts:15-47`）：47 行核心循环，可参照用 Python 重写
- `ServiceResult[T]` 统一返回模式：适合球员数据提取管线
- LLM-as-judge 评估框架：可用于验证球员属性提取质量
- 7 阶段管线编排模式：适合球员数据日更新流程

### Phase 3 依赖链

球员对位模型需要的上游数据：
- ✅ `schedule.json`（WI-1.1，已存在）
- ✅ `team_registry.csv`（WI-0.2 已校正）
- ✅ `market_public_snapshot.json`（已有）
- ⬜ 球员属性数据（V0 用现有数据提取，V1 需外部数据源）

不需要依赖 Phase 2 前端，可独立开发。前端集成点在 WI-3.6（Phase 3 末尾）。

### 现有管线接口

`build_site_data.py`（1405 行）的数据流模式：`data/processed/*.csv|json` → 内存 dict → `site/data/*.json` + `.js`。新增球员数据只需加 `build_players_json()` 函数和对应输出文件。前端 `team-detail.js`（280 行）已有 `public_references` 和 `ai_perspective` 数据契约可扩展。

## Approach

### 核心设计决策

| 决策 | 选择 | 理由 |
|------|------|------|
| 模型架构 | **λ-adjustment overlay**（叠加在 Elo+Poisson 上） | 不是独立模型，而是基于球员数据调整现有 Poisson 的 λ。优雅降级：无球员数据时退化为 base model |
| V0 数据来源 | LLM 从 team card 叙事中提取 key person | 现有数据只有叙事，~53 个球员名字散落在 300 条 Kimi reason 和 21 张 deep team card 中 |
| 调整幅度上限 | **±15%** | 球员模型是 overlay 不是替代，避免覆盖 Elo base signal |
| 与 Kimi 投票的关系 | **独立并列展示** | 两种方法论根本不同，平均会隐藏有价值的分歧。项目哲学："展示证据，不做结论" |
| V0 来源分级 | **Red Source** | LLM 从叙事提取的属性不可进入 Factor Ledger 作为事实，只能作为 baseline/seed |
| V1 外部数据优先级 | Transfermarkt > fbref > FIFA ratings | Transfermarkt 提供位置+年龄+身价，是位置对位分析最有用的三个字段 |

### 模型架构

```
现有管线                          新增球员对位层
─────────────────────────────────────────────────────
numeric_odds.py                   player_matchup_model.py
  assign_elo()                       读取 key_persons.json
  elo_expected_score()               计算 star_power 差异
  compute_match_probs()    ← overlay  调整 λ ± 15%
  → odds.json                        → player_matchup_probs.json
                                      ↓
                                    build_site_data.py
                                      build_players_json() (新增)
                                      → site/data/players.json
```

**V0 算法**（对每场比赛）：

1. 从 `odds.json` 读取 base 概率和 λ
2. 从 `key_persons.json` 读取双方 key person
3. 任一方无数据 → 跳过（优雅降级）
4. 计算 `star_power_home = Σ(key_person_score)`, `star_power_away` 同理
5. `delta = (star_home - star_away) / max(star_home + star_away, 0.01)`
6. `adjustment = delta × 0.15`（有界 ±0.15）
7. `λ_home' = λ_home × (1 + adjustment)`, `λ_away' = λ_away × (1 - adjustment)`
8. 用调整后的 λ 重新跑 Poisson 模拟
9. 记录 base vs adjusted 概率 + 调整因素

**V1 扩展**：当 `player_registry.json`（Transfermarkt 数据）存在时，将步骤 4-6 替换为位置组对位分析（ATT vs DEF, MID vs MID 等），函数签名和输出 schema 不变。

### 管线集成

遵循 `build_site_data.py` 现有模式：新增 `build_players_json()` 函数（~80 行），产出 `site/data/players.json` + `players-data.js`。数据缺失时返回 None，管线不受影响。

前端集成点：
- `team-detail.js` → 新增 `renderPlayerAnalysis(detail)` 渲染球星依赖度 + key person 列表
- `panorama.js` → `renderMatchDetail()` 增加球员调整前后对比
- `homepage.js` → `renderExternalReferenceChart()` 新增第三条柱（球员对位）
- 所有球员数据标注 Red Source badge + "只能参考" 标签

---

## Work Items

### WI-PM.1 — 共享 Poisson 模块抽取

**Goal:** 将 `numeric_odds.py` 中的 Poisson/Elo 函数提取为可导入的共享模块
**Done when:** `src/utils/poisson.py` 存在，包含 `compute_match_probs()`, `poisson_prob()`, `elo_expected_score()`；`numeric_odds.py` 改为 import 该模块；现有 7/7 测试全部通过
**Key files:** `scripts/numeric_odds.py:90`（`compute_match_probs`）, 新建 `src/utils/poisson.py`
**Dependencies:** WI-0.3（管线健康）
**Size:** S (2h)

### WI-PM.2 — Key Person 提取脚本

**Goal:** 从 21 张 deep team card + 30 条 Kimi reason 中提取结构化 key person 数据
**Done when:** `scripts/extract_key_persons.py` 产出 `data/processed/key_persons.json`，覆盖 ≥15 支队伍，每队 3-6 名 key person（含 name_en, name_zh, estimated_position, key_person_score, market_value_mentioned, evidence_quote, confidence）；star_dependency 指标已计算
**Key files:** 新建 `scripts/extract_key_persons.py`, 输入 `artifacts/team-cards/*.md`, `data/processed/kimi_reason_sample_30.csv`
**Dependencies:** WI-3.1（LLM client）—— 如未就绪，内置最小 LLM 调用函数
**Size:** L (1d)
**Note:** 此脚本运行一次（非每日），team card 更新时重跑。~21 次 LLM 调用，约 1 分钟。

### WI-PM.3 — 球员对位模型脚本

**Goal:** 基于 key person 数据计算球员调整后的比赛概率
**Done when:** `scripts/player_matchup_model.py` 产出 `data/processed/player_matchup_probs.json`；每场比赛含 base vs adjusted 概率 + 调整因素 + 双方 key person 列表；无球员数据的比赛被跳过（非报错）
**Key files:** 新建 `scripts/player_matchup_model.py`, 输入 `key_persons.json` + `odds.json` + `schedule.json`
**Dependencies:** WI-PM.1, WI-PM.2
**Size:** L (1d)

### WI-PM.4 — 管线集成

**Goal:** 将球员数据接入 `build_site_data.py` 产线
**Done when:** `build_players_json()` 函数产出 `site/data/players.json` + `players-data.js`；`_build_public_team_detail()` 新增 `player_analysis` 字段；`build_homepage_json()` 新增 `player_model` snapshot；所有输出通过 `_validate_public_text_boundary()` 检查
**Key files:** `scripts/build_site_data.py:1380`（main）, `scripts/build_site_data.py` 新增函数
**Dependencies:** WI-PM.3
**Size:** M (4h)
**Note:** 必须与 WI-PM.5 同一 commit 落地（前端需要数据契约）

### WI-PM.5 — 前端集成

**Goal:** 在球队详情、全景图、首页展示球员对位数据
**Done when:**
- `team-detail.js` 新增 `renderPlayerAnalysis()`：显示 star dependency 指标 + key person 列表 + 位置 badge
- `panorama.js` 在比赛详情中显示 base vs adjusted 概率对比
- `homepage.js` 在外部参考图表中增加第三条柱（球员对位）
- `portal.css` 新增对应 CSS 类（`.player-analysis-section`, `.key-person-card`, `.position-badge` 等）
- `team.html` 新增 `<section data-team-player-analysis>` 容器
- 所有球员数据标注 Red Source badge + "只能参考"
**Key files:** `site/js/team-detail.js`, `site/js/panorama.js`, `site/js/homepage.js`, `site/css/portal.css`, `site/team.html`
**Dependencies:** WI-PM.4
**Size:** L (1d)
**Note:** 与 WI-PM.4 同一 commit

### WI-PM.6 — 测试

**Goal:** 验证球员数据管线的正确性
**Done when:** `tests/test_build_site_data.py` 新增 `build_players_json()` 测试覆盖：完整数据、数据缺失、部分覆盖、概率归一化、public text boundary 验证；全部测试通过
**Key files:** `tests/test_build_site_data.py`
**Dependencies:** WI-PM.4, WI-PM.5
**Size:** M (4h)

### WI-PM.7 — Factor Ledger 条目

**Goal:** 为有 key person 数据的队伍生成 Factor Ledger YAML 条目
**Done when:** 每队 key person 对应一个 factor YAML 文件，遵循 `factor_ledger_entry.schema.yaml` 结构，含 observable_proxy + settlement_rule + counter_signal
**Key files:** `artifacts/fixtures/cds4polymarket/factor-ledger/` 新增文件, `src/factor_ledger/schemas/factor_ledger_entry.schema.yaml`
**Dependencies:** WI-PM.2
**Size:** M (4h)
**Note:** 与其他 WI 独立，可并行

### WI-PM.8 — Tag + 文档

**Goal:** 标记球员对位模型完成
**Done when:** `git tag upgrade-phase-3-player-model-done`；wiki 更新含球员模型页面；计划文件的 Open Questions 标记为已解决
**Dependencies:** WI-PM.6
**Size:** S (30min)

---

## 实施顺序

```
WI-PM.1 (共享 Poisson) ──→ WI-PM.3 (对位模型)
                                  ↑
WI-PM.2 (key person 提取) ───────┘
                                        ↓
WI-PM.4 (管线) ──→ WI-PM.5 (前端) ──→ WI-PM.6 (测试)
                                                        ↓
                                                 WI-PM.8 (tag)
WI-PM.7 (factor ledger) — 独立，可与 WI-PM.2~6 并行
```

WI-PM.4 + WI-PM.5 必须同一 commit 落地。

---

## Open Questions

1. ~~球员属性提取精度~~ → **已决策**：V0 作为 Red Source baseline 可接受。每次提取含 evidence_quote + confidence 字段，0.15 调整上限限制劣质提取的影响
2. ~~外部数据获取优先级~~ → **已决策**：Transfermarkt 优先（位置+年龄+身价最实用），fbref 次之，FIFA ratings 最后（游戏数据最不可靠）
3. ~~与 WI-3.4 聚合方式~~ → **已决策**：独立并列展示，不做平均。两种方法论根本不同，分歧本身有价值

## References

- `docs/plans/full-upgrade-2026-06-12.md` — 现有升级计划（Phase 0-4）
- `artifacts/team-cards/argentina.md` — 典型 deep team card（含球员叙事描述）
- `data/processed/kimi_reason_sample_30.csv` — 30 条 Kimi reason 样本
- `scripts/build_site_data.py` — 现有数据管线（~1405 行）
- `scripts/numeric_odds.py:90` — `compute_match_probs()`（Poisson 模拟核心）
- `site/js/team-detail.js` — 球队详情页数据契约（280 行）
- `site/js/panorama.js` — 全景图页面（490 行，WI-2.1 产物）
- `site/js/common.js:sourceClass()` — Red/Yellow/Green 来源 badge
- `docs/source-policy.md` — 来源分级规则
- `src/factor_ledger/schemas/factor_ledger_entry.schema.yaml` — Factor schema
- `artifacts/fixtures/cds4polymarket/factor-ledger/wc2026-a-m01-mex-rsa.factors.yaml` — Factor 条目示例
- cds4polymarket: `docs/comparisons/external-code-phase2-deep-pattern-audit-2026-05-22.md` — 可采纳模式
- cds4polymarket: `docs/superpowers/specs/2026-06-10-kimi-300-agent-brainstorm-synthesis-v2.md` — 实验优先级
