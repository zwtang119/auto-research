# 进度记录：2026-10-22 → 10-27（清华 policysim 线：1023 DNA 消融 / 1025 八臂析因 / token 三层核算 / 清洁交付）

> 范围：清华实验线一个工作周（10-22 基线审计 → 10-27 三包落位）｜ 执行：OpenCode 多会话并行（1023／1025／token 三条流水线）｜ 关联：`docs/plans/tsinghua-clean-release-2026-10-27.md`、目标仓 `policysim-research-Tsinghua`｜ 数字口径：Green 为本日从冻结数据直接复算，Red Source 为冻结模型输出

## 0. 一句话总结

**三个自包含清洁包已实际落位目标仓 `policysim-research-Tsinghua`**：1025（360 样本）、1023（630 样本）与 token 三层核算（2–10 月三次实验）；论文主表 5,220 条采用调用、原生 Total 32,261,917 经冻结账本复算一致。剩余缺口如实标注（1023 两阶段 adapter 精确字节与再分发授权、token v2 批准、视觉未目视），不阻断现有数据使用。

## 1. 时间线（2026-10-22 → 10-27）

| 日期 | 事项 | 产物（analysis/ 或 docs/） | 状态 |
|---|---|---|---|
| 10-22 | 清华基线审计 | `analysis/tsinghua-baseline-audit-20261022/` | 完成 |
| 10-23 | **1023 DNA 消融实验**（SASR/MAMR 双轨）＋协议等价核对 | `D-dna-ablation-20261023/`、`docs/investigations/tsinghua-dna-protocol-equivalence-2026-10-23.md` | 实验完成 |
| 10-25 | **1025 八臂析因实验**＋GLM 并发基准 | `analysis/tsinghua-factorial-ablation-20261025/`、`analysis/glm-concurrency-benchmark-20261025/` | 实验完成 |
| 10-26 | token 报告／插补审计／就绪审计；报告适配与统计准备 | `analysis/token-*-20261026/`、`report-adapter-prep`、`statistics-prep` | 完成 |
| 10-27 | MiniMax YAML 恢复、历史验收、补测与统计收口 | `minimax-yaml-recovery-20261027/`、`historical-acceptance-20261027/`、`statistics/verification-002/` | 完成 |
| 10-27 | token 论文三层核算（paper-accounting-v1） | `analysis/token-paper-accounting-20261027/` | 完成（52/52 测试） |
| 10-27 | 清洁交付计划定稿＋**三包落位目标仓** | `docs/plans/tsinghua-clean-release-2026-10-27.md` | 交付（见 §2） |

## 2. 清洁交付（目标仓 `policysim-research-Tsinghua`）

| 包 | 路径 | 内容 | 落位核验 |
|---|---|---|---|
| 1025 析因 | `experiments/mc-2026-10-25/` | 360 样本 JSON/HTML/PDF（1,080 份）、三视图统计、中文主报告、runtime 与离线复算 | 5,365 文件／770MB；状态 FIRST_DELIVERY，终验 INCOMPLETE 已标注 |
| 1023 消融 | `experiments/mc-2026-10-23/` | 630 样本 JSON/HTML/PDF（1,890 份）、两视图统计、中文汇总、1,890 键采用溯源、核验/复算脚本 | 10,127 文件，MANIFEST `36da6b41…bfe80` 落位复核 exit 0（本日直接执行） |
| token 核算 | `docs/token-accounting-feb-oct-2026/` | 论文主表、13,237 行资源账、Red Source 估算附录、五月历史匹配、映射与复算源码 | `DELIVERY-MANIFEST.sha256` 36 文件自检通过 |

用户四项裁定已落实：adopted-v1 唯一默认主集（附一页差异简表）；金额屏蔽仅删账户/API 运行费用、保留研究数值；全部样本三格式交付；token 包独立落位、不改共享索引。**10-27 用户裁定首版交付优先**：已验收产物独立交付，缺项标注不阻断使用，不以追加审计代替交付。

## 3. token 三层核算口径（论文用量章节依据，Green 复算）

| 层 | 规模 | 数值 | 用途 |
|---|---|---|---|
| 论文主表（最终采用调用） | 5,220 条（1023 3,360＋1025 侧车 1,860） | prompt 8,578,168／completion 23,683,749／total 32,261,917／reasoning 20,505,678 | 论文主表数字 |
| 资源账附录（全部物理记录） | 13,237 条 | 已知原生 Total 小计 47,293,807 | 覆盖与缺失披露；**含主表，不可相加** |
| 历史估算附录（Red Source，item1-v1） | 850 条原记录／1,270 字段项 | 五月编排与 Kimi 可见输出估算 | 仅估算，不混入实测 |

五月历史匹配视图另列：2,310 条计量记录、原生 Total 11,761,840（共享 usage 只计一次），不代表全部历史采用。口径纪律：reasoning 单列不叠加 Total；unknown／N-A 不补零、不倒填；1025 含 13 条成功补测＋1 本地格式修复（不增调用数）。

## 4. 本次沉淀的关键裁决（详见知识库 `framework/knowledge/auto-research-history.md` §7）

- **清洁交付五要素**：修复/补测后完整采用数据、完整分析报告、自包含脚本、隐私投影、缺项如实标注。
- **隐私投影规则**：删账户/API 凭据/运行金额/个人用户名路径（`/Users/<user>/…` → `<WORKSPACE>/`），保留研究中的政策/企业经济数值；脱敏后以新 manifest 校验，原封包留私有工作区。
- **落位最小核验集**：字节清单哈希＋关键计数复算＋敏感模式扫描；同版本复用，不整套重做。
- **adopted 主集＋legacy 追溯**：构成逐条登记（original／technical-replacement／format-repaired），原协议视图独立保留。

## 5. 真实阻塞与遗留项

1. **token v2 批准未签**：数据可用、口径完整，但原负责人 acceptance gate（`token-work/consumption-recheck-20261027-01/V2-OWNER-REQUEST.md`，私有工作区）未签署，故不称"批准版"。——需转原负责人。
2. **1023 runtime 缺口**：SASR54 tech01 与 MAMR initial 两阶段 `run_stage` 精确旧字节、代码/材料/模型输出再分发授权、PDF 字体许可待原 owner 补；补齐后出 sibling 版本重新验收。
3. **视觉 UNCONFIRMED**：两实验样本报告机器检查通过，但未经人工目视。
4. **analysis/ 工作数据未入 git**：新增分析目录合计约 30GB（`tsinghua-clean-release-20261027/` 24GB、`tsinghua-baseline-audit-20261022/` 4.2GB 等），超出 GitHub 单文件/推送现实约束；公开面已由目标仓三包承担。归档策略待裁定（LFS／外置归档／仅文档入库）。

## 6. 下一步

1. 转交 token V2-OWNER-REQUEST，闭合批准链后发版本化增补说明。
2. 1023 补交请求（`OWNER-RUNTIME-ASSETS-REQUEST-03.md`）回收后做 sibling 版本再验收。
3. 1025 终验收口：acceptance manifest、最终安全终检、人工视觉抽检。
4. 裁定 analysis/ 大体量数据归档策略；本报告不覆盖的 8–10 月初工作另立进度记录。
