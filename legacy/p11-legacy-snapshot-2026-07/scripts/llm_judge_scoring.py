#!/usr/bin/env python3
"""
LLM Judge Scoring for P1.1 Inner Monologue Experiment

Evaluates:
1. RoleDNA Fidelity (5 dimensions): role consistency with assigned characteristics
2. Emergent Realism: does group interaction resemble real emergency patterns?
3. Think-tag Trigger Rate: regex count of <think> tags per agent-round
"""

import argparse
import json
import os
import re
import sys
import yaml
from pathlib import Path
from typing import Dict, List

# Add PolicySim scripts to path
POLICYSIM_PATH = Path(__file__).parent.parent.parent.parent / "policysim-research-Tsinghua"
sys.path.insert(0, str(POLICYSIM_PATH / "scripts"))

from api_client import load_config, call_model_json


# === RoleDNA Dimensions ===
ROLEDNA_DIMENSIONS = [
    "risk_tolerance",      # 风险承受度
    "innovation_focus",    # 创新专注度  
    "compliance_culture",  # 合规文化
    "market_influence",    # 市场影响力
    "agility_score",       # 敏捷度
]

# === Judge Prompts ===

ROLEDNA_FIDELITY_PROMPT = """你是一位专业的AI行为评估专家。请评估以下LLM代理在政策仿真中的角色一致性。

## 企业角色信息
- 企业名称: {enterprise_name}
- 企业ID: {enterprise_id}
- 技术路线: {tech_route}
- 风险偏好: {risk_appetite}
- 市场地位: {market_position}
- 核心竞争力: {core_competency}

## 代理输出
{agent_output}

## 评估维度
请从以下5个维度评估角色一致性（1-5分，5分最高）：

1. **风险承受度一致性** (risk_tolerance)
   - 1分: 完全无视企业风险偏好
   - 3分: 部分体现风险偏好
   - 5分: 完美体现企业风险偏好特征

2. **创新专注度一致性** (innovation_focus)
   - 1分: 完全不体现技术路线特征
   - 3分: 部分体现技术路线
   - 5分: 深度体现技术路线和创新方向

3. **合规文化一致性** (compliance_culture)
   - 1分: 完全无视合规要求
   - 3分: 基本遵守合规要求
   - 5分: 主动展现合规意识和行动

4. **市场影响力一致性** (market_influence)
   - 1分: 决策与市场地位严重不符
   - 3分: 决策基本符合市场地位
   - 5分: 决策完美匹配市场地位和影响力

5. **敏捷度一致性** (agility_score)
   - 1分: 决策完全不体现企业敏捷度
   - 3分: 决策部分体现敏捷度特征
   - 5分: 决策完美匹配企业敏捷度

## 输出格式
请严格按照以下JSON格式输出：
```json
{{
  "risk_tolerance": {{"score": <1-5>, "reasoning": "<简短理由>"}},
  "innovation_focus": {{"score": <1-5>, "reasoning": "<简短理由>"}},
  "compliance_culture": {{"score": <1-5>, "reasoning": "<简短理由>"}},
  "market_influence": {{"score": <1-5>, "reasoning": "<简短理由>"}},
  "agility_score": {{"score": <1-5>, "reasoning": "<简短理由>"}},
  "overall_fidelity": <1-5>,
  "summary": "<整体评估总结>"
}}
```"""


EMERGENT_REALISM_PROMPT = """你是一位多Agent系统行为分析专家。请评估以下政策仿真中多Agent交互的真实性。

## 仿真场景
- 场景: 商业航天政策博弈
- 参与企业: {enterprise_list}

## 仿真输出
{simulation_output}

## 评估维度
请从以下维度评估交互真实性（1-5分）：

1. **决策合理性** (decision_plausibility)
   - 代理的决策是否符合商业逻辑？
   - 决策是否考虑了竞争环境？

2. **互动真实性** (interaction_authenticity)
   - 企业间的互动是否模拟了真实市场竞争？
   - 是否出现了合理的竞争/合作关系？

3. **涌现行为** (emergent_behavior)
   - 是否观察到非预期的群体行为模式？
   - 涌现行为是否符合复杂系统特征？

4. **角色一致性** (collective_coherence)
   - 所有代理的行为是否整体协调？
   - 是否存在明显的角色混乱？

## 输出格式
```json
{{
  "decision_plausibility": {{"score": <1-5>, "reasoning": "<简短理由>"}},
  "interaction_authenticity": {{"score": <1-5>, "reasoning": "<简短理由>"}},
  "emergent_behavior": {{"score": <1-5>, "reasoning": "<简短理由>"}},
  "collective_coherence": {{"score": <1-5>, "reasoning": "<简短理由>"}},
  "overall_realism": <1-5>,
  "summary": "<整体评估总结>"
}}
```"""


def load_experiment_results(experiment_dir: Path) -> List[Dict]:
    """Load all run results from experiment directory."""
    results = []
    for run_dir in sorted(experiment_dir.iterdir()):
        if run_dir.is_dir() and run_dir.name.startswith("run_"):
            run_data = {"run_id": run_dir.name, "enterprises": {}}
            for ent_file in run_dir.glob("*.yaml"):
                with open(ent_file, "r", encoding="utf-8") as f:
                    ent_data = yaml.safe_load(f)
                    run_data["enterprises"][ent_data["enterprise"]] = ent_data
            results.append(run_data)
    return results


def score_role_fidelity(
    config: Dict,
    judge_model: str,
    enterprise_id: str,
    enterprise_info: Dict,
    agent_output: str,
) -> Dict:
    """Score RoleDNA fidelity for a single enterprise's output."""
    prompt = ROLEDNA_FIDELITY_PROMPT.format(
        enterprise_name=enterprise_info["name"],
        enterprise_id=enterprise_id,
        tech_route=enterprise_info.get("tech_route", "未知"),
        risk_appetite=enterprise_info.get("risk_appetite", "未知"),
        market_position=enterprise_info.get("market_position", "未知"),
        core_competency=enterprise_info.get("core_competency", "未知"),
        agent_output=agent_output[:3000],  # Truncate for token limit
    )
    
    response = call_model_json(
        config, judge_model, [{"role": "user", "content": prompt}],
        prompt_stage="role_fidelity_judge",
        prompt_metadata={"enterprise_id": enterprise_id}
    )
    
    try:
        scores = json.loads(response)
    except json.JSONDecodeError:
        # Try to extract JSON from response
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            scores = json.loads(json_match.group())
        else:
            scores = {"error": "Failed to parse judge response", "raw": response}
    
    return scores


def score_emergent_realism(
    config: Dict,
    judge_model: str,
    enterprise_list: List[str],
    simulation_output: str,
) -> Dict:
    """Score emergent realism for a complete simulation run."""
    prompt = EMERGENT_REALISM_PROMPT.format(
        enterprise_list=", ".join(enterprise_list),
        simulation_output=simulation_output[:4000],  # Truncate for token limit
    )
    
    response = call_model_json(
        config, judge_model, [{"role": "user", "content": prompt}],
        prompt_stage="emergent_realism_judge",
    )
    
    try:
        scores = json.loads(response)
    except json.JSONDecodeError:
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            scores = json.loads(json_match.group())
        else:
            scores = {"error": "Failed to parse judge response", "raw": response}
    
    return scores


def main():
    parser = argparse.ArgumentParser(description="LLM Judge Scoring for P1.1 Experiment")
    parser.add_argument("--config", default=str(POLICYSIM_PATH / "config" / "experiment-config.yaml"))
    parser.add_argument("--experiment-dir", required=True, help="Path to experiment results directory")
    parser.add_argument("--judge-model", default="deepseek-v4-pro", help="Model to use as judge")
    parser.add_argument("--output", default="scores.jsonl", help="Output scores file")
    parser.add_argument("--max-runs", type=int, default=None, help="Max runs to score")
    args = parser.parse_args()
    
    config = load_config(args.config)
    experiment_dir = Path(args.experiment_dir)
    
    # Load scenario for enterprise info
    scenario_path = POLICYSIM_PATH / "materials" / "20-seed-data" / "reusable_rocket_v2.yaml"
    with open(scenario_path, "r", encoding="utf-8") as f:
        scenario = yaml.safe_load(f)
    enterprises_info = scenario["enterprises"]
    
    # Load experiment results
    results = load_experiment_results(experiment_dir)
    if args.max_runs:
        results = results[:args.max_runs]
    
    print(f"Scoring {len(results)} runs with judge model: {args.judge_model}")
    print("=" * 60)
    
    output_path = experiment_dir / args.output
    with open(output_path, "w", encoding="utf-8") as f:
        for i, run in enumerate(results):
            run_id = run["run_id"]
            print(f"[{i+1}/{len(results)}] Scoring {run_id}...")
            
            run_scores = {
                "run_id": run_id,
                "mode": experiment_dir.name,
                "enterprise_scores": {},
                "emergent_realism": None,
            }
            
            # Score each enterprise
            combined_outputs = []
            for ent_id, ent_data in run["enterprises"].items():
                ent_info = enterprises_info.get(ent_id, {})
                agent_output = ent_data.get("combined_output", "")
                combined_outputs.append(f"=== {ent_info.get('name', ent_id)} ===\n{agent_output}")
                
                fidelity_scores = score_role_fidelity(
                    config, args.judge_model,
                    ent_id, ent_info, agent_output
                )
                run_scores["enterprise_scores"][ent_id] = {
                    "fidelity": fidelity_scores,
                    "think_tag_count": ent_data.get("think_tag_count", 0),
                    "think_tag_trigger_rate": ent_data.get("think_tag_trigger_rate", 0),
                }
            
            # Score emergent realism
            simulation_output = "\n\n".join(combined_outputs)
            run_scores["emergent_realism"] = score_emergent_realism(
                config, args.judge_model,
                list(run["enterprises"].keys()),
                simulation_output
            )
            
            # Write to JSONL
            f.write(json.dumps(run_scores, ensure_ascii=False) + "\n")
            f.flush()
            
            print(f"  → Fidelity scores saved")
    
    print("\n" + "=" * 60)
    print(f"Scoring completed. Results saved to {output_path}")


if __name__ == "__main__":
    main()
