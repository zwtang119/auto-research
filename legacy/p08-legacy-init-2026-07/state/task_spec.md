# P1.2 Prediction Markets as Calibration Fields for LLM Agents

> **事实核查 (2026-07-01)**：所有声明已逐条对照源码验证。关键修正：AB测试数据丰富但Brier计算需手动实现；Factor Ledger仅设计无代码。

## Goal

Propose and validate a methodology that uses prediction markets (Polymarket) as a calibration field for LLM multi-agent deliberation. Leverage 15+ rounds of A/B testing data (v02-v16, documented in 17-round analysis report) from cds4polymarket.

## Verified Facts vs Previous Claims

| 之前声称 | 实际验证 | 影响 |
|---------|---------|------|
| "17 rounds of A/B testing" | **PARTIAL**: 27个实验目录, v02-v16=15版本号, 分析报告称"17轮" | 数据充分, 表述修正 |
| "Brier/Log Loss calibration" | **PARTIAL**: Schema已定义, YAML中有手工计算值(1个settlement), **Python自动计算函数不存在** | M1/M4的实现工作量增加 |
| "Factor Ledger" | **PARTIAL**: 设计文档完整(81行concept doc), **Python代码0行实现** | 不可声称"已有Factor Ledger" |
| "Polymarket Gamma API" | **PARTIAL**: 仅调用`/events`端点, 无rate limit/retry, 每领域最多5个事件 | 基础但够用 |
| "Judge calibration Gold-H/M/L" | **TRUE**: calibration_lib.py:34-38, 3个黄金样本用于Judge漂移检测 | 正确 |
| "6 pipelines" | **TRUE**: run_6_pipelines.py:22-29, 6领域×1问题 | 正确 |

## Core Research Question

Can prediction markets serve as an external calibration field for LLM agent simulations? Specifically: (1) Does domain knowledge injection improve Agent prediction quality relative to market consensus? (2) What fraction of factors can be evaluated against real outcomes? (3) Does the knowledge writeback loop show measurable improvement?

## Milestones (revised with verified facts)

| # | Milestone | Deliverable | Auto-verifiable | 备注 |
|---|-----------|-------------|-----------------|------|
| M1 | Extract A/B test quantitative results | metrics table per domain | ✅ CSV parsing | AB测试数据充分(27目录) |
| M1.5 | **Implement Brier/Log Loss computation** | `calc_brier.py` (~50行) | ✅ unit test | Schema已有, 需实现计算函数 |
| M2 | Select 3-5 case study events | event_candidates.json with ranking | ✅ ranking scores | ⚠️ 人工checkpoint |
| M3 | Factor evaluation analysis | per-domain assessable factor count | ✅ boolean counts | Factor Ledger设计存在, 需按设计评估 |
| M4 | Knowledge writeback effectiveness | before/after comparison on WTI loop | ✅ before/after diff | Brier计算需M1.5完成后可用 |
| M5 | Cross-domain robustness | 6-domain comparison | ✅ ANOVA | |
| M6 | Draft paper (Phase 1, target 6.0): structure + lit review + first complete draft | LaTeX compiles clean, ≥20 refs, all sections present | ✅ compile check | |
| M7 | Deep Improvement (Phase 2, target 7.5): experiment integration + figures + tables | ≥6 figures, ≥10 tables, abstract-conclusion aligned | ✅ figure/table count | |
| M8 | Sprint review (Phase 3, target 8.5): multi-round peer review loop | ≥3 review rounds, score trajectory documented | ✅ score diff check | |
| M9 | Final polish & camera-ready | zero LaTeX errors, all references verified | ✅ compile check | |

## Success Criteria

- [ ] Agent prediction quality non-inferior to market consensus (metric TBD after M1.5)
- [ ] ≥60% of assessable factors evaluable via event outcomes
- [ ] Knowledge writeback shows measurable improvement in ≥1 dimension
- [ ] Cross-domain results consistent direction (≥4/6 domains)
- [ ] M6 compile clean, M9 zero LaTeX errors

## Quality Gates (paper-writing skill)

| Gate | Description | Required For | Corresponding Milestone | Auto-verifiable |
|------|-------------|-------------|------------------------|:--:|
| Gate 2: Experiment | Clear hypothesis, statistical test, ≥3 trials per condition | Phase 1 exit | M3 (simulation runs) | ✅ |
| Gate 3: Structure | Compiles, ≤300 lines/file, abstract-conclusion alignment | Phase 2 exit | M6 (draft) | ✅ |
| Gate 4: Final Review | Blocking multi-round review, score trajectory | Submission ready | M8 (sprint review) | ✅ |

## Data Sources (read-only, verified)

- `cds4polymarket/ab-test/analysis/CDS_AB_Test_17轮综合分析报告.md` — 综合分析报告
- `cds4polymarket/ab-test/experiments/` — 27个实验目录 (v02-v23r)
- `cds4polymarket/calibration_lib.py:34-38` — Gold-H/M/L 3样本Judge校准
- `cds4polymarket/run_6_pipelines.py:22-29` — 6领域配置
- `cds4polymarket/src/backend/datasources/polymarket.py:64` — Polymarket `/events` API (基础实现, 无rate limit)

## Known Gaps (verified, not hidden)

- Brier/Log Loss: Schema defined in `settlement_record.schema.yaml:25-35`, 1 manual example in YAML, **no Python auto-computation exists** → M1.5 to implement
- Factor Ledger: `docs/concepts/factor-ledger-and-decision-sentinel.md` (81行设计), **0行Python代码** → use design spec to guide manual factor evaluation in M3
- Polymarket API: basic single-endpoint, 15s timeout, per-domain max 5 events

## Predetermined Human Checkpoint

After M2 (event selection): Human reviews top-5 case study candidates ranked by Agent. Single checkpoint, not interactive.

## Stale Detection

- `stale_count >= 2`: Pivot — change event criteria, expand domains, try different metrics
- `stale_count >= 4`: Flag human — AB data may be insufficient for claimed conclusions

## Target Venue

EMNLP 2027 / AAAI 2027 (AI + evaluation methodology track)
