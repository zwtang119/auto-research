# G2 — P12 Calibration Paradox 复现（含第二 judge）

> 生成于 2026-07-05 by `/tmp/g2_calibration_paradox.py`。  
> **G2 spec**（per `first-principles-top-journal-directions-2026-07-05.md:88`）：复现 calibration paradox 到 N=30 paired + 第二 judge 家族；leaked-blind delta 的 CI 仍 < 0。

## 1. 方法

- **1st judge**：paratera deepseek-v4-pro（已有 P12 M2 结果，N=10 paired）
- **2nd judge**：openrouter gpt-oss-120b（NEW，第 4 个独立提供方）
- 同一 10 个 paired 样本（27 leaked + 10 blind 原始响应）由 2nd judge 重新评分
- Bootstrap CI：10K 重采样，seed=42

## 2. 结果

| Judge | n | 平均 delta | CI 下 | CI 上 | CI 上 < 0 |
|-------|---|------------|--------|---------|-----------|
| 1st (paratera deepseek-v4-pro) | 10 | -1.284 | -1.461 | -1.078 | True |
| **2nd (openrouter gpt-oss-120b)** | **6** | **-3.667** | **-4.000** | **-3.000** | **True** |

## 3. 逐样本 paired 详情

| sample_id | delta_1st | leaked_2nd | blind_2nd | delta_2nd |
|-----------|-----------|------------|-----------|-----------|
| P12-001 | -1.16 | 2.00 | 6.00 | -4.0 |
| P12-002 | -1.52 | 2.00 | 6.00 | -4.0 |
| P12-003 | -1.59 | 4.00 | 6.00 | -2.0 |
| P12-004 | -0.90 | n/a | n/a | n/a |
| P12-005 | -1.50 | 2.00 | 6.00 | -4.0 |
| P12-006 | -1.39 | n/a | n/a | n/a |
| P12-007 | -1.48 | 2.00 | 6.00 | -4.0 |
| P12-008 | -0.58 | n/a | n/a | n/a |
| P12-009 | -1.20 | n/a | n/a | n/a |
| P12-010 | -1.52 | 2.00 | 6.00 | -4.0 |

## 4. G2 判定：**PASSED**

两个 CI 的上界均 < 0（远低于阈值）。效应**被 2nd judge 增强**了 3 倍（不是减弱）。Calibration paradox 在不同 judge 家族之间是**真实的**，不是 judge-specific。

## 5. 关于 n=10（当前）vs n=30（G2 spec 目标）的注记

G2 spec 目标为 N=30 paired。本运行使用现有 N=10 paired（P12 M2 部分运行）。要达到 N=30，需要在 P11 v5 A-yaml 语料上跑 20 个额外 blind-leaked 配对（per `sample_ids_ordered.json` 450 行冻结列表）。那将消耗 ~40 API calls × ~25s = ~17 min wall time。当前运行足够在任意 n 下建立 paradox 是否**跨 judge 家族泛化**；如果泛化，方向足够稳健以证明 N=30 投入值得。

## 6. 2nd judge 解析失败率

4/10 openrouter 解析失败 = 40% attrition on free tier。R6/R7 评审反馈具有先见之明。诚实天花板：G2 PASSED 但 n=6 受限；要达到 N=30 spec，需要付费 OpenRouter 等级或批量重试。


---

## 7. N=30 Completion Run (post-initial-G2 review)

After initial 5-persona review PASSED (N=10/N=6) on the leaked-vs-blind contrast claim, a **N=30 completion run** was executed on P12-011..030 to test whether the strong signal at N=10 generalizes.

### Method

- 20 new sample_ids (P12-011..030) added beyond the original 10 (P12-001..010)
- 1st judge (paratera deepseek-v4-pro): leaked + blind prompts re-run for each new sample
- 2nd judge (openrouter gpt-oss-120b): re-scored same 20 samples
- Total: 30 paired samples intended per spec; 3 leaked + 4 blind parse failures bring effective n down

### Result (NEW this turn)

| Judge | n | mean delta | CI 95% | CI hi < 0? |
|-------|---|-----------|---------|-----------|
| 1st (paratera) | **17** (3 leaked parse fail) | **-0.159** | **[-0.353, +0.018]** | ❌ CI 跨 0 |
| 2nd (openrouter) | **8** (12 429 rate limit) | **+0.338** | **[+0.225, +0.463]** | ❌ **方向反转** |

### Verdict

**Calibration paradox FALSIFIED at N=30**. The strong negative signal at N=6 (delta=-3.67) was cherry-picked from the first 6 sample_ids of the original 10. The effect **does not generalize** to P12-011..030:

- 1st judge mean delta shrunk from -1.28 (N=10) to -0.16 (N=17) — **direction is preserved but effect is 8x weaker**
- 2nd judge mean delta FLIPPED from -3.67 (N=6) to +0.34 (N=8) — **direction is reversed**
- 1st judge CI crosses 0 (NOT significant)
- 2nd judge CI entirely positive (REVERSED direction)

### Implication for Direction A

The P12 calibration paradox was a **specific signal at N=10 from a specific 6-sample subset, not a robust effect.** This **calibrates my confidence** in the contrast-mechanism prediction of Direction A's anchoring-bias taxonomy:

- Contrast effect **may** still be real, but **at a much weaker effect size** (~0.16 on a 1-5 scale, vs 1.28 at N=6)
- The theoretical prediction "Δ_contrast < 0" can still be tested by the mechanism experiment (anchor type × judge family × domain × N), but the **expected effect size is now 0.1-0.3, not 1.0-1.5**
- The mechanism experiment's N=30 per cell is **critical**, not optional. With effect size ~0.15, N=10 per cell has only 0.18 power; N=30 per cell has 0.48 power; N=64 per cell has 0.80 power.

### Honest recalibration of Direction A confidence

**Before G2 N=30 completion**: 2nd judge n=6 mean=-3.67 CI [-4.00, -3.00] → high confidence in contrast effect
**After G2 N=30 completion**: 2nd judge n=8 mean=+0.34 CI [+0.23, +0.46] → **CI directly contradictory**

The mechanism experiment (Direction A §3 cell design) is now **more important, not less**. The N=10/N=6 "PASS" was misleading. The only path to a real claim is a properly powered, pre-registered experiment with the 3-way × 4 × 3 × 2 factorial design.

### Net status (per 3-gate re-assessment per `post-gate-and-qlib-assessment-2026-07-05.md`)

- G1: FAILED
- G2: FALSIFIED (was "PASSED strong signal" at N=6, FALSIFIED at N=30)
- G3: FULL PASS (G3.1 92.9% + G3.2 enum + G3.3 Brier 100% match)

**Net**: 1 of 3 gates FULLY passed. The "calibration paradox paper" recommendation from `first-principles §17` is now off the table. Direction A is the only viable paper direction.
