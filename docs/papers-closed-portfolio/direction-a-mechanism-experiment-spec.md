# Direction A Mechanism Experiment — Detailed Cell Design

> **Parent proposal**: `docs/papers-closed-portfolio/direction-a-1-page-proposal.md`
> **Goal**: empirically test the **3-axis anchoring-bias taxonomy** (CONTRAST vs ASSIMILATION vs INSUFFICIENT-ADJUSTMENT) for LLM-as-a-judge.
> **Headline falsifiable prediction**: Δ_assimilation > 0 (judges converge to reference anchor) AND Δ_contrast < 0 (judges adjust insufficiently toward ground-truth anchor, leaving room for stricter scoring). Signs should be opposite in both anchors. This is what the taxonomy predicts and what naive "label bias" framings do NOT predict.
> **Hard gate before running**: (a) Direction A 1-page proposal passes 5-persona review (median ≥ 5.5); (b) 8-method-paper novelty check passes (no method paper uses the same framing).
> **Author / Date**: 2026-07-05 (AutoResearch)

---

## 1. Cell design (3-way × 4 × 3 × 2 factorial)

### 1.1 Anchor type axis (4 levels)

Each anchor type corresponds to a different Tversky-Kahneman mechanism:

| Level | Prompt construction | Predicted bias | Mechanism |
|-------|---------------------|----------------|-----------|
| **A1. Leaked ground-truth** | judge prompt includes the correct answer verbatim (e.g., "home_win 1-0") in addition to the agent output | **CONTRAST** (delta < 0) | Tversky-Kahneman 1974: extreme anchor → insufficient adjustment; judge anchored high → penalizes more (P12 G2 raw observation) |
| **A2. Score-tagged reference** | judge prompt includes a reference answer with its predicted probability (e.g., "model-A scored 0.7 home_win") | **ASSIMILATION** (delta > 0) | judge converges to reference's score (Li et al. 2026 arXiv:2506.22316 prior art) |
| **A3. Confidence-cue only** | judge prompt includes ONLY a confidence label (e.g., "the model was 70% confident") without any answer | **INSUFFICIENT-ADJUSTMENT** (delta < 0 for low-confidence anchor) | confidence as numeric anchor, no content to anchor against |
| **A4. No-anchor (control)** | judge prompt includes only the agent output, no extra information | ~0 (baseline) | null condition |

### 1.2 Judge family axis (3 levels — PIT-107)

3 distinct provider/model_id combinations:

| Level | Model_id | Provider | Why this level |
|-------|----------|----------|-----------------|
| **J1. Open-source mid-tier** | `qwen3.5-122b-a10b` (or `deepseek-v4-flash` if 1st call fails) | paratera | the lenient end of the reviewer-severity spectrum (median 6.0 in P12 M8 + G1 + G2 + G3 reviews) |
| **J2. Closed-source mid-tier** | `MiniMax-M3` via minimaxi OR `gpt-oss-120b` via openrouter | minimaxi (2nd-distinct provider) | the severe end of the spectrum (median 3.0 across reviews) |
| **J3. Frontier baseline** | `claude-opus-4` (or `gpt-5` if Opus is unavailable) | anthropic / openai direct | required for venue reviewer expectations (per `llm-intelligence-blocker-verdict-2026-07-05-zh.md` §一 H5); also serves as theoretical-grounding validation per the same report §四 row 6 |

Each cell is **judged by 3 judges** (cross-judge average), giving **3 × 3 = 9** judge calls per cell (3 anchor types with anchors × 3 judges, + 1 control anchor × 3 judges = 12 judge calls per domain).

### 1.3 Domain axis (2 levels)

| Level | Domain | Source | n per cell |
|-------|--------|--------|-----------|
| **D1. Gulei 2015 emergency** | Petrochemical 4·6 incident | `legacy/p11-closed-v5-minimax-m3/experiments/h5-emergence/A/yaml/` (450 P12 sample_ids) | 30 paired (P12 M2 spec) |
| **D2. cds4worldcup match outcome** | FIFA World Cup 2022/2026 matches | `cds4worldcup/artifacts/{fixtures/cds4polymarket,plan-c}/{settlement,predictions}/` | 2 unique settlements (per `rp-investigate-top-journal-2026-07-05.md` Finding 1) — N=2 is the entire population; use all available |

### 1.4 Total cell count

- 4 anchor types × 3 judge families × 2 domains = **24 cells**
- Per cell: 30 paired samples (D1) or all available (D2) = **~30 judge calls per cell** (each sample × 4 anchor conditions × ~1.5 average judges per family after attrition)
- Total: 24 × 30 = **~720 judge calls** baseline
- Per-call wall time: 25s paratera, 30s minimaxi, 35s frontier ≈ 30s average
- Total wall time: **~6 hours serial**, or **~2 hours with 3-way parallel** (3 different provider accounts)

---

## 2. Per-cell output schema

Each cell produces a JSONL row with:

```json
{
  "anchor_type": "leaked_ground_truth | score_tagged_ref | confidence_cue | no_anchor",
  "judge_family": "open_source_mid | closed_source_mid | frontier",
  "judge_model_id": "<string>",
  "provider": "paratera | minimaxi | openrouter | anthropic | openai",
  "domain": "gulei_2015 | cds4worldcup",
  "sample_id": "<P12-NNN or cds4worldcup-match-id>",
  "anchor_text": "<exact anchor content used in this prompt>",
  "agent_output": "<the LLM output being judged>",
  "predicted_score": <0-5 float or null>,
  "parse_status": "ok | null_response | schema_mismatch | length_truncated",
  "judge_call_ms": <int>,
  "ts": "<iso8601>"
}
```

The 4 anchor types × paired design lets us compute the **central Δ** for each (anchor_type, judge, domain):

- **Δ_contrast** = mean(predicted_score | A1 − A4)  → should be NEGATIVE per CONTRAST prediction
- **Δ_assimilation** = mean(predicted_score | A2 − A4)  → should be POSITIVE per ASSIMILATION prediction
- **Δ_adjustment** = mean(predicted_score | A3 − A4)  → sign depends on whether confidence-cue is high or low; per Tversky-Kahneman, should be NON-ZERO (asymmetric adjustment)

The **headline falsifiable prediction** is the **opposite sign** of Δ_contrast and Δ_assimilation.

---

## 3. Pre-registered analysis plan

### 3.1 Primary test

For each (judge_family, domain), regress predicted_score on anchor_type (one-hot) with sample_id as a fixed effect:

```
predicted_score_ijk = μ + β1 * A1_ijk + β2 * A2_ijk + β3 * A3_ijk + γ * sample_id_k + ε_ijk
```

- **β1** (A1 leaked-gt) should be **significantly negative** (CONTRAST)
- **β2** (A2 score-tagged-ref) should be **significantly positive** (ASSIMILATION)
- **β3** (A3 confidence-cue) sign depends on cue direction; expected |β3| > 0
- **β1 + β2** should be **significantly < 0** (sum is negative; CONTRAST dominates when both anchors are present)

### 3.2 Secondary tests

- **Cross-judge consistency**: β1 from J1 vs β1 from J2 vs β1 from J3 should **all have the same sign**. If signs differ → refute Direction A's universality claim.
- **Cross-domain consistency**: β1 on D1 (Gulei) vs β1 on D2 (cds4worldcup) should be the **same sign**. If signs differ → Direction A is domain-specific, not universal.
- **Effect-size cross-judge scaling**: per `MEMORY.md "Reviewer calibration pattern — provider axis"`, provider-deviation is LARGER than within-judge variance. Expected: |β_J3| (frontier) > |β_J1| (open-source) > |β_J2| (closed-source). If ordering is different → unexpected reviewer-axis effect.

### 3.3 Pre-registration lock

This spec is locked once the 5-persona review on the Direction A 1-page proposal passes. Any post-hoc change to the analysis plan goes to `state/findings.jsonl` as `level=warn, source=direction_a_pre_reg_pivot`. Surprise = data-driven, not theory-laundering.

---

## 4. Controls and threats to validity

### 4.1 Confounds

| Confound | Mitigation |
|----------|-----------|
| **Judge parsing failures (40% on OpenRouter per G2 2nd judge)** | Use paid tier OR batched retries with `max_tokens=2048`; defensive parser; only include parse=ok rows in primary analysis (sensitivity analysis with parse=fail as 0/lower-bound) |
| **Provider severity offset (frontier judges always stricter than open-source)** | Regress on per-judge z-scores within each judge family rather than raw scores; report absolute and relative effects separately |
| **Domain-specific anchor meaning (a 0.7 reference means different things in Gulei vs football)** | Test direction consistency NOT magnitude; report per-domain β1 separately and use sign-test for cross-domain claim |
| **Carryover from prior P12/G2 reviews (the model has seen Gulei/football outputs in the review prompts)** | Use fresh sample_ids (P12-031..060 or new cds4worldcup matches) that were NOT in any prior review; document exclusion in `state/findings.jsonl` |

### 4.2 Pre-registered negative result protocol

If **any** primary test fails its sign prediction, **we commit to**:

- Report the failure in the main paper's results section (NOT in appendix).
- Re-run the analysis with the alternative sign direction as a sensitivity check.
- NOT post-hoc flip the primary sign prediction. If the sign is wrong, the sign is wrong — that's a publishable negative result, not a story-failure.

---

## 5. Execution plan (after hard gate passes)

1. **Cell construction script** (`/tmp/build_direction_a_cells.py`): iterate over 4 anchor types × 3 judge families × 2 domains, build prompt variants, write cell inputs to `experiments/direction_a/cells.jsonl`.
2. **Execution runner** (`/tmp/run_direction_a.py`): for each cell, call the corresponding provider, apply parse logic, write raw judge calls to `experiments/direction_a/raw/`.
3. **Analysis script** (`/tmp/analyze_direction_a.py`): aggregate raw calls, fit the pre-registered regression, output `experiments/direction_a/results.md` and `.json`.
4. **Re-validation**: pre-registration locked at this point. Any deviation logs to findings.jsonl.

Wall time budget:
- Cell construction: 1 hour (deterministic, 0 API).
- Execution: 6 hours serial or 2 hours 3-way-parallel (3 distinct provider accounts).
- Analysis: 30 minutes (deterministic).

---

## 6. Hard-gate checklist (must pass before execution)

- [ ] Direction A 1-page proposal passes 5-persona review (median ≥ 5.5)
- [ ] 8-method-paper depth-check completes (no YES/MARGINAL on anchoring framing)
- [ ] Frontier baseline arm provisioned (Claude-Opus-4 or GPT-5 API key in `.env`)
- [ ] P12 G2 N=30 falsification acknowledged in proposal (per honest limits §6 of 1-page proposal)
- [ ] Pre-registration committed to `state/findings.jsonl` (locked analysis plan, surprise flag)
- [ ] OpenRouter free-tier 429 mitigation in place (paid tier or batched retries)

If ANY checkbox unchecked, the experiment is NOT authorized.
