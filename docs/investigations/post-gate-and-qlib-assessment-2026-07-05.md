# Post-Gate and Qlib Relevance Assessment

Date: 2026-07-05

## Executive Judgment

The other AI's report is directionally useful, but its "PASS" labels are too coarse.

Corrected status:

| Gate | Correct status | Why |
|---|---|---|
| G1 PA-degrades-fidelity abstract | **Fail** | R1=4.0 and R3=4.0, below the >=5.5 gate. Main blockers are subjective-fidelity reliability (rho=0.19), single scenario, and parse/attrition concerns. Keep as a P11 workshop pillar, not a standalone top-paper path. |
| G3 dual-ledger crosswalk | **Partial pass** | Schema sub-gates passed: 92.9% AR-to-CWCUP field coverage and no fatal enum mismatch. But the Brier sub-gate did **not** pass: `g3_brier_pass=false`, synthetic-only. The repo does contain settlement/prediction artifacts; the missing step is version-paired settlement replay. |
| G2 calibration paradox | **Strong signal, not full gate pass** | Direction is strong across two judge/provider families: first judge n=10, delta=-1.284, CI [-1.461, -1.078]; second judge n=6, delta=-3.667, CI [-4.000, -3.000]. But the stated gate was N=30 paired + second judge. Current second-judge paired n is only 6. |

The best next paper path is therefore **G2 calibration paradox**, but only after a short completion run to satisfy the original gate. Treat the present result as "high-value precondition met", not as final evidence.

## What Was Misleading In The Prior Feedback

1. **"G2 passed" is overstated.**
   It passed the sign/CI direction check, but not the N=30 paired requirement. It is a strong replication signal, not yet the gate as written.

2. **"G3 passed" hides the Brier failure.**
   The JSON explicitly records `g3_brier_pass=false`. The text says settlement records were not exported, but local inspection found:

   - `/Users/tangzw119/Documents/GitHub/cds4worldcup/artifacts/plan-c/settlement/wc2026-a-m01-mex-rsa.settlement_record.yaml`
   - `/Users/tangzw119/Documents/GitHub/cds4worldcup/artifacts/fixtures/cds4polymarket/settlement/wc2022-g-arg-ksa.settlement_record.yaml`

   So the issue is not "no settlement data exists"; it is that the G3 script did not pair the correct prediction-card version with the settlement replay.

3. **The settlement/prediction version mismatch matters.**
   The `wc2026-a-m01-mex-rsa` settlement computes Brier from `p=[0.55, 0.27, 0.18]`, matching the v0.1 prediction card:

   - `.../predictions/mvpa/wc2026-a-m01-mex-rsa.prediction_card.yaml`

   But the v0.2 card has `0.62/0.23/0.15`. A Brier replay must bind settlement to the exact locked prediction artifact, not just the same `match_id`.

## Paper Direction Ranking After Gates

| Rank | Direction | Status | Recommended action |
|---:|---|---|---|
| 1 | **G2 calibration paradox / blind > leaked judge effect** | Highest signal. Cross-provider effect direction is strong, but underpowered. | Complete N=30 paired and fill second-judge missing pairs. Then write workshop/Findings-style paper. |
| 2 | **G3 dual-ledger schema reconciliation** | Real methods value, but currently only schema evidence. | Fix prediction-card/settlement pairing and run real Brier replay. Use as methods paper or G2 appendix/validation section. |
| 3 | **P11 / PA-degrades-fidelity** | Standalone gate failed. | Use as supporting negative result or workshop pillar, not flagship claim. |

## Qlib Assessment

`/Users/tangzw119/Documents/GitHub/0ref/qlib` is a full Microsoft Qlib checkout: an AI-oriented quantitative investment platform with workflow, recorder, point-in-time data, feature, model, and backtest components. External anchors confirm this framing: Qlib is presented as an AI-oriented quant platform, and RD-Agent(Q) is the related multi-agent quant R&D system.

Useful references:

- Qlib paper: https://arxiv.org/abs/2009.11189
- Qlib GitHub: https://github.com/microsoft/qlib
- RD-Agent(Q): https://arxiv.org/abs/2505.15155

### For `auto-research`

Recommendation: **do not import qlib**.

Reason:

- Auto-research's core assets are judge calibration, evidence ledgers, schema contracts, and audit traces.
- Qlib's strongest modules are quant-market workflow, alpha metrics, point-in-time finance data, and portfolio backtesting.
- Importing qlib would add a large dependency surface and blur the current JSONL/YAML evidence-ledger reproducibility story.

Potentially borrow only the idea of `Experiment -> Recorder -> artifacts/metrics/tags`, not the package.

### For `cds4worldcup`

Recommendation: **selective reuse is useful**, but vendor small ideas/functions rather than installing qlib.

Most useful parts:

1. `qlib.contrib.eva.alpha.py`
   - IC / Rank-IC / long-short precision and return ideas can be adapted to match-outcome probability vectors.

2. `qlib.contrib.evaluate.py::risk_analysis`
   - Useful for evaluating betting-edge or prediction-edge time series, with tournament-specific scaling.

3. Qlib Recorder pattern
   - Use the naming discipline: immutable `experiment_id`, per-run `recorder_id`, logged params/metrics/artifacts.
   - Do not replace the existing YAML schemas or add MLflow unless a future paper explicitly needs sweep dashboards.

4. Point-in-time semantics
   - Conceptually useful for "what was knowable before kickoff" versus post-match settlement. This maps well to Red/Yellow/Green source boundaries.

Avoid:

- `backtest/exchange.py` and `executor.py`: equities-specific.
- `data.ops.py`: heavy calendar/instrument feature DSL, not appropriate for soccer match ledgers.
- benchmark models, RL, LightGBM/XGBoost examples: not relevant to the current paper claims.

## Recommended Next Steps

1. **Finish G2 properly.**
   Run the missing N=30 paired expansion and ensure the second judge has paired leaked/blind scores for all target samples. Current n=6 is not enough to claim the original gate.

2. **Repair G3 Brier replay.**
   Build a version-pair resolver:

   - input: `match_id`
   - select the locked prediction card whose probabilities match settlement calculation
   - recompute Brier/log-loss
   - emit mismatch warnings when v0.1/v0.2 cards disagree

3. **Use qlib only to strengthen cds4worldcup validation.**
   Add qlib-inspired metrics after Brier/log-loss: rank correlation, top-class precision, long/short-style directional accuracy, and a small risk/edge summary. This improves validation quality, not novelty by itself.

4. **Paper plan after the fixes**
   If G2 N=30 remains negative across two judges, write the **calibration paradox paper** first. G3 becomes the reproducibility/schema appendix. qlib-inspired cds4worldcup metrics can become an external validation subsection, not the main contribution.

## Bottom Line

The portfolio improved after the gates, but not as much as the prior AI's table implies.

The real state is:

- G1 failed cleanly.
- G3 schema bridge is real but Brier replay is unfinished.
- G2 is the best discovery, but still needs the N=30 completion run before it should be treated as a publishable claim.

`qlib` is useful as a **validation-pattern library for cds4worldcup**, not as a core dependency for auto-research.
