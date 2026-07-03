# Vendor — vendored dependencies

> Auto-research vendors a subset of `policysim-research-Tsinghua` so any
> experiment runner can `clone → install deps → run` without an external
> polyrepo dependency on `~/Documents/GitHub/policysim-research-Tsinghua`.

## Layout

```
vendor/
├── policysim_scripts/                 # scripts/*.py we call from experiments
│   ├── api_client.py                  # load_config + create_client + call_model
│   └── prompt_logger.py               # provenance logger (used by api_client)
├── policysim_config/                  # policysim-research-Tsinghua/config
│   └── experiment-config.yaml         # models + api_endpoints + prompt defaults
└── policysim_materials/               # policysim-research-Tsinghua/materials
    └── 20-seed-data/
        └── reusable_rocket_v2.yaml    # Gulei scenario (referenced by P11 v5)
```

## Why these four only

| File | Used by | Reason included |
|---|---|---|
| `api_client.py` | P12 `experiments/run_leaked_baseline.py` (and future runners) | LLM call surface |
| `prompt_logger.py` | `api_client` (one-line import) | without this, `api_client` fails to import |
| `experiment-config.yaml` | `api_client.load_config` | model + provider + endpoint registry |
| `reusable_rocket_v2.yaml` | P11 v5 Gulei scenario, indirectly used for any P12 sample that imports from this scenario | canonical source |
| (NOT included) `anti_template.yaml` | P11 reuses it via `policysim_scripts/*.py`; not loaded by api_client | avoidable until someone imports a `generate_*` script — at which point, vendor on demand |
| (NOT included) `gt_thresholds.yaml` | P11 ground-truth thresholds | not needed by `call_model` runner path |

## How experiment runners import these

Add this prelude to any new experiment runner that calls LLMs:

```python
import sys
from pathlib import Path

P12_ROOT = Path(__file__).resolve().parent.parent
AUTO_RESEARCH_ROOT = P12_ROOT.parent.parent
sys.path.insert(0, str(AUTO_RESEARCH_ROOT / "framework" / "vendor" / "policysim_scripts"))

from api_client import load_config, call_model   # noqa: E402
```

And load the config from the vendored copy:

```python
CONFIG = load_config(str(AUTO_RESEARCH_ROOT / "framework" / "vendor" / "policysim_config" / "experiment-config.yaml"))
```

## Sync policy

When `policysim-research-Tsinghua` upstream changes, run:

```bash
just sync-policysim-vendor   # or hand-run the cp commands
```

and commit a new vendor revision. Vendored content is treated as **read-only**
in this repo — edit in upstream, then re-vendor.

## License inheritance

The policysim-research-Tsinghua upstream is private to the project owner.
Vendor-derived files inside this repo follow the same access policy: visible
to the owner and collaborators, not for redistribution.
