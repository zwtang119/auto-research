# Downloads 顶层 PDF 扫描报告：不确定性决策相关文献

- 扫描范围：`/Users/tangzw119/Downloads/` 顶层 `*.pdf`（非递归），共 109 个文件
- 方法：pypdf 提取每份 PDF 前 1–2 页文本（>20MB 仅首页）+ PDF metadata；识别标题/作者/主题后人工分类
- 原始提取数据：`first_pages.json`；提取脚本：`extract.py`
- 日期：2026-07-21

## A. 直接相关（1 个）

1. **THE RECOGNIZED INFORMATION PICTURE FOR DISTRIBUTED MARITIME OPERATIONS (1).pdf**
   - 标题：The Recognized Information Picture for Distributed Maritime Operations
   - 作者/机构：Jeffrey P. Elliott，美国海军研究生院（Naval Postgraduate School, Monterey）硕士学位论文，2025-03，NPS Calhoun 存档（hdl.handle.net/10945/73644），美国政府作品
   - 关联点：研究如何为分布式海上作战（DMO）构建"公认信息图景"（RIP）——把多源、不完整、含噪声的传感器与情报信息融合成统一作战图景，直接服务于信息不全/不确定条件下的海上指挥决策。是本批 109 个文件中唯一以"信息不全下的作战决策支撑"为核心命题的外部文献（严格说是信息融合→决策支撑，故亦可视为 B 组之首）。

## B. 间接相关（8 个）

1. **DISTRIBUTED MARITIME OPERATIONS AND UNMANNED SYSTEMS TACTICAL EMPLOYMENT.pdf**
   - NPS 系统工程 Capstone 报告，Christopher H. Popa、Sydney P. Stone 等约 20 人（含新加坡国防系统人员），Monterey, CA；首页未见年份，199 页
   - 关联点：分布式海上作战与无人系统的战术运用与 C2 决策，含不确定环境下的兵力分配/战术选择问题。
2. **Mapping China's Strategic Space.pdf**
   - Nadège Rolland，NBR（The National Bureau of Asian Research）报告，96 页；首页未标注年份
   - 关联点：战略/情报分析，基于公开信号推断大国战略意图——典型的信息不全下的判断活动。
3. **Tree-of-Thoughts.pdf**
   - Shunyu Yao（Princeton）、Dian Yu、Jeffrey Zhao、Thomas L. Griffiths、Yuan Cao、Karthik Narasimhan 等（Princeton + Google DeepMind）
   - 关联点：把问题求解建模为思维树上的搜索与"深思熟虑决策"，摘要明确指出要突破 LM 推理中 token 级从左到右的 decision-making 局限；与多路径不确定性下的选择直接相关。
4. **Graph of Thoughts- Solving Elaborate Problems with Large Language Models.pdf**
   - Maciej Besta、Nils Blach、Torsten Hoefler 等（ETH Zurich 等）
   - 关联点：ToT 的图结构推广，对推理路径的建模与选择。
5. **self_play_survey.pdf**
   - Deli Chen，《Self-Play in the Age of Foundation Models: A Comprehensive Survey》，75 页
   - 关联点：博弈论基础（含不完美信息博弈）与自我对弈训练，是"对抗性不确定下决策"的方法论谱系综述。
6. **frai-08-1593017.pdf**
   - Cristian Jimenez-Romero、Alper Yegenoglu、Christian Blum，《Multi-agent systems powered by large language models: applications in swarm intelligence》，Frontiers in Artificial Intelligence 8:1593017，2025-05
   - 关联点：LLM 多智能体群体智能应用于仿真与集体决策。
7. **2506.14496v2.pdf**
   - Muhammad Atta Ur Rahman、Melanie Schranz、Samira Hayat（Lakeside Labs, Austria），《LLM-Powered Swarms: A New Frontier or a Conceptual Stretch?》
   - 关联点：LLM 群体系统协调/集体行为的概念审视。
8. **ChandimaMaduwantha.pdf**
   - Chandima Maduwantha（University of Kelaniya, Sri Lanka），《Swarm Intelligence in Multi-Agent Systems: Recent Advances and Applications》
   - 关联点：多智能体系统中的群体智能综述，涉及去中心化协调决策。

## C. 明显无关大类（100 个）

1. **用户自有 CDS 项目材料（16 个）**：CDS-BP-0721、Copy-of-10-Slides-to-Win-Investors（含副本）、CDS_Strategic_Decision_Infrastructure_(2)、Computational_Decision_Infrastructure、Computational_Decision_Space、计算决策空间（CDS）深度解析、基于计算决策空间（CDS）的认知型政策仿真系统研究、面向安全决策的计算决策空间建模与多智能体博弈推演方法研究、PolicySim_Cognitive_Emergence、Generative_Emergency_Decision_Intelligence_(4)、CDS_学术讨论_v2、涉密行业认知方法论、台海局势知识闭环分析报告、🔒四象飞轮·台海涉密认知闭环分析、商业航天政策动态仿真与决策支撑系统。
   - 注：主题上正是"深层不确定性下的重大决策"，但属用户自己的项目产出而非外部文献。
2. **CDS 仿真推演输出报告（16 个）**：AI 监管法案 ×2、特朗普关税 ×3、WTI 油价 ×3（prompt-optimized ×2 + exp-C）、美伊停火、美国对伊军事打击、高油价 7 分钟打击窗口、商业航天政策动力学评估 ×4（行动计划 ×2、武汉、湖北）。
3. **世界杯主题（4 个）**：2026_World_Cup_White_Paper、世界杯实验论文框架 ×2、Kimi 因子池动态校准基础方案。
4. **用户研究/项目文档（10 个）**：应急决策策略锦标赛开题报告 + 论文选题 ×2、国家重点研发任务书 20.3、应急管理智能决策知识库 ×2、项目简介 ×2、海关绩效评价、清华 Polaris vs JHU GenWar 对比简报。
5. **课程/经典教材（20 个）**：灾害模拟与仿真 2025 秋课件 9 个、钱学森工程控制论/控制论相关 4 个、系统思维与系统工程、课程论文（唐志伟 ×2、ALPT、ZRJ、詹晓玲）、10x Team Fellowship 申请。
6. **AI 行业材料（8 个）**：AI 能力谱系 ×4、自治研究系统分类框架、追问 1、AI 研究院技术报告、普通人 AI 自学指北。
7. **商业/事务文档（17 个）**：OPC 社区 ×3、国家数据集团具身智能 ×4、种子轮 BPV3、PMO 物理安全、知识库接口、信息采集确认函、Pending Invoice、胜软科技 IPO 问询回复（442 页财报类）、AINative 创始人手册、Startup Skill Architect、ByteDance 动画脚本、Microsoft agentic SOC 白皮书。
8. **其他主题英文论文（9 个）**：Nature 中国风光互补、联邦学习 MLLM 部署（Computer Communications）、Nucleotide Transformer（Nature Methods）、TranscriptFormer（Science）、TreeReview、MEMO、AsyncThink（2510.26658）、Least-to-Most Prompting、Towards a Science of Scaling Agent Systems。

## 无法读取/判断

- 无损坏文件（109/109 均可打开）。
- 纯图像 PDF（无文本层，按文件名归类，未做 OCR）：CDS_Strategic_Decision_Infrastructure_(2)、Computational_Decision_Infrastructure、Computational_Decision_Space、Generative_Emergency_Decision_Intelligence_(4)、PolicySim_Cognitive_Emergence、信息采集分析系统确认函、系统思维与系统工程0411（CamScanner 扫描件）、钱学森与控制论、[控制论] 工程控制论两册（仅提取到 pdfFactory 水印）。
- 重复副本（内容相同的 "(1)" 文件）已并入各大类计数。
