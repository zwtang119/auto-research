# Papers (`papers/`)

> Updated: 2026-07-03
> Each paper directory is a self-contained research artifact.
> Framework rules binding on Day 0: see [`docs/portfolio/FRAMEWORK-RULES.md`](../FRAMEWORK-RULES.md).

## Active papers

| Code | Directory | Title | Status | Lead |
|---|---|---|---|---|
| **P7** | `papers/p07-signal-fusion/` | Multi-source signal fusion / evidence input layer | initialized | (legacy init under `legacy/p07-legacy-init-2026-07/`) |
| **P8** | `papers/p08-market-calibration/` | Prediction-market calibration / settlement layer | initialized | (legacy init under `legacy/p08-legacy-init-2026-07/`) |
| **P12** | `papers/p12-judge-calibration/` | LLM Judge Calibration | M1 closed | current main line |
| **P1+P2** | `papers/p1p2-evidence-ledger/` | Evidence RAG + Factor Ledger (concept mainline) | initialized | consumes P7/P8/P12 outputs |

## Closed / historical (under `legacy/`)

| Code | Directory | Status | Notes |
|---|---|---|---|
| P11 | `legacy/p11-closed-v5-mimo/` | closed at 7.0/10 | git repo, history preserved |
| P11 | `legacy/p11-closed-v5-minimax-m3/` | closed 2026-07-03 (Mimo integration recommended) | git repo, history preserved |
| P11 | `legacy/p11-legacy-snapshot-2026-07/` | non-versioned mix-bag parent | no git; reference only |
| P7 | `legacy/p07-legacy-init-2026-07/` | initialized-only | no experiments |
| P8 | `legacy/p08-legacy-init-2026-07/` | initialized-only | no experiments |

## Cross-cutting rule (R1)

Every active paper directory MUST be self-contained for inputs that the
paper depends on as evidence. Cross-folder inputs (e.g. P12 reads from
`legacy/p11-closed-v5-minimax-3/experiments/h5-emergence/A/yaml/`) MUST be
materialized into the consumer's directory before the producer can be
retired. See [`FRAMEWORK-RULES.md`](../FRAMEWORK-RULES.md) rule R1.

Each active paper that *currently* has a cross-folder dependency writes a
**copy-in plan** at `papers/<N>/state/source-of-truth.md` before its M1
closes. P12 will write one at M2 close.
