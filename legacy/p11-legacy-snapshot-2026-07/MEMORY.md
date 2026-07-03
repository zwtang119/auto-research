# AutoResearch 实验约束

- 代码源只读，不修改 PolicySim / cds-keyperson / cds4polymarket 的任何源码
- 所有输出写在本实验目录内
- 遇到无法解决的阻塞，写到 state/blocked.md，不要中断等待人工

## P1.1 Inner Monologue Experiment

**M1 Completed**: Created 3 scripts for the experiment:
1. `scripts/inner_monologue_experiment.py` - Main experiment runner with 3 modes
2. `scripts/llm_judge_scoring.py` - LLM Judge for RoleDNA fidelity and emergent realism
3. `scripts/statistical_analysis.py` - Statistical hypothesis testing (H1-H4)

**Key Design Decisions**:
- Mode B (inner_monologue) uses character-immersed `<think>` tags with role-specific instructions
- Mode C (pure_analysis) uses logical analysis `<think>` tags without role immersion
- Control instructions are appended to the first-round user message
- Uses existing PolicySim api_client.py for model calls (read-only)
- Anti-template Jaccard check prevents repetitive outputs

**Dependencies**:
- PolicySim MC engine at `/Users/tangzw119/Documents/GitHub/policysim-research-Tsinghua/`
- DeepSeek-V4-Pro model via Paratera API
- scipy for statistical tests

**Next Steps**:
- M2: Run 3-mode × 50-run experiment (150 total runs)
- M3: LLM Judge auto-scoring
- M4: Statistical analysis + paper writing
