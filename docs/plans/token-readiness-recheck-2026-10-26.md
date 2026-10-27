# Token 复核与最终接入准备

日期：2026-10-26。

## Goal / Background
复核暂行版 token 口径与1023/1025最终接入条件；接近完成不等于完成。旧报告与计算脚本位于 `analysis/token-imputation-audit-20261026/` 及 `docs/investigations/token-report-2026-10-26.md`。

## Approach / Work Items
- [x] Item 1（pair，大，无依赖）：独立复算旧账、字段语义与调用身份，检查实验完成凭据。交付 `analysis/token-readiness-audit-20261026/` 的可复算审计、证伪清单与CHANGELOG；只读源实验。
- [x] Item 2（fresh pair，大，依赖Item 1复核）：修正已确认的不当语义与追加契约，准备离线接入工具/回归测试和完成闸门。旧暂行数值不静默覆盖；新版本与旧快照明确替代，不双计。交付新版准备材料与测试结果。
- [x] 编排者直接复核关键代理断言与测试，记录确认/证伪/未确认，给用户总结。

## Hard go/no-go
运行中实验、历史源仓只读，不启动/停止/重启、不发API/探针；封存仓库零读写，证据快照不改。无完成凭据、无停写确认或有补跑时不得发布最终总量。缺失usage不填0，reasoning不盲加completion。按realpath只消除别名，真实retry不得因fingerprint相同删除。已有1023/1025快照与最终数据不得简单ADD-only叠加。

## Open Questions
completion/reasoning跨provider语义是否有独立证据；物理调用与记录数覆盖；失败/重试是否被源系统保存；实验是否达到可接受终态。

## References
- `analysis/token-imputation-audit-20261026/append-1023-1025-checklist.md`
- `docs/plans/token-report-2026-10-26.md`

## 工作区保护
开始时发现非本次工作：`legacy/p11-closed-v5-minimax-m3`、`papers/p12-judge-calibration/wiki/index.md`、`papers/p1p2-evidence-ledger/wiki/index.md` 有改动；不触碰。

## Item2 交付（2026-10-26）
独立新包 `analysis/token-final-readiness-20261026/`；更正入口 `docs/investigations/token-readiness-recheck-2026-10-26.md`。19项离线回归通过；replacement-view、语义安全投影、双遍集合/内容与symlink边界验证已实现。仅有限准备范围完成；生产完成凭据可信审批及scope/adoption验证未实现，发布仍NO-GO，不宣称实验终态。Item1与编排者复核状态不由本执行者代勾。

## 编排者最终直接复核（2026-10-26）
- 独立读取旧CSV确认7765保留/4498替代；独立zipfile遍历确认三模型SASR各105条及completion和。
- `audit.py audit`：AUDIT PASS；completion NO-GO。
- `python3 -m unittest discover -s analysis/token-final-readiness-20261026 -p 'test_*.py' -v`：19/19通过。
- `readiness.py verify-release`：RELEASE HASH PASS；final NO-GO。
- `readiness.py dry-run`：DRY-RUN PASS，historical7765/superseded4498/observed replacement5346/preview13111；native_values_unchanged=true。这是非原子审计观察的预览，不是最终实验量。
- 生产完成凭据可信审批、整体终态接受、scope/adoption完整验证仍未实现；本轮不声称端到端接入就绪。
