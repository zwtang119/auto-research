# P2.1 Multi-Source Signal Fusion for Multi-Agent Decision Support

> **事实核查 (2026-07-01)**：所有声明已逐条对照源码验证。SignalFusionEngine链功能完整但规模较小；数据源数量需修正。

## Goal

Systematically validate the Signal Fusion pipeline (SignalNormalizer → SignalFusionEngine → Forecaster → Calibrator) from cds-keyperson in an emergency decision context. Demonstrate that when Agents receive fused structured signals instead of raw scattered data, deliberation quality measurably improves. Perform source ablation to identify which data sources contribute most to decision quality.

## Verified Facts vs Previous Claims

| 之前声称 | 实际验证 | 影响 |
|---------|---------|------|
| "~800 lines of SignalFusionEngine" | **FALSE**: signal_normalizer(48行)+fusion_engine(71行)+forecaster(62行)+calibrator(86行)=**267行**。加pipeline(160行)=427行 | 规模大幅高估。链是功能完整的，但代码量仅声称的1/3 |
| "14 datasources" | **PARTIAL**: 14个.py文件, 但`__init__.py`和`base.py`是基础设施。实际12个数据源实现, **polymarket标记为INACTIVE** | 修正为"12 active + 1 inactive" |
| "SignalNormalizer→FusionEngine→Forecaster→Calibrator pure function chain" | **TRUE**: forecast_pipeline.py:6-9明确导入顺序, 链正常执行 | 正确 |
| "3-scenario forecast (base/downside/upside)" | **TRUE**: forecaster.py:27-31返回base/downside/upside三个文本字段 | 正确 |
| "Calibrator detects over_optimism/over_pessimism" | **TRUE**: calibrator.py:41-63, 2.0x比率阈值 | 正确 |
| "8-dimension QA" | **TRUE**: QUALITY_ASSURANCE.md:11-21, 3基础+5扩展 | 正确 |
| "5 MemoryLayer implementations" | **PARTIAL**: 6个具体类(Mem0Memory/Mem0Adapter/Vector/Graph/Hybrid/Mock), 功能各异的5个 | 近似正确 |

## Core Research Question

In multi-agent emergency deliberation, does structured signal fusion (12 active data sources → normalized signals → lens weights → 3-scenario forecasts) improve Agent decision quality compared to providing agents with raw, unfused data?

## Predetermined Configuration (set before AutoResearch starts)

**Data Source Grouping** (pre-defined to avoid ambiguity, verified against actual datasources):
```
Group A "Market Signals": polymarket(INACTIVE), finance, macro, energy → 3 active
Group B "Event Intelligence": geopolitics, sanctions, news, aviation → 4 active
Group C "Reference Knowledge": academic, wikipedia, weather, sports → 4 active
Group D "Domain Specific": (emergency/environment/culture not in actual datasources — use available: academic+weather)
```

**修正说明**：原始的Group D（emergency/environment/culture）不在cds-keyperson的实际12个数据源中。需重新设计分组或使用现有数据源的领域分类。

**Revised Grouping**:
```
Group A: finance(YahooFinance+Binance), macro(WorldBank), energy(Energi) → 5 data sources
Group B: geopolitics(GDELT+IFRCGO), sanctions(OFAC), news(RSS), aviation(OpenSky+Celestrak) → 7 data sources
Group C: academic(OpenAlex), wikipedia(Wikipedia), weather(OpenMeteo), sports(TheSportsDB) → 4 data sources
```

## Scenario: Gulei petrochemical disaster (same as PolicySim baseline)

## Milestones

| # | Milestone | Deliverable | Auto-verifiable |
|---|-----------|-------------|-----------------|
| M1 | Extract SignalFusionEngine from cds-keyperson | reusable fusion module (267行) + adapter | ✅ unit tests pass |
| M2 | Gulei scenario data enrichment | 12-source data pull for Gulei context | ✅ data completeness check |
| M3 | Controlled experiment: raw vs fused | 4 conditions × 100 MC runs = 400 runs | ✅ jsonl output count |
| M4 | Source ablation experiment | remove each group sequentially, measure impact | ✅ ANOVA |
| M5 | Bias detection validation | Calibrator over_optimism/over_pessimism detection accuracy | ✅ confusion matrix |
| M6-M9 | Paper writing | complete LaTeX | ✅ compile check |

## Quality Gates (paper-writing skill)

| Gate | Description | Required For | Corresponding Milestone | Auto-verifiable |
|------|-------------|-------------|------------------------|:--:|
| Gate 2: Experiment | Clear hypothesis, statistical test, ≥3 trials per condition | Phase 1 exit | M3 (400 MC runs) | ✅ |
| Gate 3: Structure | Compiles, ≤300 lines/file, abstract-conclusion alignment | Phase 2 exit | M6 (draft) | ✅ |
| Gate 4: Final Review | Blocking multi-round review, score trajectory | Submission ready | M8 (sprint review) | ✅ |

## Success Criteria

- [ ] Fused-signal condition shows significantly better "历史吻合度" than raw-data (p < 0.05)
- [ ] At least 1 data source group removal causes ≥20% decision quality degradation
- [ ] Calibrator bias detection accuracy ≥ 80% (validated against known biased inputs)
- [ ] Paper compiles with zero LaTeX errors

## Experiment Design

**4 conditions × 100 MC runs each:**
```
Condition A: No external data (LLM-only baseline)
Condition B: Raw unfused data (all 12 sources as unstructured text)
Condition C: Fused signals (lens weights + 3-scenario forecast as structured input)
Condition D: Fused signals + bias diagnosis (C + calibrator output as additional context)
```

**Ablation** (on Condition C, 50 runs per group):
```
Full (12 sources) → Remove Group A → Remove Group B → Remove Group C
Measure: Δ in 历史吻合度, resource utilization, response time
```

## Data Sources (read-only, verified)

- `cds-keyperson/src/backend/services/signal_fusion_engine.py` — 71行, 融合归一化信号为lens weights
- `cds-keyperson/src/backend/services/signal_normalizer.py` — 48行, 补充recency_weight
- `cds-keyperson/src/backend/services/forecaster.py` — 62行, 生成base/downside/upside三情景
- `cds-keyperson/src/backend/services/calibrator.py` — 86行, over_optimism/over_pessimism偏差检测
- `cds-keyperson/src/backend/services/forecast_pipeline.py` — 160行, 链编排文件
- `cds-keyperson/src/backend/datasources/` — 12 active datasource implementations + 1 INACTIVE(polymarket)
- **Total chain: 267 lines (427 with pipeline)** — thin but fully functional

## Known Limitations (verified, not hidden)

- SignalFusionEngine规模较小(267行), 算法简单(recency线性插值+方向加权)
- Forecaster生成的是文本描述而非数值概率——与Brier/Log Loss校准不直接兼容
- Calibrator仅检测2.0x比率偏差, 无统计检验
- polymarket数据源标记为INACTIVE
