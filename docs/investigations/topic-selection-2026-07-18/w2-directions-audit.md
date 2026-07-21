# W2 — 4 方向诚实审计（GO/PARK/KILL 决策依据）

日期：2026-07-18
作者：w2 agent（auto-research side audit）
边界：本审计仅服务于本仓库 auto-research 端的 4 个方向草稿内部审计。另有 w1/w3 并行 agent 在写其他文件，不动。
合规：本审计仅是「盘点 + 建议」，不强行触发项目 D17 决策规则。

---

## 0. 摘要：本审计的最终一句话判断

四个方向（D1 / D2 / D3 / D4）共享一个共同的诚实弱点——**对 G3 dual-ledger crosswalk 92.9% forward coverage 的自报数字，没有任何 draft 承认独立 audit 实测的真实覆盖率为 64.3% (9/14)**。其上 D2 的 features (a)+(b) 在 AR side 数学上不可计算、D3 §6 是 methodology spec 不是 experiment、D4 是 inheritance 三个 child 草稿的 collapse 而非真合成。Top-journal KILL verdict（2026-07-06 cross-project-roi §七）本审计日仍成立。

| Dir | ceiling | acceptance | GO/PARK/KILL |
|---|---|---|---|
| **D1** G3 standalone | ACL/EMNLP Findings 7.0-7.5 | 25-35% | **PARK** |
| **D2** verdict-reversal | Findings only (marginal) | 25-35% if AUROC>0.7；否则 honest-negative-result | **PARK** |
| **D3** + harness-evolution ablation | Findings 7.0-7.5 additive | 25-35% additive to D1 | **PARK**（作为 D1 appendix 看待，独立 paper 不推荐）|
| **D4** cross-direction joint | Findings 7.5-8.0 contingent | 35-45% self-report contingent；失败则 PARTIAL | **KILL** |

---

## 1. 输入材料清单

| 文件 | 行数 | 状态 |
|---|---|---|
| `auto-research/docs/papers-closed-portfolio/directions-attempt-2026-07-18/d1-g3-standalone-paper-draft.md` | 121 | 完整 |
| `auto-research/docs/papers-closed-portfolio/directions-attempt-2026-07-18/d2-verdict-reversal-paper-draft.md` | 99 | 完整 |
| `auto-research/docs/papers-closed-portfolio/directions-attempt-2026-07-18/d2-rescore-card.md` | 32 | 完整 |
| `auto-research/docs/papers-closed-portfolio/directions-attempt-2026-07-18/d3-g3-with-harness-ablation-draft.md` | 142 | 完整 |
| `auto-research/docs/papers-closed-portfolio/directions-attempt-2026-07-18/d4-cross-direction-joint-paper-synthesis.md` | 118 | 完整 |
| `auto-research/state/progress.json` | 117 | 完整 |
| `auto-research/docs/papers-closed-portfolio/g3-dual-ledger-crosswalk.md` | 83 | 完整（schema bridge 实锤）|
| `auto-research/docs/papers-closed-portfolio/g3-dual-ledger-crosswalk.json` | 30 | 完整（g3_brier_pass=false, status=synthetic_test_only）|
| `auto-research/docs/investigations/archive/cross-project-roi-2026-07-06.md` | 318 | 完整（真实 64.3% 来源 + 跨项目 ROI）|

搜索过但找不到：`g3_crosswalk.py`（0 命中）、`22-investigation` schema 规范（0 命中）、G3 字段映射 supplementary figure（无 supplementary 路径）。

---

## 2. 关键 audit discoveries（先于四方向分析）

### 2.1 G3 self-report 92.9% vs verified 64.3% —— 4 draft 共同的最大诚实缺口

**Self-report（`g3-dual-ledger-crosswalk.{md,json}`）**：

- AR evidence_ledger_entry：14 个 required fields
- 13/14 = **92.9%** forward coverage
- 8/12 = 66.7% reverse coverage
- Enum overlap：`['branch']` only

**Verified recount（cross-project-roi §(E) 独立 ROI 分析师重测）**：

| 字段组 | AR (14-field) | CWCUP (12-field) |
|---|---|---|
| AR-only unique | 7（freshness / freshness_window / freshness_ratio / authority / applicability / audit_trace / missing_prerequisites）| — |
| CWCUP-only unique | — | 4（origin / match_id / direction / quantified_threshold）|
| 共享（语义严格匹配）| 9 | 9 |
| **真实覆盖** | **9/14 = 64.3% AR→CWCUP** | **9/12 = 75% CWCUP→AR** |

Self-report 92.9% 是 AR-centric lenient counting（含 confidence_before[0,1]↔confidence_0_10[0,10] 这种「数值范围跨度的 shape transformation」算「匹配」+ 把 7 AR-only 字段当「不必有 CWCUP 对应」的 scope 假设）。Enum 仅 1/5 重叠（`branch` only），与 self-report 一致。

**对四 draft 的影响**：D1 / D2 / D3 / D4 各自在自己的 Abstract/§1/§3.1 中 anchor 92.9% 作为 crosswalk 有效性的核心证据，**无人提到 64.3% 的核验发现**。审稿人只要进入 schema bridge 复算就会立即发现 7 AR-only 字段（freshness trio + authority + applicability + audit_trace + missing_prerequisites）的语义 loss 没有 honest acknowledgement。

D1 在 §3.1 自己写了 "Six AR fields are unique to AR"——也漏掉了 missing_prerequisites，列了 6/7 而非 7/7。

### 2.2 Brier "2/2 100% match" 是 version-pair resolver 的产物，Brier vectors 仍是 placeholder

**Self-report**：
- `progress.json` 2026-07-05T03:25:28Z："G3.3 Brier replay with version-pair resolver: 2/2 settlements matched (100%)"
- `cross-project-roi` §(C) post-gate-and-qlib-assessment 25-30：「The JSON explicitly records `g3_brier_pass=false`. The text says settlement records were not exported, but local inspection found: ... `wc2026-a-m01-mex-rsa.settlement_record.yaml` ... `wc2022-g-arg-ksa.settlement_record.yaml`」

也就是说：settlement records **确实在 disk 上存在**（2 个真实 .yaml），但最初 `g3-dual-ledger-crosswalk.json` 的 g3_brier_pass=false 反映的是 version-pair ambiguity（v0.1 [0.55,0.27,0.18] vs v0.2 [0.62,0.23,0.15]）。第二次跑通了，原因不是新数据而是消歧义解决。

D1 §4 的 2/2 100% 是 consistent 的，但 **§4 的表（S1/S2 cal_loss / disc_loss / refinement cells）全是 (value) placeholder**——不是造假，是诚实 placeholder。

**新增真实数据（2026-07-08 之后，与本审计同期或稍前）**：
- `cds4worldcup-settlement-experiment-executed-2026-07-08.md` 报告：3 张新 settlement record（wc2026-b-m02 / c-m01 / f-m01），n=48 Brier=0.2392（<0.25 baseline）
- **这意味着 2026-07-18 时点真实 Brier 可用数据 ≥ 5 settlements**，但 D1/D2/D3/D4 都没采用

**对四 draft 的影响**：D1 在 §4 锚定 N=2 是诚实但不必要的；D2 的 "22-investigation corpus" 无法 trace 到这 5 个 settlement record 中的任何一个——因为 22-investigation 是 auto-research harness 内的 findings，不是 cds4worldcup settlement records；D2 用错 corpus 子集。

### 2.3 arXiv metadata cross-assignment 是 desk-reject trigger

10 个 arXiv ID 在 D1 / D2 / D3 / D4 间交叉引用，但作者/年份 metadata 不完全一致（仅抽查 5 个 ID）：

| arXiv ID | D1 | D2 | D3 | D4 | 是否一致？ |
|---|---|---|---|---|---|
| 2606.04217 | — | "Zhang et al. (2026)" | "Zhang et al. (2026)" | inherit | 一致 |
| 2607.01661 | — | "Li D. et al. (2024)" | "Kumar et al. (2026)" | inherit | **不一致**（同 ID 不同作者+年）|
| 2607.09921 | "Jajal (2026)" | "Lin et al. (2026)" | "Lin et al. (2026)" | inherit | **不一致**（D1 与 D2/D3 不一致）|
| 2605.03310 | "Nechepurenko (2026)" | "Nechepurenko (2026)" | "Nechepurenko (2026)" | inherit | 一致 |
| 2607.09349 | "Caruzzo (2026)" | "Caruzzo (2026)" | "Caruzzo (2026)" | inherit | 一致 |
| 2604.25850（AHE）| — | — | "Lin et al. (2026)" | inherit | D1 §2 标 arXiv:2604.07236 for harness 引发不同作者署名 |
| 2603.28052（Meta-Harness）| — | — | "Lee et al. (2026)" | inherit | OK |
| 2606.20683（华为/PKU）| — | — | "Han et al. (2026)" | inherit | OK |

至少有 arXiv:2607.01661 / arXiv:2607.09921 两个 ID 在 draft 间作者归属不一致。审稿人会立刻质疑——这是 ACL/EMNLP 的 desk-reject trigger。

### 2.4 22-investigation corpus 在 disk 上无独立 schema 证据

- D2 §3.1：D2 自承 "a verdict $v_i$ is a record produced by the harness at epoch $t_0$, carrying a probability vector $p^{(i)} = (p_1, ..., p_k)$ over $k$ outcomes and an asserted outcome $a_i$"
- D2 §5 limitations #3 自承："the construction of the pre-reversal oracle assumes that the corpus has realised re-adjudication records. The reversal label $y_i$ is defined by the outcome of a re-adjudication that has actually occurred; without a realised re-adjudication, $y_i$ is undefined and the predictor cannot be trained or evaluated"
- `find -name "*22-investigation*"` schema spec → 0 hits
- progress.json 多次 mention 22 investigations 但无 schema 文件 path

**对 D2/D4 的影响**：corpus precondition 在 disk 上无法被独立验证；但这不是 audit 的 collapse point——见下 §2.5，feature (a)+(b) 在 AR side 数学不成立是一个独立、更强的 collapse point。

---

## 3. D4 联合论文专项事实核验（按 task brief 要求）

**D4 关键声明**：

> §1："D2 = the detector built from the instrument. Verdict-reversal prediction: collects, for each verdict `v_i` at the pre-reversal epoch `t_0`, the **D1 instrument's two signals** (`r^(i)` and the Murphy triple)"
>
> §3 C2 PASS：「Removing the unique-data substrate (22-investigation corpus or Gulei 2015 scenario) does not collapse the methodology: the joint method remains trainable on any audit-trail corpus satisfying (a) dual-ledger crosswalk compatibility, (b) probability vector at `t_0`, (c) realised re-adjudication records.」
>
> §3 C5 PASS (on method)：「The D1 instrument is reproducible without unique data (crosswalk is a schema, Murphy decomposition is algorithmic)」

**D2 §3.2 关键声明**（被 D4 引用为 "D1 instrument's two signals"）：

> "We construct two features for each verdict from the G3 dual-ledger crosswalk ... The crosswalk maps 13 of the 14 auto-research required fields forward onto the cds4worldcup schema"
>
> 「**Feature (a): Crosswalk projection residual** ... we compute the residual $r^{(i)} = \|v_i - \Pi^{\dagger}(\Pi(v_i))\|$, the L1 distance between the verdict's field contents as recorded under $L^{AR}$ and the contents recovered by projecting forward to $L^{CWCUP}$ and back. The residual is zero when the crosswalk losslessly round-trips the verdict, and positive when the round-trip loses information — for example, when the principal-counter-signal projection drops all but the first element of a `contradicting_evidence` list」
>
> 「**Feature (b): Murphy-decomposed Brier sub-components** ... Given the probability vector $p^{(i)}$ carried by the verdict at $t_0$, we form a *pre-outcome Murphy decomposition*」

**逐项核验结果**：

| D4/D2 关键子声明 | G3 crosswalk 是否支持？ | 真实可计算？ | 核验来源 |
|---|---|---|---|
| 14→12 字段正向投影 13/14 | 部分：self-report 92.9%，verified 64.3% (9/14) | 7 AR-only 字段在 CWCUP 侧消失 | g3-dual-ledger-crosswalk.md §2 表 |
| feature (a)：Π→CWCUP→Π† round-trip | **不支持**：磁盘无 `g3_crosswalk.py`（0 命中）；D1/D2 均未明文定义 Π† 的算法 | **不可计算**：信息论上不可能 round-trip（7 AR-only 字段 Π→CWCUP 即丢失，Π† 回不来）| grep + 信息论论据 |
| feature (a) example "principal-counter-signal projection drops all but the first element of contradicting_evidence" | D1 §3.1 crosswalk 表格中 `contradicting_evidence[]` → `counter_signal (string)` 确实标 "DIFFERENT shape (list vs string)" | 部分 support；但 Π† 「回填 list」的算法在 D1/D2/磁盘都无定义 | g3-dual-ledger-crosswalk.md §2 |
| feature (b)：pre-outcome Murphy decomposition on **probability vector** $p^{(i)}$ at $t_0$ | AR side `confidence_before` 是 SCALAR [0,1]；CWCUP side 是 vector | **AR side 数学无定义**：feature (b) 需 multi-outcome 概率向量做 bin partition；AR evidence_ledger_entry 只载 scalar confidence_before | g3-dual-ledger-crosswalk.md §2 |
| feature (b)：partition $[0,1]$ interval into $B$ equipopulated bins over the **training split** | 需 training split empirical forecast distribution | 22-investigation corpus 是 D2 自创 framing，disk 上无 schema spec；training-split bin partition 不是 G3 crosswalk output | disk search |
| 22-investigation corpus 携带 dual-ledger + pre-reversal vector | D2 §1 假设 verdict $v_i$ carry $p^{(i)} = (p_1, ..., p_k)$ | **corpus precondition 不可 verify**：D2 §5 limitations #3 自觉诚实承认 | progress.json + disk search |
| D1 "instrument" 的 two per-record signals = $(r^{(i)}, \text{Murphy triple})$ | **D1 不输出这些**：D1 §3-4 输出是 (a) cross-coverage 92.9% 作为总体数；(b) per-settlement Murphy-decomposed Brier vector ⟨Brier, cal_loss, disc_loss, refinement⟩ | D4 §1 的描述是 **factually incorrect 简化**：reconciliation-loss signal 是 D2 自创 feature，不来自 D1 | D1 §4 + D2 §3.2 |

### 3.5 核验结论

D4 联合论文声称 "D2 §3.2 reconciliation-loss features（feature (a) projection residual, feature (b) pre-reversal epoch Murphy-decomposed Brier components）直接复用 G3 dual-ledger crosswalk" 在以下 4 个具体子声明上**部分或全部不成立**：

1. **feature (a) 在 D1 disk artifacts 上不可计算**——磁盘上无 `g3_crosswalk.py`，Π→CWCUP 阶段在 7 AR-only 字段上信息 loss，Π† round-trip 在该 loss 上信息论不可逆
2. **feature (b) 在 AR side 数学上无定义**——multi-outcome probability vector 是 CWCUP 侧的特性；AR evidence_ledger_entry 只载 scalar confidence_before，没有 multi-outcome probability vector 让 Murphy bin partition 工作
3. **22-investigation corpus** 在磁盘上**无 schema 证据**——D2 §5 limitations #3 已诚实承认但 D4 §1 没 surfaced 这个诚实缺口
4. **D1 "instrument" 不输出 $(r^{(i)}, \text{Murphy triple})$**——D4 §1 自报 "the instrument produces two per-record signals: (i) crosswalk projection residual r^(i) and (ii) the triple of Murphy components" 是不准确的：D1 §3-§4 输出是总体覆盖率数字 + per-settlement Murphy-decomposed Brier vector；不是 per-record projection residual。

**结论**：D4 联合论文的 inheritance 链是 **collapse 而非 synthesize**。三个 child drafts 每一个都 honest-fail 在自己的 context（D1/G3 自报 92.9% vs verified 64.3%；D2 features 数学不可计算；D3 §6 是 spec 不是 experiment），D4 把这些 fails 整合（"unified methodology stack"）而不是 engineered away。Integration 不是 Resolution。

D2 §5 limitations #4 已诚实承认："the reconciliation-loss signal may be specific to ledger-schema-reversal as a failure mode ... Bug classes that leave the reconciliation loss invariant but perturb other features of the verdict (the retrieval trace, the prompt-level state) are not detected by this method"——这本身就 honest 标记了 projection residual / Murphy triple 是不完整检测器；D4 §1 没 surface 这个 honest 标记。

---

## 4. 四方向各自 audit

### 4.1 D1 — G3 Standalone (settlement reconciliation)

#### (a) 一句话核心 claim
跨域 LLM-as-judge audit trail schema 之间的 **settlement reconciliation**（dual-ledger crosswalk + 正交 enum 分析 + Murphy-decomposed Brier replay）是 schema-engineering 原语，与 Hyndman hierarchical forecast reconciliation 同名异实；2/2 settlement 在 100% Brier replay match。

#### (b) 自称 vs 真实证据

| 维度 | self-reported | verified on disk | 缺口 |
|---|---|---|---|
| Forward coverage | 92.9% (13/14) | 64.3% (9/14) | **−28.6 pp** |
| Reverse coverage | 66.7% (8/12) | 75% (9/12) | +8.3 pp（investigator 重组）|
| Cross-field enum match | 1/5 (`branch`) | 1/5 (`branch` only) | 一致 |
| N=2 settlements 100% Brier match | 2/2 (progress.json 2026-07-05) | vectors 仍是 placeholder | vectors 未填 |
| Hyndman disambiguation | §1 主动命名 | 文字工作 | OK |
| Deceptive grounding analogy | §3.4 显式映射 | arXiv:2607.09349 真伪未独立 verified | metadata 风险 |
| G3.3 Brier (real settlement records) | "100%" 2/2 | 真实 records 仅 5 settlements on disk (2026-07-18)；D1 仅用 2 | 数据可得但未采用 |

**最关键缺口**：G3 92.9% 是 self-report anchor 但未经语义严格核验。审稿人进入 schema bridge 复算就会发现 7 AR-only 字段（freshness trio + authority + applicability + audit_trace + missing_prerequisites）的语义 loss 没有 honest acknowledgement。D1 §3.1 列了 6 个 AR-only 字段，**漏掉了 missing_prerequisites**（7→6 偏移）。

#### (c) 天花板 + 接收概率 + 依据

- 项目 disposition（progress.json + cross-project-roi）：ACL/EMNLP Findings 7.0-7.5，25-35% 接受率
- 上 main-track ≥7.5 缺：第三 settlement（实有 ≥5 on disk 但 D1 未采用）、external validation（G5 标准 fail：人工 gold-set 或 public benchmark tie-in 缺）、Brier vectors honest fill
- Top-journal KILL verdict（前几轮成立）本审计日仍成立——D1 没突破 G3 ceiling

#### (d) 最脆弱三点

1. **92.9% self-report 的 robust 缺口**：审稿人会要求 13/14 字段语义证明；7 AR-only 字段的「可忽略」声明会被 contest。一旦承认 64.3% 是真实语义匹配覆盖，则 D1 核心证据 anchor 失效（从 13/14 到 9/14 = -28.6pp）
2. **N=2 = illustrative 而非 statistical**：D1 §5 自承 "100% replay success on two settlements is illustrative, not statistical"——这与 §4 "No settlement-reconciliation violation was detected on either record" 矛盾：100% match 在 N=2 是 base-rate artefact，无法证 method performance
3. **Deceptive grounding analogy 是 narrative 不是实证**：§3.4 写 AR `factor_type = falsifier` → CWCUP `event_relation = precursor` 是 violation 范例，但 (i) 无 detector 实现（"We do not claim a closed-form detector for this violation class"——§3.4 末句自报）；(ii) 无反例证明该违反类在 22 investigations 或 2 settlements 中真实存在

#### 推荐：**PARK**
理由：D1 是 4 draft 中**唯一可独立投稿**的目标，但需先在 64.3% 真实值上重写 §3.1 字段映射表。诚实承认 "92.9% AR-centric lenient counting" + "64.3% strict semantic counting" 反而提升 credibility。25-35% Findings 概率与既有项目 disposition 一致，可作为唯一活跃目标维持。

---

### 4.2 D2 — Verdict-Reversal Prediction (reconstructed framing)

#### (a) 一句话核心 claim
用 G3 dual-ledger crosswalk 提供的 reconciliation-loss 信号（projection residual + pre-outcome Murphy decomposition）+ 22-investigation corpus 训练的 logistic classifier，可在 re-adjudication 之前预测 LLM-as-judge 哪些 verdict 会反转。

#### (b) 自称 vs 真实证据

| 维度 | self-reported | verified on disk | 缺口 |
|---|---|---|---|
| C1 single insight sentence | reconstructed PASS (d2-rescore-card) | self-eval, 非 external 5-persona review | C1 自评成立 |
| C2 what's new | 边际 PASS | component-incremental（Murphy-decomposed Brier 来自 Nechepurenko 2026；crosswalk 来自 G3；pre-reversal prediction 来自 Caruzzo 2026 analogous）| honesty OK |
| 22-investigation corpus | D2 §4-§5 存在 | **disk 上无 schema 实体**：find `22-investigation` schema spec 0 hits；D2 §5 limitation #3 自承 corpus precondition 不可外部 verify | **precondition 不可 verify** |
| Pre-reversal probability vector at $t_0$ | D2 §3.2 假设 | AR `confidence_before` 是 scalar [0,1]；**不是 multi-outcome vector**；CWCUP 才有 vector | **feature (b) 数学无定义** |
| Crosswalk projection Π round-trip | D2 §3.2 feature (a) claim | 7 AR-only 字段在 CWCUP 侧消失，Π→CWCUP 信息 loss → Π† 无 round-trip | **feature (a) 不可计算** |
| AUROC, $N_{gt}$, $N$, precision, ECE | `4-FICV AUROC [PLACEHOLDER-NOT-COMPUTED-YET]` | 5 个 magnitudes 全部 placeholder | placeholder 占 100% |
| NeurIPS 2026 E&D failure-mode-exposure 入口 | D2 §1 引用 | 该 guidance document 是否实际公开存在未独立 verified | metadata 风险 |
| Deceptive grounding analogy | D2 §1 引用 | arXiv:2607.09349 真伪未独立 verified | 同上 |
| F4 7-check 整体 | 5/7 FAIL → 7/7 PASS (1 marginal) | (rescore-card self-eval, 未受 external 5-persona review) | self-eval |

**最关键缺口**：(i) "reconciliation-loss signal" 在 D2 §3.2 中依赖 features (a) and (b)，但 feature (a) projection residual 在 G3 crosswalk 的 7 AR-only 字段情形下信息论不可逆；(ii) feature (b) 需要 multi-outcome 概率向量，AR evidence_ledger_entry 只载 scalar confidence_before，Murphy decomposition bin partition 需 $p_i \geq 1$ 维 vector。当 framing 自承 "verdict $v_i$ carry probability vector $p^{(i)} = (p_1, ..., p_k)$"——这是 D2 假设但未 trace 到 22-investigation corpus 任一 verdict 在 on-disk 上自带 vector 的证据。

#### (c) 天花板 + 接收概率 + 依据

- D2-rescore-card 自评：ACL/EMNLP Findings 边际 PASS；main-track 仅 marginal
- Honest trajectory：
  - **若 AUROC > 0.7 in 4-FICV**：Findings 7.0-7.5，25-35% acceptance
  - **若 0.55-0.65**：honest marginal，**reframe 作 honest-negative-result**（d2-rescore-card honest bottom-line 已显式推荐此路径）
  - **若 ≈ 0.5**：negative-result paradigm，paper 价值转为 method-publication-of-negative-trial
- Top-journal KILL verdict 前几轮成立；本 audit 日仍成立

#### (d) 最脆弱三点

1. **Pre-reversal probability vector 在 AR side 数学无定义**：feature (b) Murphy decomposition multi-outcome bin assignment 需 vector；AR confidence_before 是 scalar 不行。要么 D2 改用 post-outcome Murphy（破坏 framing）；要么改用 CWCUP side records（跨 ledger 时信息 loss）；要么构造 synthetic vector 凑 feature（不诚实）
2. **22-investigation corpus 不可 external verify**：D2 §5 limitations 已承认 "the corpus was produced as the run-history of a single research codebase, and the reversal labels are whatever that run-history realised"——如果 reversal labels 在 corpus 中不存在（如 harness 实际从未产生过 reversal），则 reconstruction 永远是 placeholder paper
3. **N=22 × 4 folds = small-sample AUROC CI 太宽**：审稿人立即 challenge：D2 §4.4 提 3 ablation 但全部 placeholder；reviewers 引 receiver operating characteristic small-sample econometrics 拒绝 result 是大概率事件

#### 推荐：**PARK**
理由：reconstruction 自评已诚实，residuals 表达 trained-on-paper 模式有结构，但 two-function 数学不可计算 + corpus 未独立 verify = paper 不能 in good faith submit。建议：在 auto-research git tree 中 grep 任何 pre-reversal probability vector 证据（schema spec / sample record）；如不存在则 D2 是 permanently placeholder paper，应 KILL；如存在且可 compute 则重新 audit feature (a)/(b) 可计算性。

---

### 4.3 D3 — G3 + Harness-Evolution Ablation

#### (a) 一句话核心 claim
settlement reconciliation 方法在 incrementally layered harness configurations（B → B+ATP → B+ATP+VA → B+ATP+VA+SGR）下保持 robust（92.9% forward coverage ≥80%、Murphy components 稳定、stage (iv) violation detector 在 SGR layer 精准）。§6 Harness-Evolution Ablation 是 substantive 新内容。

#### (b) 自称 vs 真实证据

| 维度 | self-reported | verified on disk | 缺口 |
|---|---|---|---|
| D1 primary contribution | INHERITS D1 92.9% self-report | 同 D1：64.3% verified | 同 D1 缺口（-28.6pp）|
| §6 Harness-Evolution Ablation 是 substantive 新内容 | D3 §1 §6 自承 | **disk 无 4-layer harness 实现**：grep B+ATP/B+ATP+VA/SGR code 0 命中；4 configurations 在 harness-engineering literature 是**概念**，本项目无实现 | §6 是 methodology spec, **不是 ablation experiment** |
| H1 crosswalk resilience ≥80% all layers | HYPOTHESIZED-NOT-TESTED | 无 on-disk 实验数据 | placeholder |
| H2 component sensitivity asymmetry | HYPOTHESIZED-NOT-TESTED | 无 on-disk 实验数据 | placeholder |
| H3 SGR uniquely catches stage (iv) | HYPOTHESIZED-NOT-TESTED | 无 on-disk 实验数据 | placeholder |
| AHE/Meta-Harness 等 4 occupant papers | D3 §1 §2 cite | arXiv:2604.25850 (AHE) 在 D1/D3 归属不一致（D1 §2 标 arXiv:2604.07236 for harness；D3 §1 标 arXiv:2604.25850 for AHE by Lin et al.）| **citation integrity 风险** |
| D3 §6.4 与 AHE check-loop pillar 本质冲突 | D3 §6.4 自承 AHE 已 propose closed-loop check analogous to SGR | 若 AHE 已有 SGR-like layer，D3 H3 关于 "SGR uniquely catches stage (iv)" 的 novelty 被重叠 | novelty 与 prior work 边界不清 |

**最关键缺口**：D3 §6 substantive new contribution 全部 HYPOTHESIZED-NOT-TESTED；4 harness layer 配置需要在 harness 实现层面写新代码（不是 paper 写作）。D3 是 methods paper 草稿但 §6 是 methodology spec，不是 experiment report。

#### (c) 天花板 + 接收概率 + 依据

- 项目 disposition：G3 methods paper 增量（H1-H3 hypotheses added）
- Honest ceiling 与 D1 同档：ACL/EMNLP Findings 7.0-7.5
- §6 在 D1 之上 additive = workshop-paper 增量；单独不够撑 D3 论文独立投稿
- 若 H1-H3 hypotheses 一旦 fill：可能升 Findings 7.5-8.0，但 review panel require separate §6 报告 + main paper

#### (d) 最脆弱三点

1. **H1-H3 都是 placeholder hypotheses**：D3 §6.3 自报 "HYPOTHESIZED-NOT-TESTED"——这是诚实的，但也是脆弱的："a failed hypothesis is informative" 作 §6.3 安慰；审稿人看 "placeholder = unstable claim"
2. **§6 ablation 假设 harness 4-layer 在 codebase 可配**：B → B+ATP → B+ATP+VA → B+ATP+VA+SGR 在 harness-engineering literature（Lee/Lin/Han/Ning 2026）是**概念**，本项目 harness 配置层面无 codebase 实证——4-layer chain 实际上是 spec draft，不是 experiment
3. **AHE/Meta-Harness 列为 occupant papers 但实际借鉴可能不充分**：D3 §1 引 4 篇作 "occupied subspace"，但 §6 ablation 增量未触及它们具体 layer 实现细节；reviewer 可能 score §6 为 "too thin to read as a contribution to the occupied subspace"

#### 推荐：**PARK**（作为 D1 的 §7 appendix 看待，不作独立 paper）
理由：§6 substantive content 是 methodology spec 不是 experiment。把 §6 fold 进 D1 作 appendix 比独立 D3 论文更 honest。H1-H3 hypotheses 留下次 priority；本 audit 日若必须出唯一投稿目标则 D1 单一文件 > D3 单一文件。

---

### 4.4 D4 — Cross-Direction Joint Paper Synthesis

#### (a) 一句话核心 claim
D1 (instrument) → D2 (detector built from instrument) → D3 (ablation axis on detector) 形成 unified methodology stack；联合论文满足全部 5 条 Gewin 选题判据且全 PASS，honest ceiling ACL/EMNLP Findings 7.5-8.0，main-track plausible if placeholders resolve。

#### (b) 自称 vs 真实证据

| 维度 | self-reported | verified on disk | 缺口 |
|---|---|---|---|
| C1 single key message | "Joint sentence names instrument + detector + ablation"—PASS | D4 §2 self-eval，**未受 external 5-persona review** | 是自评 |
| C2 what's new (Removal-of-data-uniqueness survival) | 边际 PASS | inherit D1+D2+D3 intersection, no paradigm shift | honesty OK |
| 22-investigation corpus | 三 drafts 共用 substrate | 同 D2：corpus 不可在 disk 上被独立 verify | 同 D2 缺口 |
| D1 92.9% coverage | inherit from D1 | 64.3% verified | inherit 缺口（-28.6pp）|
| **D2 dual-ledger reuse** | D4 §1 "D2 collects, for each verdict `v_i` at the pre-reversal epoch `t_0`, the D1 instrument's two signals (r^(i) and the Murphy triple)" | **3 项 false simplification**（详见 audit §3 上文）| **3 项 fail** |
| D3 H1-H3 hypotheses | inherit from D3 | placeholder | 同 D3 缺口 |
| D4 Recommendation against D17 | D4 §6 "this document is a **synthesis, not a recommendation**" | honest procedure compliance | OK |
| 14 arXiv ID 引用 consistency | D4 §3 标 "all 14 primary-source arxiv IDs from the union" | **5+ inconsistency**（D1/D2/D3 各自归属 arXiv:2607.01661, 2607.09921, 2604.25850 metadata 不一致）| citation integrity 风险 |

**专项核验（按 task brief 要求）详见 §3**：D4 联合论文声称 D2 §3.2 features (a)+(b) 直接复用 G3 dual-ledger crosswalk——核验结果**部分/全部不成立**：

1. feature (a) Π→CWCUP→Π† round-trip 在 7 AR-only 字段情形下信息论不可逆
2. feature (b) pre-outcome Murphy 需要 multi-outcome probability vector；AR side 只载 scalar
3. 22-investigation corpus 不可在 disk 上 verify 携带 precondition
4. D4 §1 把 D2 features 简化为 "D1 instrument produces two per-record signals" 是 **factually incorrect 简化**——D1 输出是 cross-coverage 分数 + Brier replay match vector；D2 的 reconciliation-loss signal 是 D2 自创 feature，不来自 D1

#### (c) 天花板 + 接收概率 + 依据

- D4 honest §5 自身承认："higher upside, higher soundness risk than any of the three standalone drafts"——四种风险：
  1. **Placeholder risk**：placeholders resolve 失败则 C2-PARTIAL published
  2. **N=2 + N=22 + N=4 chain amplifies joint uncertainty**——reviewer 立即 challenge
  3. **C1 dilution risk in execution**：8 页压缩使 integration 变 enumeration
  4. **Soundness under AHE/Meta-Harness**：D3 §6.4 与 AHE check-loop pillar 重叠，novelty bound 不清
- Honest ceiling: ACL/EMNLP Findings 7.5-8.0 (placeholder contingent); main-track **not possible**
- 若 placeholders resolve as predicted：Findings 接受率 self-report 35-45%
- 若 placeholders 失败（D2 AUROC ≤ 0.55）：C2-PARTIAL published，D4 跌 honest-negative-result 框架

#### (d) 最脆弱三点

1. **3 个 child draft 是 premises inheritance, not synthesis**：D4 是 composition doc；inherit D1 缺口 (92.9% → 64.3%) + D2 缺口 (feature (a) 不可计算 + feature (b) AR side 无 vector) + D3 缺口 (§6 placeholder)。3 child 脆弱性是 additive 不是 multiplicative——但 D4 把 3 draft 「集成」为单方法学 stack 是 multiplicative 在 soundness 维度（任一 child fail → joint fail）
2. **N=2 + N=22 + N=4 联合不确定性**：D4 §5 honest limit #2 明示 "a reviewer is statistically entitled to ask whether the conjoint AUROC has confidence intervals tight enough to support a C3-positioned novelty claim"——reviewer 立即 challenge 的点
3. **AHE closed-loop check pillar 与 H3 hypothesis 实质冲突**：D3 §6.4 自承 AHE check-loop pillar analogous to SGR——若 AHE 已有 SGR-like layer，D3 H3 关于 "SGR uniquely catches stage (iv) events" 的 novelty 是重叠，需 reviewer-side disambiguation 而 D4 没做

#### 推荐：**KILL**
理由：
- D4 是 synthesis 文档**而非 paper draft**：D4 §6 自我 qualify "this document is a **synthesis, not a recommendation**"——synthesis doc 不是 paper
- D4 §5 honest caveat #1 自我警示：「A joint paper submitted with placeholders is not a paper; a joint paper submitted after a run that resolves the placeholders as different from the predicted range ... drops from C2-PASS to C2-PARTIAL」
- D4 §5 honest caveat #2 自我警示：「A reviewer is statistically entitled to ask whether the conjoint AUROC has confidence intervals tight enough」
- D4 §5 honest caveat #4 自我警示：「reviewers familiar with AHE may push back on whether the addition is methodologically distinct or whether it is a re-treading of AHE's check-loop pillar」
- inheritance 的 3 个 child 缺口必须先各自 fix 才有 joint paper 谈——而 child 缺口是 substantive project-level work, 不是 paper-write work
- 即使 3 child 都 fix，D4 "joint paper" 在 reviewer 视角仍是 "D1 with extra verifier on top"——单一 paper 仍 containable

---

## 5. 横向比较 + 收口

| Dir | ceiling | acceptance | empirical state | self-reported vs verified gap | GO/PARK/KILL |
|---|---|---|---|---|---|
| **D1** G3 standalone | ACL/EMNLP Findings 7.0-7.5 | 25-35% | 2/2 Brier replay (vectors placeholder)；5 settlements 数据可得但未采用 | 92.9% → 64.3% (−28.6 pp) | **PARK** |
| **D2** verdict-reversal | Findings only (marginal) | 25-35% if AUROC>0.7；否则 honest-negative-result | 5 placeholders | feature (a) 不可计算 + feature (b) AR side 无 vector + corpus 不可 verify | **PARK** |
| **D3** + harness-evolution ablation | Findings 7.0-7.5 additive | 25-35% additive to D1 | 3 hypotheses HYPOTHESIZED-NOT-TESTED | inherit D1 gap + §6 是 spec 不是 experiment | **PARK**（作 D1 §7 appendix，独立 paper 不推荐）|
| **D4** cross-direction joint | Findings 7.5-8.0 contingent | 35-45% self-report contingent；失败则 PARTIAL | inherit 3 child 缺口 | multiplicative gap：child drafts 全 fail → joint fail；D1 instrument 的 factually incorrect 简化 3 项 | **KILL** |

---

## 6. 关键 audit findings 收敛

1. **"诚实 G3 覆盖率" 是 4 draft 共同的最大诚实弱点**：所有 draft inherit 自报 92.9% 但 verified 64.3%（跨项目 ROI §(E) 实测）。**建议：在任何 draft 投稿前先做 schema bridge 复算，承认 64.3% 是真实 semantics-matched 覆盖而非 92.9% AR-centric lenient counting**——重写 §3.1 字段映射表时该 honest 重写能提升 credibility
2. **D4 联合论文的 inheritance 是 collapse 而非 synthesize**：3 child drafts 每一个的脆弱性都 honest-fail 在自己 context；D4 stacked fails without engineering solution。Integration ≠ Resolution
3. **arXiv metadata inconsistency 是 desk-reject trigger**：至少 arXiv:2607.01661 (D2: Li D. et al. 2024 vs D3: Kumar et al. 2026), arXiv:2607.09921 (D1: Jajal vs D2/D3: Lin et al.) 跨 draft 归属不一致。建议 cross-attribution reconciliation 表格维护每 arXiv ID 唯一 author-year mapping
4. **D2 的 precondition sanity 是 "silent fail"**：22-investigation corpus 是 framing but disk 上无 schema 证据；feature (a)+(b) pre-conditions (projection round-trip, multi-outcome vector) 在 AR side 数学不成立。若 framework 实际无 vector-carrying 字段则在 feature 层 fail；若 framework 有但未在 corpus 子集中则应 reframe 数据子集
5. **项目 disposition 与 4 drafts 一致**：TOP-JOURNAL KILL verdict from 2026-07-06 仍成立——D2/D3/D4 都没突破 G3 ceiling, 都停在 ACL/EMNLP Findings。Joint paper 的 "main-track possible if placeholders resolve" 是 pure speculation, 不是事实
6. **D17 rule 合规**：D4 自身已遵守 "synthesis not recommendation" discipline; 本 audit 文件同样——是 **盘点 + 建议**, 不强行 trigger 项目 decision rule

---

## 7. 推荐决策（短期，1-2 周可执行）

1. **D1: PARK + request 复算**：在 9/14 = 64.3% 的真值上重写 §3.1 字段映射表；honestly report "92.9% AR-centric lenient counting" + "64.3% strict semantic counting"。同时采用 2026-07-08 后的 5 个 settlement record 替代 N=2 baseline
2. **D2: PARK + request corpus probe**：在 auto-research git tree 中 grep 任何 pre-reversal probability vector 证据（schema spec / sample record）。如不存在则 D2 是 permanently placeholder paper, KILL；如存在则重新 audit feature (a)/(b) 可计算性
3. **D3: PARK + drop as independent paper, fold into D1 as §7 appendix**：§6 H1-H3 hypotheses 是 methodology spec 不是 experiment；append to D1 比独立 D3 论文更 honest
4. **D4: KILL as independent paper**——保留作内部 reference doc；不投 D4-only submission。若 D1+D2 都 fix 之后，仍有 reviewer-side "joint paper" 价值，作 EMNLP Findings 增刊 re-submit
5. **Top-journal KILL 仍成立**（per cross-project-roi 2026-07-06 §七）；不动摇；auto-research 自身不投稿顶刊主 track
6. **Direction K（cross-project methodology validation paper）从跨项目 ROI 评估已知**：是 G3 + Tsinghua 协同的副产品，仅作 G3 methods paper 的扩展，不另起；Tsinghua 论文本身 ceiling = SCI Q1，加方法论层 = ACL/EMNLP Findings

---

## 8. 局限性声明

1. **本 audit 不读 3 项目（Policysim-v0.2 / cds4polymarket / policysim-research-Tsinghua）完整 state**：w1/w3 由并行 agent 写；本文件仅服务于 auto-research 端 4 draft 的内部 audit
2. **arXiv 真伪 verification 是 partial**：cross-assignment 的 inconsistent metadata 我只点 3 个 ID（2607.01661, 2607.09921, 2604.25850），没全部扫；若读 D1/D2/D3/D4 全文所有 arXiv ID 数量大于 10，inconsistency 可能更多
3. **本 audit 没 run g3_crosswalk.py**：script 在 disk 上找不到（0 搜索结果），所以 schema bridge 复算是基于已存 .md/.json。"real measured 64.3%" 来自 cross-project-roi §(E) 的 prior analysis, 我未独立复算；但 64.3% 的来源（7 UNIQUE TO AR 字段表 + 9 share 字段表）在 crosswalk.md §2 中**实际可 verify**
4. **本 audit 假设 22-investigation corpus 确实在 disk 某处 but not addressable to me**：grep `22-investigation` schema spec 0 hits，但 progress.json 多次 mention。D2 §5 limitation #3 已诚实承认 corpus 存在性是 unimpeachable——我无法独立 verify, 但 audit 结论不依赖于此：因为 (a) feature 在 AR side 数学无定义 与 (b) 7 AR-only 字段信息 loss 已足以 KILL D2 不可计算性，与 corpus 是否存在无关
5. **w1/w3 平行 agent 的产出我没读**：本 audit 不与 w1/w3 concurrent 互动；用户决策时建议同时读 3 个 w files 做 cross-check
6. **5-persona review scores (Bohr/Dirac/Feynman/Mendel/Curie) 都不出自真正 multi-agent task**：本 audit 没触发 5-persona review on 4 drafts，只 self-eval reader's perspective；若项目决意 D2/D3/D4 继续推进，5-persona review (R1+R3 >= 5.5 hard gate, G2/K 触发 closure 标准) 是下一个必走闸门
7. **Direction K (cross-project) 未在本 audit 评估**：范围限制于 auto-research 端 4 draft；Direction K 已在 cross-project-roi 2026-07-06 §五评估（ACL/EMNLP Findings 7.0-7.5，30-40% accept），本 audit 不重评

---

## 9. 交叉引用

- D1 draft：`auto-research/docs/papers-closed-portfolio/directions-attempt-2026-07-18/d1-g3-standalone-paper-draft.md`
- D2 draft：`auto-research/docs/papers-closed-portfolio/directions-attempt-2026-07-18/d2-verdict-reversal-paper-draft.md`
- D2 rescore：`auto-research/docs/papers-closed-portfolio/directions-attempt-2026-07-18/d2-rescore-card.md`
- D3 draft：`auto-research/docs/papers-closed-portfolio/directions-attempt-2026-07-18/d3-g3-with-harness-ablation-draft.md`
- D4 draft：`auto-research/docs/papers-closed-portfolio/directions-attempt-2026-07-18/d4-cross-direction-joint-paper-synthesis.md`
- G3 crosswalk artifact：`auto-research/docs/papers-closed-portfolio/g3-dual-ledger-crosswalk.{md,json}`
- Project history：`auto-research/state/progress.json`
- Cross-project ROI（含 64.3% 实测）：`auto-research/docs/investigations/archive/cross-project-roi-2026-07-06.md`
- post-gate-and-qlib-assessment（含 G3 Brier 真实 data on disk）：`auto-research/docs/investigations/archive/post-gate-and-qlib-assessment-2026-07-05.md`
- cds4worldcup-settlement-experiment-executed（含 2026-07-08 后续 3 settlement records）：`auto-research/docs/investigations/cds4worldcup-settlement-experiment-executed-2026-07-08.md`
- Top-journal KILL verdict (cross-referenced)：`auto-research/docs/investigations/rethink-2026-07-06-zh.md`（progress.json event 引用）
- G3 methods paper outline：`auto-research/docs/papers-closed-portfolio/g3-methods-paper-outline.md`（M10 milestone, 与 D1/D3 内容有部分重叠）
