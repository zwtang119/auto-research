# Novelty Depth-Check: Direction A (Unified Anchoring-Bias Taxonomy for LLM Judges)

Date: 2026-07-05 (evening)
Source: User-run Google deep search → pasted results
Impacts: `docs/investigations/top-journal-verdict-2026-07-05-zh.md` §四/§五/§七

---

## Candidate Direction (being checked for novelty)

**Unified anchoring-bias taxonomy for LLM-as-a-judge**, grounded in Tversky-Kahneman anchoring-and-adjustment theory:
- Maps "leaked ground truth → stricter scoring" (G2 in this project) onto **CONTRAST effect**
- Maps "score-tagged reference answer → lenient scoring" (Li et al. 2026, arXiv:2506.22316) onto **ASSIMILATION effect**
- Validated by a mechanism experiment varying **anchor type × judge family × domain**

---

## Check 1: Three LLM-as-a-Judge Surveys

### 1A. Gu et al. 2024 — "A Survey on LLM-as-a-Judge"
- arXiv: **2411.15594** (2024); journal-published in *The Innovation* (2026)
- Authors: Jiawei Gu, Xuhui Jiang, Zhichao Shi, Hexiang Tan, Xuehao Zhai, Chengjin Xu, Wei Li, Yinghan Shen, Shengjie Ma, Honghao Liu, Saizhuo Wang, Kun Zhang, Zhouchi Lin, Bowen Zhang, Lionel Ni, Wen Gao, Yuanzhuo Wang, Jian Guo
- Taxonomy: **task-agnostic vs judgment-specific** biases; bias inventory = position, verbosity, self-enhancement, diversity, cultural, concreteness, sentiment
- Uses anchoring/contrast/assimilation/prospect-theory terms? **NO**
- Mentions "leaked ground truth" or "leakage bias" as a named bias type? **NO**
- **Critical gap statement (verbatim, from survey's future work)**: calls for **"a more formal theoretical framework"** and says the field **lacks a solid theoretical foundation**; also calls for a **"unified and comprehensive benchmark"** to quantify biases, but not a unified cognitive-bias taxonomy.
- Verdict: **ADJACENT BUT NOT PRE-EMPTING** — explicitly leaves the door open for a cognitive-bias framework. **This is the ideal novelty anchor for Direction A's related-work section.**

### 1B. Li et al. 2024 — "From Generation to Judgment: Opportunities and Challenges of LLM-as-a-judge"
- arXiv: **2411.16594** (2024); EMNLP 2025
- Authors: Dawei Li, Bohan Jiang, Liangjie Huang, Alimohammad Beigi, Chengshuai Zhao, Zhen Tan, Amrita Bhattacharjee, Yuxuan Jiang, Canyu Chen, Tianhao Wu, Kai Shu, Lu Cheng, Huan Liu
- Taxonomy: **what to judge / how to judge / how to benchmark**; biases framed as position/verbosity/self-enhancement
- Uses anchoring/contrast/assimilation/prospect-theory terms? **NO**
- Mentions "leaked ground truth" or "leakage bias"? **NO**
- Future-work closest statement: future work should focus on **"analyzing and understanding the root causes of these biases"** — does NOT call for a unified cognitive-bias framework.
- Verdict: **ADJACENT BUT NOT PRE-EMPTING**

### 1C. Li et al. 2024 — "LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods"
- arXiv: **2412.05579** (2024)
- Authors: Haitao Li, Qian Dong, Junjie Chen, Huixue Su, Yujia Zhou, Qingyao Ai, Ziyi Ye, Yiqun Liu
- Taxonomy: Functionality / Methodology / Applications / Meta-evaluation / Limitations; **contains a "Cognitive-Related Biases" subsection** (closest to target)
- "Cognitive-Related Biases" actual items: **overconfidence, self-enhancement, refinement-aware, distraction, fallacy-oversight** — **NOT anchoring/contrast/assimilation**
- Uses anchoring/contrast/assimilation/prospect-theory terms? **NO**
- Mentions "leaked ground truth" or "leakage bias" as a dedicated category? **NO** — only mentions "data leakage and evaluation bias" in the context of KIEval and related evaluation setups, as a problem those methods help address, **not as a dedicated bias category**
- Future work: organized around more efficient/effective/reliable LLM judges, **not a unified cognitive-bias framework**
- Verdict: **CLOSEST PRIOR ART, BUT NOT PRE-EMPTING** — has a "Cognitive-Related Biases" bucket but the actual items are different. This is the survey a reviewer would cite as "closest"; Direction A must differentiate explicitly from this bucket.

### Survey check synthesis
- All 3 surveys: **none frames LLM-judge bias in anchoring/contrast/assimilation terms as a formal cognitive-bias taxonomy**
- Gu et al. explicitly asks for a formal theoretical framework → **strongest novelty support**
- Li et al. 2024 (2412.05579) has a "Cognitive-Related Biases" bucket with different items → **must differentiate in related work**
- Leakage-as-distinct-bias is also a gap (only mentioned as a problem KIEval addresses, not a named bias category)

---

## Check 2: CoBBLEr (Koo et al., arXiv:2309.17012, 2023) — **REVISED VERDICT**

### **CORRECTION (2026-07-05 晚 — 8-paper method-layer search surfaced this paper)**

- **CoBBLEr IS real**, but was **misidentified** by the morning explore agent on three points:
  1. **Spelling**: "CoBBLEr" (camelcase = **Co**gnitive **B**ias **B**enchmark for **L**LMs as **E**valuato**r**s) — not "COBBLER"
  2. **Venue**: arXiv preprint (Sep 2023) with v3 Sep 2024 — **NOT ACL 2024**
  3. **Authors**: Koo, Lee, Raheja, Park, Kim, Kang (Univ. of Minnesota) — confirmed via citation in Wang et al. 2025 (arXiv:2504.09946 §2: "Koo et al., 2023")

- **Canonical reference**: arXiv:2309.17012 (2023), DOI 10.48550/arXiv.2309.17012, project page `https://minnesotanlp.github.io/cobbler/`

### Paper content
- Measures **6 cognitive biases** in LLM-as-evaluator: Egocentric, Position, Bandwagon, Authority, Sentiment, Confusion (per abstract & project page)
- Empirical finding: "average of 40% of comparisons across all models" exhibit bias
- Correlation with human preferences: RBO = 49.6% (misaligned)
- 15 LLMs evaluated across 4 size ranges

### Threat assessment (REVISED)
- **Threat level: MEDIUM (upgraded from LOW)** — CoBBLEr IS the closest prior art on "cognitive-bias taxonomy for LLM-as-judge", which is exactly what Direction A proposes. A reviewer WILL cite it.
- **BUT**: Direction A still has 3 concrete differentiators from CoBBLEr:
  1. **Theoretical grounding**: Direction A is anchored in **Tversky-Kahneman (1974) anchoring-and-adjustment theory** as the unifying mechanism. CoBBLEr enumerates 6 cognitive biases descriptively but does NOT propose a unifying theoretical lens.
  2. **Mechanism experiment design**: Direction A varies anchor type × judge family × domain to **test specific falsifiable predictions** (Δ_contrast < 0, Δ_assimilation > 0, signs opposite). CoBBLEr measures bias prevalence, not mechanism.
  3. **Specific anchor types**: Direction A focuses on **anchor-based** biases (leaked GT → contrast; score-tagged ref → assimilation); CoBBLEr's 6 biases do NOT include either leaked-GT or score-tagged-ref as a named bias.

### Verdict (REVISED)
- CoBBLEr **partially pre-empts** Direction A's general claim of "cognitive-bias framework novelty" — but **does NOT pre-empt** the specific anchoring-and-adjustment mechanism or the predicted sign asymmetry (Δ_contrast vs Δ_assimilation).
- **Required action**: add CoBBLEr to Direction A's related-work section as **closest prior art** with explicit 3-axis differentiation (theory / mechanism / anchor types). Do NOT pretend CoBBLEr doesn't exist — it does, and any reviewer who does a 30-second search will find it.

---

## Check 3: Method-paper layer (8 papers — COMPLETED 2026-07-05 晚)

All 8 method papers queried via Exa + arXiv + Semantic Scholar + project pages. Each scored YES/NO/MARGINAL on 4 dimensions per `docs/papers/method-paper-depth-check-prompt.md`.

### 8-paper summary table

| # | Paper | arXiv/Venue | Anchoring framing? | Unified taxonomy? | Leakage-as-bias? | Score-tagged-ref? | Threat to Direction A |
|---|---|---|---|---|---|---|---|
| 1 | **KIEval** | arXiv:2402.15043 (ACL 2024) | NO — focuses on data contamination / dynamic evaluation | NO — no bias taxonomy proposed | NO — addresses contamination differently | NO | LOW — different problem |
| 2 | **OffsetBias** | EMNLP Findings 2024 (arXiv:2407.06551) | NO — 6 bias types listed descriptively (length, position, etc.) | NO — no unifying framework | NO | NO | LOW — descriptive taxonomy only |
| 3 | **CALM** | arXiv:2410.02736 ("Justice or Prejudice?") | NO — 12 bias types listed, all named differently | NO — enumerative, no anchoring lens | NO — "data leakage" mentioned but not as bias category | NO | LOW — closest bias enumeration |
| 4 | **JudgeDeceiver** | arXiv:2403.17710 (DOI 10.1145/3658644.3690291) | NO — adversarial attack paper, position-bias defense only | NO — attack, not taxonomy | NO | NO | LOW — attack framework, not bias taxonomy |
| 5 | **Auto-J** | arXiv:2310.05470 (note: NOT 2308.15024 as originally cited) | NO — generative judge trained on scenario-criteria data | NO — no bias taxonomy | NO | NO | LOW — judge model, not bias theory |
| 6 | **CRITIC** | arXiv:2305.11738 (note: NOT 2305.17138 as originally cited) | NO — tool-interactive self-correction framework | NO | NO | NO | LOW — self-correction, not bias theory |
| 7 | **JudgeLM** | arXiv:2310.17631 (note: NOT 2310.17654) | NO — 3 bias types: position / knowledge / format | NO — descriptive only | NO | NO | LOW — fine-tuned judge + 3 descriptive biases |
| 8 | **Prometheus / Prometheus-2** | arXiv:2405.01535 | NO — focus on direct assessment + pairwise ranking formats | NO — no bias taxonomy proposed | NO | NO | LOW — open-source evaluator model |

### Key findings

1. **NO method paper (0/8) uses anchoring / contrast / assimilation / prospect-theory framing** for LLM-judge bias. Direction A's theoretical lens is genuinely novel at the method-paper level.

2. **Several minor citation errors** in the original prompt file — corrected above:
   - Auto-J: arXiv:2310.05470 (not 2308.15024)
   - CRITIC: arXiv:2305.11738 (not 2305.17138)
   - JudgeLM: arXiv:2310.17631 (not 2310.17654)
   - These ID corrections are bookkeeping only — paper content unchanged.

3. **CALM (Justice or Prejudice?) is the closest method-paper** with 12 named bias types — but they are descriptive (egocentric, position, bandwagon, etc.) and do NOT map onto anchoring theory. Direction A's CONTRAST/ASSIMILATION/ADJUSTMENT framing is genuinely orthogonal.

4. **Combined with Check 2 (CoBBLEr revision)**: CoBBLEr is the closest prior art on the "cognitive-bias taxonomy" axis, but it does NOT use anchoring/contrast/assimilation terms. Direction A's theoretical lens is novel even against CoBBLEr.

### Verdict
- Direction A **proceeds to proposal stage** with full method-paper novelty clearance.
- Related-work section must cite CoBBLEr (Koo et al. arXiv:2309.17012) as closest prior art with 3-axis differentiation (theory / mechanism / anchor types).

---

## Updated Novelty Assessment

| Dimension | Before (2026-07-05 morning) | After (2026-07-05 evening — survey + CoBBLEr) | After (2026-07-05 晚 — 8 method-papers + CoBBLEr revision) |
|---|---|---|---|
| Survey coverage check | 2 surveys checked via WebFetch | 3 surveys checked via Google deep search ✅ | 3 surveys ✅ |
| Theoretical-framework gap | Unconfirmed | Confirmed — Gu et al. explicitly calls for it ✅ | Confirmed ✅ |
| CoBBLEr threat | Unknown (explore agent timed out) | Cannot be located → threat LOW | **REAL (arXiv:2309.17012, 2023)** → threat MEDIUM, requires explicit differentiation ✅ |
| Method-paper coverage (8 papers) | Not done | Still not done | **0/8 use anchoring/contrast/assimilation framing** ✅ |
| Overall novelty verdict | "plausible but not 100% confirmed" | "significantly strengthened, ready for proposal stage" — pending method-paper check | **"novelty confirmed on anchoring-and-adjustment mechanism; CoBBLEr requires explicit differentiation in related work; proposal stage cleared"** ✅ |

---

## Recommendation

1. **Proceed to write the Direction A 1-page proposal** — already drafted at `docs/papers/direction-a-1-page-proposal.md`. **Update required**: add CoBBLEr to related-work with 3-axis differentiation (theory / mechanism / anchor types).
2. **Method-paper check completed** (0/8 use anchoring framing). No method paper pre-empts Direction A's theoretical lens.
3. **CoBBLEr handling**: do NOT delete it from related work. Add explicit citation with the 3-axis differentiator table. This converts a "missed prior art" weakness into "we are aware of and differentiate from" — strictly stronger proposal.
4. **Hard gate before any large-token mechanism experiment**: 5-persona review on the updated proposal (median ≥ 5.5) + frontier baseline arm provisioned + P12 G2 N=30 falsification acknowledged in proposal §6.

---

## Citations

- Gu, J. et al. "A Survey on LLM-as-a-Judge." arXiv:2411.15594 (2024); *The Innovation* (2026). https://arxiv.org/abs/2411.15594
- Li, D. et al. "From Generation to Judgment: Opportunities and Challenges of LLM-as-a-judge." arXiv:2411.16594 (2024); EMNLP 2025. https://arxiv.org/abs/2411.16594
- Li, H. et al. "LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods." arXiv:2412.05579 (2024). https://arxiv.org/html/2412.05579v2
- Li et al. 2026 "Evaluating Scoring Bias in LLM-as-a-Judge" arXiv:2506.22316. https://arxiv.org/abs/2506.22316 (the score-tagged-reference → lenient prior art Direction A maps onto assimilation)
- **Koo, R., Lee, M., Raheja, V., Park, J. I., Kim, Z. M., Kang, D.** "Benchmarking Cognitive Biases in Large Language Models as Evaluators" — **CoBBLEr**: **Co**gnitive **B**ias **B**enchmark for **L**LMs as **E**valuato**r**s. arXiv:2309.17012 (Sep 2023, v3 Sep 2024). https://arxiv.org/abs/2309.17012 — project page https://minnesotanlp.github.io/cobbler/ — **closest prior art; requires explicit differentiation in Direction A related work**
- Yu, Z. et al. "KIEval" arXiv:2402.15043 (ACL 2024) https://arxiv.org/abs/2402.15043
- Park, J. et al. "OffsetBias" arXiv:2407.06551 (EMNLP Findings 2024) https://aclanthology.org/2024.findings-emnlp.57/
- Ye, J. et al. "Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge" (CALM) arXiv:2410.02736 https://arxiv.org/abs/2410.02736
- Shi, J. et al. "JudgeDeceiver" arXiv:2403.17710 https://arxiv.org/abs/2403.17710
- Li, J. et al. "Auto-J" arXiv:2310.05470 https://arxiv.org/abs/2310.05470
- Gou, Z. et al. "CRITIC" arXiv:2305.11738 https://arxiv.org/abs/2305.11738
- Zhu, L. et al. "JudgeLM" arXiv:2310.17631 https://arxiv.org/abs/2310.17631
- Kim, S. et al. "Prometheus 2" arXiv:2405.01535 https://arxiv.org/abs/2405.01535

---

## Cross-references

- Parent report: `docs/investigations/top-journal-verdict-2026-07-05-zh.md` §四/§五/§七
- Pair investigator findings: `docs/investigations/rp-investigate-top-journal-2026-07-05.md`
- LLM-intelligence blocker analysis: `docs/investigations/llm-intelligence-blocker-verdict-2026-07-05-zh.md`
