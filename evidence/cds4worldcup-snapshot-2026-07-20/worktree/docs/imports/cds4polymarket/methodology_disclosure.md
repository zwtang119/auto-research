# Methodology Disclosure

> Status: frozen-before-MVP-A
> Version: v0.1

## 1. Experiment Identity

This experiment is a World Cup public calibration wind tunnel for CDS. It tests protocol discipline, not football expertise.

## 2. What This Experiment Is

- A pre-registration test.
- A factor-ledger adjudication test.
- A probability scoring and settlement test.
- A knowledge update test.

## 3. What This Experiment Is Not

- It is not betting advice.
- It is not a trading system.
- It is not a model leaderboard.
- It does not claim CDS, MAMR, or any LLM predicts football better than markets.

## 4. Model Cycle

```text
official schedule/source snapshot
-> match package freeze
-> prediction card generation
-> schema validation
-> pre-match lock
-> official settlement
-> factor adjudication
-> score calculation
-> protocol failure review
-> knowledge update log
```

## 5. Prompt and Config Card

Each prediction card records:

- provider and exact model id
- model version observation time
- prompt version and hash
- temperature
- max retries
- fixed reasoning budget
- source cutoff time
- whether market, odds, or public AI baseline was exposed

MVP-A default: market/odds/public AI baseline is not exposed to the CDS model.

## 6. Source Gate and Parser Blacklist

Green Sources can enter formal match packages. Red Sources can only serve as baseline, candidate seed, parser fixture, or manual review material.

Blacklisted by default:

- LLM-generated summaries as facts
- Kimi probabilities, rankings, and win rates as CDS model input
- Excel/PDF fields without row-level source URLs
- social-platform summaries
- sources with known parser errors

## 7. Notes and Memory Budget

| Field | MVP-A Limit |
|---|---:|
| prior notes | 5 |
| note length | 1200 chars each |
| candidate factors reviewed | 6 per match |
| Kimi-derived candidates reviewed | 3 per match |
| Kimi-derived factors tracked | 1 per match |

## 8. Factor Ledger Adjudication

Every tracked factor must have:

- observable proxy
- quantified threshold
- settlement rule
- counter-signal
- adjudicator independence
- confidence 0-10

## 9. Baselines and Scoring

MVP-A records Brier Score, Log Loss, baseline coverage, factor adjudication yield, cost per valid prediction, and protocol failure rate. MVP-A does not report significance or model advantage.

## 10. Protocol Failure Taxonomy

| Failure Type | Meaning |
|---|---|
| `lock_failure` | Prediction was not locked before kickoff or was overwritten. |
| `schema_failure` | Required prediction, factor, or settlement schema failed. |
| `source_gate_failure` | Red Source entered formal match package as fact. |
| `baseline_missing` | Required baseline was missing without recorded reason. |
| `outcome_semantics_dispute` | Task outcome semantics were ambiguous or mixed. |
| `factor_inconclusive` | Factor cannot be adjudicated from post-match evidence. |
| `prompt_config_drift` | Model or prompt execution differs from locked config. |
| `parser_blacklist_hit` | Blacklisted source or parser field was hit. |

## 11. Known Limitations

- Football has high irreducible variance.
- MVP-A sample size is too small for capability claims.
- Many sports factors may be hard to adjudicate without licensed event data.
- Public AI artifacts can contaminate reasoning if not separated.
- Market and odds baselines may be unavailable or non-archivable for some matches.

## 12. Planned Improvements

- Phase 2: expand from 3-5 to 8-12 matches if locks and schemas hold.
- Phase 3+: test knowledge injection and multi-model sensitivity after at least 30 valid cards.
- Phase 4+: report bootstrap confidence intervals after at least 50 valid cards.
