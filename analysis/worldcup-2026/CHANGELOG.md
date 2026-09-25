# CHANGELOG — analysis/worldcup-2026/

> 分析副本增补日志。每条记录：内容、来源、时间、执行者。封存仓库(cds4worldcup)零读写；证据快照只读；本目录可写。

## 2026-09-11（Paper A 连贯工作稿 · 不改证据）

- **内容**：将 skeleton、§3/§4/§5.2/§5.3、摘要稿、claims-master、理由审计、谱系与 FIFA memo 收束为一篇连贯工作稿。
- **落盘**：`docs/plans/paper-a-full-draft-2026-09-11.md`（计划目录，不覆盖冻结开题/路线图）。
- **未执行**：未读写封存仓、未改 evidence、未跑 `fig6_and_metrics`、未做 G2 一键复算。
- **口径**：均匀 Brier 不采用 0.02083；数字均标未经本轮 G2。
- **执行者**：本会话写作；未 git commit。

## 2026-07-27（落盘重整合 · 4 章「四个新观点」再评估终稿）

- **内容**：将对话中已交付但仅存文本的《2026 世界杯算法对比论文——四个新观点的深度再评估》（4 章 / 26–27 源）基于冻结工作文件重新整合为正式文件。
- **中间产物（4 章草稿，均已落盘）**：
  - `_dr-ch1-v2-grouping-2026-07-27.md`（分组规则再评估）— 来源：bracket-aware-ranking / bracket-encoding-verification / claim-verification 等工作文件；执行者：topic-researcher-12
  - `_dr-ch2-v3-cds-timeline-2026-07-27.md`（西班牙夺冠时间线）— 来源：bracket-encoding-verification / market-sentiment-and-n48 / 证据快照 cds_championship.json / market_public_snapshot.json / kimi_agent_inventory.csv；执行者：topic-researcher-13
  - `_dr-ch3-v2-cape-verde-2026-07-27.md`（佛得角之夜市场情绪）— 来源：market-sentiment-and-n48 + Croxson&Reade2018 / Snowberg&Wolfers2010 / Angelini&DeAngelis2026 / Wolfers&Zitzewitz2004 等；执行者：topic-researcher-14
  - `_dr-ch4-v2-polymarket-2026-07-27.md`（Polymarket 定价机制）— 来源：faction-lmu-polymarket + UMA 官方文档 / Kalshi(CEPR) / 预测市场学术文献；执行者：topic-researcher-15
- **框架部分（Phase 4）**：目录 + 引言 + 结论 + 27 条 APA 参考文献 — 执行者：report-writer（程文成）
- **终稿（Phase 5）**：`worldcup-four-claims-reassessment-2026-07-27.md`（368 行 / 27 源 / Final QA 通过）— 执行者：report-publisher（傅梓铭）
- **事实底座（锁定，不得回潮）**：冠军西班牙/亚军阿根廷/季军英格兰/第四法国（英格兰 6–4 法国）；引擎 top-3 {西,法,阿}≠实际{西,阿,英}；CDS 平线 0.0325–0.0331；kimi 冻结 23.82% 7-18 前领先 7-18/19 被反超。
- **合规**：未输出投注建议、未报告收益率；Green/Red 分级；封存仓库零读写、证据快照只读。
- **备注**：终稿「待完善事项」记录 2 项轻微问题（参考文献 Murphy1977 与 all-paper-claims-master 链接目标重叠；跨章小节绝对层级差异，源继承非错误），均非阻断。
- **未执行**：未 git commit/push（按 AGENTS.md 须用户授权）。
