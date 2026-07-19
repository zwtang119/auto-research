# AutoResearch Framework History

> **Scope**: framework-level evolution. Per-paper histories live in each
> `papers/<N>-<topic>/state/iteration_log.jsonl`.
> **QREF index**: this file now also embeds the framework-level index of the
> 6 0ref QREFs (per `wiki/0ref-methodology-landscape.md`) and the 62-PIT cross-project
> pitfalls catalog (per `wiki/pitfalls-and-recoveries.md`).

---

## 1. QREF index (per 0ref-methodology-landscape.md)

> **How to use**: when starting a new paper or major refactor, scan the relevant
> QREF-NNN and apply its 1-2 unique design decisions. Do NOT mass-port — adopt
> the pattern that fits this paper's scope.

| QREF | Subproject | Pattern to apply here | Applicable auto-research file |
|------|------------|-----------------------|------------------------------|
| [QREF-001] | mem0 | Provider pattern (5 类别抽象) | `framework/vendor/policysim_config/experiment-config.yaml` (LLM provider list) + new `framework/schemas/provider-pattern.md` (NOT YET WRITTEN) |
| [QREF-002] | nanoclaw | Two-DB session split (host/container 严格单写者) + pnpm 3-day minimumReleaseAge | `state/` already split; supply-chain guard NOT YET (per R11) |
| [QREF-003] | dspy | "Programming—not prompting" Signature/Module/Optimizer | `framework/schemas/data-contracts.md` (signature) + future `framework/schemas/optimizer-spec.md` (NOT YET) |
| [QREF-004] | claude-mem | 43-line极简 AGENTS.md 范式 + 每日 npm-check-updates SOP | This file (target ≤ 200 lines) + future `framework/scripts/dependency-upgrade.sh` (NOT YET) |
| [QREF-005] | institute-one | 10 Hard rules + "One execution path" + Conditional-claim | **Section 0 above** (10 rules applied directly) |
| [QREF-006] | claudish | `provider@model[:concurrency]` 路由语法 | `framework/vendor/policysim_config/experiment-config.yaml` (already uses similar; future: extract to `framework/scripts/route-model.sh`) |

---

## 2. PIT index (per wiki/pitfalls-and-recoveries.md)

> **How to use**: when a paper's `state/findings.jsonl` records a `pitfall_id`
> starting with `PIT-` (NOT `PIT-<EXP>-`), check the wiki catalog for the
> full description. The 12 PITs below are the most relevant at framework
> level (per F1 5-min summary "必读门槛" thinking).

| PIT | Title | Framework-level action |
|------|-------|------------------------|
| [PI-001] | 多供应商 LLM API 路由的"硬编码陷阱" | `framework/vendor/policysim_config/` already has 5 providers; ensure no new paper hardcodes a 6th |
| [PI-002] | protocol/ 冻结与现实漂移的张力 | `framework/schemas/{data-contracts, experiment-pitfalls}` are the framework's "frozen" surface; any drift is a defect, not evolution |
| [PI-003] | AGENTS.md 权威顺序 + 不得"会话记忆"覆盖 | This file (auto-research-history.md) is the analog; future: `framework/AGENTS.md` once AGENTS.md is needed |
| [PI-004] | "绿光 ≠ 无 bug" 的提交门禁钩子 | Mirror in `framework/scripts/preflight.sh` (NOT YET — only paper-level preflight exists) |
| [PI-005] | "全绿"声明无证据 = phantom bug | Mirror in commit-msg hook (NOT YET — paper `verify:`段 not yet enforced at framework level) |
| [PI-006] | sub-agent 失败时的"原地 retry loop"反模式 | `framework/watchdog/L1/` may need 3-retry cap; check `L1.sh` |
| [PI-008] | 阶段锁 (Stabilize / Deliver / Improve 单态机) | Apply to every paper's M-stage: M1=Stabilize, M2-M7=Deliver, M8=Improve |
| [PI-009] | 单步迭代上限 3 次 + 收敛报告 | Per-paper iteration cap; `state/iteration_log.jsonl.unresolved_weakness` is the convergence report |
| [PI-017] | 来源 3 级分级 (Green/Yellow/Red) 进因子账本 | `state/source-of-truth.md` (NEW, see §3 below) implements this for cross-folder sources |
| [PI-019] | 知识库审计 (audit.py) 0 issues = 必过门 | Mirror in `framework/scripts/audit.sh` (NOT YET — no framework-level audit) |
| [PI-024] | 密钥边界硬约束 (API Key 与运行时隔离) | `docs/SECRETS.md` already exists; verify it is the only `.env` template |
| [PI-044] | "绿光 ≠ 无 bug" warning 块 + 唯一状态入口 | `state/` IS the single source; per-paper `state/` files implement this |

**Inverse lookup** (per-paper `pitfall_id` from `state/findings.jsonl`):
- PIT-XXX (no EXP prefix) → look in this table + wiki catalog.
- PIT-<EXP>-XXX → look in `framework/schemas/experiment-pitfalls.md` only.

---

## 3. 2026-07-03 — Framework-level R1 closure file created

**Event**: `state/source-of-truth.md` created (the framework-level mirror of
R1's closure-checklist requirement).

**Why**:
- R1 §Enforcement line 39-41: "every paper's `state/checklist.yaml` (or
  `state/closure_checklist.md`) must list each external source and the
  materialization step before closure."
- Until today, no framework-level file existed that:
  1. Documents the **mechanism** of R1 (not just the rule).
  2. Mirrors cross-paper dependencies (P12 → P11 v5) in one place.
  3. Provides the **9-step M8 closure checklist** (per QREF-005 institute-one
     Hard rule #6 parallel).
- Audit trigger: 62-PIT catalog's reverse-audit (`wiki/pitfalls-catalog-reverse-audit.md`)
  identified R1+state-file integrity as a meta-risk; the 2026-07-03 work
  block on `state/_唯一_状态入口.md` (from the catalog's "立即可做" list)
  led here.

---

## 4. Pre-2026-07-03 history (carried from prior version of this file)

### 2026-07-03 — Monorepo bootstrap

**Event**: auto-research/ promoted from a multi-paper workspace to a
**framework monorepo**.

**Why**:
- Victor Chen reference site (`victorchen96.github.io`) mirrors the
  Deli_AutoResearch long-horizon protocol.
- User wanted the framework to outlive any single paper.
- 14 active files referenced cross-paper content (data-contracts,
  pitfalls) — proof of cross-paper need.
- 0 active scripts reusable across papers — proof that premature full
  scaffold would be empty bins.

**Decisions bound this session**:

| Decision | Rationale | Source |
|---|---|---|
| Single monorepo | Minimal disruption to P12 progress; framework shares one `git log` over time | user Q1 |
| Active papers under `papers/`, closed under `legacy/` | Lifecycle visible from path; R3 | rename-proposal §3 |
| Framework-level dirs only when ≥2 papers need them | YAGNI; the promotion rule locked in §3 of restructure-blueprint | user Q2 |
| R1 Single-Source-of-Truth | Closure-time copy-in: a paper must own its inputs before closing; deprecated sources can be retired | FRAMEWORK-RULES R1 + per-paper `state/source-of-truth.md` |
| Use Deli_AutoResearch convention | State-file skeleton already matched; constraint #2 zero-interaction already in `R6`; §9 engineering constraints validated by 9 unit tests + manifest guard | user Q4 |
| Heartbeat watchdog: deferred | User explicitly opted against heartbeat for Day 1; re-evaluate at first stall | user (c) |
| website hub (GitHub Pages): future | Not in scope this turn; user has not built `<owner>.github.io` yet | user §1 |

**Execution milestones**:

- 9 directory renames (active ↔ legacy split)
- 31 active-scope files `sed`-patched for old-paths → new-paths
- 3 runtime scripts in P12 had path-arithmetic fixed
- 9 / 9 P12 unit tests GREEN post-rename
- `OBSOLETE.md` at repo root for cite-restoration
- `docs/portfolio/FRAMEWORK-RULES.md` written (7 rules)
- `papers/README.md` written (active + closed tables)
- `papers/p12-judge-calibration/state/source-of-truth.md` written (closure checklist)
- `framework/{README, schemas/{data-contracts, experiment-pitfalls}, knowledge/auto-research-history}/` created (minimal scaffold)
- 14 schema path references rewritten (depth-aware across papers/, docs/, framework/)
- 0 broken refs after rewrite (verified by `readlink -f`)

---

## 5. Open questions / next actions

- [ ] User build `<owner>.github.io` and link `website/` content to it (Day-1+)
- [ ] Decide whether to apply `claude-prompt.md` SKILL reference per paper (Day-2+ if any paper agent drifts)
- [ ] At first P12 stall (3+ consecutive iterations with 0 new findings), enable heartbeat L2
- [ ] At M8 closure, execute the 7-step source-of-truth plan in
      `papers/p12-judge-calibration/state/source-of-truth.md`
- [ ] (NEW) Add `framework/AGENTS.md` per PI-003 (AutoResearch has no AGENTS.md currently — R1 mitigation)
- [ ] (NEW) Add `framework/scripts/preflight.sh` per PI-004 (commit-msg hook for "全绿" gate at framework level)
- [ ] (NEW) Add `framework/scripts/audit.sh` per PI-019 (knowledge base audit at framework level)
- [ ] (NEW) Add `framework/schemas/provider-pattern.md` per QREF-001 (5-category Provider abstraction)

---

## 6. Risk register (today)

| Risk | Status |
|---|---|
| P12 reads P11 from `legacy/` — fragile cross-folder dep | Mitigated by R1 + framework-level `state/source-of-truth.md` (NEW today) + paper-level copy |
| 9 dirs moved; paper cites pre-rename | Mitigated by `OBSOLETE.md` (root) for 9 old paths |
| Framework scaffold may be too thin | Mitigated by promotion rule; first cross-paper need will trigger expansion |
| Heartbeat not enabled | Accepted by user; trade-off faster Day-1 M2 vs no auto-restart |
| (NEW) 8 R-rules (R8-R20) exist in global MEMORY but not in `docs/portfolio/FRAMEWORK-RULES.md` | Identified today; FRAMEWORK-RULES.md rewrite is the #3 priority |
| (NEW) No framework-level preflight / audit scripts | Identified today; future work |

---

*Original 61-line file retained as section 4 for audit trail. Sections 0-3 + 5-6 are the
2026-07-03 additions per the framework-level R1 closure work + QREF/PIT index.*

