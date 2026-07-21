# Investigation: Hardcoded Value Fixes — Risk & Blast Radius

**Date**: 2026-06-13
**Status**: Complete

## Summary

两项硬编码修复的爆炸范围均很小：P0（Transfermarkt UA 伪装）改 1 个字符串，零下游影响；P1（模型参数重复）涉及 2 个文件的 import 改动，不影响 qualification.py 等独立模块。

## Symptoms

- `fetch_transfermarkt_squads.py` 使用伪装 Chrome User-Agent 抓取 Transfermarkt — 合规风险
- `BASE_GOALS=1.35`、`MAX_GOALS=7`、`HOME_ADV=1.12`、`LAMBDA_MIN/MAX=0.3/3.5` 在 `numeric_odds.py` 和 `coach_simulation.py` 中各写一遍 — 同步风险

## Background / Prior Research

无外部事实需求。所有信息在工作区内可获取。

## Investigator Findings

### P0 — Transfermarkt User-Agent 伪装

#### (a) 下游依赖链

```
fetch_transfermarkt_squads.py
  → data/processed/transfermarkt_squads.json
    → coach_simulation.py (唯一消费者, line 59: SQUADS path)
      → coach_formations.json + coach_simulation.json
        → build_site_data.py (读 coach 模型输出, 不直接读 transfermarkt JSON)
          → site/data/*.json
```

- `build_site_data.py` **不直接读取** `transfermarkt_squads.json`（搜索确认：文件中无此引用）
- `coach_simulation.py` 是唯一消费者

#### (b) CI 调用情况

| 工作流 | 是否运行此脚本 |
|--------|:---:|
| `daily-update.yml` | ❌ 不运行（Coach 步骤是 TODO 注释, lines 48-53） |
| `market-snapshot.yml` | ❌ 不运行 |
| `ci.yml` | ❌ 不运行 |
| `Makefile` | ❌ 无相关 target |

**结论：此脚本仅在本地手动运行，CI 不涉及。**

#### (c) Fallback 机制完整性

脚本有 **三层 fallback**：

1. **单队 fallback**（`scrape_all_teams`, lines 686-698）：如果某队抓取失败或 <15 球员 → 使用手动数据
2. **全量 fallback**（`--fallback` 参数，lines 741-769）：所有 48 队都用手动数据
3. **测试模式**（`--test`）：只抓 2 队，其余 fallback

手动数据覆盖全部 48 队（`_MANUAL_FALLBACK_DATA`，lines 417-652），包含球员姓名、位置、身价、年龄、俱乐部。标记为 `source=manual_fallback`（Yellow 来源等级）。

#### (d) 修复方案与爆炸半径

| 方案 | 改动 | 风险 |
|------|------|------|
| A：换诚实 UA | 改 `HEADERS["User-Agent"]` 一行 | Transfermarkt 可能返回 403 → fallback 自动生效 |
| B：加 ToS 声明 | 在文件头注释加 `仅供本地一次性研究使用` | 零代码风险 |
| C：A+B | 同时做 | 最低合规风险 |

**爆炸半径：零。** 无论 Transfermarkt 是否封杀，fallback 机制保证 48 队数据不缺。CI 不运行此脚本，不影响自动化管线。

---

### P1 — 模型参数常量重复

#### (a) 精确重复清单

| 常量 | numeric_odds.py | coach_simulation.py | poisson.py |
|------|:---:|:---:|:---:|
| 基础进球 | `BASE_GOALS_PER_TEAM=1.35` (L53) | `BASE_GOALS=1.35` (L65) | — |
| 主场优势 | `HOME_ADVANTAGE_FACTOR=1.12` (L54) | `HOME_ADV=1.12` (L66) | — |
| 最大进球 | `MAX_GOALS=7` (L55) | `MAX_GOALS=7` (L67) | `max_goals=7` (函数默认值, L26/L65) |
| λ 下限 | `0.3` (inline, L213) | `LAMBDA_MIN=0.3` (L68) | — |
| λ 上限 | `3.5` (inline, L214) | `LAMBDA_MAX=3.5` (L69) | — |

#### (b) 调用链分析

```
numeric_odds.py
  → from src.utils.poisson import poisson_prob, compute_match_probs_from_lambdas
  → compute_match_probs_from_lambdas(lam_home, lam_away, MAX_GOALS)  # 显式传入
  → λ 计算在 compute_match_probs() 内，用 inline max(0.3, min(3.5, ...))

coach_simulation.py
  → from src.utils.poisson import compute_match_probs_from_lambdas
  → compute_match_probs_from_lambdas(lam_h, lam_a, MAX_GOALS)  # 显式传入
  → λ 计算在 compute_lambdas() 内，用 max(LAMBDA_MIN, min(LAMBDA_MAX, ...))
```

**关键发现：两个调用者都显式传入 `MAX_GOALS`，不依赖 poisson.py 的默认值 7。**

#### (c) qualification.py 是否共享这些常量？

**不共享。** `qualification.py` 有完全独立的代码路径：

- 自己实现了 `_poisson_sample()` 函数（不 import poisson.py）
- 使用**不同的默认值**：`expected_goals_home=1.5`, `expected_goals_away=1.0`（L138-139）
- 以及：`expected_goals_home=1.3`, `expected_goals_away=1.1`（L304-305，用于后续比赛）
- λ 下限 `0.3` 在 qualification.py 内 inline 使用（L150-153）

这些值与 numeric_odds/coach_simulation 的 `1.35` 不同，是**有意的差异**（qualification 模拟更保守）。

#### (d) 修复方案与爆炸半径

**方案：创建 `src/utils/constants.py`**

```python
# src/utils/constants.py
"""共享模型参数常量"""
BASE_GOALS = 1.35
HOME_ADVANTAGE = 1.12
MAX_GOALS = 7
LAMBDA_MIN = 0.3
LAMBDA_MAX = 3.5
```

改动清单（精确到行）：

| 文件 | 改动 | 风险 |
|------|------|------|
| 新建 `src/utils/constants.py` | 定义 5 个常量 | 无 |
| `numeric_odds.py` L53-55 | 删除 3 行，加 `from src.utils.constants import ...` | 低 — 同目录 import |
| `numeric_odds.py` L213-214 | 把 inline `0.3`/`3.5` 改为 `LAMBDA_MIN`/`LAMBDA_MAX` | 低 |
| `coach_simulation.py` L65-69 | 删除 5 行，加 `from src.utils.constants import ...` | 低 — 同目录 import |
| `poisson.py` L26, L65 | 默认值 `max_goals=7` 可改为 `from constants import MAX_GOALS` 或保持不变 | 可选 — 当前不影响正确性 |

**不需要改的文件：**
- `qualification.py` — 独立参数，不受影响 ✅
- `championship.py` — 不使用这些常量 ✅
- `build_site_data.py` — 只读输出 JSON，不关心常量 ✅
- `cds_path_simulation.py` — 调用 qualification/championship，不直接使用这些常量 ✅

**爆炸半径：2 个文件 + 1 个新文件，其余 0 影响。**

---

## Investigation Log

### Phase 2 - Context Builder Analysis
**Hypothesis:** Both fixes are low-risk, local changes
**Findings:** Confirmed. P0 has zero CI footprint and comprehensive fallback. P1 involves exactly 2 files with explicit parameter passing.
**Evidence:** context_builder selected 12 files, file_search confirmed dependency chains
**Conclusion:** Confirmed — both fixes are safe with minimal blast radius

### Verification - Manual file_search
**Hypothesis:** fetch_transfermarkt_squads.py is not referenced in CI or Makefile
**Findings:** Search for "fetch_transfermarkt" found matches only in the script itself and one design doc. Zero CI references.
**Evidence:** file_search returned 8 matches across 3 files, none in .github/workflows/ or Makefile
**Conclusion:** Confirmed — script is local-only

### Verification - qualification.py independence
**Hypothesis:** qualification.py does not share model constants with numeric_odds/coach_simulation
**Findings:** qualification.py has its own _poisson_sample() with different default values (1.5, 1.0 vs 1.35)
**Evidence:** file_search for "expected_goals|LAMBDA_MIN|BASE_GOALS" shows qualification.py L138-139 uses 1.5/1.0, not 1.35
**Conclusion:** Confirmed — qualification.py is independent

## Root Cause

不是 bug，而是设计债务：

1. **P0**：Transfermarkt 脚本为了提高抓取成功率伪装了 UA，但没有合规声明。脚本本身已有完善的 fallback 机制，合规风险是唯一问题。
2. **P1**：两个模型（Elo+Poisson 基线 vs Coach 对位）在各自文件中独立定义了相同的数值参数，缺乏共享常量机制。当参数需要对齐调整时，需要同时修改两处。

## Recommendations

### P0 — 立即可做（5 分钟）

`scripts/fetch_transfermarkt_squads.py` line 87-92：
- 将 `HEADERS["User-Agent"]` 改为 `"cds4worldcup-squad-fetcher/1.0 (research-only)"`
- 在文件头 docstring 中加一行：`注意：此脚本仅供本地研究使用。Transfermarkt 数据受其 ToS 保护。`
- 如果 Transfermarkt 封杀诚实 UA → 使用 `--fallback` 模式即可

### P1 — 短期可做（30-60 分钟）

1. 新建 `src/utils/constants.py`（5 个常量）
2. `numeric_odds.py`：删除 L53-55，import from constants；L213-214 用 `LAMBDA_MIN/MAX`
3. `coach_simulation.py`：删除 L65-69，import from constants
4. `poisson.py` 的 `max_goals=7` 默认值可保持不变（两个调用者都显式传入）
5. `qualification.py` 不动（独立参数）

## Preventive Measures

- CI 中永远不应添加 `fetch_transfermarkt_squads.py` 的自动运行步骤（除非改用官方 API）
- 新模型脚本如果使用相同参数，应 import `src/utils/constants.py` 而非复制粘贴
- 考虑在 `constants.py` 中加注释说明各参数的物理含义和调参依据
