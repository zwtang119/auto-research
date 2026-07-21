# Long-Horizon Agent Usage Guide

> **类型**: internal-guide
> **状态**: draft
> **日期**: 2026-06-11
> **范围**: 指导项目维护者如何试用长程 agent 工具进行数据监控、资料采集和状态回写。
> **公开边界**: 本指南是内部操作文档，不是主页内容；不得在公开主页中宣传具体工具品牌、免费额度或暗示项目已经使用。

## 1. 当前定位

CDS4WorldCup 可以把长程 agent 工具作为内部辅助能力，用于比赛周期内的重复性任务：

- 定期检查公开数据源是否更新。
- 生成数据快照和抓取日志。
- 把候选事实写入 review queue。
- 更新 source ledger 草稿。
- 提醒人类复核需要进入 Factor Ledger 的候选项。

截至本指南创建时，该能力尚未正式投入 CDS4WorldCup 运行。因此：

- 不把它写成项目成果。
- 不在主页展示具体工具名。
- 不把 agent 输出直接当成 Green Source。
- 不让 agent 自动写入 Factor Ledger 正式条目。

## 2. 适合它做什么

适合：

- 长时间、重复性、低创造性的数据巡检。
- 多来源状态同步，例如赛程、伤病、阵容、市场 baseline 快照。
- 生成“待人工复核”的候选清单。
- 在任务较长时保持 checkpoint 和恢复状态。
- 为人类维护者整理“今天有什么变了”。

不适合：

- 自动判断一条新闻是否为 Green Source。
- 自动把 Red/Yellow Source 升级为事实输入。
- 自动给出投注、赔率价值、收益率或仓位建议。
- 自动改写 `docs/references/**` 或发布敏感材料。
- 直接生成未审计的公开结论。

## 3. 安装与启动

官方页面提供两种入口：

```bash
curl -fsSL https://mimo.xiaomi.com/install | bash
```

或：

```bash
npm install -g @mimo-ai/cli
```

注意：`npm view @mimo-ai/cli` 在 2026-06-11 显示 npm 包描述为 placeholder release。实际可用安装方式以官方页面和本机安装结果为准。

首次启动通常会引导选择模型接入方式。不要把 API key、登录凭据或个人 token 写入本仓库。

## 4. 推荐项目目录

如需在本项目试用，建议只让工具读写这些目录：

- 可读：`wiki/`, `docs/`, `data/processed/`, `site/data/`, `artifacts/reports/`
- 可写：`data/staging/`, `artifacts/reports/`, `wiki/annotations/`
- 禁止写：`schema/`, `templates/`, `example/`, `docs/references/`
- 禁止提交：任何 API key、token、cookies、本地登录状态、`docs/references/**`

建议新增但尚未创建的 staging 路径：

```text
data/staging/
  live-source-snapshots/
  review-queue/
  source-ledger-drafts/
```

## 5. 推荐任务模板

### 5.1 每日公开信号巡检

```text
Goal:
检查 CDS4WorldCup 允许使用的公开数据源是否有更新，生成待人工复核摘要。

Constraints:
- 遵守 docs/source-policy.md。
- 不输出投注建议、收益率、仓位或赔率价值判断。
- Kimi / market 只能作为 public baseline 或外部共识参照。
- 未核验信息写入 data/staging/review-queue/，不要写入 Factor Ledger。
- 不读取或复制 docs/references/**。

Output:
- data/staging/live-source-snapshots/YYYY-MM-DD-summary.md
- data/staging/review-queue/YYYY-MM-DD-candidates.md
- 简短列出 source、time window、candidate claim、source level、recommended human review action。
```

### 5.2 Polymarket Snapshot 辅助整理

```text
Goal:
读取已有 Polymarket API 快照或本地 market baseline 数据，整理公开共识摘要。

Constraints:
- 市场数据 source_level=Yellow。
- 只描述 market snapshot status、coverage、last_fetched_at、consensus gap。
- 禁止使用 buy/sell/bet/value/edge/profit/ROI/PnL/Sharpe/Kelly。
- 禁止给出任何投注建议。

Output:
- data/staging/live-source-snapshots/YYYY-MM-DD-market-summary.md
- 如数据缺失，写 missing_with_reason，不要编造数值。
```

### 5.3 Factor Candidate Review Queue

```text
Goal:
从已公开且允许读取的数据中整理候选 Factor Ledger 条目，供人类复核。

Constraints:
- 只生成候选，不写正式 Factor Ledger。
- 每个候选必须包含 observable_proxy、settlement_rule、time_window、source_url_or_path、source_level。
- source_level 不是 Green 时，标记为 needs_verification。
- Kimi reason 只能进入 Marginalia 或 candidate seed，不得直接进入 Factor Ledger。

Output:
- data/staging/review-queue/YYYY-MM-DD-factor-candidates.md
```

## 6. 人工复核流程

所有 agent 产物进入公开页面前必须经过人工复核：

1. 检查 source level 是否符合 `docs/source-policy.md`。
2. 检查是否包含禁止内容：投注建议、ROI、PnL、Sharpe、仓位、赔率价值判断。
3. 检查事实字段是否有公开可复核来源和时间窗口。
4. 检查 candidate 是否具备 observable proxy 与 settlement rule。
5. 合格后才允许进入 `data/processed/`、正式 artifacts report 或 wiki memo。

## 7. 主页展示边界

主页可以展示：

- 数据快照更新时间。
- review queue 待复核数量。
- source watcher 状态。
- baseline refresh 状态。
- settlement queue 状态。

主页不展示：

- 具体长程 agent 工具品牌。
- 免费 token / 供应商活动。
- benchmark 宣称。
- “我们使用了某某工具”的营销句。
- 未经复核的 agent 结论。

## 8. 推荐试运行步骤

1. 在本地新建 staging 目录：

```bash
mkdir -p data/staging/live-source-snapshots data/staging/review-queue data/staging/source-ledger-drafts
```

2. 先用只读任务试运行，不允许写正式目录。

3. 让工具生成一天的 review queue 草稿。

4. 人工复核草稿，记录哪些字段有用、哪些容易误判。

5. 如果连续 3 次巡检都能稳定产出可复核材料，再考虑写技术决策页，决定是否纳入项目常规流程。

## 9. Stop Conditions

出现以下情况应停止自动化运行并回到人工模式：

- 工具无法稳定遵守 source policy。
- 工具把 Red/Yellow Source 写成事实输入。
- 工具输出投注建议或赔率价值判断。
- 工具读取或复制 `docs/references/**`。
- 工具在无数据时编造数值。
- 工具修改 `schema/`、`templates/` 或 `example/`。

## 10. 后续决策

若试运行有效，应另建技术决策页记录：

- 是否纳入常规数据监控流程。
- 允许读写的目录边界。
- 输出文件 schema。
- 人工 review SLA。
- 失败回滚和审计方式。

在该决策完成前，长程 agent 工具只作为内部可选能力，不作为 CDS4WorldCup 公开能力展示。

> [!memo] 2026-06-11 初稿
>
> 根据用户反馈创建：主页不展示具体工具品牌；本指南仅用于内部试用和操作边界说明。
