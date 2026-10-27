# Token 正式消费交接计划（候选 v1 与批准路径）

日期：2026-10-27；执行者：OpenCode glm-5.3。

## Goal

为全项目 token 统计的正式消费提供授权链完整的交接：精确 inventory（verifier 命令、代码闭包、schema/版本、原证据 hash 与批准状态）、policy 机器对象、阻断稳定接口、只读 verifier 与测试；现有证据不足则产出待批请求，不自签。

## Background

- token 并行线 W1 WAITING_HANDOFF（`analysis/tsinghua-clean-release-20261027/token-work/HANDOFF.md:1`）。
- T2 恒 NO-GO 不得改/绕过；1023 统计脚本 hash 冲突 BLOCKED；用户既有授权不可外推（见 `docs/investigations/token-consumption-handoff-2026-10-27.md:1`）。

## Approach

只读调查四个冻结 token 包 + clean-release 交接元数据 → 直接计算 hash/冲突 → 新建独立候选包 `analysis/token-consumption-handoff-20261027-v1/`（目标先查不存在）→ 只读 verifier + 测试 → seal → 调查/计划文档。

## Work Items

- [x] 精确 inventory：5 组代码闭包 SHA256、verifier 命令候选、输入/schema producer-consumer 版本链、26 条证据登记（hash+批准状态）。
- [x] policy：退出码按组件（1023 mixed_zero_nonzero / 1025 unknown_null / verifier 0 保留未实现、2 等待、3 结构违规、4 unknown）；正式采用与资源量分离接受；停写/无补跑三类证据分层（as-of 操作者说明 vs 永久证明 NOT_ESTABLISHED）。
- [x] 阻断核查：B1 冲突活体复检入 verifier；旧绑定不得替新 gate 映射；B4 T2 文本标记检查。
- [x] 只读 verifier + JSON schema：篡改→3、缺批准→2、合成记录阻断（B5）、pre-seal 标记、testing-root/symlink/越界拒绝；14/14 测试。
- [x] approval-request A1–A8（PENDING，无签名）；已批旧项与待批分开列举。
- [x] HANDOFF/CHANGELOG/manifest/docs。

## 硬性 No-Go 闸门

- 不自签、不构造 approval-record、不修改旧 approval/T2/旧包/clean-release/封存仓。
- v1 无 acceptance 路径：exit 0 不可达；任何"通过"宣称均为违规。
- 生产通过 = owner 批准记录（绑定 request hash、A1–A8、身份+日期）+ 新 v2 包实现可审计 gate；缺一即 NO-GO。

## Open Questions

- owner 是否按 A1 指定既有四包 verify 命令为批准 verifier，还是另建新入口。
- A8 的 1023 superseding 落地时点（独立于本包批准）。

## References

- `analysis/token-consumption-handoff-20261027-v1/HANDOFF.md:1`、`handoff.json:1`、`policy/consumption-policy-v1.json:1`、`approval/approval-request-v1.json:1`、`blockers/blockers-v1.json:1`。
- `analysis/tsinghua-clean-release-20261027/1023-work/OWNER-SUPERSEDING-REQUEST.md:1`；`docs/investigations/token-consumption-handoff-2026-10-27.md:1`。
