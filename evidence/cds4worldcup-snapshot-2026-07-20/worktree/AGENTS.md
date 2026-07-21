# AGENTS.md — Agent 工作指引

## 你是谁

你正在为 CDS4WorldCup 项目工作。这是一个路径空间与可校准知识实验项目，使用计算决策空间（CDS）方法论对 2026 FIFA 世界杯进行结构化路径分析。

## 优先阅读

1. `CLAUDE.md` — 项目结构与工作流
2. `wiki/index.md` — 知识库全貌
3. `docs/source-policy.md` — 来源分级规则（**必须遵守**）
4. 当前正在执行的 `specs/` 文件

## 核心规则

### 知识库操作
- **读**：每次对话开始读 `wiki/index.md`，沿 `[[wikilink]]` 读取相关页面
- **写**：新概念 → `wiki/concepts/`，技术决策 → `wiki/decisions/`，历史记录 → 页内批注
- **批注格式**：`> [!memo] YYYY-MM-DD 内容`
- **完成后**：更新 `wiki/index.md`，运行 `python3 scripts/audit.py --root wiki/`

### Spec 执行
- `specs/` 下的文件是设计规格，**只读参考**，不要修改
- 按 spec 中的任务顺序逐步执行
- 每个任务完成后在 wiki 记录进展
- 如遇到 spec 与现实不符的情况，在 wiki 的对应决策页面记录偏差和原因

### 开发代码
- 所有代码放在 `src/` 下对应子目录
- 分析脚本 → `src/analysis/`
- 数据处理 → `src/data/`
- 结果发布 → `src/publish/`
- 工具函数 → `src/utils/`
- 结果输出到 `results/`，使用 Markdown 格式

### 来源纪律（必须遵守）
- 严格遵守 `docs/source-policy.md` 的来源分级规则
- **Green Source** 才能作为事实输入进入因子账本
- **Red Source** 只能作为 baseline 或叙事材料
- 不输出投注建议，不报告收益率

### 技术约束
- Marginalia 工具脚本（`scripts/`）使用零依赖 Python 3.10+
- 知识库是纯 Markdown，不引入数据库或在线服务
- 不修改 `schema/`、`templates/`、`example/` 目录——这些是 Marginalia 协议定义
- `docs/references/` 是敏感文档目录，绝不上库

### 文件边界
- 你可以自由操作 `wiki/`、`src/`、`results/`、`data/` 目录
- `specs/` 只读
- `docs/` 可以追加，不要删除已有内容
- 根目录配置文件（CLAUDE.md 等）不要随意修改
- `docs/references/` 中的文件永远不要提交到 git

## 当不确定时

1. 先查 `wiki/` 看是否已有相关记录
2. 如果 wiki 没覆盖到，在 `wiki/concepts/` 创建新页面
3. 对于技术选型问题，在 `wiki/decisions/` 记录决策过程
4. 涉及来源可信度问题时，查阅 `docs/source-policy.md`


<claude-mem-context>
# Memory Context

# [cds4worldcup] recent context, 2026-06-12 11:42am GMT+8

Legend: 🎯session 🔴bugfix 🟣feature 🔄refactor ✅change 🔵discovery ⚖️decision 🚨security_alert 🔐security_note
Format: ID TIME TYPE TITLE
Fetch details: get_observations([IDs]) | Search: mem-search skill

Stats: 50 obs (15,253t read) | 3,308t work | -361% savings

### Jun 11, 2026
3544 11:27p ✅ Build script modified to remove AI/Kimi references from public site data
3545 11:28p 🔵 Site HTML and JavaScript still contain extensive AI/Kimi references requiring removal
3546 11:29p 🔵 Project documentation review reveals strict source policy and verification requirements
### Jun 12, 2026
3547 12:50a 🔵 Project context exploration for MiMo integration brainstorming
3548 12:51a 🔵 CDS4WorldCup project architecture and source policy constraints identified
3549 " 🔵 Data pipeline architecture reveals strict public/private boundary enforcement
3550 12:52a 🔵 Homepage optimization spec reveals detailed design principles and constraints
3551 12:57a ⚖️ Experimental calibration prioritized over content updates
3552 " 🔵 MiMo Code architecture and design principles documented
3553 " 🔵 MiMo Code GitHub repository not found at expected path
3554 12:58a ⚖️ Operational model comparison completed, design ready for approval
S585 MiMo Code long-horizon campaign design shift from daily runbook to continuous season task (Jun 12 at 12:59 AM)
S586 MiMo Code positioned as season research factory replacing repetitive cognitive labor rather than prediction automation (Jun 12 at 1:01 AM)
S587 Season Campaign Daemon design with 7×24 supervisor dispatching bounded MiMo tasks (Jun 12 at 1:02 AM)
S588 OpenClaw capability verification before framework selection (Jun 12 at 1:05 AM)
S589 24-hour long-horizon research sprint model for MiMo Code integration (Jun 12 at 1:07 AM)
S590 Stable control document architecture for 24-hour MiMo research sprints (Jun 12 at 1:10 AM)
3555 1:13a ⚖️ Planning phase completed with 24-hour research sprint model selected
S591 MiMo Season Campaign Operations Infrastructure Setup (Jun 12 at 1:13 AM)
3556 " 🔵 Doc-coauthoring skill available for structured document creation workflow
3557 1:14a 🔵 Project structure analysis for MiMo campaign documentation placement
3558 " 🔵 Existing long-horizon agent usage guide defines operational boundaries and constraints
3559 " 🔵 Project documentation structure established with design specs and plans
3560 " 🔵 Existing audit infrastructure and minimal results directory structure discovered
3561 " ✅ MiMo operational directory structure created for 24-hour research sprints
3562 1:16a 🟣 MiMo season campaign infrastructure implemented with comprehensive control documentation
3563 " 🟣 MiMo season campaign infrastructure fully implemented with comprehensive control system
3564 " ⚖️ MiMo Code integration strategy for World Cup season updates
3565 1:17a ✅ Documentation structure updated for MiMo season campaign ops
3566 " ✅ Path space spec document cross-referenced with MiMo ops
3568 " 🔵 Audit tool link detection lag despite documentation updates
3569 " ✅ Link format standardized for mimo-season-campaign-ops reference
3570 " ✅ Link format standardization applied successfully
3571 " 🔴 Orphan page detection issue resolved through link format standardization
3572 " 🔴 Documentation cross-linking fixes verified and confirmed
3573 1:18a 🔵 Verification-before-completion skill defines evidence-first workflow principle
3578 " 🔴 Whitespace issues detected in new ops documentation files
3579 1:19a 🔴 Trailing whitespace removed from ops documentation files
3580 " 🔴 Whitespace cleanup successfully applied to ops documentation
3581 " 🔴 Whitespace validation passed after cleanup
S592 Audit and recover missing kimi data for 27 teams (Jun 12 at 1:19 AM)
3583 1:32a 🔵 27 of 48 teams missing kimi probability data
3584 " 🔵 kimi_baseline_signals_matrix.csv schema structure documented
S593 Verify actual MiMo campaign execution time using file timestamps instead of trusting session claims (Jun 12 at 1:32 AM)
3585 7:36a 🟣 World Cup 2026 qualification tracker with 27 new teams
3586 " 🔵 World Cup 2026 campaign execution time verified
3587 7:37a 🔵 Campaign execution time was 13 minutes, not 4.5 hours as claimed
3588 " 🔵 File listing confirms 13-minute campaign execution, not 4.5 hours
3589 11:05a 🔵 Research requirements established for three-part codebase analysis
3590 11:06a ⚖️ Parallel agent dispatch pattern selected for three-part analysis
3591 " 🔵 Primary session prepared for three-part analysis with skill loading and context gathering
3592 " 🔵 Refactoring spec implementation details revealed with 17-file change plan across 4 batches
3593 11:08a 🔵 Primary session executed parallel agent dispatch for three-part analysis workflow
3594 " 🔵 P0 CSS media query bug confirmed in portal.css lines 1351-1379
3595 " 🔵 CDS4WorldCup multi-layered code inspection underway
3596 11:09a 🔵 Multi-track codebase analysis and institute-one research for potential MiMo integration
3598 11:10a 🔵 Empty observation session - no work detected
3597 " 🔵 MiMo Code long-horizon architecture analyzed for World Cup research integration patterns
3599 11:11a 🔵 Institute-one vault writer and workflow engine architecture analyzed for World Cup research patterns
S595 Research institute-one integration with CDS4WorldCup for MiMo World Cup research compatibility (Jun 12 at 11:11 AM)
**Investigated**: No exploration was conducted in the observed session. The user requested analysis of institute-one and CDS4WorldCup integration potential, but no files were read, no code was examined, and no tool executions were performed.

**Learned**: Nothing was learned because the observed session contained only the user's initial research prompt without any execution trace or work products.

**Completed**: No work was completed. The session captured only the request stage without progressing to file reading, analysis, or synthesis.

**Next Steps**: Cannot determine next steps as the observed session did not progress beyond the initial request stage. The intended next steps would have been: (1) reading institute-one source code to verify architecture, (2) analyzing CDS4WorldCup constraints, (3) evaluating MiMo integration patterns, and (4) producing Chinese synthesis of integration feasibility.
</claude-mem-context>