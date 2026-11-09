# 世界杯主线 — 主题导航（dreaming D2 · A 簇 20 篇）

> 生成：2026-11-09｜覆盖 `index.json` topic=`世界杯主线` 的 20 篇（挂起 18 / archived 1 / superseded 1）
> 性质：导航页，细节下沉原文；状态准绳以 [`CLAUDE.md`](../../CLAUDE.md)「当前活跃主线」表为准。不改任何原文。

## 当前有效结论

- **⏸ 无限期挂起、投稿暂停**（用户 2026-09-25 裁定，`CLAUDE.md:11`）。恢复时可能随 cds4polymarket P1–P7 同步投稿，视校对人意见。
- 主线版本口径**待裁定（C1）**：双论文路线图 v1.7 / 开题 v2.1 vs 单篇开题 v1.3。`docs/INDEX.md` C1 明列，**不擅自二选一**。
- 论文定位：审计链锚定的多预测者对账协议（audit-chain-anchored reconciliation protocol），主语是**协议**不是「谁猜对冠军」（`paper-a-full-draft-2026-09-11.md:35`）。
- Nature gap assessment 的 PASS/PARTIAL **只评设计、不评结果**；原文自承「设计阶段的 PASS 只值设计阶段的分」（`two-paper-roadmap-nature-gap-assessment-2026-07-21.md:10`）。

## 权威链

| 文档 | 版本 / 角色 | 注意 |
|---|---|---|
| [`proposal-worldcup-algorithms-v2.md`](../../docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms-v2.md) | v2.0，四阶段流水线重构、H5 协议完整性向量 | 与 v1.4 **同名同题并存**，都标「2026-07-20 主线裁定」→ C1 的具体体现 |
| [`proposal-worldcup-algorithms.md`](../../docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms.md) | v1.4，§1.4 设计哲学（受 FM 6-0 启发的类比） | 上表「开题 v1.3」指本文件早期版本；勿与 v2.0 混用 |
| [`worldcup-two-paper-roadmap-2026-07-21.md`](../../docs/roadmaps/worldcup-two-paper-roadmap-2026-07-21.md) | v1.7（W5 后 Paper A 定位降级） | 2026-07-21 用户裁定双篇拆分 |
| [`worldcup-two-paper-roadmap-2026-07-21-working.md`](../../docs/roadmaps/worldcup-two-paper-roadmap-2026-07-21-working.md) | v1.8（v1.6 三轮外部复核 + v1.7 润色 + 终审 N-1–N-5 修复） | `index.json` 有 `supersedes` 但 status=挂起 → 见 `notes-audit.md` A 类唯一 1 条 |
| [`worldcup-paper-topic-2026-07-19.md`](../../docs/investigations/worldcup-paper-topic-2026-07-19.md) | W6 终裁备忘录，`superseded` | 用户裁定降为参考，不独立成线 |
| [`paper-a-full-draft-2026-09-11.md`](../../docs/plans/paper-a-full-draft-2026-09-11.md) | 连贯工作稿 v0.1（2026-09-11，最新） | §3/§4/§5.2/§5.3 分节初稿早于它（07-25~27），落位以 `paper-a-skeleton-2026-07-25.md` 为准 |
| [`worldcup-algorithms-comparison-paper-2026-07-20.md`](../../docs/plans/worldcup-algorithms-comparison-paper-2026-07-20.md) | v1.1 方案，硬闸门 W1/G1 → W2/G0 → W4/G2 | 顺序不可换：导出完整性依赖溯源结论 |

## 已验证数字（转录原文 `path:line`，未独立复算）

- 引用锚 **`923e23a`**：`paper-a-s04-data-draft-2026-07-25.md:5` 明确 v2 §5.6 原文的 `e8d74aa` 已按 2026-07-25 披露更正。
- 快照漂移实例：`odds.json` MEX-RSA home_win `0.7629`(6/12) vs `0.7004`(7/01)；全程用 `git show 88a9bfd:data/processed/odds.json` 单一时间戳版本（`cds4worldcup-settlement-experiment-executed-2026-07-08.md:34`）。
- P4 审计自述：夺冠分布 93.5% 错配、ε^深度衰减律、共享幻觉（「哈兰德 2.33 亿欧」×9 等）——`paper-a-abstract-intro-bold-2026-07-29.md:35`。**属文档自述，未复算**。
- 三级证据结构：封存仓 `/Users/.../cds4worldcup` 零读写、`evidence/` 字节级只读、`analysis/` 可写并逐条记 CHANGELOG（`CLAUDE.md:49-55`）。

## 撤回与陷阱

- ❌ **不输出投注建议、不报告收益率**（`CLAUDE.md:71`）；事实声明引 Green Source，预测数字引 Red Source 并标 ex-ante 版本。
- ❌ 论文数字一律以我方管线从冻结数据复算为准，**不引用项目自评数字**（`CLAUDE.md:70`）。
- ❌ `paper-a-full-draft`:6 自承「**未执行 G2 一键复算**、文中数字转引自分析副本，**进投稿前须以 bundle 复算替换**」。不得把工作稿数字当已验收结果。
- ❌ 代理（oracle/pair/explore）断言必须直接计算复核后入档（`CLAUDE.md:69`）；2026-07-20 有 4 条断言 2 证伪 1 漏检的先例。
- ❌ 别把 v1.4 与 v2.0、v1.7 与 working v1.8 当同一版本；别把 `paper-a-skeleton` v0.1（待用户确认）当定稿。
- ❌ 开题 v2.0:10 评审状态仍「待 R1」；别称已通过评审。

## 未决

| 项 | 状态 |
|---|---|
| C1 主线版本口径 | **待裁定**，只标注不裁决（`docs/INDEX.md` C1） |
| 挂起恢复 | 无限期；投稿暂停 |
| Paper A / B | 工作稿 / B0 计划阶段，均未投稿 |
| `paper-a-skeleton-2026-07-25.md` | v0.1「待用户确认后填内容」 |
| R1 评审 | 未做（v2.0:10） |
| 分节初稿 §5.3 | 仅标题与骨架，内容未展开 |

## 原文入口

[`docs/investigations/`](../../docs/investigations/) ｜ [`docs/plans/`](../../docs/plans/) ｜ [`docs/roadmaps/`](../../docs/roadmaps/) ｜ [`docs/reviews/`](../../docs/reviews/) ｜ [`docs/INDEX-DETAILS.md`](../../docs/INDEX-DETAILS.md) A 节 ｜ [`docs/index.json`](../../docs/index.json)

> 本页由 dreaming 生成，写入新目录，原文 0 改动。新增报告后重跑做梦，先校验权威链是否被取代，禁止叠加新旧版本。
