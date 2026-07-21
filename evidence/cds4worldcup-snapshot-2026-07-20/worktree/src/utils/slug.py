"""slug.py — 球队名 → URL slug"""


def slugify(team_name: str) -> str:
    """将球队英文名转为 URL-safe slug。

    例: "Costa Rica" → "costa-rica", "Côte d'Ivoire" → "côte-divoire"
    """
    return team_name.lower().replace(" ", "-").replace("'", "")
