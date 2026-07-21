"""kimi.py — Kimi 300 Agent 数据处理共享函数"""

def group_kimi_by_team(agents: list[dict]) -> dict[str, list[dict]]:
    """按 champion 字段（中文队名）分组 Kimi agent 数据。"""
    by_team: dict[str, list[dict]] = {}
    for a in agents:
        champ = a.get("champion", "").strip()
        if champ not in by_team:
            by_team[champ] = []
        by_team[champ].append(a)
    return by_team


def compute_signals(team: dict, kimi_agents: list[dict], kimi_prob) -> list[str]:
    """计算 kimi_baseline_signals。

    Args:
        team: 球队 registry 行（需有 coverage_status 字段）
        kimi_agents: 该队的 Kimi agent 列表
        kimi_prob: 概率字符串（如 "12.34" 或 "N/A"）
    """
    has_kimi = team.get("coverage_status") == "champion/top3"
    signals: list[str] = []

    if has_kimi:
        factions_seen = {a.get("faction", "unknown") for a in kimi_agents}
        if kimi_prob != "N/A":
            try:
                prob_val = float(kimi_prob)
                if prob_val > 10:
                    signals.append("high_kimi_probability")
                if prob_val < 5:
                    signals.append("kimi_longshot")
            except (ValueError, TypeError):
                pass
        if len(kimi_agents) > 20:
            signals.append("broad_faction_support")
        if len(factions_seen) >= 5:
            signals.append("cross_faction_consensus")

    return signals


def build_section_9(kimi_agents: list[dict], kimi_prob, today: str) -> str:
    """构建 §9 Marginalia Notes 内容。

    Args:
        kimi_agents: 该队的 Kimi agent 列表
        kimi_prob: 概率字符串
        today: 日期字符串 (YYYY-MM-DD)
    """
    lines: list[str] = []
    if kimi_agents:
        factions_seen = sorted({a.get("faction", "unknown") for a in kimi_agents})
        lines.append("## 9. Marginalia Notes\n")
        lines.append(f"### Kimi 300 Agent 摘要（{len(kimi_agents)} 条预测）\n")
        lines.append(f"- 派别分布: {', '.join(factions_seen)}")
        lines.append(f"- Kimi 聚合概率: {kimi_prob}%")
        lines.append("")
        lines.append("#### 代表性 reason（前 5 条）\n")
        for a in kimi_agents[:5]:
            faction = a.get("faction", "unknown")
            conf = a.get("confidence", "N/A")
            reason = a.get("reason", "")
            lines.append(f"- [{faction}] conf={conf}: \"{reason}\"")
        lines.append("")
        lines.append(f"> [!memo] {today} Kimi reason 暂作为 Red Source / 候选线索保留。")
        lines.append("> 等待 Plan B2 Codability Census 完成后决定哪些可进入 Factor Ledger。\n")
    else:
        lines.append("## 9. Marginalia Notes\n")
        lines.append("无 Kimi agent 预测数据。\n")
    return "\n".join(lines)
