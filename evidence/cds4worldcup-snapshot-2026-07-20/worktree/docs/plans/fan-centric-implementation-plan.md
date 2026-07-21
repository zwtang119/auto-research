# 实施计划：球迷视角 IA 改造

> 生成时间：2026-06-13
> 状态：执行中

## 概述

按 spec (`docs/superpowers/specs/2026-06-13-fan-centric-ia-redesign.md`) 实施。分为 3 个独立工作项。

---

## Item 1: 首页 (index.html + homepage.js + portal.css)

**Goal**: 将首页改为对话流（Hero→热力图→焦点比赛→选球队→AI视角→页脚），新文案，新增焦点比赛区块。

**Done when**:
- `node --check site/js/homepage.js` 无语法错误
- `site/index.html` 加载了 coach-sim-data.js 和 schedule-data.js
- `site/index.html` 只有 5 个 section + footer（无旧区块）
- homepage.js 包含 renderFocusMatches() 函数
- homepage.js 不包含 renderObstacleChart/Matrix/Baselines/Signals/Snapshot/Monitoring/ResearchLog/ExternalReferenceChart
- portal.css 包含 .focus-match-card / .fmc-* 样式

**Key files**: site/index.html, site/js/homepage.js, site/css/portal.css

**Notes**:
- index.html 已经改好了（新增了 coach-sim-data.js + schedule-data.js，新文案，移除了旧区块）
- homepage.js 部分改了但语法有错——旧函数残留导致。需要从头完整重写 homepage.js
- 已有的 renderSummary(), renderHeatmap(), renderTeamTeasers(), renderAiPerspectives() 逻辑可复用
- 新增 renderFocusMatches()——从 odds-data.js 和 coach-sim-data.js 计算 max(|diff|) Top 6

**Strategy**: 完整重写 homepage.js（不要在旧文件上修补），避免残留旧函数。

---

## Item 2: 球队详情页 (team.html + team-detail.js)

**Goal**: 将球队详情页从 11 个数据展示区块改为咨询分析论证链（论点→证据→反证→关键变量→验证→共识→附录）。

**Done when**:
- `node --check site/js/team-detail.js` 无语法错误
- team.html 结构包含：论点、证据链、反证、关键变量、验证、共识、折叠附录
- team-detail.js 包含路径衰减计算（stages[i] - stages[i+1]）
- team-detail.js 对比其他热门队的衰减值

**Key files**: site/team.html, site/js/team-detail.js

**Data structures**:
- `CDS4WORLDCUP_CDS_PATHS.teams[canonical_name]`: { qualification.qual_prob, championship.championship_prob, championship.path_nodes[{cumulative_prob}] }
- `CDS4WORLDCUP_TEAM_DETAILS.teams[slug]`: { analysis.opening, analysis.thesis, analysis.sections[], primary_obstacles[], required_breakthroughs[], watchlist[], ai_perspective, public_references }
- `CDS4WORLDCUP_SCHEDULE.groups[group_letter].matches[]`: { match_id, round, date, home, away, home_code, away_code }
- `CDS4WORLDCUP_ODDS.predictions[]`: { match_id, home_team, away_team, home_win, draw, away_win }
- `CDS4WORLDCUP_BASELINES.baselines`: { fifa_ranking/elo/market → { teams: [{slug, probability}] } }

**6 stages mapping**: [qual_prob, path_nodes[0].cumulative_prob, path_nodes[1].cumulative_prob, path_nodes[2].cumulative_prob, path_nodes[3].cumulative_prob, championship_prob]

---

## Item 3: 比赛详情页修复 (match.html + match.js)

**Goal**: 修复 match.html 导航死胡同——在 VS Hero 双方队名上加 `<a>` 链接到 team.html。

**Done when**:
- match.js renderHero() 中双方队名是可点击链接 → team.html?team=SLUG

**Key files**: site/match.js (renderHero 函数)

---

## 进度

- [x] Item 0: index.html 重写（已完成）
- [ ] Item 1: homepage.js + portal.css
- [ ] Item 2: team.html + team-detail.js
- [ ] Item 3: match.js 导航修复
