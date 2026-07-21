# 球迷视角信息架构重设计: Plan

## Goal

将 CDS4WorldCup 公站从"球队视角"（pick a team → see everything）转为"球迷视角"（answer my question → let me explore），以 4 个核心球迷问题重新组织首页和站点导航。

## Background

### 根本性视角偏差（用户反馈）

当前站点的信息架构以"球队"为主轴：首页有 8 张球队卡、球队列表页有 48 张卡、球队详情页是 10 个 section。但球迷的心智模型不是"我要了解一支球队"，而是：

1. **"我应该看哪场比赛？"** → 比赛级视角（哪场最刺激/最关键）
2. **"下一场什么时候踢？"** → 时间级视角（倒计时/赛程表）
3. **"我支持的队能走多远？"** → 路径级视角（阶段概率热力图）
4. **"大家怎么看？意见统一吗？"** → 分歧级视角（多源对比）

### 数据资产现状（探索发现）

| 球迷问题 | 关键数据文件 | 加载状态 | 备注 |
|---------|------------|---------|------|
| Q1: 哪场好看 | odds-data.js（72场概率）, coach-sim-data.js（72场另一种模型概率） | ❌ 未加载 | 两模型对同一场比赛可差 28%（如 MEX-RSA: 70% vs 42%） |
| Q2: 什么时候踢 | schedule-data.js（104场完整赛程+16场馆+时区） | ❌ 未加载 | match.js 用 fetch 按需加载，但首页无赛程信息 |
| Q3: 能走多远 | cds-paths-data.js（48队6阶段概率） | ✅ 已加载 | 热力图已实现 |
| Q4: 意见统一吗 | predictions-data.js（10派系×8队分解）, baselines-data.js（3基线） | 部分已加载 | predictions-data.js 完全未用；public_consensus_gap 结构已搭但为空 |

**核心发现**：4 个球迷问题中 3 个有数据但完全没接入页面。最丰富的分歧数据（predictions-data.js 的 10 派系分解 + 两模型比赛级对比）从未展示。

### 设计参考（design-draft-2.html 的球迷模式）

design-draft-2.html 展示了球迷视角的设计语言：
- **焦点比赛**：手动精选 + 倒计时（live/soon/future）+ 三段概率条 → "先盯这 6 场"
- **分歧区**：三色横条并列（Elo/市场/模型） → "分歧本身值得看"
- **Live Ticker**：滚动新闻流 + 脉冲绿点 → "正在发生什么"
- **Momentum Sparkline**：7 日趋势 SVG + delta 值 → "在变强还是在掉"

### 当前页面导航缺口

- match.html 是导航死胡同（无球队链接）
- 首页没有比赛级信息（无赛程、无比赛推荐）
- 全景图是唯一有比赛信息的页面，但以"完整赛程"呈现而非"推荐看哪场"

## Open Questions

- 焦点比赛是用算法筛选（概率差最大的比赛 = 最刺激）还是需要人工标注？
- Live Ticker 的数据来源是什么？当前没有实时数据管道。
- Momentum Sparkline 需要 7 日历史数据，当前只有单一时间点的数据，如何处理？

## References

- 数据资产审计：explore agent "Fan-relevant data assets" 的完整发现
- 设计参考：site/design-draft-2.html 的焦点比赛/分歧/Ticker/热力图分析
- 现有信息架构：docs/superpowers/specs/2026-06-13-site-information-architecture-design.md
