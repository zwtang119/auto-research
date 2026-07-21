# Changelog

本文件记录 CDS-NLUI 项目的所有版本变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/)。

## [0.4.0] - 2026-06-13

### Changed

- CDS 路径分析情景描述（trigger）从英文翻译为中文（如 "Win all remaining matches → guaranteed top 2" → "赢下全部剩余比赛 → 确保前二出线"）
- Bracket 依赖轮次名从英文缩写改为中文（R16→16强、QF→八强、SF→半决赛、Final→决赛）
- 交叉验证 Trae AI 报告：ISSUE-001（AI 模块空白）为误报，ISSUE-002（英文）已修复

### Added

- 48 队夺冠路径推演卡全部升级为 `deep-description`（27 张薄切片占位 → 完整 11 节分析）
- Plan C MVP1 预注册：3 场未踢比赛 prediction_card + factor_ledger（B2 卡塔尔vs瑞士、C1 巴西vs摩洛哥、F1 荷兰vs日本）
- Plan C MVP1 复盘闭环：A1 墨西哥 2-0 南非完整 settlement（Brier 0.3078, 2/3 因子有明确结果）
- Settlement 产物：settlement_record、knowledge_update_log、protocol_failure_log
- Schema 合规审计报告 `docs/investigations/plan-c-schema-compliance-2026-06-13.md`

### Fixed

- 修正全部 48 张 path card 的分组引用（原有多张卡引用错误小组对手）
- 修正 mex-rsa factor ledger 的 4 处 schema enum 违规（settled_* → complete, inconclusive_data_gap → inconclusive）
- 修正 argentina.md "德尚"复制粘贴错误 → "斯卡洛尼"
- 修正 portugal.md "F 组"残留 → 删除

## [0.3.0] - 2026-06-12

### Added

- 赛程解析器 `scripts/parse_schedule.py` — 从 Wikipedia 数据解析 72 场小组赛 + 淘汰赛
- 全景赛程页面 `site/panorama.html` — 12 组 × 3 轮赛程矩阵 + 概率热力
- 比赛详情页 `site/match.html` — 单场深度分析 + 概率条
- 球队详情增强 — 小组赛程 + 夺冠概率对比
- Elo + Poisson 数值预测基线 `scripts/numeric_odds.py`
- GitHub Actions 每日市场快照自动化 `market-snapshot.yml`
- CDS 路径模拟引擎 `scripts/cds_path_simulation.py`（qualification + championship 两层）
- Poisson 模型工具 `src/utils/poisson.py`
- 3 个 baseline 数据填充（FIFA ranking proxy, Elo proxy, market public）
- 深度视觉检查报告 + GitHub Pages 部署问题调查报告

### Fixed

- P0: panorama.js `formatDate()` 未定义 — 移入 common.js 共享
- P1: baselines 数据含禁止词汇 — 清洗 description 字段
- P0-1: Elo 显示错误修复
- P0-2: 夺冠概率归一化修复
- P0+P1: 代码质量修复（来自 investigation）

### Changed

- CDS 辩论系统（WI-3.5）被路径模拟引擎替代
- 导航整合：主页 → 全景图 → 球队 → 比赛完整导航链
- CSS/JS 共享函数提取到 common.js

## [0.2.0] - 2026-06-11

### Changed

- 项目更名为 CDS4WorldCup，明确定位为路径空间与可校准知识实验
- 新增 `src/`、`data/`、`results/`、`site/` 开发与发布目录结构
- 新增 GitHub Actions CI（PR 门禁：知识库审计、敏感文件检查、Markdown lint、结构完整性）
- 新增 GitHub Actions Pages 自动发布（推送到 main 即发布到 GitHub Pages）
- 新增 `.markdownlint.json` Markdown 规范配置
- 新增 `.github/PULL_REQUEST_TEMPLATE.md` PR 模板
- 新增 `docs/source-policy.md` 来源分级规则
- 完善 `.gitignore`：排除敏感文件、IDE 配置、Python 缓存等
- 更新 `README.md`、`CLAUDE.md`、`AGENTS.md` 为 CDS4WorldCup 定位

## [0.1.0] - 2026-06-07

### Added

- 项目初始化：基于 Marginalia v0.3.1 搭建知识管理框架
- `CLAUDE.md` — AI 助手发现层入口
- `README.md` — 项目概述
- `schema/` — Marginalia 协议规则（rules.md、node-types.md、first-ingest.md）
- `scripts/` — 知识库工具脚本（init.py、audit.py、verify.py）
- `templates/` — 页面模板（concept、decision、annotation）
- `example/` — 示例知识库
- `wiki/` — 初始知识库，摄入 CDS 项目核心文档
  - 概念页面：CDS、NLUI、决策控制面
  - 决策记录：CDS 业务重构设计、NLUI Decision Workspace MVP
  - 批注：CDS 一页纸核心叙事沉淀
