# Portfolio AutoResearch Task Spec

> Scope: `/Users/tangzw119/Documents/GitHub/auto-research` portfolio layer  
> Created: 2026-07-03  
> Controller: AutoResearch protocol, file-state first

## Goal

Turn the topic-5 experiment portfolio into a stop/pivot/execute research pipeline:

1. Close P11 as a mainline while preserving reusable findings.
2. Launch P12 judge calibration as the fastest 60-point paper candidate.
3. Reframe P1+P2+P8 as the high-ceiling evidence-structured decision-making line.
4. Keep P2.1 signal fusion only as an evidence input layer unless it becomes evidence topology.

## Milestones

| # | Milestone | Deliverable | Auto-verifiable |
|---|---|---|---|
| M0 | Portfolio roadmap | `docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md` | File exists and names priorities |
| M1 | Directory index | `README.md` + `docs/portfolio/project-index.md` | Root links resolve |
| M2 | P11 closure | P11 state updated + closure memo | `CLOSED_AS_MAINLINE` status appears |
| M3 | P12 scaffold | `p1.3-judge-calibration/` or equivalent with state files | task_spec + progress exist |
| M4 | P12 viability probe | blind/leaked/pairwise/probe metrics | result table exists |
| M5 | P1+P2 schema | factor ledger schema + 10 examples | schema + examples exist |
| M6 | P1.2 settlement layer | Brier/Log Loss implementation or spec | tests or checked script exists |
| M7 | P2.1 evidence input | evidence ledger adapter spec | adapter/spec exists |
| M8 | Review gate | five-persona review for P12 and P1+P2 | review JSON/MD exists |

## Current Priorities

1. P12 fast viability.
2. P11 closure and sample extraction.
3. P1+P2 evidence ledger design.

## Success Criteria

- P11 no longer consumes mainline repair effort.
- P12 reaches a clear go/no-go decision within 3-6 active work days.
- P1+P2 has a minimal factor-ledger schema with settlement path.
- All major decisions are reflected in state files, not only chat.

## Stale Rules

- `stale_count >= 2`: pivot structural constraint.
- `stale_count >= 4`: stop automation and write blocked reason.
- Do not run new large experiments without a corresponding paper claim and gate.
