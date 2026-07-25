# 路线图工作副本数据一致性审计（R3）

- 审计日期：2026-07-22
- 审计对象：`docs/roadmaps/worldcup-two-paper-roadmap-2026-07-21-working.md`（v1.5）与 `analysis/worldcup-proposal-review/stage2-literature-table.csv`
- 方法：按 `data-analysis` skill 工作流，以 DuckDB/SQL 检查 CSV；路线图数字逐条人工复核。
- 口径说明：CSV 没有独立 `status` 字段，因此本报告将 `verified_date IS NOT NULL` 作为“有核验记录”的可计算代理。CSV 行号含表头（L01 位于第 2 行）。

## 1. 文献底座结构化核对

### 1.1 总数与 verified 声明

**确认一致（但有口径限制）。**

DuckDB 结果：总行数 37，`id` 去重后 37；`verified_date` 非空 37、空值 0，且所有记录日期均为 2026-07-21。因此，路线图“37 篇 verified”的数量声明与可计算代理一致（`docs/roadmaps/worldcup-two-paper-roadmap-2026-07-21-working.md:9`；`analysis/worldcup-proposal-review/stage2-literature-table.csv:2-38`）。配套摘要也明确写成“37 行，verified 37/37 = 100%”（`analysis/worldcup-proposal-review/stage2-data-summary.md:3`）。

限制：CSV 只有 `verified_date`，没有 `verified/unverified` 状态列，故无法从 CSV 独立区分“日期已填但核验未通过”的情形；本结论验证的是 37/37 均有核验日期，而不是重做联网真实性核验。

### 1.2 年份分布

**确认一致。**

| 年份 | DuckDB 条数 |
|---:|---:|
| 2007 | 1 |
| 2019 | 1 |
| 2024 | 4 |
| 2025 | 7 |
| 2026 | 24 |

合计 37；与摘要 D1 完全一致（`analysis/worldcup-proposal-review/stage2-data-summary.md:63-71`）。

### 1.3 主题（domain）分布

**确认一致。**

| domain | DuckDB 条数 |
|---|---:|
| LLM预测 | 12 |
| 足球预测 | 11 |
| 校准方法 | 10 |
| 预测市场 | 4 |

合计 37；与摘要 D2 完全一致（`analysis/worldcup-proposal-review/stage2-data-summary.md:75-82`）。

### 1.4 方法标签（method_keywords）分布

**确认一致。**

按分号拆分 `method_keywords` 得 112 个标签实例、105 个不同标签。高频项为：Brier 8；agentic、Elo、fine-tuning、leaderboard、Murphy decomposition、RPS 各 2；其余 98 个不同标签各 1。摘要 D5 所列高频项与 SQL 一致（`analysis/worldcup-proposal-review/stage2-data-summary.md:101-103`）。

## 2. 路线图关键文献与 CSV crosswalk

| 关键文献 | 结果 | CSV 证据 |
|---|---|---|
| AMW（Agarwal–Moehring–Wolitzky） | **不一致：底座缺口** | CSV 37 条中无记录；路线图正文承重引用见 `docs/roadmaps/worldcup-two-paper-roadmap-2026-07-21-working.md:89,93-97,107`，参考文献见同文件 `:288` |
| Foresight Arena | **确认一致** | L36，`analysis/worldcup-proposal-review/stage2-literature-table.csv:37`；路线图 `:133,297` |
| Bosse | **确认一致** | L18，CSV `:19`；路线图 `:125,298` |
| InfoDelphi | **确认一致** | L37，CSV `:38`；路线图 `:129,299` |
| Scaling Agent Systems | **不一致：底座缺口** | CSV 37 条中无记录；路线图上游/方法/参考文献见 `docs/roadmaps/worldcup-two-paper-roadmap-2026-07-21-working.md:8,129,140,300` |
| Dunning | **不一致：底座缺口** | CSV 37 条中无记录；路线图机制注记和参考文献见 `docs/roadmaps/worldcup-two-paper-roadmap-2026-07-21-working.md:89,292` |
| Prophet Arena | **确认一致** | L13，CSV `:14`；路线图 `:129` |
| ForecastBench | **确认一致** | L12，CSV `:13`；路线图 `:129` |
| Hindcast | **确认一致** | L15，CSV `:16`；路线图 B0 (vi) 与版本记录见 `:163,279` |

结论：九项关键文献中六项在底座，三项（AMW、Scaling Agent Systems、Dunning）缺失。尤其 AMW 是 v1.3 后的承重主干，不能仅以 §10 单列参考文献替代“37 篇 verified 底座”中的结构化记录。

## 3. 路线图内部数字一致性

### 3.1 §4.7 调用量公式、各臂配置与区间

1. **确认一致：300 探针算术。** 300 分身 × 2 家族 = 600 次/任务；600 × 50 = 30,000 = 3×10⁴，因此“任务数 ≤50 → 约 ≤3×10⁴ 次调用”计算正确（`docs/roadmaps/worldcup-two-paper-roadmap-2026-07-21-working.md:171,174`）。
2. **确认一致：旧方案算术。** 10³–10⁴ 个预测 × 300 × 2 = 6×10⁵–6×10⁶，即 60 万–600 万（同文件 `:176`）。
3. **无法判定：主干 10⁴–10⁵ 与头条 10⁴–10⁶ 是否由配置推出。** 路线图未给 Stage 1 的定量 `moderate n`、Stage 2 的最终 MDE 样本量、探索臂任务数与辩论臂占比；且公式中的“已结算预测数”究竟是任务数还是已含臂比较的预测数存在语义歧义。正文也承认逐臂估计会令 Stage 1 预算乘 6 并顶破 10⁵ 上界（同文件 `:137,173`）。因此区间可视作规划包络，但尚不能由现有参数复算确认。
4. **不一致：确认性主干合计上界的加总表述。** Stage 1 被写为约 10⁴–10⁵，Stage 2 被写为“同量级或更低”，但随后主干“合计”仍写 10⁴–10⁵（同文件 `:173`）。若二者均达到 10⁵，合计可达 2×10⁵；数量级仍是 10⁵，但严格区间上界不是 10⁵。应明确该区间是 order-of-magnitude，而非硬数值边界，或把加总上界写为约 2×10⁵。
5. **确认一致：头条区间包容已列子账。** 300 探针硬上限 3×10⁴，辩论再乘 3–5，且正文保留逐臂乘 6 的超支情形；10⁴–10⁶ 作为含探索臂的宽量级包络没有与已列配置直接冲突（同文件 `:173-175`），但仍受上一条“无法定量复算”限制。

### 3.2 §4.3 power 锚点与 §4.6/§8 引用

**确认一致。** §4.3 将锚点限定为“α*=0.02、80% power、约 350 个已结算二元预测/单一比较”，并强调时间聚簇与三元任务需重算（`docs/roadmaps/worldcup-two-paper-roadmap-2026-07-21-working.md:133,138-140`）。§4.6 B0.5 要求实测聚簇设计效应回填 power 账，B2 按 MDE 定量（同文件 `:164,166`）；§8 又要求 OSF 冻结 Stage 2 主效应/MDE，期末考按 MDE 定量（同文件 `:243,245-246`）。后两处没有把 350 错当作每臂固定样本数，引用链一致。

### 3.3 B0 六件交付物

**确认一致。** 执行摘要明确“六件”（`docs/roadmaps/worldcup-two-paper-roadmap-2026-07-21-working.md:21`）；§4.6 枚举 (i)–(vi) 六件（同文件 `:159,163`）；§8 检查点也列六件同名交付物（同文件 `:242`）。

### 3.4 B0.5 go/no-go 在 §4.6、§7、§8 的一致性

**不一致：§7 风险表漏列 token-overlap 判据，且“未过”应覆盖全部判据。**

- §4.6 B0.5 的完整集合含：四项管线层、四项测量层（其中包括 token-overlap 区分度）、充分性验证、manipulation check（`docs/roadmaps/worldcup-two-paper-roadmap-2026-07-21-working.md:164`）。
- §8 检查点含四项管线层、三项概括测量层、两项强制交付物，但也未明列 token-overlap；它可被“通过 go/no-go”总括，但枚举不是完整复写（同文件 `:243`）。
- §7 “pilot 未过 go/no-go”一行声称列出 §4.6 B0.5 判据，却枚举时漏掉 token-overlap 区分度（同文件 `:233`）。

处置建议：§7 与 §8 均补入“token-overlap 区分度（不足则换分布级指标）”，或改成“以 §4.6 B0.5 全部判据为准”，避免读者把精简枚举误认为穷尽清单。除这一漏项外，“任一未过即不放量 B1、修复后重跑”的逻辑一致。

## 4. §9 版本记录与正文抽查

1. **无法判定：v1.3 当时的“四件”无法仅由当前快照复原。** v1.3 记录明确写“四件交付物规格化”（`docs/roadmaps/worldcup-two-paper-roadmap-2026-07-21-working.md:257`）；当前正文是 v1.5 的六件（同文件 `:163`）。这是增量版本记录与当前版本应有的差异，不构成当前件数冲突；但仅凭当前文件无法逐项核验 v1.3 当时四件的名称与范围。
2. **确认一致：v1.3 新增 §10。** 版本记录声称新增 §10 参考文献（同文件 `:260`），当前正文确有 §10（同文件 `:284-304`）。
3. **确认一致：v1.4 四扩五。** v1.4 记录写“B0 交付物四件扩五件”，新增信息隔离 SOP (v)（同文件 `:269,276`）；当前 §4.6 的 (v) 正是信息隔离 SOP（同文件 `:163`）。
4. **确认一致：v1.5 五扩六。** v1.5 记录写新增 (vi) Hindcast 占位调查（同文件 `:279`）；当前 §4.6 (vi) 与 §8 六件清单均存在该项（同文件 `:163,242`）。

## 5. 结论

- 路线图“37 篇 verified”在“37 行且 37/37 有 `verified_date`”口径下成立；年份、domain、关键词分布与配套摘要一致。
- 明确底座缺口 3 项：AMW、Scaling Agent Systems、Dunning。
- 明确内部不一致 2 类：主干区间把两个至多 10⁵ 的阶段合计仍写成至多 10⁵（量级成立、严格上界不成立）；§7/§8 的 B0.5 判据枚举漏 token-overlap 区分度。
- 另有无法判定项：因 `moderate n`、Stage 2 最终 MDE 样本量及探索臂配比未冻结，10⁴–10⁵/10⁴–10⁶ 区间目前不能从公式完整复算。
