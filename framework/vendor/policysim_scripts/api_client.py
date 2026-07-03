"""统一 API 调用模块 — 支持所有模型供应商的 OpenAI 兼容接口。

所有 LLM 调用都通过 call_model / call_model_json 入口。
当 prompt_log_dir 参数设置时，自动记录完整 prompt 和 response 到
prompt-log.jsonl + prompts/ 子目录（借鉴 cds4polymarket 的 prompt provenance 设计）。
"""

import os
import time
import yaml
import httpx
from openai import OpenAI

from prompt_logger import log_prompt_call


def load_config(config_path="config/experiment-config.yaml"):
    """加载主配置文件。"""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def create_client(config, provider):
    """根据供应商创建 OpenAI 兼容客户端。"""
    endpoint = config["api_endpoints"][provider]
    api_key = os.environ.get(endpoint["api_key_env"])
    if not api_key:
        raise ValueError(f"Missing env var: {endpoint['api_key_env']}")
    return OpenAI(base_url=endpoint["base_url"], api_key=api_key,
                  timeout=httpx.Timeout(480.0, connect=30.0))


def call_model(config, model_name, messages, temperature=None, max_tokens=None,
              prompt_log_dir=None, prompt_stage=None, prompt_metadata=None):
    """调用指定模型，返回 (文本响应, token用量字典)。自动处理重试。

    Args:
        prompt_log_dir: 若设置，将完整 prompt+response 写入此目录。
        prompt_stage: 日志中的阶段标识（如 generate_sasr, gt2_annotation）。
        prompt_metadata: 日志中的额外元数据（如 enterprise_id, run_id）。
    """
    model_cfg = config["models"][model_name]
    client = create_client(config, model_cfg["provider"])

    params = {
        "model": model_cfg["model_id"],
        "messages": messages,
        "temperature": temperature if temperature is not None else model_cfg["params"].get("temperature", 0.7),
        "max_tokens": max_tokens if max_tokens is not None else model_cfg["params"].get("max_tokens", 2048),
    }

    for attempt in range(3):
        try:
            response = client.chat.completions.create(**params)
            content = response.choices[0].message.content
            usage = {}
            if response.usage:
                usage = {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                }
            # Prompt provenance: 当 prompt_log_dir 设置时记录完整调用
            # 使用 try/except 防止日志失败导致已收到的 API 响应丢失
            if prompt_log_dir:
                try:
                    log_prompt_call(
                        log_dir=prompt_log_dir,
                        stage=prompt_stage or "unknown",
                        model=model_name,
                        messages=messages,
                        response=content,
                        call_kind="call_model",
                        metadata=prompt_metadata,
                    )
                except Exception as log_err:
                    print(f"    WARNING: prompt logging failed: {log_err}")
            return content, usage
        except Exception as e:
            if attempt < 2:
                wait = 2 ** (attempt + 1)
                print(f"    Retry {attempt+1}/3 after {wait}s: {e}")
                time.sleep(wait)
            else:
                raise


def call_model_json(config, model_name, messages, temperature=None, max_tokens=None,
                    prompt_log_dir=None, prompt_stage=None, prompt_metadata=None):
    """调用模型并尝试解析 JSON 响应。

    Args:
        prompt_log_dir: 若设置，将完整 prompt+response 写入此目录。
        prompt_stage: 日志中的阶段标识。
        prompt_metadata: 日志中的额外元数据。
    """
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
    # Prompt provenance: 当 prompt_log_dir 设置时记录完整调用
    # 使用 try/except 防止日志失败导致已收到的 API 响应丢失
    if prompt_log_dir:
        try:
            log_prompt_call(
                log_dir=prompt_log_dir,
                stage=prompt_stage or "unknown",
                model=model_name,
                messages=messages,
                response=content,
                call_kind="call_model_json",
                metadata=prompt_metadata,
            )
        except Exception as log_err:
            print(f"    WARNING: prompt logging failed: {log_err}")
    return content
