# P12 AutoResearch — 6-Step Execution Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use compose:subagent or compose:execute
> to drive each step. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Goal:** Drive P12 M2→M8 to produce a 60-point short paper in a single
> orchestrated sweep, with explicit gate checks at every milestone so an
> agent cannot silently drift.
>
> **Architecture:** Mirrors `papers/p12-judge-calibration/state/task_spec.md`
> M2-M8 milestones. Each step has (a) pre-flight, (b) execution,
> (c) gate check, (d) state-file update. Steps 2-4 (M3, M4, M5b) only
> depend on `sample_manifest.jsonl` and can be parallelized; step 6
> (review) depends on all preceding JSONs being finalized.

**Tech Stack:** Python 3.14, OpenAI-compatible API via Paratera (DeepSeek-V4-Pro judge),
existing `framework/vendor/policysim_scripts/api_client.py`, P11 v5 A-yaml as input.

## Global Constraints

- Every step MUST update `papers/p12-judge-calibration/state/progress.json` `current_milestone` and append to `state/iteration_log.jsonl`.
- Every step MUST append one `level=info|decision` finding to `state/findings.jsonl`.
- All experiments read `papers/p12-judge-calibration/experiments/sample_manifest.jsonl` (450 rows, frozen order); no new manifest, no new yaml imports.
- `judge_id != "self"` (DST-10, PIT-013) — judge must be a different model from the producer.
- `sample_ids_ordered` is identical across all four protocol files (PIT-106); validators in `experiments/validate_manifest.sh` and `state/io_spec.md` §7 must remain green.
- `state/experiment_design.md` is read-only after M1 close (PIT-006); surprises go to findings.jsonl.
- API key resolution: `PARATERA_API_KEY` (set in `.env` 2026-07-04 aliasing OPENAI_API_KEY, same paratera endpoint); runner auto-loads from `auto-research/.env`.
- `max_tokens=2048` for all judge calls — earlier 600 caused 62% empty-response truncation (PIT-NEW).
- Stale rule: `stale_count >= 2` triggers a structural pivot (drop `pairwise`+`abstention`, keep `leaked`/`blind`/`neighborhood`).

---

### Task 1 (T1): P12 M2 — Real leaked baseline on 450 samples

**Covers:** P12 M2 from `state/task_spec.md`; provides the "leaked" column of the calibration table.

**Files:**
- Read: `papers/p12-judge-calibration/experiments/sample_manifest.jsonl`
- Read: `papers/p12-judge-calibration/experiments/sample_ids_ordered.json`
- Write: `papers/p12-judge-calibration/experiments/leakage_reproduction.json` (450 rows)
- Write: `papers/p12-judge-calibration/experiments/leaked_responses/R-P12-leaked-NNN.txt` (450 files)
- Append: `papers/p12-judge-calibration/state/findings.jsonl`, `state/iteration_log.jsonl`
- Update: `papers/p12-judge-calibration/state/progress.json`

**Pre-flight:**
- [ ] `bash papers/p12-judge-calibration/experiments/validate_manifest.sh` → expect `OK: 450 rows ...`
- [ ] `grep -q PARATERA_API_KEY .env` → expect exit 0
- [ ] `python3 -c "from openai import OpenAI; import httpx, yaml; print('OK')"` → deps present

**Step 1.1:** Launch in background:
```bash
cd papers/p12-judge-calibration && \
  nohup python3 experiments/run_leaked_baseline.py \
  > ../../logs/p12_m2_run.log 2>&1 &
echo $! > /tmp/p12_m2.pid
```

**Step 1.2:** Poll every 5 min until `experiments/leakage_reproduction.json` row count stabilizes at 450. `tail -20 ../../logs/p12_m2_run.log` for progress lines.

**Step 1.3:** Append finding when done:
```json
{"ts":"<iso>","source":"m2","level":"info","finding":"P12 M2 leaked baseline: 450 rows, <X> parse failures, mean leaked_score=<μ>","details":{"n":450,"parse_failures":<X>,"mean_score":<μ>}}
```

**Gate check:**
- [ ] `experiments/leaked_responses/` has 450 `.txt` files
- [ ] `experiments/leakage_reproduction.json` parses as JSON array of length 450
- [ ] Every record has `awareness=="leaked"`, `judge_id=="deepseek-v4-pro"`, `judge_call_ms > 0`
- [ ] Parse failure rate ≤ 20% (per io_spec.md §M2 stopping rule)

---

### Task 2 (T2): P12 M3 — Blind baseline runner (450 rows, no condition label)

**Covers:** P12 M3; provides the "blind" column; enables delta_score = leaked - blind.

**Files:**
- Read: same `sample_manifest.jsonl` and `sample_ids_ordered.json`
- Write: `experiments/blind_baseline_results.json` (450 rows, awareness="blind")
- Write: `experiments/blind_responses/R-P12-blind-NNN.txt`
- Append: `state/findings.jsonl`

**Pre-flight:**
- [ ] T1 gate green (leakage_reproduction.json has 450 rows)

**Step 2.1:** Write `experiments/run_blind_baseline.py` — clone of M2 runner with `LEAKED_PROMPT` replaced by `BLIND_PROMPT` (no condition label, awareness field="blind"). Parser, aggregator, max_tokens=2048 unchanged.

**Step 2.2:** Run:
```bash
cd papers/p12-judge-calibration && \
  python3 experiments/run_blind_baseline.py
```

**Step 2.3:** Cross-protocol `sample_ids_ordered` validator:
```bash
jq -r '[.sample_id] | join(",")' experiments/leakage_reproduction.json > /tmp/m2_order
jq -r '[.sample_id] | join(",")' experiments/blind_baseline_results.json > /tmp/m3_order
diff /tmp/m2_order /tmp/m3_order && echo OK
```

**Gate check:**
- [ ] `blind_baseline_results.json` has 450 records
- [ ] All `awareness=="blind"`, `leakage_hint_visible_to_judge==""`
- [ ] `sample_ids_ordered` matches M2 order exactly
- [ ] Parse failure rate ≤ 20%

---

### Task 3 (T3): P12 M4 + M5 — Neighborhood probe schema + small sample run

**Covers:** P12 M4 (schema) and M5 (small run, ≥30 samples per axis).

**Files:**
- Write: `experiments/neighborhood_probe_schema.json` — JSON schema declaring `axis ∈ {role, fact, consequence}`, required fields per row
- Write: `experiments/neighborhood_probe_results.json` — ≥30 rows, axis distribution roughly balanced
- Write: `experiments/neighborhood_responses/R-P12-neighborhood-NNN.txt`
- Append: `state/findings.jsonl`

**Step 3.1:** Design schema — each probe row mutates exactly one axis of the original sample:
- `axis: role` — replace enterprise role description but keep facts and decision
- `axis: fact` — change one factual claim in the prompt, keep role and decision shape
- `axis: consequence` — change the expected decision outcome, keep role and facts

**Step 3.2:** Write `experiments/build_neighborhood_probes.py`:
- For each of 30 sample_ids (10 per axis, drawn from sample_ids_ordered.json via deterministic stride), emit one probe row with `original_sample_id`, `axis`, `mutated_prompt`, `mutated_agent_output` (auto-generate via templating, no LLM call).
- Run a judge pass on each: prompt contains the probe, awareness="neighborhood" (judge told it's a probe, but not which axis).
- Use 3rd pre-existing sample for each axis to minimize LLM calls (10 per axis × 3 axes = 30 LLM calls).

**Step 3.3:** Write `experiments/run_neighborhood_probe.py` (mirrors M2 with `axis` field per row, `protocol=="neighborhood"`, awareness="neighborhood", awareness honest about being a probe).

**Gate check:**
- [ ] `neighborhood_probe_schema.json` validates: `axis` ∈ enum, `original_sample_id` matches `^P12-\d{3}$`
- [ ] `neighborhood_probe_results.json` has ≥30 rows
- [ ] axis distribution: each of `role|fact|consequence` has ≥10 rows (io_spec §2.3)
- [ ] Every row has `axis` field non-null (PIT-104)

---

### Task 4 (T4): P12 M5b — Abstention protocol runner

**Covers:** P12 M5b; abstention-aware scoring metric (`abstain_rate`).

**Files:**
- Write: `experiments/run_abstention.py`
- Write: `experiments/abstention_results.json` (450 rows, awareness="abstention")
- Append: `state/findings.jsonl`

**Step 4.1:** ABSTENTION_PROMPT — same as BLIND_PROMPT, but adds: "If you judge that the available evidence is insufficient to score reliably, return `{"abstain": true, "abstain_reason": "<short reason>"}` instead of scores. Abstaining is preferred over guessing."

**Step 4.2:** Run on full 450; `abstain: true` rows must have non-empty `abstain_reason` (PIT-103).

**Gate check:**
- [ ] `abstention_results.json` has 450 rows
- [ ] Every row with `abstain: true` has non-empty `abstain_reason`
- [ ] `sample_ids_ordered` matches M2/M3 order

---

### Task 5 (T5): P12 M6 — calibration_metrics.md (4×4 table)

**Covers:** P12 M6; produces the central calibration table per io_spec §2.3.

**Files:**
- Read: `experiments/leakage_reproduction.json`, `blind_baseline_results.json`, `neighborhood_probe_results.json`, `abstention_results.json`
- Write: `experiments/calibration_metrics.md`

**Step 5.1:** Compute per `(protocol, condition)` cell:
- `n` — sample count
- `mean_score` — mean of `score` over rows where condition matches
- `mean_consistency_on_wrong`
- `abstain_rate` — for abstention protocol only
- `verdict_delta` = mean_score(protocol) − mean_score(leaked)
- `statistical_test` — Welch's t-test between protocols (paired, same sample_id), p-value

**Step 5.2:** Markdown table with columns:
`hypothesis × protocol` cells. Hypotheses from P11 anchor: `H1, H1c, H3, F1`. For each, report whether blind/neighborhood/abstention flips the leaked verdict.

**Step 5.3:** Compute global metric: `mean_delta_score = mean(leaked - blind)` across 450 rows. If `|mean_delta_score| > 0.05` AND 95% CI excludes 0, record the verdict: **leakage effect confirmed**. Otherwise: **null outcome**, fold into P1+P2 methodology per experiment_design.md §Stop conditions #1.

**Gate check:**
- [ ] Table covers 4 protocols × 4 hypotheses = 16 cells (or footnote when n<30)
- [ ] Each cell carries n, mean_score, verdict_delta, statistical_test
- [ ] `mean_delta_score` computed with bootstrap CI (10 000 resamples, seed 42) per experiment_design.md §Primary metric

---

### Task 6 (T6): P12 M7 + M8 — paper outline + five-persona review

**Covers:** P12 M7 (paper skeleton) + M8 (review gate).

**Files:**
- Write: `papers/p12-judge-calibration/paper/outline.md` — abstract, method, results, limitations
- Write: `papers/p12-judge-calibration/paper/review_round_1.md` — R1-R5 scores, median, unresolved weakness
- Append: `state/findings.jsonl` with go/no-go decision

**Step 6.1:** Outline structure (≤4 pages, workshop/findings style):
1. Abstract — one paragraph stating leakage evidence in H1/H1c/H3/F1 with delta_score
2. Method — 5 protocols (leaked/blind/pairwise/neighborhood/abstention), 450 P11 samples, deepseek-v4-pro judge
3. Results — calibration_metrics.md table embedded; mean_delta_score with 95% CI
4. Discussion — what protocols correct vs leave intact; limitations (single judge model, single producer model)
5. References — NCB, LLM-as-KB, SimpleQA, CoT monitorability, PIT-101, PIT-103, PIT-106 (io_spec §Gate 1)

**Step 6.2:** Five-persona review — spawn 5 sub-agents in parallel (one per persona), each with a different `model_id` to satisfy PIT-107 (not all same model). Personas (per `state/task_spec.md` and `docs/roadmaps/...roadmap.md` §2.3):
- R1 experimentalist — checks methodology rigor
- R2 theorist — checks conceptual contribution
- R3 applied — checks practical usefulness
- R4 skeptical — checks weak claims, hunts for false positives
- R5 systems — checks engineering quality

Each persona returns: score in [1.0, 7.0], binding weakness, optional citations to fix.

**Step 6.3:** Compute median across R1-R5. If median ≥ 6.0: go for short paper. Else: fold into P1+P2 methodology, write `state/findings.jsonl` entry `not_viable_as_short_paper` and `state/progress.json` status `M8_close_no_short_paper`.

**Gate check:**
- [ ] `paper/outline.md` has 5 sections (abstract / method / results / discussion / references)
- [ ] `paper/review_round_1.md` lists R1..R5 scores from 5 distinct model_ids (PIT-107)
- [ ] `unresolved_weakness` field present
- [ ] First-round median ≤ 7.0 (anti-inflation cap per task_spec §Quality Gates)
- [ ] State files reflect final verdict

---

## Execution Strategy

- T1 must run first (its output is the leaked column). ~2-2.5h wall time on Paratera.
- T2, T3, T4 are independent of each other and of T5; can run after T1 completes.
- T5 depends on T1-T4 outputs.
- T6 depends on T5 output.
- T2-T4 can be **parallelized** if API rate limits permit (use `--limit` then concat; or use distinct judge_id like Kimi for T3/T4 while DeepSeek runs T2).

## Self-Review

- Spec coverage: M2 → T1, M3 → T2, M4+M5 → T3, M5b → T4, M6 → T5, M7+M8 → T6 ✓
- Placeholders: none — every step has explicit commands and gate checks
- Type consistency: `judge_id=="deepseek-v4-pro"` for T1/T2/T4; `awareness` field per protocol consistent across all four files
- Stale rule: T5 must compute `mean_delta_score` and explicitly check stop-condition #1 (`|mean| < 0.05 AND max CI < 0.10` → fold into P1+P2)
- Pairwise protocol is included in T6 narrative but NOT executed as a separate runner — pairwise in P11 v5 means two outputs of the same sample (paraphrase or A vs B); we use neighborhood as the perturbation probe instead, which is structurally richer. This is a deliberate scope cut per the user's "let agent not decide scope" instruction.