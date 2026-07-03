# P1.1 Inner Monologue → RoleDNA Role Consistency Validation

## Overview

This experiment validates whether exposing agent inner monologue (character-immersed `<think>` tags) improves role-behavior consistency with assigned RoleDNA, and whether consistent role behavior leads to more realistic emergent group dynamics in emergency simulations.

## Experimental Design

**3 modes × Gulei scenario × 50 MC runs each = 150 total runs**

| Mode | Description | Control Instruction |
|------|-------------|---------------------|
| **Mode A (no_think)** | Baseline - no think tags | None |
| **Mode B (inner_monologue)** | Character-immersed thinking | 【角色沉浸要求】 |
| **Mode C (pure_analysis)** | Logical analysis only | 【思维模式要求】 |

## Hypotheses

- **H1**: Inner-monologue agents show higher RoleDNA fidelity scores than no-think agents (p<0.05)
- **H2**: Pure-analysis agents show logically cleaner but less-characteristic decisions
- **H3**: Think-tag trigger rate ≥ 85% in Mode B
- **H4**: Spearman's ρ between RoleDNA risk_tolerance and agent cautiousness ≥ 0.4

## Scripts

### 1. `scripts/inner_monologue_experiment.py`

Main experiment runner that:
- Loads PolicySim scenario and anti-template configuration
- Builds prompts with mode-specific control instructions
- Runs MAMR (Multi-Agent Multi-Round) simulations
- Tracks think-tag trigger rates

**Usage:**
```bash
# Run Mode A (no_think) baseline
python scripts/inner_monologue_experiment.py --mode no_think --runs 50

# Run Mode B (inner_monologue)
python scripts/inner_monologue_experiment.py --mode inner_monologue --runs 50

# Run Mode C (pure_analysis)
python scripts/inner_monologue_experiment.py --mode pure_analysis --runs 50
```

### 2. `scripts/llm_judge_scoring.py`

LLM Judge evaluation that:
- Scores RoleDNA fidelity across 5 dimensions
- Evaluates emergent realism of group interactions
- Tracks think-tag trigger rates

**Usage:**
```bash
# Score no_think results
python scripts/llm_judge_scoring.py --experiment-dir experiments/no_think --judge-model deepseek-v4-pro

# Score inner_monologue results
python scripts/llm_judge_scoring.py --experiment-dir experiments/inner_monologue --judge-model deepseek-v4-pro
```

### 3. `scripts/statistical_analysis.py`

Statistical hypothesis testing that:
- Tests H1: Inner monologue superiority (one-sided t-test)
- Tests H2: Decision quality non-inferiority
- Tests H3: Think-tag trigger rate (binomial test)
- Tests H4: Spearman correlation

**Usage:**
```bash
python scripts/statistical_analysis.py \
  --no-think-dir experiments/no_think \
  --inner-monologue-dir experiments/inner_monologue \
  --output statistical_report.json
```

## Dependencies

- PolicySim MC engine: `/Users/tangzw119/Documents/GitHub/policysim-research-Tsinghua/`
- DeepSeek-V4-Pro model via Paratera API
- Python packages: pyyaml, scipy, numpy

## Output Structure

```
experiments/
├── no_think/
│   ├── metadata.json
│   ├── run_001/
│   │   ├── LANDSPACE.yaml
│   │   ├── SPACETIMETECH.yaml
│   │   └── ISPACE.yaml
│   └── ...
├── inner_monologue/
│   └── ...
├── pure_analysis/
│   └── ...
└── scores.jsonl
```

## Success Criteria

- [ ] Mode B (inner_monologue) RoleDNA fidelity > Mode A by ≥ 0.5 (p<0.05)
- [ ] Mode B decision quality non-inferior to Mode A
- [ ] Think-tag trigger rate ≥ 85% in Mode B
- [ ] Spearman's ρ between RoleDNA risk_tolerance and cautiousness ≥ 0.4

## Paper Target

- **Title**: *Inner Monologue as a Window into Multi-Agent Reasoning: Validating Role Consistency in Emergency AI Systems*
- **Venue**: ACL 2027 / EMNLP 2027
