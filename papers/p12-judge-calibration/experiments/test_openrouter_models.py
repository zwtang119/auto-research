#!/usr/bin/env python3
"""P12 / framework — OpenRouter free-tier model smoke tester.

Reads 4 OpenRouter-routed models from `framework/vendor/policysim_config/experiment-config.yaml`:
  - openai/gpt-oss-120b:free
  - nvidia/nemotron-3-ultra-550b-a55b:free
  - google/gemma-4-31b-it:free
  - nvidia/nemotron-3-super-120b-a12b:free  (DEPRECATED — kept for audit, will skip)

For each non-deprecated model, sends one chat.completions request and reports
status (OK / 401 / 403 / 429 / 5xx / timeout) and elapsed time.

If OPENROUTER_API_KEY is not set in environment / .env, prints a 5-step
acquisition guide and exits 0 (no test run).

Run from anywhere:
    python3 experiments/test_openrouter_models.py
"""
from __future__ import annotations
import json
import os
import sys
import time
from pathlib import Path

# --- Locate config and load .env ---
SCRIPT = Path(__file__).resolve()
P12_ROOT = SCRIPT.parent.parent
AUTO_ROOT = P12_ROOT.parent.parent
VENDOR_ROOT = AUTO_ROOT / "framework" / "vendor"
CONFIG = VENDOR_ROOT / "policysim_config" / "experiment-config.yaml"
ENV_FILE = AUTO_ROOT / ".env"


def _load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if v:  # only set if value is non-empty (skip blank placeholders)
            os.environ.setdefault(k, v)


_load_env_file(ENV_FILE)


# --- OpenRouter-routed model targets ---
TARGETS = [
    ("gpt-oss-120b",       "openai/gpt-oss-120b:free",                  False),
    ("nemotron-3-ultra",   "nvidia/nemotron-3-ultra-550b-a55b:free",    False),
    ("gemma-4-31b",        "google/gemma-4-31b-it:free",               False),
    ("nemotron-3-super",   "nvidia/nemotron-3-super-120b-a12b:free",    True),   # DEPRECATED
]


def print_acquisition_guide() -> None:
    print("=" * 70)
    print("OPENROUTER_API_KEY is not set. Cannot run smoke test.")
    print("=" * 70)
    print()
    print("5-step acquisition guide:")
    print()
    print("1. Visit https://openrouter.ai and sign in (Google / GitHub OAuth).")
    print("2. Go to https://openrouter.ai/keys and click 'Create Key'.")
    print("   The key starts with 'sk-or-v1-'.")
    print("3. Open your project .env:")
    print(f"      {ENV_FILE}")
    print("4. Uncomment / add this line (replace with your real key):")
    print("      OPENROUTER_API_KEY=sk-or-v1-...")
    print("5. Re-run:")
    print("      python3 experiments/test_openrouter_models.py")
    print()
    print("OpenRouter free-tier rate limits:")
    print("  - 20 requests/minute, 200 requests/day per model (as of 2026-07)")
    print("  - Sufficient for smoke tests and small calibration runs; NOT for 450×N batches.")
    print()


def main() -> int:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print_acquisition_guide()
        return 0

    print(f"OPENROUTER_API_KEY found (len={len(api_key)}, prefix={api_key[:10]}...)")
    print()

    # Import OpenAI client (OpenRouter is OpenAI-compatible)
    try:
        from openai import OpenAI
        import httpx
    except ImportError:
        print("FATAL: openai + httpx not installed. Run: pip install openai httpx", file=sys.stderr)
        return 2

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        timeout=httpx.Timeout(60.0, connect=10.0),
    )

    prompt = 'Reply with ONLY this exact JSON, no markdown: {"ok": true, "model": "<your-id>"}'
    print(f"{'model_id':50s} {'status':10s} {'time':>7s}  preview")
    print("-" * 95)

    any_ok = False
    for alias, model_id, deprecated in TARGETS:
        if deprecated:
            print(f"{model_id:50s} {'SKIP-DEP':10s} {'—':>7s}  (deprecated 2026-05-06)")
            continue
        t0 = time.time()
        try:
            r = client.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=64,
            )
            content = (r.choices[0].message.content or "").strip()
            elapsed = time.time() - t0
            any_ok = True
            print(f"{model_id:50s} {'OK':10s} {elapsed:6.1f}s  {content[:60]!r}")
        except Exception as e:
            elapsed = time.time() - t0
            err_name = type(e).__name__
            err_msg = str(e)[:80]
            status = "ERR"
            for code in ("401", "403", "404", "429"):
                if code in err_msg:
                    status = code
                    break
            print(f"{model_id:50s} {status:10s} {elapsed:6.1f}s  {err_name}: {err_msg}")
        print()

    print("=" * 95)
    if any_ok:
        print("PASS: at least one OpenRouter free-tier model responded.")
        print()
        print("To use these models from a runner, reference them by alias:")
        print('  cfg["models"]["gpt-oss-120b"]        → openai/gpt-oss-120b:free')
        print('  cfg["models"]["nemotron-3-ultra"]    → nvidia/nemotron-3-ultra-550b-a55b:free')
        print('  cfg["models"]["gemma-4-31b"]         → google/gemma-4-31b-it:free')
    else:
        print("FAIL: no OpenRouter free-tier model responded. Check API key + rate limits.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())