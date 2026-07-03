## Goal
将 Deli AutoResearch 的框架协议和论文写作 skill group 安装为本项目的 Mimo Code skills。
完成后写入 .mimo/skills/ 目录，并在控制台输出 "Skills installed: ✓ deli-autoresearch-framework ✓ paper-writing-skill-group"。

## 工作方式

### Step 1: 读取源材料
读以下两个 HTML 文件（它们是完整的技能文档，用英文+中文编写）：
- `/Users/tangzw119/Documents/GitHub/0ref/skill/victorchen96.github.io/auto_research/framework.html`
- `/Users/tangzw119/Documents/GitHub/0ref/skill/victorchen96.github.io/auto_research/skill/paper-writing.html`

### Step 2: 创建 Skill #1 — deli-autoresearch-framework
从 framework.html 中提取以下内容，写入 `.mimo/skills/deli-autoresearch-framework/SKILL.md`：

必须包含：
- **状态文件协议**: state/ 目录下所有文件的格式和作用（task_spec.md, progress.json, findings.jsonl, directions_tried.json, iteration_log.jsonl）
- **停滞检测规则**: stale_count ≥ 2 → pivot 换策略, ≥ 4 → 标记人工
- **心跳看门狗**: L0/L1/L2 三层机制
- **子 Agent 调度模式**: Pattern A(目标驱动), B(并行探索), C(实验执行), D(验证)
- **工程约束**: 每轮最多 5 个大文件, 单文件 ≤300 行, 状态通过文件传递而非对话记忆, 每 20 条引文验证一次, 优先多样性而非深度
- **日志规范**: logs/ 下三种 jsonl（work/orchestrator/heartbeat）的写入时机和格式

### Step 3: 创建 Skill #2 — paper-writing-skill-group
从 paper-writing.html 中提取以下内容，写入 `.mimo/skills/paper-writing-skill-group/SKILL.md`：

必须包含：
- **5 个子技能**: Literature Survey, Paper Structure & Logic, Experiment Design, Academic Figures & Tables, Peer Review Simulation
- **Phase 路由**: Phase 0(Topic) → Phase 1(Draft, iter 1-6, target 6.0) → Phase 2(Deep Improvement, iter 7-9, target 7.5-8.0) → Phase 3(Sprint, iter 10+, target 8.5+)
- **4 个 Quality Gate**: Gate 1(Literature: ≥80 refs, within-1yr≥40%, arXiv≤60%) / Gate 2(Experiment: hypothesis+stat test+≥3 trials) / Gate 3(Structure: 0 compile errors, ≤300 lines/file, abstract-conclusion aligned) / Gate 4(Figures: ≥10 tables+≥6 figures, booktabs) / Gate 5(Final Review: blocking)
- **Peer Review 协议**: 5 个 reviewer persona（R1 实验者/R2 理论者/R3 完美主义者/R4 综合者/R5 新人），各自评分权重
- **反通胀规则**: 首轮评分上限 7.0, 每轮最大 +1.5, 至少保留 1 个未解决弱项
- **弱项路由表**: 每个 reviewer 发现的弱项路由到哪个子技能修复
- **文献四阶段漏斗**: Recall(关键词搜索)→Score(LQS 5维打分)→Classify(A/B/C/D引用深度)→Upgrade(arXiv→accepted, 交叉验证 DBLP)
- **图表标准**: booktabs 三线表, 无竖线, 实验数据 mean±std, 标题包含结论而非仅描述
- **评分轨迹**: 6.0(workshop)→7.0(main conf)→8.0(Strong Accept)→8.5(top)

### Step 4: 验证
- 确保两个 SKILL.md 均可读、结构清晰
- 确认 Mimo Code 能通过 skill 系统加载它们
- 输出安装确认信息

## 关键约束
- 从 HTML 中提取的是**规则和标准**，不是 HTML 标签。转换后的 SKILL.md 必须用 纯 Markdown
- 保留原文中的所有数值阈值（≥80 refs, within-1yr≥40%, stale_count≥2 等）——这些是硬约束，不可改写
- Skill 文件路径必须匹配 Mimo Code 的 skill 发现机制（`.mimo/skills/<skill-name>/SKILL.md`）
- 不要遗漏 framework.html 中的工程约束和子 Agent 调度模式
