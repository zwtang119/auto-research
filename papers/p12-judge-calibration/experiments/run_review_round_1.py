#!/usr/bin/env python3
"""P12 M8 — Five-persona review runner.

Reads `experiments/calibration_metrics.md` + `paper/outline.md`, then calls
5 distinct model reviewers via Paratera (PARATERA_API_KEY from .env) and
writes scores + binding weaknesses to `paper/review_round_1.md`.

PIT-107: 5 distinct model_ids required.
PIT-107 (anti-inflation): first round ≤ 7.0.
Roadmap §11: median ≥ 6.0 → go for short paper; else fold into P1+P2.

Reviewer set (smoke-tested 2026-07-04 — all OK via PARATERA_API_KEY):
  R1 experimentalist → deepseek-v4-pro
  R2 theorist        → kimi-k2.5
  R3 applied         → MiniMax-M3
  R4 skeptical       → deepseek-v4-flash
  R5 systems         → qwen3.5-122b-a10b
"""
from __future__ import annotations
import json
import os
import re
import statistics
import sys
import time
from pathlib import Path

P12_ROOT = Path(__file__).resolve().parent.parent
EXPERIMENTS = P12_ROOT / "experiments"
PAPER = P12_ROOT / "paper"
CALIBRATION_MD = EXPERIMENTS / "calibration_metrics.md"
OUTLINE_MD = PAPER / "outline.md"
OUT_REVIEW_MD = PAPER / "review_round_1.md"

# (persona label, model_id, system-prompt flavor)
REVIEWERS = [
    ("R1 experimentalist (methodology rigor)", "deepseek-v4-pro",
     "You are R1, an experimentalist. Score methodology rigor: pre-registration, "
     "control conditions, sample size relative to claim strength, statistical test choice."),
    ("R2 theorist (conceptual contribution)", "kimi-k2.5",
     "You are R2, a theorist. Score conceptual contribution: is the 5-protocol set "
     "a real advance over prior calibration work, or a re-branding?"),
    ("R3 applied (practical usefulness)", "MiniMax-M3",
     "You are R3, an applied researcher. Score practical usefulness: would a practitioner "
     "actually use this protocol set? Are the metrics actionable?"),
    ("R4 skeptical (false-positive hunting)", "deepseek-v4-flash",
     "You are R4, a skeptical reviewer. Hunt for false positives: does the leakage "
     "claim hold up? Is the partial-data verdict defensible?"),
    ("R5 systems (engineering quality)", "qwen3.5-122b-a10b",
     "You are R5, a systems reviewer. Score engineering quality: pipeline scripts, "
     "manifest validators, unit tests, schema enforcement, reproducibility."),
]

VENDOR_ROOT = P12_ROOT.parent.parent / "framework" / "vendor"
POLICYSIM_SCRIPTS = VENDOR_ROOT / "policysim_scripts"
POLICYSIM_CONFIG = VENDOR_ROOT / "policysim_config" / "experiment-config.yaml"


def _load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        os.environ.setdefault(k, v)


def parse_score_and_weakness(text: str) -> tuple[float | None, str]:
    """Parse JSON {\"score\": N, \"weakness\": \"...\"}; fall back to regex."""
    if text:
        m = re.search(r"\{[^{}]*\"score\"\s*:\s*([0-9.]+)[^{}]*\"weakness\"\s*:\s*\"([^\"]*)\"[^{}]*\}", text)
        if m:
            return float(m.group(1)), m.group(2)
        m = re.search(r"SCORE:\s*([0-9.]+)", text)
        w_match = re.search(r"WEAKNESS:\s*(.+)", text, re.DOTALL)
        if m:
            return float(m.group(1)), (w_match.group(1).strip() if w_match else "(none)")
    return None, "(unparseable response)"


def build_prompt(persona_flavor: str, calibration_md: str, outline_md: str) -> str:
    return f"""You are reviewing a paper draft for a workshop / findings-track submission.

# Paper claim (P12)
The paper claims that blind, pairwise, neighborhood-probe, and abstention-aware
judging protocols can each correct a false-positive conclusion that a label-aware
(leaked) judge produces on P11's role-conditioned agent outputs. The contribution
is the protocol set, not a leaderboard.

# Calibration summary (excerpt of experiments/calibration_metrics.md)
```markdown
{calibration_md[:6000]}
```

# Paper outline (paper/outline.md)
```markdown
{outline_md[:4000]}
```

# Your persona
{persona_flavor}

# Your task
Return ONLY this JSON (no markdown, no other text):
{{"score": <integer 1-7>, "weakness": "<one sentence, 10-30 words>"}}

Score 1-7 per roadmap §11 anti-inflation cap (first round ≤ 7.0).
"""


def main() -> int:
    _load_env_file(P12_ROOT.parent.parent / ".env")

    if not CALIBRATION_MD.exists() or not OUTLINE_MD.exists():
        print(f"FATAL: missing {CALIBRATION_MD} or {OUTLINE_MD}", file=sys.stderr)
        return 2

    calibration_md = CALIBRATION_MD.read_text()
    outline_md = OUTLINE_MD.read_text()

    sys.path.insert(0, str(POLICYSIM_SCRIPTS))
    from api_client import load_config, call_model
    cfg = load_config(str(POLICYSIM_CONFIG))

    # Pre-flight
    for _, model_id, _ in REVIEWERS:
        provider = cfg["models"][model_id]["provider"]
        api_key_env = cfg["api_endpoints"][provider]["api_key_env"]
        if not os.environ.get(api_key_env):
            print(f"FATAL: env ${api_key_env} not set for {model_id}", file=sys.stderr)
            return 2

    results = []
    for persona_label, model_id, flavor in REVIEWERS:
        prompt = build_prompt(flavor, calibration_md, outline_md)
        t0 = time.time()
        try:
            content, usage = call_model(
                cfg, model_id,
                [{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=2048,   # deepseek-v4-pro uses thinking-mode that eats tokens; 512 truncates JSON
                prompt_stage="p12_m8_review",
            )
            elapsed = time.time() - t0
            score, weakness = parse_score_and_weakness(content)
            results.append({
                "persona": persona_label,
                "model_id": model_id,
                "score": score,
                "weakness": weakness,
                "raw_response_preview": (content or "")[:200],
                "elapsed_s": round(elapsed, 1),
                "completion_tokens": (usage or {}).get("completion_tokens", 0),
                "ok": score is not None,
            })
            print(f"  {model_id:25s} -> score={score} ({elapsed:.1f}s)", flush=True)
        except Exception as e:
            elapsed = time.time() - t0
            results.append({
                "persona": persona_label,
                "model_id": model_id,
                "score": None,
                "weakness": f"(API error: {type(e).__name__}: {str(e)[:120]})",
                "raw_response_preview": "",
                "elapsed_s": round(elapsed, 1),
                "completion_tokens": 0,
                "ok": False,
            })
            print(f"  {model_id:25s} -> FAIL ({elapsed:.1f}s) {type(e).__name__}", flush=True)

    scores = [r["score"] for r in results if r["score"] is not None]
    median_score = statistics.median(scores) if scores else None
    max_score = max(scores) if scores else None

    # Write review_round_1.md (overwrite the author-derived stub)
    lines = []
    lines.append("# P12 Review Round 1 — Five-Persona Review")
    lines.append("")
    lines.append(f"> Generated {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} by "
                 f"`experiments/run_review_round_1.py`.")
    lines.append("> 5 distinct model_ids (PIT-107); all via PARATERA_API_KEY.")
    lines.append("> Pair with `experiments/calibration_metrics.md` and `paper/outline.md`.")
    lines.append("")
    lines.append("## 1. Reviewer set")
    lines.append("")
    lines.append("| # | Persona | model_id | score | binding weakness |")
    lines.append("|---|---------|----------|-------|------------------|")
    for r in results:
        score_str = f"{r['score']:.1f}" if r['score'] is not None else "n/a"
        lines.append(f"| {r['persona'].split()[0]} | {r['persona']} | `{r['model_id']}` | "
                     f"{score_str} | {r['weakness']} |")
    lines.append("")
    lines.append("## 2. Aggregate")
    lines.append("")
    if scores:
        lines.append(f"- Median score across R1..R5: **{median_score:.1f}**")
        lines.append(f"- Mean score: {statistics.mean(scores):.2f}")
        lines.append(f"- Max score: {max_score:.1f}")
        lines.append(f"- Per-reviewer latency: min={min(r['elapsed_s'] for r in results):.1f}s, "
                     f"max={max(r['elapsed_s'] for r in results):.1f}s")
    else:
        lines.append("- All reviewers failed; no median available.")
    lines.append("")
    lines.append("## 3. Verdict")
    lines.append("")
    if median_score is None:
        lines.append("- **Verdict**: `inconclusive` — all reviewers errored. Rerun after fixing API issues.")
    elif median_score >= 6.0:
        lines.append(f"- **Verdict**: `go_short_paper` (median ≥ 6.0)")
        lines.append("- Action: proceed to polish M7 outline into a 4-page workshop submission.")
    else:
        lines.append(f"- **Verdict**: `fold_into_p1_p2` (median < 6.0)")
        lines.append("- Action: stop P12 standalone paper effort; methodology becomes part of "
                     "P1+P2 evidence-ledger work.")
    lines.append("")
    lines.append("## 4. Anti-inflation cap compliance (roadmap §11)")
    lines.append("")
    if max_score is not None and max_score <= 7.0:
        lines.append(f"- Max reviewer score = {max_score:.1f} ≤ 7.0 ✓ (anti-inflation cap)")
    elif max_score is not None:
        lines.append(f"- **WARNING**: max reviewer score = {max_score:.1f} > 7.0. Cap violated; "
                     "down-weight this round and re-run with stricter prompt.")
    lines.append("")
    lines.append("## 5. `unresolved_weakness` (single most-cited)")
    lines.append("")
    if results:
        # Pick the highest-scoring reviewer's binding weakness (least critical but
        # still named) — or the lowest-scoring if median is below threshold.
        sorted_results = sorted(results, key=lambda r: r["score"] if r["score"] is not None else 99)
        if median_score is not None and median_score < 6.0:
            lines.append(f"> {sorted_results[0]['weakness']}  *(from {sorted_results[0]['model_id']}, "
                         f"score={sorted_results[0]['score']:.1f})*")
        else:
            lines.append(f"> {sorted_results[-1]['weakness']}  *(from {sorted_results[-1]['model_id']}, "
                         f"score={sorted_results[-1]['score']:.1f})*")
    lines.append("")
    lines.append("## 6. Calibration context (read `experiments/calibration_metrics.md` for full table)")
    lines.append("")
    lines.append("Auto-excerpt of Section 3 verdict from calibration_metrics.md:")
    lines.append("```")
    cal_section3 = ""
    in_section3 = False
    for line in calibration_md.splitlines():
        if line.startswith("## 3."):
            in_section3 = True
        elif in_section3 and line.startswith("## 4."):
            break
        elif in_section3:
            cal_section3 += line + "\n"
    lines.append(cal_section3.rstrip())
    lines.append("```")
    lines.append("")
    lines.append("## 7. Required follow-up actions")
    lines.append("")
    if median_score is not None and median_score >= 6.0:
        lines.append("1. Polish `paper/outline.md` into a 4-page workshop draft")
        lines.append("2. Add a \"Reproducibility\" appendix listing exact commands")
        lines.append("3. Cite the 5 reviewer models in the methodology section")
    else:
        lines.append("1. Record this verdict in `state/findings.jsonl` (level=decision, "
                     "source=p12_m8_review_round_1)")
        lines.append("2. Update `state/progress.json`: status → `m8_close_no_short_paper`")
        lines.append("3. Carry the 5-protocol design into P1+P2 evidence-ledger methodology")
    lines.append("")

    OUT_REVIEW_MD.write_text("\n".join(lines))
    print(f"\nWrote {OUT_REVIEW_MD}")

    # Also save raw results as JSON for downstream scripts
    results_path = EXPERIMENTS / "review_round_1_results.json"
    results_path.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"Wrote {results_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())