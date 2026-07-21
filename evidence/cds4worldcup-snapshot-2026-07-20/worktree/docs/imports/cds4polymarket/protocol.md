# World Cup Calibration Protocol

## Phase -1: Historical Smoke Test

Use 1-3 historical matches to confirm:

- task semantics are unambiguous
- prediction card shape is usable
- factor ledger entries can be adjudicated
- settlement record can compute Brier and Log Loss
- failure log can distinguish protocol failure from bad prediction

Go/No-Go: if a single historical match cannot be scored within the frozen schema, do not enter Phase 1.

## Phase 0: Data and Protocol Freeze

Required before MVP-A:

- methodology disclosure frozen
- source gate and parser blacklist frozen
- official schedule snapshot captured
- factor adjudication rubric frozen
- schemas frozen
- lock mechanism documented

Go/No-Go: if any required artifact is missing, do not enter MVP-A.

## MVP-A: Real-Time Manual Loop

Scope:

- first 3-5 World Cup matches
- manual YAML
- single model
- 2-3 high-observability factors per match
- at least one baseline or a recorded missing reason

Hard prohibitions:

- no betting advice
- no trading metrics
- no model leaderboard
- no claims of beating markets or public AI

## Schema Notes

### data_sources Format

The factor ledger schema uses `data_sources: list[string]` (simplified string format) instead of the object format shown in the spec §10 example (`- source_id: "name"`). This is a deliberate simplification: each string is a source_id that resolves to full metadata in `data/source_ledger.md`. The two formats are semantically equivalent — source provenance, capture time, and allowed use are managed centrally in the source ledger, not duplicated in each factor entry.
