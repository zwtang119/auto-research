# Token 正式消费交接调查：批准链缺项与候选包 v1

日期：2026-10-27；执行者：OpenCode glm-5.3。Green Source：全部关键事实由本会话直接计算复核（shasum/JSON 解析），未派生子代理、未调用外部模型/网络、未重跑实验/API、未 commit/push。

## 结论

**不存在可交付的"批准版"生产消费交接；已产出候选包 `analysis/token-consumption-handoff-20261027-v1/`（WAITING_APPROVAL，verifier exit 2，ready=false）与待批请求 A1–A8。** 生产门禁未过，本文件不宣称任何 gate 已通过。

## 直接复核的关键事实（Green Source）

- **T2 恒 NO-GO**：`analysis/token-final-readiness-20261026/readiness.py` gate() 无条件返回 NO-GO（含 'production evidence approval and scope/adoption validation not implemented'）；脚本 SHA-256 `9dde512d…`（15699B），本任务零修改零绕过。
- **1023 统计脚本 hash 冲突（B1）**：实际 `parent-statistics-verification-01/verify.py` = `bfc058dc…`/5462B；`statistics/STATISTICS_COMPLETE.json`（parent_independent_script）与 `statistics/final-closeout-001/manifest.json`（artifacts）两处绑定 `184369b8…`/5326B；`DELIVERY.json:51-53` 绑定新脚本。旧绑定不能替代新通过 gate 映射；解法仅原 owner 按 `1023-work/OWNER-SUPERSEDING-REQUEST.md:1` 五项最小承接（append-only 新版本）。
- **代码闭包**（closure_sha256 = 组内 {relpath: sha256} 规范 JSON 的 SHA-256）：1023-append `40dc4f48…`、1025-append `5e5771ce…`、final-readiness `37a03858…`、paper-accounting `90cac4e0…`、token-work `21ce1b3a…`（逐文件 hash 见包内 inventory）。
- **1025 adoption 映射**：`report-work/inputs-v2/public/provenance/adoption.jsonl` 与 `builds/1025-v1/…` 双处 hash 相同 `12f63a14…`，1080 行；join 等 W5-a，不单独代表 1860 资源采用。
- **既有授权边界**：三层核算批准（`docs/plans/token-paper-accounting-2026-10-27.md:9`）仅覆盖该包执行交付；1023/1025 attestation 有限；1025 独立交付批准不外推至 token 生产 gate；三线并行仅为启动授权。以上均不构成对 A1–A8（verifier 指定/代码闭包/退出码例外/全项目 scope）的签字。
- **退出码证据**：1023 = mixed（MAMR closeout host exit=2 记录在案，非零不代签为零；多处 returncode=0；pilot terminal unknown）；1025 = overall_exit_code=null（unknown≠0）。
- **停写/无补跑**：无任何包主张整树停写或永久无补跑（1023 completion-evidence 明示 monitors still write；1025 attestation 明示 claims_not_made）。用户"1没有了"仅登记为截至 2026-10-27 的操作者说明（非签名、非全历史证明），与 permanent_full_history_proof=NOT_ESTABLISHED 分层。

## 交付物（全部新增，未改任何旧文件）

- 包：`analysis/token-consumption-handoff-20261027-v1/`（HANDOFF、handoff.json、schema、verifier+inventory、policy、approval-request、blockers B1–B5、CHANGELOG、release-manifest、14 项测试）。
- 本调查 + 计划 `docs/plans/token-consumption-handoff-2026-10-27.md:1`。

## 安全边界（编排复查修正后）

v1 删除生产解锁路径：任何批准记录（含合成完整记录）不能达 exit 0/ready=true（B5）；缺 seal 报 pre-seal-not-consumable；TCH_REPO_ROOT 测试钩子标 testing-root 且拒绝 symlink/越界；测试 PASS/seal PASS 均非生产授权。真正通过需 owner 批准记录 + 新 v2 包（可审计 acceptance gate），本候选保留不覆盖。

## 离线验证命令

```sh
PYTHONDONTWRITEBYTECODE=1 python3 analysis/token-consumption-handoff-20261027-v1/verifier/verify_handoff.py verify   # 预期 exit 2
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s analysis/token-consumption-handoff-20261027-v1/test -p 'test_*.py' -v  # 14/14
```

## 遗留缺项（诚实清单）

A1–A8 全部 PENDING：批准版 verifier 入口未指定、代码闭包未批、schema 绑定未批、批准人身份未定、全项目 completion/scope/adoption 未批、退出码接受策略未签、停写/无补跑范围未签、1023 superseding 未执行。机器 ready=false 逐实验 reason codes 见 `handoff.json:1`。
