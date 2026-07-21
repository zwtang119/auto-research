# 项目终止记录（Project Closure）

- **日期**：2026-07-18
- **状态**：**CLOSED** — 用户决策，全项目终止
- **终止触发**：第一性原理选题终裁完成并交付后，用户选择记录结论并结束项目，不投入 C1 方向的 4-gate 资源。

---

## 1. 最终结论（终裁摘要）

全文见 `docs/investigations/topic-selection-2026-07-18/verdict-topic-selection-first-principles.md`（依据同目录 w1 标准 / w2 审计 / w3 景观三份报告）。

- **D4 联合论文 → KILL**：「D2 复用 G3 crosswalk」经逐项核验四处不成立（projection residual 信息论不可逆；AR 侧无多结果概率向量；22-investigation corpus 无磁盘 schema；D1 不输出 D4 声称的 per-record 信号）。
- **D2 → KILL**（特征数学不可计算）；**D3 → 并入 D1**（§6 是 spec 不是实验）；**D1 → PARK**（自报 92.9% vs 实测 64.3%；Findings 7.0-7.5 诚实版，未执行）。
- **唯一顶刊可行方向**：把「AI 自动化研究」作为实证对象（W3-C1：长周期过程 trace + 失败模式 taxonomy + stop/pivot 决策边界），GO 附 4 条硬 gate（见 §4）。**用户选择不启动** → 按终裁 §6 拒绝条款，诚实结论为：**本项目没有已验证的顶刊课题**。
- **「AI 做 Auto Research」是否新方向**：作为造系统——不新，拒绝（赛道饱和、frontier lab 占位、SOTA 卡在 20-42%）；作为研究对象——新且是文献最大空白，但未及验证即终止。

## 2. 幸存资产（未来重启时的入口）

| 资产 | 路径 | 说明 |
|---|---|---|
| 选题终审包 | `docs/investigations/topic-selection-2026-07-18/` | w1 第一性原理标准（三层溯源）、w2 D1-D4 审计、w3 景观+资产、verdict memo |
| 过程 trace | `state/progress.json`（18 events）、`state/findings.jsonl`、`state/iteration_log.jsonl`、`logs/` | 带证伪决策记录的长周期研究 trace，公开文献无等价物 |
| 方法论沉淀 | `framework/knowledge/`、`framework/schemas/`、`docs/papers-closed-portfolio/g3-methods-paper-outline.md` | 含 first-class paper 中译 + exemplar 标尺 + PIT 反模式库 |
| 原始实验数据 | `legacy/p11-*/experiments/`（30+ raw-data 目录）、`papers/*/wiki/` | P11 三条件对照实验等 |
| 外部结算锚 | cds4worldcup settlement records（5 个，姊妹项目） | Brier replay 真实锚 |

## 3. 各方向终态

| 方向 | 终态 |
|---|---|
| P11 inner monologue | CLOSED（workshop pillar，负结果保留） |
| P12 judge calibration | G2 N=30 FALSIFIED（N=6 系 cherry-pick） |
| P1+P2 evidence ledger | CLOSED（fold into P12，median 4.0） |
| P7 / P8 | research_grade_acceptable（方法学层，非论文） |
| Direction A anchoring | FOLDED（review + 机制实验双证伪） |
| G3 / D1 dual-ledger | PARK（Findings 诚实版，未执行） |
| D2 / D4 | KILLED（2026-07-18 终裁） |
| D3 | 并入 D1 appendix |
| C1 AI-auto-research 实证 | GO 附 gate → **DORMANT**（用户不投资源，未启动） |

## 4. 重启条件（C1 的 4 条硬 gate）

若未来重启，从 verdict memo §5 启动：G1 trace 数据集发布化；G2 taxonomy 盲应用于 ≥5 个公开失败记录（覆盖率 ≥70%）；G3 预注册 + 评分者 κ≥0.6；G4 红线句复审。任一不过则降级 Findings/workshop，不硬冲。

## 5. 保留说明

不删除、不移动任何文件；`legacy/` 与各子项目 `.git` 历史保持原样；本文件与 `state/progress.json` 为项目终态的权威记录。
