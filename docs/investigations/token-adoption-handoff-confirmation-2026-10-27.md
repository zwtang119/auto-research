# 1023 / 1025 采用集：恢复核查与编排者确认

日期：2026-10-27；记录者：OpenCode gpt-6.1-sol。

## 结果与确认来源

**Green Source：编排者直接 CSV 筛选复核（用户本次恢复消息转达），并由本会话对既有封装的 active ledger 再次直接计算确认。** 两个来源的条数及四项原生 token 小计全部一致。编排者确认不冒充本会话执行记录，不视为外部审计签字。

| 采用视图 | 记录 | prompt | native completion | native total | native reasoning |
|---|---:|---:|---:|---:|---:|
| 1023 正式采用 | 3,360 | 5,320,782 | 14,851,291 | 20,172,073 | 12,847,207 |
| 1025 侧车有效采用关联 | 1,860 | 3,257,386 | 8,832,458 | 12,089,844 | 7,658,471 |
| 两实验上述采用视图合计 | 5,220 | 8,578,168 | 23,683,749 | 32,261,917 | 20,505,678 |

Green Source：`analysis/token-1025-append-20261027/active-ledger.csv:1`（表头；以下条件筛选全表），`docs/investigations/token-report-complete-2026-10-27.md:1`。此处是已有分析冻结包，不是 `evidence/` 证据快照。

筛选条件：

- 1023：`experiment == "1023" and adoption == "adopted"`。
- 1025：`experiment == "1025" and sidecar_adoption in {"sidecar-adopted", "sidecar-format-repaired-original-call"}`。
- 各组按 `prompt_tokens_value`、`completion_tokens_value`、`total_tokens_value`、`reasoning_tokens_value` 分别求和；所选记录四字段均非空，状态均为 `measured`。

**确认 / 证伪 / 漏检登记：** 本次交接的三组条数、十二项 token 小计均确认；未检出差异。此次仅复算采用视图，不构成对全项目范围、原 parser 有效性或 provider 执行/计费的完整审核。

## 已有目标与封装状态

恢复时先检查目标，发现完整报告、1025 replacement 分析包及计划验收记录已存在；未重复构建、重采集或派生会话。Green Source：`docs/plans/token-1025-append-2026-10-27.md:26`、`analysis/token-1025-append-20261027/README.md:1`。

本会话执行只读命令：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 analysis/token-1025-append-20261027/release.py verify
```

返回 `{"status": "PASS", "operation": "verify", "files": 52}`。本次读取时：

- `analysis/token-1025-append-20261027/release-manifest.json` SHA-256：`88cd5bd9e04c0f2edfd788e16d94a729ab228f2fda98bd43789c3aa737030b8f`。
- `analysis/token-1025-append-20261027/active-ledger.csv` SHA-256：`c3556cd8c32fb82ed2aa063a9cc62a805cfcfc000de9dfc0f0e122240b343bf4`。

已有 `analysis/token-1025-append-20261027/check-run.json:1` 记录此前 30/30 回归、独立 verify 与两遍确定性通过；本次只读查看，不冒称重新执行了这些测试，不运行会改写日志的 `run_checks.py`。

本文件是封装完成后的独立交接补充，**不在上述 52 文件封装内**；未修改或重封既有分析包、报告及计划。最初 RepoPrompt 读取超时后改用本地只读检查；未重试 ACP 配置或重复派生会话。

## 解释边界

- 32,261,917 是上述两个采用视图的原生 total 合计，不是全资源账或全项目最终消耗；采用视图嵌套于各自资源账，不能与资源账相加。
- 1025 的 1,860 条是侧车关联口径，不替代或叠加原主结果有效采用集 1,846 条；本地格式修复关联不代表新增一次 API 调用，也不把事后补测改称原协议预注册完整结果。
- native reasoning 单独展示，不额外加到 native total；没有据此新推断 reasoning 与 completion 的包含关系。
- 缺失 usage 不填零、不由后续成功倒填；二月 unknown/N/A、五月估算与全项目发送分母/整体退出/永久停写等原有限制不变。
- 本次未访问实验活动源或封存仓库，未发起实验 API 调用、启停实验进程、运行旧包脚本、commit 或 push；未触碰发现的既有 `legacy/`、`papers/` 等工作区改动。
