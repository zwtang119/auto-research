"""
poisson.py — 共享 Poisson 模拟函数

从 numeric_odds.py 提取的泊松分布计算函数，供多个预测模型复用。

来源等级: Red（模型输出，非事实）
依赖: 仅 stdlib（math）
"""

import math


def poisson_prob(lam, k):
    """泊松分布 P(X=k)

    Args:
        lam: 期望值 λ (>= 0)
        k: 观测值 (非负整数)

    Returns:
        P(X=k) 概率值
    """
    return (lam ** k) * math.exp(-lam) / math.factorial(k)


def simulate_goal_matrix(lam_home, lam_away, max_goals=7):
    """构建联合进球概率矩阵 P(home=i, away=j)

    Args:
        lam_home: 主队期望进球数
        lam_away: 客队期望进球数
        max_goals: 进球截断上限（含）

    Returns:
        dict of dict: matrix[i][j] = P(home=i, away=j)
    """
    matrix = {}
    for i in range(max_goals + 1):
        row = {}
        for j in range(max_goals + 1):
            row[j] = poisson_prob(lam_home, i) * poisson_prob(lam_away, j)
        matrix[i] = row
    return matrix


def normalize_probs(home_win, draw, away_win):
    """归一化胜/平/负概率，使总和为 1.0

    Args:
        home_win: 主胜概率
        draw: 平局概率
        away_win: 客胜概率

    Returns:
        (home_win, draw, away_win) 归一化后的三元组
    """
    total = home_win + draw + away_win
    if total > 0:
        home_win /= total
        draw /= total
        away_win /= total
    return (home_win, draw, away_win)


def compute_match_probs_from_lambdas(lam_home, lam_away, max_goals=7):
    """从 λ 值直接计算胜/平/负概率

    组合 simulate_goal_matrix + 聚合 + 归一化。

    Args:
        lam_home: 主队期望进球数
        lam_away: 客队期望进球数
        max_goals: 进球截断上限（含）

    Returns:
        (home_win, draw, away_win) 三元组
    """
    matrix = simulate_goal_matrix(lam_home, lam_away, max_goals)

    p_home_win = 0.0
    p_draw = 0.0
    p_away_win = 0.0

    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            p = matrix[i][j]
            if i > j:
                p_home_win += p
            elif i == j:
                p_draw += p
            else:
                p_away_win += p

    return normalize_probs(p_home_win, p_draw, p_away_win)
