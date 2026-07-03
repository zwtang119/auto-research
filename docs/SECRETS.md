# Secrets

The `auto-research/.env` file is **loaded at runtime** by experiment scripts
(including `papers/<N>/experiments/run_*_baseline.py`) and the watchdog
L1 patrol. The shell `.env.loader` lives inline in each script — no
python-dotenv dependency.

## File mode

`.env` MUST be `chmod 600` (owner read/write only). Public `.gitignore`
excludes `.env`; this is the **second** line of defense.

Verify per session:

```bash
ls -l auto-research/.env
# expected: -rw------- (600)
```

If the mode is `0644`, run:

```bash
chmod 600 auto-research/.env
```

## `.env.sample` (committed) vs `.env` (gitignored)

| File | Comitted? | Content |
|---|---|---|
| `.env.sample` | yes | schema: variable names + placeholder values (including the public `OPENAI_BASE_URL=https://llmapi.paratera.com`) |
| `.env` | NO | real keys |

`.env.sample` is safe to inspect publicly. Anyone with the contents still
needs the actual API key to spend budget.

## Why not python-dotenv?

Adding `python-dotenv` is one more dependency at every L2 call point. A
12-line stdlib loader is in every script that needs it:

```python
def _load_env_file(path: Path) -> None:
    if not path.exists(): return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line: continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k, v.strip().strip('"').strip("'"))
```

Standalone stdlib reduces both dependency surface and the surprise of
"import dotenv fails — does the env load?".

## What's where

The model + base_url etc. live in `.env` (per-experiment). The model
*registry* (which key maps to which provider) lives in
`framework/vendor/policysim_config/experiment-config.yaml` (vendored, in
the public repo, **does not contain keys**).

Together these two files let `api_client.call_model` resolve model
names to actual HTTP calls.
