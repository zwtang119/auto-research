You are a literature-search specialist. I am preparing a top-journal method paper on a Unified Anchoring-Bias Taxonomy for LLM-as-a-Judge, grounded in Tversky-Kahneman anchoring-and-adjustment theory. The taxonomy will map:
  - "leaked ground truth → stricter scoring" (observed in our P12 calibration-paradox project) onto the CONTRAST anchoring effect.
  - "score-tagged reference answer → lenient scoring" (Li et al. 2026, arXiv:2506.22316) onto the ASSIMILATION anchoring effect.
  - Other anchors (confidence-cue, format-cue, etc.) onto other Tversky-Kahneman effects (adjustment, priming).

The 3 LLM-as-a-Judge surveys have been checked and DO NOT use anchoring/contrast/assimilation/prospect-theory framing as a formal cognitive-bias taxonomy. Gu et al. 2024 (arXiv:2411.15594) explicitly calls for a "more formal theoretical framework" and "unified and comprehensive benchmark" — but no method paper has yet been checked.

I need a focused check on **8 specific method papers** that may have used anchoring/contrast/assimilation/prospect-theory framing for LLM-judge bias WITHOUT it being picked up by the surveys. For each, return YES/NO/MARGINAL on:
  (a) Does it use anchoring/contrast/assimilation/prospect-theory framing?
  (b) Does it frame LLM-judge bias as a unified cognitive bias taxonomy?
  (c) Does it name "leaked ground truth" or "leakage bias" as a dedicated bias category?
  (d) Does it name "score-tagged reference" as a bias source?

# The 8 method papers (sorted by relevance to anchoring-bias framing)

1. **KIEval** — arXiv:2402.15043 (2024). Iterative Key-knowledge Evaluation; addresses leakage-adjacent issues via dynamic key-knowledge extraction.
2. **OffsetBias** — EMNLP Findings 2024. Debiasing via curated data; covers multiple bias types.
3. **CALM** — NeurIPS Safe GenAI Workshop 2024. Catalogues 12 LLM-judge biases.
4. **JudgeDeceiver** — arXiv 2024. Prompt-injection attack on judges.
5. **Auto-J** — arXiv:2308.15024 (2023). Automated judge with bias analysis.
6. **CRITIC** — arXiv:2305.17138 (2023). Self-critique framework.
7. **JudgeLM** — arXiv:2310.17654 (2023). Fine-tuned judge models.
8. **Prometheus / Prometheus-2** — arXiv 2024. Fine-tuned evaluator; bias discussion.

# Output format

For each paper, return a JSON object with these fields:

{
  "paper": "<short name>",
  "arxiv_or_venue": "<id>",
  "answer_a_anchoring_framing": "YES|NO|MARGINAL — <1-sentence evidence + verbatim quote if YES/MARGINAL>",
  "answer_b_unified_taxonomy": "YES|NO|MARGINAL — <1-sentence evidence>",
  "answer_c_leakage_as_bias": "YES|NO|MARGINAL — <1-sentence evidence>",
  "answer_d_score_tagged_ref": "YES|NO|MARGINAL — <1-sentence evidence>",
  "threat_to_direction_A": "HIGH|MEDIUM|LOW|NONE — <1 sentence>",
  "verbatim_quote_or_null": "<short verbatim quote, or null>",
  "url": "<canonical arxiv or venue URL>"
}

Return the 8 results as a single JSON array. Use Google + arXiv + Semantic Scholar. If a paper cannot be located, set threat_to_direction_A = "NONE", all answers = "NO", and verbatim_quote_or_null = "<paper not found by standard search>".

# Context: this is the LAST layer of the novelty depth-check before writing the proposal.

If ANY paper answers YES or MARGINAL on (a) or (b), flag it for explicit differentiation in the related-work section. If ALL answer NO on (a)+(b) and the taxonomy is genuinely novel, confirm that direction A can proceed to the proposal stage without further literature search.

Be honest: do NOT fabricate quotes. If you cannot find a verbatim quote, say so. Prefer returning "NO" with a specific reason over hallucinating a YES.

# Survey references (already checked, do not re-check)
- Gu, J. et al. 2024. "A Survey on LLM-as-a-Judge." arXiv:2411.15594. https://arxiv.org/abs/2411.15594
- Li, D. et al. 2024. "From Generation to Judgment." arXiv:2411.16594. https://arxiv.org/abs/2411.16594
- Li, H. et al. 2024. "LLMs-as-Judges: A Comprehensive Survey." arXiv:2412.05579. https://arxiv.org/html/2412.05579v2
- Li et al. 2026. "Evaluating Scoring Bias in LLM-as-a-Judge." arXiv:2506.22316. https://arxiv.org/abs/2506.22316 (the score-tagged-reference → lenient prior art that maps onto ASSIMILATION in our taxonomy)
