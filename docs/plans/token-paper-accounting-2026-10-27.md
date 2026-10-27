# Token 论文三层核算实施与验收计划

日期：2026-10-27；执行者：OpenCode gpt-6.1-sol。

## Goal
新建 `analysis/token-paper-accounting-20261027/` 与 `docs/investigations/token-report-paper-accounting-2026-10-27.md`：论文主表切换到1023正式采用3,360条与1025侧车关联1,860条；资源账附录；历史可信估算另列Red Source。只在新包/新文档写入，不改旧包。

## Background
用户恢复及steering明确批准三层核算。Green Source：`analysis/token-1025-append-20261027/active-ledger.csv:1`、`release-manifest.json:1`；编排者CSV直接确认见 `docs/investigations/token-adoption-handoff-confirmation-2026-10-27.md:1`。恢复时完整旧交付已存在，新三层目标不存在；交接补充不是本工作项的完成替代品。

## Approach
离线固定既有封装的账本、采用绑定、报告、历史估算与适用性说明；复制前后检查集合与SHA-256，不访问活动源、封存仓或证据快照，不运行旧包脚本、不调API、不启停实验、不重复派生会话、不commit/push。

1. 资源CSV逐字节保留，原字段与行序不变；新mapping用资源行号与复合物理身份（experiment/run/call_id/attempt/archive/hash）映射，不能单用call_id/fingerprint去重。
2. 主采用集只收1023 `adoption=adopted` 与1025两类sidecar采用；历史五月 `scope=balanced` 的generation/track_a/track_b独立冻结为历史匹配视图，不声称历史论文全部采用或重试完整性；benchmark不并主表。
3. 既有ORCH-MEAN与KIMI-RATIO值/状态/区间保留，item1-v1标Red；S3只作历史情景，S4/旧目标/PROVIDER-DIFFERENCE不启用。失败请求、reasoning、未知字段均无新估算。
4. 独立verify不导入生成器，重建选择/映射、逐字段保留、分组与coverage、估算分离、报告一致性；负向测试与跨hash-seed双遍确定性；显式seal后只读verify。

## Work Items
- [x] 固定输入及来源锁，三层账与逐条mapping。
- [x] 主报告、历史匹配范围/未知项/资源及估算附录。
- [x] 独立verify、回归、双遍确定性。
- [x] REVIEW/README/CHANGELOG、release封装及只读验收。

## 硬 go/no-go
来源hash或集合变动、旧包变化、资源原字段/字节改变、身份冲突、采用绑定不匹配、5220及四字段不符、历史范围冒充全部采用、未知填0/新增失败或reasoning估算、估算混入native总量、独立验证/测试/确定性失败，均NO-GO。通过仅允许三层论文核算交付，不等于全项目最终消耗。

## Open Questions
五月没有本次新增逐条采用凭据，历史balanced只是冻结匹配范围；原parser语义未重跑。全项目统一发送/计费分母、整体退出/永久停写、未知usage/二月IDE成本未建立，不填补也不升级为完整总量。1025侧车补测/格式修复不改称原协议完整结果。

## References
`docs/investigations/token-report-complete-2026-10-27.md:1`；`analysis/token-imputation-audit-20261026/estimators.yaml:1`；本次用户恢复/steering消息。

## 完成与验收记录

Green Source：`analysis/token-paper-accounting-20261027/verification.json:1`、`check-run.json:1`、`REVIEW.md:1`。三层核算限定范围GO；全项目最终消耗NO-GO。

主采用5220，prompt8,578,168 / completion23,683,749 / native total32,261,917 / reasoning20,505,678，均measured全覆盖；与编排者直接确认完全一致。历史五月匹配2310记录/11,761,840另列，不冒称全部历史采用；resource13237行原CSV字节相同；Red Source/item1-v1估算850记录1270字段逐值保留，native资源已知47,293,807不混入估算。

独立verify PASS，52/52回归通过，hash seed1/937双遍13文件确定性PASS。新release显式seal，检查通过后仅release verify只读核验；旧包/实验/旧报告不改，无API/进程启停/派生会话/commit/push。交付完整新包与 `docs/investigations/token-report-paper-accounting-2026-10-27.md:1`，不是只有handoff。
