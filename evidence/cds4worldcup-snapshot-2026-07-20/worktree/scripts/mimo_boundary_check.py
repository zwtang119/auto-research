#!/usr/bin/env python3
"""MiMo 写入边界检查脚本。

验证 MiMo sprint 的产出是否只写在允许目录中。
零依赖，Python 3.10+。
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

# MiMo 允许写入的目录（相对项目根目录）
ALLOWED_PREFIXES = [
    "data/ops/candidate/",
    "data/ops/review_queue/",
    "data/ops/mimo_outputs/",
    "results/ops/",
]

# MiMo 绝对禁止写入的目录
FORBIDDEN_PREFIXES = [
    "data/processed/",
    "artifacts/team-cards/",
    "wiki/",
    "site/",
    "schema/",
    "templates/",
    "example/",
    "docs/references/",
    ".git/",
]


def get_git_status() -> list[str]:
    """运行 git status --short 获取变更文件列表。"""
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"ERROR: git status failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return lines


def classify_path(rel_path: str) -> str:
    """分类文件路径：allowed / forbidden / unknown。"""
    for prefix in FORBIDDEN_PREFIXES:
        if rel_path.startswith(prefix):
            return "forbidden"
    for prefix in ALLOWED_PREFIXES:
        if rel_path.startswith(prefix):
            return "allowed"
    return "unknown"


def main() -> int:
    lines = get_git_status()
    if not lines:
        print("OK: No changes detected.")
        return 0

    violations = []
    allowed = []
    unknown = []

    for line in lines:
        # git status --short format: " M path/to/file" or "?? path/to/file"
        parts = line.split(maxsplit=1)
        if len(parts) < 2:
            continue
        status_code, rel_path = parts
        classification = classify_path(rel_path)

        if classification == "forbidden":
            violations.append((status_code, rel_path))
        elif classification == "allowed":
            allowed.append((status_code, rel_path))
        else:
            unknown.append((status_code, rel_path))

    if allowed:
        print(f"ALLOWED ({len(allowed)}):")
        for code, path in allowed:
            print(f"  {code} {path}")
        print()

    if unknown:
        print(f"UNKNOWN ({len(unknown)}) — please review:")
        for code, path in unknown:
            print(f"  {code} {path}")
        print()

    if violations:
        print(f"VIOLATIONS ({len(violations)}) — MUST FIX:")
        for code, path in violations:
            print(f"  {code} {path}")
        print("\nMiMo must NOT write to forbidden directories.")
        return 1

    print("OK: No boundary violations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
