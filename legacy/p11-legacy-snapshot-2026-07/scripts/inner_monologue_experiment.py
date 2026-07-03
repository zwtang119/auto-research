#!/usr/bin/env python3
"""
P1.1 Inner Monologue → RoleDNA Role Consistency Validation

3 modes × Gulei scenario × 50 MC runs each = 150 total runs

Mode A (baseline): No think tags — current PolicySim default
Mode B (inner_monologue): <think>(角色内心独白)</think> before each decision
Mode C (pure_analysis): <think>纯逻辑分析, no inner monologue</think> before each decision
"""

import argparse
import json
import os
import random
import re
import sys
import time
import yaml
from pathlib import Path
from typing import Dict, List, Optional

# === API Client Functions (copied from PolicySim to avoid import issues) ===

def load_config(config_path: str) -> Dict:
    """Load the main configuration file."""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def create_client(config: Dict, provider: str):
    """Create OpenAI-compatible client based on provider."""
    from openai import OpenAI
    import httpx
    
    endpoint = config["api_endpoints"][provider]
    api_key = os.environ.get(endpoint["api_key_env"])
    
    # Fallback to OPENAI_API_KEY if provider-specific key is not set
    if not api_key and provider in ["paratera", "deepseek"]:
        api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError(f"Missing env var: {endpoint['api_key_env']}")
    
    # Use OPENAI_BASE_URL as fallback for base_url
    base_url = endpoint["base_url"]
    if not base_url and provider in ["paratera", "deepseek"]:
        base_url = os.environ.get("OPENAI_BASE_URL", endpoint["base_url"])
    
    return OpenAI(
        base_url=base_url,
        api_key=api_key,
        timeout=httpx.Timeout(480.0, connect=30.0)
    )


def call_model(
    config: Dict,
    model_name: str,
    messages: List[Dict],
    temperature: float = None,
    max_tokens: int = None,
    prompt_stage: str = None,
    prompt_metadata: Dict = None,
    enable_thinking: bool = True,
) -> tuple:
    """Call the specified model, return (text_response, token_usage_dict)."""
    model_cfg = config["models"][model_name]
    client = create_client(config, model_cfg["provider"])
    
    params = {
        "model": model_cfg["model_id"],
        "messages": messages,
        "temperature": temperature if temperature is not None else model_cfg["params"].get("temperature", 0.7),
        "max_tokens": max_tokens if max_tokens is not None else model_cfg["params"].get("max_tokens", 2048),
    }
    
    # Enable thinking mode for DeepSeek models
    if enable_thinking and "deepseek" in model_cfg["model_id"].lower():
        params["extra_body"] = {"enable_thinking": True}
    
    for attempt in range(3):
        try:
            response = client.chat.completions.create(**params)
            content = response.choices[0].message.content
            
            # Get reasoning content if available
            reasoning_content = None
            if hasattr(response.choices[0].message, 'reasoning_content'):
                reasoning_content = response.choices[0].message.reasoning_content
            
            usage = {}
            if response.usage:
                usage = {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                }
            
            # Return both content and reasoning_content
            return content, usage, reasoning_content
        except Exception as e:
            if attempt < 2:
                wait = 2 ** (attempt + 1)
                print(f"    Retry {attempt+1}/3 after {wait}s: {e}")
                time.sleep(wait)
            else:
                raise


def call_model_json(
    config: Dict,
    model_name: str,
    messages: List[Dict],
    temperature: float = None,
    max_tokens: int = None,
    prompt_stage: str = None,
    prompt_metadata: Dict = None,
) -> str:
    """Call model and try to parse JSON response."""
    model_cfg = config["models"][model_name]
    client = create_client(config, model_cfg["provider"])
    
    params = {
        "model": model_cfg["model_id"],
        "messages": messages,
        "temperature": temperature or model_cfg["params"].get("temperature", 0.7),
        "max_tokens": max_tokens or model_cfg["params"].get("max_tokens", 2048),
        "response_format": {"type": "json_object"},
    }
    
    response = client.chat.completions.create(**params)
    content = response.choices[0].message.content
    return content


# === Experiment Configuration ===

POLICYSIM_PATH = Path(__file__).parent.parent.parent.parent / "policysim-research-Tsinghua"

# === Control Instructions for each mode ===

CONTROL_INSTRUCTIONS = {
    "no_think": "",  # No additional instruction
    
    "inner_monologue": """
【角色沉浸要求】在你的思考过程（<think>标签内）中，请遵守以下规则：
1. 完全代入你所代表的企业角色，以该角色的视角进行思考
2. 考虑该角色的性格特征、风险偏好、技术路线和市场定位
3. 思考过程中体现角色的独特决策风格（如：激进型会考虑机会成本，保守型会考虑风险规避）
4. 反映角色对政策的真实态度和情感反应
5. 思考竞争对手时，从角色的立场出发分析威胁和机会

示例格式：
<think>作为{企业名}的决策者，我需要考虑...
我的{技术路线}决定了...
考虑到我的{风险偏好}，我认为...
竞争对手的{行为}对我的影响是...
""",
    
    "pure_analysis": """
【思维模式要求】在你的思考过程（<think>标签内）中，请遵守以下规则：
1. 进行纯逻辑分析，不代入任何角色情感
2. 从客观第三方视角分析政策影响
3. 使用数据和事实进行推理，避免主观判断
4. 分析各方利益相关者的立场，但不偏袒任何一方
5. 给出理性的决策建议，基于效用最大化原则

示例格式：
<think>政策分析：该政策的核心目标是...
定量影响：对行业的影响预计为...
风险评估：主要风险因素包括...
理性决策：基于效用最大化，建议...
"""
}


def load_scenario(scenario_path: str = None) -> Dict:
    """Load the Gulei scenario data."""
    if scenario_path is None:
        scenario_path = POLICYSIM_PATH / "materials" / "20-seed-data" / "reusable_rocket_v2.yaml"
    with open(scenario_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_anti_template(config_path: str = None) -> Dict:
    """Load anti-template configuration."""
    if config_path is None:
        config_path = POLICYSIM_PATH / "config" / "anti_template.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_prompt_with_mode(
    mode: str,
    enterprise_id: str,
    enterprise_data: Dict,
    policy: Dict,
    anti_template: Dict,
    round_num: int = 1,
    landscape: Optional[str] = None,
) -> List[Dict]:
    """Build prompt with mode-specific control instruction."""
    
    frameworks = anti_template["prompt_variants"]["frameworks"]
    contexts = anti_template["prompt_variants"]["context_seeds"]
    
    framework = random.choice(frameworks)
    context = random.choice(contexts)
    enterprise_name = enterprise_data["name"]
    
    base = f"{context}\n\n{framework.format(enterprise=enterprise_name)}\n\n"
    
    # Policy text
    policy_text = ""
    for ch in policy["chapters"]:
        policy_text += f"## {ch['chapter']}\n"
        for prov in ch["key_provisions"]:
            policy_text += f"- {prov}\n"
        policy_text += "\n"
    
    base += f"## 政策内容\n{policy_text}\n"
    
    # Enterprise profile
    base += f"## 企业画像：{enterprise_name} ({enterprise_id})\n"
    base += f"- 技术路线: {enterprise_data['tech_route']}\n"
    base += f"- 规模: {enterprise_data['scale']}\n"
    base += f"- 供应链策略: {enterprise_data['supply_chain_strategy']}\n"
    base += f"- 安全合规禀赋: {enterprise_data['security_compliance']}\n"
    base += f"- 标准跟随策略: {enterprise_data['standard_following']}\n\n"
    
    # One-shot format example
    base += """## 输出格式示范（仅供格式参考，内容与本实验无关）

```yaml
一阶效应:
  - 效应名称: 购车补贴直接刺激需求
    描述: 补贴政策直接降低新能源汽车购车成本，短期内显著刺激消费者购买意愿
    可能性: 高
二阶效应:
  - 效应名称: 充电基础设施投资加速
    描述: 新能源汽车销量激增带动充电桩建设需求，相关产业链获得投资拉动
    可能性: 中
三阶效应:
  - 效应名称: 传统汽修行业转型压力
    描述: 新能源车保有量持续增长，传统燃油车维修服务需求萎缩，汽修行业面临结构性转型
    可能性: 低
```

请严格参照上述 YAML 格式输出你对商业航天政策的分析（内容完全不同，自行推理）。\n\n"""
    
    # Add mode-specific instruction
    control_instruction = CONTROL_INSTRUCTIONS.get(mode, "")
    if control_instruction:
        # Replace {企业名} placeholder
        control_instruction = control_instruction.replace("{企业名}", enterprise_name)
        base += control_instruction
    
    # MAMR-specific instructions
    if round_num == 1:
        base += "这是多智能体多轮博弈的第1轮。你代表{enterprise}的决策层。\n".format(enterprise=enterprise_name)
        base += "请分析政策影响，并做出企业的策略决策。\n"
        base += "输出 YAML 格式：决策、理由、预期效应（一阶/二阶/三阶）。\n"
    else:
        summary = landscape or ""
        base += f"这是多智能体多轮博弈的第{round_num}轮。\n"
        base += f"上一轮竞争态势摘要：\n{summary}\n\n"
        base += "请基于新的竞争态势，调整你的策略决策。\n"
        base += "输出 YAML 格式：调整后的决策、理由、新发现的效应。\n"
    
    return [{"role": "user", "content": base}]


def synthesize_landscape(
    config: Dict,
    model_name: str,
    round_outputs: Dict[str, str],
    enterprises_data: Dict,
    round_num: int = 0,
) -> str:
    """Centralized topology: aggregate all enterprise decisions into landscape summary."""
    decisions_text = ""
    for ent_id, output in round_outputs.items():
        ent_name = enterprises_data[ent_id]["name"]
        decisions_text += f"### {ent_name} ({ent_id})\n{output[:800]}\n\n"
    
    prompt = f"""你是一个政策博弈分析师。请基于以下各企业的决策，生成一份简洁的"竞争态势摘要"。

要求：
1. 总结各企业的主要策略选择和立场
2. 指出竞争冲突和互补关系
3. 识别可能的市场格局变化
4. 200字以内

各企业决策：
{decisions_text}

请直接输出竞争态势摘要。"""
    
    landscape, _ = call_model(
        config, model_name, [{"role": "user", "content": prompt}],
        prompt_stage="mamr_landscape_synthesis",
        prompt_metadata={"round": round_num}
    )
    return landscape


def compute_jaccard(text_a: str, text_b: str) -> float:
    """Compute Jaccard similarity between two texts."""
    set_a = set(text_a.split())
    set_b = set(text_b.split())
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union > 0 else 0


def count_think_tags(text: str) -> int:
    """Count <think> tags in text."""
    return len(re.findall(r'<think>', text))


def generate_mamr_run(
    config: Dict,
    model_name: str,
    mode: str,
    enterprises_data: Dict,
    policy: Dict,
    anti_template: Dict,
    run_id: int,
    mamr_rounds: int = 3,
) -> List[Dict]:
    """Generate one MAMR run with specified mode.
    
    Returns: list of run data dicts, one per enterprise
    """
    total_token_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    results = {ent_id: {"responses": []} for ent_id in enterprises_data}
    landscape = None
    
    for round_num in range(1, mamr_rounds + 1):
        round_outputs = {}
        
        for ent_id, ent_data in enterprises_data.items():
            messages = build_prompt_with_mode(
                mode, ent_id, ent_data, policy, anti_template,
                round_num, landscape=landscape
            )
            
            # Retry with anti-template check
            for attempt in range(anti_template["output_constraints"]["max_retries"] + 1):
                response, usage, reasoning_content = call_model(
                    config, model_name, messages,
                    prompt_stage="generate_mamr",
                    prompt_metadata={
                        "enterprise_id": ent_id,
                        "run_id": run_id,
                        "round": round_num,
                        "condition": mode
                    }
                )
                
                if usage:
                    total_token_usage["prompt_tokens"] += usage.get("prompt_tokens", 0)
                    total_token_usage["completion_tokens"] += usage.get("completion_tokens", 0)
                    total_token_usage["total_tokens"] += usage.get("total_tokens", 0)
                
                # Anti-template Jaccard check
                if results[ent_id]["responses"]:
                    jaccard = max(
                        compute_jaccard(response, prev)
                        for prev in results[ent_id]["responses"]
                    )
                    if jaccard >= anti_template["output_constraints"]["jaccard_similarity_threshold"]:
                        if attempt < anti_template["output_constraints"]["max_retries"]:
                            messages[0]["content"] += "\n注意：请避免重复之前的分析角度。"
                            continue
                break
            
            # Store response with reasoning content
            round_outputs[ent_id] = response
            results[ent_id]["responses"].append(response)
            if reasoning_content:
                results[ent_id]["reasoning_content"] = results[ent_id].get("reasoning_content", [])
                results[ent_id]["reasoning_content"].append(reasoning_content)
            time.sleep(0.3)
        
        # Synthesize landscape for next round
        if round_num < mamr_rounds:
            landscape = synthesize_landscape(
                config, model_name, round_outputs, enterprises_data,
                round_num=round_num
            )
    
    # Build output for each enterprise
    run_data_list = []
    for ent_id, ent_data in enterprises_data.items():
        combined_output = "\n\n---\n\n".join(results[ent_id]["responses"])
        
        # Count think tags across all rounds
        total_think_tags = sum(count_think_tags(r) for r in results[ent_id]["responses"])
        
        # Build run data
        run_data = {
            "run_id": run_id,
            "mode": mode,
            "model": model_name,
            "enterprise": ent_id,
            "enterprise_name": ent_data["name"],
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
            "rounds": results[ent_id]["responses"],
            "combined_output": combined_output,
            "token_usage": total_token_usage,
            "think_tag_count": total_think_tags,
            "think_tag_trigger_rate": total_think_tags / mamr_rounds,
        }
        
        # Add reasoning content if available
        if "reasoning_content" in results[ent_id]:
            run_data["reasoning_content"] = results[ent_id]["reasoning_content"]
        
        run_data_list.append(run_data)
    
    return run_data_list


def main():
    parser = argparse.ArgumentParser(description="P1.1 Inner Monologue Experiment")
    parser.add_argument("--config", default=str(POLICYSIM_PATH / "config" / "experiment-config.yaml"))
    parser.add_argument("--mode", required=True, choices=["no_think", "inner_monologue", "pure_analysis"],
                        help="Experiment mode")
    parser.add_argument("--model", default="deepseek-v4-pro",
                        help="Model to use (default: deepseek-v4-pro)")
    parser.add_argument("--runs", type=int, default=50,
                        help="Number of MC runs per mode (default: 50)")
    parser.add_argument("--rounds", type=int, default=3,
                        help="Number of MAMR rounds (default: 3)")
    parser.add_argument("--output-dir", default=None,
                        help="Output directory (default: experiments/<mode>/)")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--skip-existing", action="store_true",
                        help="Skip runs whose output file already exists")
    args = parser.parse_args()
    
    random.seed(args.seed)
    
    config = load_config(args.config)
    scenario = load_scenario()
    anti_template = load_anti_template()
    policy = scenario["policy"]
    enterprises = scenario["enterprises"]
    
    # Output directory
    if args.output_dir:
        out_base = Path(args.output_dir)
    else:
        out_base = Path(f"experiments/{args.mode}")
    
    out_base.mkdir(parents=True, exist_ok=True)
    
    # Save experiment metadata
    metadata = {
        "experiment": "P1.1 Inner Monologue",
        "mode": args.mode,
        "model": args.model,
        "total_runs": args.runs,
        "rounds_per_run": args.rounds,
        "enterprises": list(enterprises.keys()),
        "seed": args.seed,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "status": "running"
    }
    with open(out_base / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"Starting P1.1 experiment: mode={args.mode}, model={args.model}")
    print(f"Total runs: {args.runs}, Rounds per run: {args.rounds}")
    print(f"Output directory: {out_base}")
    print("=" * 60)
    
    for run_idx in range(1, args.runs + 1):
        run_dir = out_base / f"run_{run_idx:03d}"
        
        # Skip if already exists
        if args.skip_existing and run_dir.exists():
            print(f"[{run_idx}/{args.runs}] SKIP (already exists)")
            continue
        
        run_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"[{run_idx}/{args.runs}] Generating run...")
        
        run_data_list = generate_mamr_run(
            config, args.model, args.mode,
            enterprises, policy, anti_template,
            run_id=run_idx, mamr_rounds=args.rounds
        )
        
        # Save results for each enterprise
        for run_data in run_data_list:
            ent_id = run_data["enterprise"]
            out_path = run_dir / f"{ent_id}.yaml"
            with open(out_path, "w", encoding="utf-8") as f:
                yaml.dump(run_data, f, allow_unicode=True, default_flow_style=False)
        
        # Calculate average think tag trigger rate for this run
        avg_trigger_rate = sum(r["think_tag_trigger_rate"] for r in run_data_list) / len(run_data_list)
        print(f"  → Think tag trigger rate: {avg_trigger_rate:.2%}")
        
        time.sleep(0.5)
    
    # Update metadata
    metadata["status"] = "completed"
    metadata["completed_at"] = time.strftime("%Y-%m-%dT%H:%M:%S+08:00")
    with open(out_base / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print(f"Experiment completed. Results saved to {out_base}")


if __name__ == "__main__":
    main()
