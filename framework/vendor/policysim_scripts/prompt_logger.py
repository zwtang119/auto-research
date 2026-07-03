"""
Prompt Logger — 轻量级 LLM prompt 持久化模块。

借鉴 cds4polymarket 的 prompt_provenance_service.py，但大幅简化：
- 不使用 Pydantic / contextvars（policysim 是同步脚本架构）
- PromptRecord 用普通 dict
- 只依赖标准库（hashlib, json, uuid, datetime, pathlib）

使用方式：
  from prompt_logger import log_prompt_call
  log_prompt_call(
      log_dir=exp_dir / "prompt-logs",
      stage="generate_sasr",
      model="deepseek-v4-flash",
      messages=[{"role": "user", "content": "..."}],
      response="AI 回复内容",
  )

每次调用会在 log_dir 下写入：
  prompt-log.jsonl          # 索引 + 哈希（每条一行 JSON）
  prompts/
    <record_id>.prompt.md   # 完整 messages 文本
    <record_id>.response.txt # 完整 response 文本
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


def _sha256_text(text: str) -> str:
    """计算文本的 SHA-256 哈希。"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _utc_now_iso() -> str:
    """当前 UTC 时间 ISO 格式。"""
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _messages_to_text(messages: list[dict[str, str]]) -> str:
    """将 messages 列表转为可读文本。"""
    parts = []
    for msg in messages:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        parts.append(f"## Role: {role}\n\n{content}")
    return "\n\n---\n\n".join(parts)


def _ensure_dir(path: Path) -> None:
    """确保目录存在。"""
    path.mkdir(parents=True, exist_ok=True)


def log_prompt_call(
    *,
    log_dir: Path | str,
    stage: str,
    model: str,
    messages: list[dict[str, str]],
    response: str,
    call_kind: str = "call_model",
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """记录一次 LLM 调用的完整 prompt 和 response。

    Args:
        log_dir: prompt-logs 目录路径
        stage: 调用阶段（如 generate_sasr, gt2_annotation, validate_track_a）
        model: 模型名称
        messages: 发送给 LLM 的完整 messages 列表
        response: LLM 返回的文本
        call_kind: 调用类型（call_model / call_model_json）
        metadata: 额外元数据（如 enterprise_id, run_id, round_num 等）

    Returns:
        PromptRecord dict，包含 record_id 和所有哈希
    """
    log_dir = Path(log_dir)
    _ensure_dir(log_dir)
    prompts_dir = log_dir / "prompts"
    _ensure_dir(prompts_dir)

    # 生成唯一 record_id
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    record_id = f"prompt-{ts}-{uuid4().hex[:8]}"

    # 完整文本
    prompt_text = _messages_to_text(messages)

    # 写入文件
    prompt_file = prompts_dir / f"{record_id}.prompt.md"
    response_file = prompts_dir / f"{record_id}.response.txt"
    prompt_file.write_text(prompt_text, encoding="utf-8")
    response_file.write_text(response, encoding="utf-8")

    # 哈希
    prompt_sha256 = _sha256_text(prompt_text)
    response_sha256 = _sha256_text(response)

    # 构建 record
    meta = dict(metadata) if metadata else {}
    record: dict[str, Any] = {
        "record_id": record_id,
        "created_at_utc": _utc_now_iso(),
        "stage": stage,
        "call_kind": call_kind,
        "model": model,
        "prompt_file": f"prompts/{record_id}.prompt.md",
        "response_file": f"prompts/{record_id}.response.txt",
        "prompt_sha256": prompt_sha256,
        "response_sha256": response_sha256,
        "prompt_chars": len(prompt_text),
        "response_chars": len(response),
        "num_messages": len(messages),
        "metadata": meta,
    }

    # 追加到 JSONL
    jsonl_path = log_dir / "prompt-log.jsonl"
    with open(jsonl_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return record
