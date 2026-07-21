"""csv_helpers.py — CSV 读取工具"""

import csv


def load_csv(path) -> list[dict]:
    """读取 CSV 文件并返回 DictReader 列表。"""
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))
