#!/usr/bin/env python3
"""
Statistical Analysis for P1.1 Inner Monologue Experiment

Tests:
1. Mode B (inner_monologue) RoleDNA fidelity > Mode A (no_think) by ≥ 0.5 on 5-point scale (p<0.05)
2. Mode B decision quality non-inferior to Mode A
3. Think-tag trigger rate ≥ 85% in Mode B
4. Spearman's ρ between RoleDNA risk_tolerance and agent cautiousness behavior ≥ 0.4
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
from scipy import stats


def load_scores(experiment_dirs: Dict[str, Path]) -> Dict[str, List[Dict]]:
    """Load scores from multiple experiment directories."""
    all_scores = {}
    
    for mode, exp_dir in experiment_dirs.items():
        scores_file = exp_dir / "scores.jsonl"
        if not scores_file.exists():
            print(f"Warning: {scores_file} not found, skipping {mode}")
            continue
        
        scores = []
        with open(scores_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    scores.append(json.loads(line))
        all_scores[mode] = scores
    
    return all_scores


def extract_fidelity_scores(scores: List[Dict]) -> Dict[str, List[float]]:
    """Extract RoleDNA fidelity scores per enterprise."""
    fidelity_by_ent = {}
    
    for run in scores:
        for ent_id, ent_scores in run.get("enterprise_scores", {}).items():
            if ent_id not in fidelity_by_ent:
                fidelity_by_ent[ent_id] = []
            
            fidelity = ent_scores.get("fidelity", {})
            if "overall_fidelity" in fidelity:
                fidelity_by_ent[ent_id].append(fidelity["overall_fidelity"])
    
    return fidelity_by_ent


def test_h1_inner_monologue_superiority(
    mode_a_scores: List[float],
    mode_b_scores: List[float],
    min_diff: float = 0.5,
    alpha: float = 0.05,
) -> Dict:
    """Test H1: Mode B fidelity > Mode A fidelity by ≥ min_diff.
    
    Uses one-sided t-test.
    """
    if len(mode_a_scores) < 3 or len(mode_b_scores) < 3:
        return {"test": "H1", "status": "insufficient_data", "n_a": len(mode_a_scores), "n_b": len(mode_b_scores)}
    
    mean_a = np.mean(mode_a_scores)
    mean_b = np.mean(mode_b_scores)
    diff = mean_b - mean_a
    
    # One-sided t-test: H0: diff <= min_diff, H1: diff > min_diff
    t_stat, p_value = stats.ttest_ind(mode_b_scores, mode_a_scores, alternative='greater')
    
    # Also test if diff >= min_diff
    diff_p_value = 1 - stats.t.cdf((diff - min_diff) / np.sqrt(np.var(mode_a_scores)/len(mode_a_scores) + np.var(mode_b_scores)/len(mode_b_scores)))
    
    return {
        "test": "H1",
        "hypothesis": f"Mode B fidelity > Mode A by ≥ {min_diff}",
        "mean_a": round(mean_a, 3),
        "mean_b": round(mean_b, 3),
        "diff": round(diff, 3),
        "t_stat": round(t_stat, 3),
        "p_value_greater": round(p_value, 4),
        "p_value_diff_ge_min": round(diff_p_value, 4),
        "significant": diff_p_value < alpha and diff >= min_diff,
        "n_a": len(mode_a_scores),
        "n_b": len(mode_b_scores),
    }


def test_h2_non_inferiority(
    mode_a_scores: List[float],
    mode_b_scores: List[float],
    non_inferiority_margin: float = 0.3,
    alpha: float = 0.05,
) -> Dict:
    """Test H2: Mode B decision quality non-inferior to Mode A.
    
    Non-inferiority test: Mode B >= Mode A - margin
    """
    if len(mode_a_scores) < 3 or len(mode_b_scores) < 3:
        return {"test": "H2", "status": "insufficient_data"}
    
    mean_a = np.mean(mode_a_scores)
    mean_b = np.mean(mode_b_scores)
    
    # One-sided t-test for non-inferiority
    t_stat, p_value = stats.ttest_ind(mode_b_scores, mode_a_scores, alternative='greater')
    
    # Check if mode_b is within margin of mode_a
    is_non_inferior = mean_b >= mean_a - non_inferiority_margin
    
    return {
        "test": "H2",
        "hypothesis": f"Mode B quality >= Mode A - {non_inferiority_margin}",
        "mean_a": round(mean_a, 3),
        "mean_b": round(mean_b, 3),
        "diff": round(mean_b - mean_a, 3),
        "t_stat": round(t_stat, 3),
        "p_value": round(p_value, 4),
        "is_non_inferior": is_non_inferior,
        "significant": p_value < alpha and is_non_inferior,
        "n_a": len(mode_a_scores),
        "n_b": len(mode_b_scores),
    }


def test_h3_think_tag_trigger_rate(
    trigger_rates: List[float],
    min_rate: float = 0.85,
) -> Dict:
    """Test H3: Think-tag trigger rate ≥ 85% in Mode B."""
    if not trigger_rates:
        return {"test": "H3", "status": "no_data"}
    
    mean_rate = np.mean(trigger_rates)
    std_rate = np.std(trigger_rates)
    
    # Binomial test: is the proportion significantly >= min_rate?
    n = len(trigger_rates)
    successes = sum(1 for r in trigger_rates if r >= min_rate)
    
    # One-sided binomial test
    binom_p = stats.binom_test(successes, n, min_rate, alternative='greater') if n > 0 else 1.0
    
    return {
        "test": "H3",
        "hypothesis": f"Think-tag trigger rate >= {min_rate}",
        "mean_rate": round(mean_rate, 4),
        "std_rate": round(std_rate, 4),
        "min_rate": round(min(trigger_rates), 4),
        "max_rate": round(max(trigger_rates), 4),
        "p_value": round(binom_p, 4),
        "significant": binom_p < 0.05 and mean_rate >= min_rate,
        "n": n,
    }


def test_h4_spearman_correlation(
    risk_tolerance_scores: List[float],
    cautiousness_scores: List[float],
    min_rho: float = 0.4,
    alpha: float = 0.05,
) -> Dict:
    """Test H4: Spearman's ρ between risk_tolerance and cautiousness ≥ 0.4.
    
    Note: cautiousness is inverse of risk_tolerance in behavior.
    """
    if len(risk_tolerance_scores) < 5 or len(cautiousness_scores) < 5:
        return {"test": "H4", "status": "insufficient_data"}
    
    # Spearman correlation
    rho, p_value = stats.spearmanr(risk_tolerance_scores, cautiousness_scores)
    
    return {
        "test": "H4",
        "hypothesis": f"Spearman ρ >= {min_rho}",
        "rho": round(rho, 4),
        "p_value": round(p_value, 4),
        "significant": p_value < alpha and rho >= min_rho,
        "n": len(risk_tolerance_scores),
    }


def generate_summary_report(results: Dict, output_path: Path):
    """Generate a summary report."""
    report = []
    report.append("=" * 70)
    report.append("P1.1 Inner Monologue Experiment - Statistical Analysis Report")
    report.append("=" * 70)
    report.append("")
    
    # Overall summary
    all_passed = all(r.get("significant", False) for r in results.values())
    report.append(f"Overall Result: {'ALL HYPOTHESES CONFIRMED' if all_passed else 'SOME HYPOTHESES FAILED'}")
    report.append("")
    
    # Individual test results
    for test_name, test_result in results.items():
        report.append(f"--- {test_name} ---")
        report.append(json.dumps(test_result, indent=2, ensure_ascii=False))
        report.append("")
    
    report.append("=" * 70)
    
    report_text = "\n".join(report)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_text)
    
    print(report_text)
    return report_text


def main():
    parser = argparse.ArgumentParser(description="Statistical Analysis for P1.1 Experiment")
    parser.add_argument("--no-think-dir", required=True, help="Path to no_think experiment results")
    parser.add_argument("--inner-monologue-dir", required=True, help="Path to inner_monologue experiment results")
    parser.add_argument("--pure-analysis-dir", default=None, help="Path to pure_analysis experiment results")
    parser.add_argument("--output", default="statistical_report.json", help="Output report file")
    args = parser.parse_args()
    
    experiment_dirs = {
        "no_think": Path(args.no_think_dir),
        "inner_monologue": Path(args.inner_monologue_dir),
    }
    if args.pure_analysis_dir:
        experiment_dirs["pure_analysis"] = Path(args.pure_analysis_dir)
    
    # Load all scores
    all_scores = load_scores(experiment_dirs)
    
    if "no_think" not in all_scores or "inner_monologue" not in all_scores:
        print("Error: Both no_think and inner_monologue scores are required")
        sys.exit(1)
    
    # Extract fidelity scores
    fidelity_no_think = extract_fidelity_scores(all_scores["no_think"])
    fidelity_inner_monologue = extract_fidelity_scores(all_scores["inner_monologue"])
    
    # Aggregate across enterprises
    all_fidelity_no_think = []
    for ent_scores in fidelity_no_think.values():
        all_fidelity_no_think.extend(ent_scores)
    
    all_fidelity_inner_monologue = []
    for ent_scores in fidelity_inner_monologue.values():
        all_fidelity_inner_monologue.extend(ent_scores)
    
    # Extract think tag trigger rates
    trigger_rates = []
    for run in all_scores.get("inner_monologue", []):
        for ent_id, ent_scores in run.get("enterprise_scores", {}).items():
            trigger_rates.append(ent_scores.get("think_tag_trigger_rate", 0))
    
    # Run statistical tests
    results = {}
    
    # H1: Inner monologue superiority
    results["H1_fidelity_superiority"] = test_h1_inner_monologue_superiority(
        all_fidelity_no_think,
        all_fidelity_inner_monologue
    )
    
    # H2: Non-inferiority (using emergent realism as proxy for decision quality)
    realism_no_think = [r.get("emergent_realism", {}).get("overall_realism", 3) 
                       for r in all_scores["no_think"] if r.get("emergent_realism")]
    realism_inner_monologue = [r.get("emergent_realism", {}).get("overall_realism", 3)
                              for r in all_scores["inner_monologue"] if r.get("emergent_realism")]
    
    results["H2_decision_non_inferiority"] = test_h2_non_inferiority(
        realism_no_think,
        realism_inner_monologue
    )
    
    # H3: Think tag trigger rate
    results["H3_think_tag_rate"] = test_h3_think_tag_trigger_rate(trigger_rates)
    
    # Save results
    output_path = Path(args.output)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Generate summary report
    report_path = output_path.with_suffix(".txt")
    generate_summary_report(results, report_path)
    
    print(f"\nResults saved to {output_path}")
    print(f"Report saved to {report_path}")


if __name__ == "__main__":
    main()
