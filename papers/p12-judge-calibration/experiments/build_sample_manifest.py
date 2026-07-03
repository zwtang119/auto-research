#!/usr/bin/env python3
"""P12 M1 sample-manifest builder.

Reads P11 v5 A-yaml files at
  ../legacy/p11-closed-v5-minimax-m3/experiments/h5-emergence/A/yaml/
filters to 3 standard conditions (inner_monologue, no_think, pure_analysis),
emits experiments/sample_manifest.jsonl + experiments/sample_ids_ordered.json
in the frozen order described in state/experiment_design.md.

No LLM calls. Idempotent: re-running yields byte-identical output
(other than `imported_at` timestamp) provided the source files are unchanged.

Run from .../papers/p12-judge-calibration/:
    python experiments/build_sample_manifest.py
"""
from __future__ import annotations
import hashlib
import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# --- Paths (resolved relative to this file, location-independent) -----------
P12_ROOT = Path(__file__).resolve().parent.parent
# P12 sits at .../auto-research/papers/p12-judge-calibration/; two levels up is auto-research.
AUTO_ROOT = P12_ROOT.parent.parent
P11_ROOT = (AUTO_ROOT / "legacy" / "p11-closed-v5-minimax-m3")
P11_A_YAML = (P11_ROOT / "experiments" / "h5-emergence"
                       / "A" / "yaml")
P11_METADATA = P11_ROOT / "experiments" / "h5-emergence" / "metadata.json"

EXPERIMENTS = P12_ROOT / "experiments"
MANIFEST_PATH = EXPERIMENTS / "sample_manifest.jsonl"
FROZEN_PATH = EXPERIMENTS / "sample_ids_ordered.json"

# --- Frozen enumeration -----------------------------------------------------
STANDARD_CONDITIONS = ["inner_monologue", "no_think", "pure_analysis"]
ENTERPRISES_ALPHA = ["ISPACE", "LANDSPACE", "SPACETIMETECH"]
RUN_IDS = [f"{i:03d}" for i in range(1, 51)]   # 001..050

TZ_UTC8 = timezone(timedelta(hours=8))


def now_iso() -> str:
    return datetime.now(TZ_UTC8).strftime("%Y-%m-%dT%H:%M:%S+08:00")


def sha12(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:12]


def producer_model() -> str:
    """Read producer model from P11 metadata if available; fallback explicit."""
    try:
        meta = json.loads(P11_METADATA.read_text())
        return meta["experiments"]["A"]["model"]
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        return "DeepSeek-V4-Flash"


def build_rows() -> list[dict]:
    prod = producer_model()
    rows: list[dict] = []
    counter = 0
    for cond in STANDARD_CONDITIONS:
        for ent in ENTERPRISES_ALPHA:
            for rid in RUN_IDS:
                fname = f"{cond}_{ent}_run{rid}.yaml"
                full = P11_A_YAML / fname
                if not full.exists():
                    print(f"warn: skipping missing {fname}", file=sys.stderr)
                    continue
                counter += 1
                rel = str(full.relative_to(AUTO_ROOT))
                rows.append({
                    "sample_id": f"P12-{counter:03d}",
                    "source_path": rel,
                    "source_sha256_prefix": sha12(full),
                    "original_condition": cond,
                    "original_enterprise": ent,
                    "original_run_id": rid,
                    "producer_model": prod,
                    "judge_model_planned": "DeepSeek-V4-Flash",
                    "condition_visible_to_judge": False,
                    "imported_at": now_iso(),
                })
    return rows


def main() -> int:
    EXPERIMENTS.mkdir(parents=True, exist_ok=True)
    rows = build_rows()
    if len(rows) != 450:
        print(
            f"warn: produced {len(rows)} rows, expected 450",
            file=sys.stderr,
        )
    with MANIFEST_PATH.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with FROZEN_PATH.open("w", encoding="utf-8") as f:
        json.dump([r["sample_id"] for r in rows], f,
                  ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"wrote {len(rows)} rows -> {MANIFEST_PATH}")
    print(f"wrote {len(rows)} ids  -> {FROZEN_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
