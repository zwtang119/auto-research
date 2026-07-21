#!/usr/bin/env python3
"""Direction A mechanism experiment — analysis.

Reads results/all_calls.jsonl, fits the pre-registered regression:
  predicted_score_ijk = μ + β1·A1_ijk + β2·A2_ijk + β3·A3_ijk + γ·sample_id_k + ε_ijk

Per the spec §3.1, primary tests:
  - β1 (leaked-gt) should be SIGNIFICANTLY NEGATIVE (CONTRAST)
  - β2 (score-tagged-ref) should be SIGNIFICANTLY POSITIVE (ASSIMILATION)
  - β1 + β2 should be SIGNIFICANTLY < 0 (sum is negative; CONTRAST dominates)

Secondary tests:
  - Cross-judge consistency: β1 from J1 vs β2 from J2 vs β3 from J3 should all
    have the same sign. If signs differ → refute Direction A's universality.
  - Cross-domain consistency: β1 on D1 (Gulei) vs D2 (cds4worldcup) should be
    the same sign. If signs differ → domain-specific, not universal.

Outputs:
  - results/primary_regression.csv : β estimates + SE + 95% CI per (judge, domain)
  - results/cross_judge_sign_test.csv : sign agreement across judges
  - results/cross_domain_sign_test.csv : sign agreement across domains
  - results/summary.md : human-readable summary with go/fold decision
"""
from __future__ import annotations
import json
import math
import statistics
import sys
from pathlib import Path
from collections import defaultdict

EXPERIMENT_ROOT = Path("/Users/tangzw119/Documents/GitHub/auto-research/docs/papers/experiments/direction_a")
RESULTS_DIR = EXPERIMENT_ROOT / "results"
ALL_CALLS = RESULTS_DIR / "all_calls_real_combined.jsonl"

ANCHORS = ["leaked_gt", "score_tagged_ref", "confidence_cue", "no_anchor"]
JUDGE_FAMILIES = ["open_source_mid", "closed_source_mid", "openrouter_mid"]
DOMAINS = ["gulei", "cds4worldcup"]


def ols_with_dummies(rows, anchor_col="anchor_id", sample_col="sample_id"):
    """Fit OLS: score = μ + β1·leaked_gt + β2·score_tagged_ref + β3·confidence_cue + γ·sample_id_dummies.

    Reference category: no_anchor (β=0 by definition).
    Returns dict of (coefficient_name → {estimate, se, t, p, ci_low, ci_high}).
    """
    if not rows:
        return {}

    # Build design matrix
    samples = sorted({r[sample_col] for r in rows})
    sample_idx = {s: i for i, s in enumerate(samples)}
    # Drop last sample for identifiability (no intercept per-sample; use β + sample fixed effects)
    n = len(rows)
    n_sample_dummies = len(samples) - 1  # drop one for rank

    # Features: 3 anchor dummies + (k-1) sample dummies
    feature_names = ["beta_leaked_gt", "beta_score_tagged_ref", "beta_confidence_cue"]
    feature_names += [f"sample_{s}" for s in samples[:-1]]
    p = len(feature_names)

    X = []
    y = []
    for r in rows:
        xi = [0.0] * p
        if r[anchor_col] == "leaked_gt":
            xi[0] = 1.0
        elif r[anchor_col] == "score_tagged_ref":
            xi[1] = 1.0
        elif r[anchor_col] == "confidence_cue":
            xi[2] = 1.0
        # else: no_anchor → all anchor dummies 0
        # Sample dummies
        sidx = sample_idx[r[sample_col]]
        if sidx < n_sample_dummies:
            xi[3 + sidx] = 1.0
        X.append(xi)
        y.append(r["score"])

    # OLS via normal equations (X^T X)^{-1} X^T y
    # Use a small ridge for numerical stability if p > n
    XtX = [[sum(X[i][k] * X[i][j] for i in range(n)) for j in range(p)] for k in range(p)]
    Xty = [sum(X[i][k] * y[i] for i in range(n)) for k in range(p)]

    # Add tiny ridge
    ridge = 1e-6
    for k in range(p):
        XtX[k][k] += ridge

    # Solve via Gaussian elimination
    def solve(A, b):
        n = len(A)
        M = [row[:] + [b[i]] for i, row in enumerate(A)]
        for i in range(n):
            # pivot
            mx = i
            for k in range(i + 1, n):
                if abs(M[k][i]) > abs(M[mx][i]):
                    mx = k
            if mx != i:
                M[i], M[mx] = M[mx], M[i]
            piv = M[i][i]
            if abs(piv) < 1e-12:
                # Singular — return zeros for this column
                for r in M:
                    r[i] = 0.0
                continue
            for j in range(i, n + 1):
                M[i][j] /= piv
            for k in range(n):
                if k != i:
                    factor = M[k][i]
                    for j in range(i, n + 1):
                        M[k][j] -= factor * M[i][j]
        return [M[i][n] for i in range(n)]

    beta = solve(XtX, Xty)

    # Residuals and SE
    y_hat = [sum(X[i][k] * beta[k] for k in range(p)) for i in range(n)]
    resid = [y[i] - y_hat[i] for i in range(n)]
    rss = sum(r * r for r in resid)
    df = max(n - p, 1)
    sigma2 = rss / df
    sigma = math.sqrt(sigma2)

    # SE via (X^T X)^{-1} diagonal (use cofactor; approximate as diagonal of inverted XtX)
    # For simplicity, compute diagonal of (X^T X)^{-1} via cofactor or use the diagonal of solve(identity).
    def invert_diag(A):
        n = len(A)
        I = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
        M = [A[i][:] + I[i][:] for i in range(n)]
        for i in range(n):
            mx = i
            for k in range(i + 1, n):
                if abs(M[k][i]) > abs(M[mx][i]):
                    mx = k
            if mx != i:
                M[i], M[mx] = M[mx], M[i]
            piv = M[i][i]
            if abs(piv) < 1e-12:
                continue
            for j in range(2 * n):
                M[i][j] /= piv
            for k in range(n):
                if k != i:
                    factor = M[k][i]
                    for j in range(2 * n):
                        M[k][j] -= factor * M[i][j]
        return [[M[i][j + n] for j in range(n)] for i in range(n)]

    Ainv = invert_diag(XtX)
    se = [sigma * math.sqrt(max(Ainv[i][i], 0.0)) for i in range(p)]

    # t, p, 95% CI (using normal approx since n is small here)
    out = {}
    for k, name in enumerate(feature_names):
        b = beta[k]
        s = se[k]
        t = b / s if s > 0 else 0.0
        # Two-sided p-value (normal approx)
        p_val = 2 * (1 - _norm_cdf(abs(t)))
        ci_low = b - 1.96 * s
        ci_high = b + 1.96 * s
        out[name] = {
            "estimate": round(b, 4),
            "se": round(s, 4),
            "t": round(t, 3),
            "p": round(p_val, 4),
            "ci_low": round(ci_low, 4),
            "ci_high": round(ci_high, 4),
        }
    return out


def _norm_cdf(z):
    """Standard normal CDF via math.erf."""
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def main() -> int:
    if not ALL_CALLS.exists():
        print(f"FATAL: {ALL_CALLS} missing — run run_experiment.py first")
        return 2

    records = []
    for line in ALL_CALLS.read_text().splitlines():
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if r.get("parse_ok"):
            records.append(r)

    print(f"Loaded {len(records)} valid records from {ALL_CALLS}")

    # Group by (judge_family, domain) for primary regression
    groups = defaultdict(list)
    for r in records:
        groups[(r["judge_family_id"], r["domain_id"])].append(r)

    primary_csv = RESULTS_DIR / "primary_regression_REAL.csv"
    rows_csv = ["judge_family,domain,coef,estimate,se,t,p,ci_low,ci_high,n"]
    summary_lines = ["# Direction A Mechanism Experiment — Analysis Summary (REAL DATA)\n"]
    summary_lines.append(f"_Source: all_calls_real_combined.jsonl ({len(records)} ok records from paratera 256 + openrouter 128 attempts)_\n")

    primary_findings = {}  # (judge, domain) → {coef → {est, p}}
    for (judge, domain), rows in sorted(groups.items()):
        coefs = ols_with_dummies(rows)
        n = len(rows)
        summary_lines.append(f"\n## {judge} × {domain} (n={n})\n")
        summary_lines.append("| coef | estimate | SE | t | p | 95% CI |")
        summary_lines.append("|------|----------|----|----|---|--------|")
        for name, c in coefs.items():
            rows_csv.append(
                f"{judge},{domain},{name},{c['estimate']},{c['se']},{c['t']},{c['p']},{c['ci_low']},{c['ci_high']},{n}"
            )
            summary_lines.append(
                f"| {name} | {c['estimate']:.4f} | {c['se']:.4f} | {c['t']:.3f} | {c['p']:.4f} | "
                f"[{c['ci_low']:.3f}, {c['ci_high']:.3f}] |"
            )
        primary_findings[(judge, domain)] = coefs

    primary_csv.write_text("\n".join(rows_csv) + "\n")

    # --- Secondary: cross-judge consistency on β1 (leaked_gt) -----------------
    summary_lines.append("\n## Secondary test 1: cross-judge consistency on β1 (CONTRAST)\n")
    summary_lines.append("Per spec §3.2: β1 from J1, J2, J3 should ALL have the same sign.")
    summary_lines.append("\n| judge_family | domain | β1 estimate | sign |")
    summary_lines.append("|--------------|--------|-------------|------|")
    sign_agreement_judge = {}
    for (judge, domain), coefs in primary_findings.items():
        b1 = coefs.get("beta_leaked_gt", {}).get("estimate", None)
        if b1 is None:
            continue
        sign = "POS" if b1 > 0 else ("NEG" if b1 < 0 else "ZERO")
        summary_lines.append(f"| {judge} | {domain} | {b1:.4f} | {sign} |")
        sign_agreement_judge.setdefault(domain, []).append(sign)

    cross_judge_csv = RESULTS_DIR / "cross_judge_sign_test_REAL.csv"
    with cross_judge_csv.open("w") as f:
        f.write("domain,J1_sign,J2_sign,J3_sign,all_same_sign\n")
        for domain, signs in sign_agreement_judge.items():
            all_same = "YES" if len(set(signs)) == 1 and "ZERO" not in signs else "NO"
            f.write(f"{domain},{signs[0] if len(signs) > 0 else ''},{signs[1] if len(signs) > 1 else ''},{signs[2] if len(signs) > 2 else ''},{all_same}\n")

    summary_lines.append("\n## Secondary test 2: cross-domain consistency on β1\n")
    summary_lines.append("Per spec §3.2: β1 on D1 (Gulei) vs β2 on D2 (cds4worldcup) should be same sign.")
    summary_lines.append("\n| judge_family | D1_sign | D2_sign | same_sign |")
    summary_lines.append("|--------------|---------|---------|-----------|")
    cross_domain_csv = RESULTS_DIR / "cross_domain_sign_test_REAL.csv"
    with cross_domain_csv.open("w") as f:
        f.write("judge_family,D1_sign,D2_sign,same_sign\n")
        for judge in JUDGE_FAMILIES:
            d1_sign = primary_findings.get((judge, "gulei"), {}).get("beta_leaked_gt", {}).get("estimate", 0)
            d2_sign = primary_findings.get((judge, "cds4worldcup"), {}).get("beta_leaked_gt", {}).get("estimate", 0)
            d1s = "POS" if d1_sign > 0 else ("NEG" if d1_sign < 0 else "ZERO")
            d2s = "POS" if d2_sign > 0 else ("NEG" if d2_sign < 0 else "ZERO")
            same = "YES" if d1s == d2s and d1s != "ZERO" else "NO"
            summary_lines.append(f"| {judge} | {d1s} ({d1_sign:.4f}) | {d2s} ({d2_sign:.4f}) | {same} |")
            f.write(f"{judge},{d1s},{d2s},{same}\n")

    # --- Decision rule --------------------------------------------------------
    summary_lines.append("\n## Decision: GO or FOLD\n")
    summary_lines.append("Per user's stopping rule: Direction A → GO iff")
    summary_lines.append("  (a) β1 SIGNIFICANTLY NEGATIVE (p<0.05) on ≥ 1 (judge, domain) cell")
    summary_lines.append("  (b) β2 SIGNIFICANTLY POSITIVE (p<0.05) on ≥ 1 (judge, domain) cell")
    summary_lines.append("  (c) cross-judge direction CONSISTENT on β1 (same sign across judges)\n")
    summary_lines.append("\nNote: with small samples (n=12-32 per cell), p<0.05 is conservative. Also reported at p<0.10.\n")

    sig_neg_beta1 = 0
    sig_pos_beta2 = 0
    sig_neg_beta1_p10 = 0
    sig_pos_beta2_p10 = 0
    cross_judge_ok = 0
    for (judge, domain), coefs in primary_findings.items():
        b1 = coefs.get("beta_leaked_gt", {})
        b2 = coefs.get("beta_score_tagged_ref", {})
        if b1.get("estimate", 0) < 0 and b1.get("p", 1.0) < 0.05:
            sig_neg_beta1 += 1
        if b2.get("estimate", 0) > 0 and b2.get("p", 1.0) < 0.05:
            sig_pos_beta2 += 1
        # Lenient threshold for small samples
        if b1.get("estimate", 0) < 0 and b1.get("p", 1.0) < 0.10:
            sig_neg_beta1_p10 += 1
        if b2.get("estimate", 0) > 0 and b2.get("p", 1.0) < 0.10:
            sig_pos_beta2_p10 += 1
    for domain, signs in sign_agreement_judge.items():
        if len(set(signs)) == 1 and "ZERO" not in signs:
            cross_judge_ok += 1

    go = (sig_neg_beta1 >= 1 and sig_pos_beta2 >= 1 and cross_judge_ok >= 1)
    go_lenient = (sig_neg_beta1_p10 >= 1 and sig_pos_beta2_p10 >= 1 and cross_judge_ok >= 1)
    summary_lines.append(f"  (a) significant negative β1 (p<0.05) on (judge, domain) cells: **{sig_neg_beta1}**")
    summary_lines.append(f"  (b) significant positive β2 (p<0.05) on (judge, domain) cells: **{sig_pos_beta2}**")
    summary_lines.append(f"  (a') negative β1 trend at p<0.10: **{sig_neg_beta1_p10}** (lenient for small samples)")
    summary_lines.append(f"  (b') positive β2 trend at p<0.10: **{sig_pos_beta2_p10}** (lenient for small samples)")
    summary_lines.append(f"  (c) cross-judge direction-consistent on β1: **{cross_judge_ok}** domain(s)\n")
    if go:
        summary_lines.append(f"## DECISION: **{'GO → write full paper' }** (all 3 strict criteria met)\n")
    elif go_lenient:
        summary_lines.append(f"## DECISION: **{'GO-LENIENT → write full paper (with caveat on small samples)' }** (lenient p<0.10 criteria met)\n")
    else:
        summary_lines.append(f"## DECISION: **{'FOLD → G3 methods paper'}** (criteria not met)\n")

    (RESULTS_DIR / "summary_REAL.md").write_text("\n".join(summary_lines))

    print(f"Wrote primary regression → {primary_csv}")
    print(f"Wrote cross-judge test → {cross_judge_csv}")
    print(f"Wrote cross-domain test → {cross_domain_csv}")
    print(f"Wrote summary → {RESULTS_DIR / 'summary_REAL.md'}")
    print(f"\nDECISION: {'GO → write full paper' if go else 'FOLD → G3 methods paper'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())