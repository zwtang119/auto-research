# CDS4WorldCup Homepage Optimization Spec

> **类型**: homepage-design-spec
> **状态**: draft-for-review
> **日期**: 2026-06-11
> **范围**: 主页信息架构、数据展示、交互规格与验收标准；不包含施工实现。
> **约束**: 严格遵守 `docs/source-policy.md`；不读取、复制或发布 `docs/references/**`；不输出投注建议、收益率或仓位建议。

## 1. 背景

当前主页已经完成 v0：它解释了 CDS4WorldCup 的基本定位，提供 48 队路径卡入口，并展示 Plan A/B/C 的阶段状态。

但截至 2026-06-11，项目能力已经明显超过“静态研究门户”：

- 48 队 Team Path Card 全覆盖，21 队 deep-description，27 队 thin-slice。
- 21 张深描卡完成内部审计，全部通过来源边界、结构完整性和可结算性检查。
- 已有 109 条结构化阻力记录，9 类 obstacle type，89 条可结算 Miracle Package 条件。
- 已完成 Kimi 300 Agent 数据门控、直觉锚定、reason 边界处理与 public AI baseline 集成。
- 已完成 Baseline Suite 设计，覆盖 uniform、defending champion、FIFA ranking、Elo、market public baseline、Kimi public AI baseline。
- Plan C Factor Ledger 协议闭环验证通过，prediction card、factor ledger、settlement record 三类 schema 可支持 MVP1 单场预注册闭环。
- 已具备 Python 数据预处理管线，可将 Markdown 路径卡转换成静态 JSON。
- 用户补充：项目已接入 Polymarket API，可调用市场相关数据；公开主页应展示构建期快照，而不是浏览器实时拉取。
- 用户补充：项目可以使用新的长程 agent 工具作为内部数据采集与监控能力，但截至本 spec 修订时尚未投入项目运行，不应在主页展示或暗示已经使用。
- 用户补充：本地已有论文材料 `docs/references/paper/outline.md` 与 `docs/references/paper/abstract-v0.4-cn.md`，可作为内部叙事参考，但不得直接发布敏感目录内容。

主页需要从“项目说明页”升级为“世界杯路径空间研究驾驶舱”：既要让普通访客愿意继续点进去，也要让专业访客快速理解方法论、边界、数据资产和实验可信度。

## 2. 目标

### 2.1 面向人类访客

访客进入首页后的 10 秒内应理解：

1. 这里不直接猜冠军，而是拆开看：每支球队真要夺冠，得过哪些坎。
2. 页面第一步要很明确：先选一支球队，看它的夺冠路。
3. 这是一个认真做的数据项目，但说给球迷听时必须说人话：哪条信息靠谱、哪条只是参考、哪里还缺数据，都要讲清楚。

首页要吸引人浏览的方式不是堆技术名词，而是提供四种自然入口：

- **选球队**：我支持的队想夺冠，得先过哪几关？
- **看难点**：世界杯冠军路上，大家最容易卡在哪？
- **看外界怎么看**：AI 和市场现在怎么想？这些只能当参考，不能当结论。
- **看后续更新**：比赛开始后，哪些判断会被验证，哪些会被打脸？

页面优先级必须是：

```text
先选队 > 看门道 > 信不信由证据说话
```

主页不是一上来讲论文和系统架构，而是先让球迷知道“我该点哪儿”，再慢慢看到数据和方法。

### 2.2 面向项目本身

首页需要传递：

1. CDS4WorldCup 不是“预测榜”，而是把每支球队的夺冠路摊开来看。
2. 项目已经有可运行的数据底座：球队路径卡、对照组、可核验条件、来源分级、静态发布管线、外部市场快照。
3. 市场和 Kimi 只能作为“外界怎么看”的参考，不能当成项目自己的事实依据。
4. 项目价值在于：不只说“我猜谁赢”，而是说“要赢必须发生什么，赛后能不能对账”。
5. 主页应成为普通球迷、研究访客和后续论文/数据发布共同进入项目的门面。

## 3. 参考产品学习

### 3.0 外部评审意见取舍

本 spec 采纳以下方向：

- GitHub Pages 下所有复杂数据清洗应发生在构建期，而不是浏览器端。
- 首页前端只读取预烘焙 JSON，不解析 CSV，不直接请求外部 API。
- Polymarket 等外部信号应通过构建期快照或 GitHub Actions 定时任务进入静态 JSON。
- 首页视觉应优先用零依赖 HTML/CSS 图表，避免为少量柱状图/矩阵引入图表库。
- 首页默认用户路径应前置为“选球队”。
- 外部参照与公开数据快照合并成“外界怎么看”，减少信息过载。

本 spec 拒绝以下方向：

- 不引入 Astro / Next / 其他前端框架作为 v1 前提；当前纯静态 HTML/CSS/JS 足够。
- 不让浏览器直接调用 Polymarket API；避免 CORS、限流、凭证暴露和快照不可复现。
- 不把首页数据拆成过多 JSON 文件；v1 使用 `site/data/homepage.json` 单入口，首页仅放轻量球队小卡。若 payload 后续超过可接受范围，再拆分。
- 不采用 “Epistemic Tension Index” 这类容易显得过度建模的命名；统一使用 `public_consensus_gap`，并明确不是投资信号。
- 不做“所有模块全尺寸展开”的长卷轴；深度内容进入紧凑区块或二级页面。

### 3.1 Polymarket

可借鉴：

- 用“市场卡片”承载复杂事件：标题、概率、成交/活跃度、更新时间，信息密度高。
- 把更新时间、状态变化和事件分类作为入口，让用户感觉页面是活的。
- 事件分类、搜索、榜单式浏览降低进入成本。

不能借鉴：

- 不采用交易、下注、收益、value、PnL、ROI、仓位等表达。
- 不把市场概率包装为事实或行动建议。
- 不把 “market says X%” 放在首屏中心，避免项目被误读为投注或赔率站。

主页借鉴方式：

- 使用“外界怎么看”模块展示市场公开参照的状态、更新时间、数据覆盖率和来源边界。
- 概率只作为外部参考，配套显示“不是投注建议 / 不作为 CDS 事实输入”。
- 所有市场数据必须有 `source_level=Yellow` 或更严格的标记，并记录抓取时间。

### 3.2 Design Arena Leaderboard

可借鉴：

- Leaderboard 本身不是孤立榜单，而是连接了 categories、models、methodology、users。
- 排名页保留方法论入口，让用户知道分数如何产生。
- 用侧边导航 / 顶部导航把“看结果”和“看方法”并列，而不是隐藏方法。

不能借鉴：

- 不做“CDS 排名打败 Kimi/市场”的竞赛叙事。
- 不输出未校准的模型排行榜。

主页借鉴方式：

- 设置“方法和来源 / 外部参照 / 球队路径 / 更新记录”的清晰导航。
- 在每个数据面板旁提供小型方法说明或来源标签。
- 对外部参照做“准备好了没有 / 当前状态”表，而不是胜负榜。

### 3.3 Kimi 300 Agent 页面

可借鉴：

- 首屏有强视觉钩子：300 Agent、热力榜、阵营方阵、滚动 ticker。
- Agent reason 的戏剧性可以吸引非专业访客继续阅读。
- 热力图适合表达 crowd baseline 的集中度与分歧。

不能借鉴：

- 不把 Kimi 300 Agent 作为独立专家群体。
- 不把 Kimi 概率或 reason 直接作为 CDS 事实输入。
- 不在首页制造“AI 已经算出冠军”的误解。
- 不使用“押冠军”“热力榜即结论”或带下注暗示的互动语言。

主页借鉴方式：

- 使用“AI 参考”模块展示 Kimi 覆盖率、主要参考结果、派别信号、缺失状态。
- 明确写出：Kimi 只能参考，不能进入可对账的判断账本。
- Agent reason 可作为二级页面或折叠材料，不应成为首页事实叙述主体。

### 3.4 长程 Agent 工具边界

项目可以在内部评估长程 agent 工具，用于赛事周期的数据采集、状态回写、checkpoint 验证和人工 review queue 准备。

但主页不应展示具体工具品牌、供应商能力、额度信息或“我们使用了某工具”的叙事。原因：

- 该能力尚未投入项目运行，不能被写成既有成果。
- 工具不是 CDS4WorldCup 的研究贡献，公开展示会稀释项目主体。
- 主页目标是解释路径空间、来源纪律和可结算知识，而不是为外部工具做广告。

执行要求：

- 首页可以展示“数据更新状态”“快照时间”“待人工复核队列”等系统状态。
- 首页不得出现具体长程 agent 工具名、供应商名、额度信息或 benchmark 宣称。
- 如需指导项目维护者使用长程 agent 工具，应另写内部指南，不放入公开主页叙事。

## 4. 主页定位

### 4.1 推荐叙事

语言原则：

- 面向访客的标题、按钮、卡片说明必须优先使用中国球迷听得懂的中文。
- 英文术语只允许作为开发字段、数据字段或括号里的补充，不应成为页面主文案。
- 不说“路径空间范畴转换”，要说“不是猜冠军，是看夺冠要过哪些关”。
- 不说“external consensus / public AI baseline”，要说“外界怎么看 / AI 参考 / 市场参考”。
- 不说“settlement”，要说“赛后对账 / 赛后验证”。
- 不说“source boundary”，要说“这条信息能不能当真、能不能进账本”。

首屏主句：

> 48 支球队，每队都有一条夺冠路。

副句：

> 我们不直接猜谁会夺冠。我们想看清楚：一支球队真要捧杯，得过哪些坎，哪些迹象要提前出现，哪些判断赛后能对上账。

备选首屏钩子：

- `如果阿根廷夺冠，世界得变成什么样？`
- `法国要卫冕，最难的几关是哪几关？`
- `你支持的球队，离冠军到底差哪口气？`

首屏指标标签面向访客应使用中文：

- `48 队全覆盖`
- `21 队深度拆解`
- `109 个夺冠难点`
- `89 条可赛后对账`
- `6 组外部参照`
- `公开数据快照`

首屏必须保留大白话边界：

> Kimi 和市场数据只代表“外界怎么看”，不是我们的事实依据，也不是投注建议。

### 4.2 视觉方向

建议采用“赛前战术板 + 研究手记”的混合风格：

- 不是体育博彩站，不使用刺激性赔率 UI。
- 不是论文 PDF，不做大段文字墙。
- 不是传统 BI dashboard，不把首屏塞满图表。
- 需要有“这个项目正在跑”的感觉：状态灯、更新时间、来源标签、球队路径、更新记录。

色彩应避免单一米色/棕色主题继续扩张。保留当前 parchment / ink 的研究质感，但引入少量高对比功能色：

- 可靠事实：深绿
- 待核验线索：琥珀
- 只能参考：暗红
- 数据快照：青色 / 蓝绿
- 已锁定规则：深墨色

## 5. 信息架构

首页应从“系统说明书”改为“球迷能逛得进去的入口”。外部评审里关于“先选球队”、渐进式展开和构建期预计算的建议应采纳；关于排行榜化、博彩化、框架化重构的建议应拒绝。

### 5.1 顶部导航

建议导航项：

- `首页`
- `选球队`
- `看难点`
- `外界怎么看`
- `方法和来源`
- `更新记录`

其中当前阶段只需要保证 `首页` 与 `选球队` 可用；其他可以锚点跳转到首页模块，或在后续页面扩展。

### 5.2 三层页面结构

页面按三层展开：

1. **先让人点进去**：首屏、选球队、当前进度。目标是在 10 秒内让用户知道该点什么。
2. **再给一点门道**：夺冠难点、外界怎么看。目标是给出 1-2 个球迷能记住的数据观察。
3. **最后让人放心**：方法和来源、更新流程、论文/报告、更新记录。目标是解释哪些信息靠谱、怎么赛后对账、项目现在跑到哪一步。

首屏不应同时塞入完整驾驶舱、对照表、论文结构和日志。深度内容可以存在，但必须压缩成折叠、锚点或二级入口。

### 5.3 首页模块顺序

#### Module A: 首屏 / 先把话说明白

目的：在首屏讲明白“这不是猜冠军”，并给出一个具体钩子。

内容：

- 主句：`48 支球队，每队都有一条夺冠路。`
- 副句解释“不是猜冠军，是拆夺冠条件”。
- 可轮换或固定的一句球队钩子：
  - `如果阿根廷夺冠，这个世界必须发生什么？`
  - `法国要卫冕，需要哪些条件同时成立？`
  - `你支持的球队，需要破解哪几个阻力？`
- 主按钮：`选一支球队看看`
- 次按钮：`看看大家最难过哪关`、`我们怎么判断`
- 指标带：球队总数、深度拆解、简版拆解、夺冠难点、可赛后对账条件、外部参照组、数据快照状态。

首屏必须保留大白话边界：

> Kimi 和市场数据只代表“外界怎么看”，不是我们的事实依据，也不是投注建议。

数据来源：

- `site/data/homepage.json`
- 由构建期脚本聚合 `site/data/meta.json`、processed CSV 与外部快照状态。

#### Module B: 选球队

目的：把用户带到最容易探索的 48 队入口。这是首页第一主流程，不应排在驾驶舱之后。

内容：

- 搜索框或精选入口：西班牙、法国、阿根廷、葡萄牙、英格兰、德国、摩洛哥、巴西。
- 每张球队小卡显示：队名、旗帜、所属大洲、深度版/简版、一句话夺冠路、最主要的 2 个难点、资料完整度、进入完整路径卡的链接。
- 推荐增加一个“随机抽一条世界线”轻交互，但只跳转路径卡，不生成新结论。

规则：

- 不按“夺冠概率”排序作为默认排序。
- 推荐默认排序：深度版优先 + 队名排序，或按资料完整度排序。
- 如果展示 Kimi 覆盖状态，只显示“有没有参考数据”，不把 Kimi 概率变成排序主轴。

#### Module C: 当前进度

目的：用球迷能懂的话展示“这个项目已经跑起来了”，替代系统味过重的研究驾驶舱。

推荐布局：一行 4 个紧凑状态卡，desktop 横排，mobile 两列或纵排。

面板：

1. **球队覆盖**：48 队都有路径卡，21 队是深度版，27 队是简版。
2. **夺冠难点**：已经拆出 109 个难点，其中 89 条可以赛后对账。
3. **怎么验账**：每条关键判断都要能说清楚“看什么数据、怎么算兑现”。
4. **外部参考**：Kimi 有部分参考数据；市场数据只展示构建期快照状态。

文案原则：

- 用“这些判断赛后能不能对账”替代 “Factor Ledger schema: pass”。
- 用“公开快照更新时间”替代 “live signal status”，避免静态页误导用户以为浏览器正在实时拉取。
- Kimi=Red、Market=Yellow 必须在卡片内可见。

#### Module D: 夺冠难点

目的：这是首页第一个“真正有料”的数据模块，需要给球迷一个能记住的观察。

推荐可视化：

- HTML/CSS 横向条形图：各类夺冠难点出现多少次。
- HTML/CSS Grid 小矩阵：几个典型球队分别卡在哪些关。
- 一个重点观察卡片：只突出一个数据观察，例如 `最常见的难点不只是实力差距，而是小比分依赖、心理压力、签表强度这些东西叠在一起`。
- 小注释：出现得多，不代表对每队都一样重要。

当前可用数据：

| obstacle_type | count |
|---|---:|
| `low_scoring_dependency` | 18 |
| `psychological_pressure` | 16 |
| `bracket_strength` | 16 |
| `base_strength_gap` | 15 |
| `tactical_mismatch` | 15 |
| `squad_depth` | 14 |
| `injury_risk` | 10 |
| `travel_fatigue` | 3 |
| `favorite_collision` | 2 |

讲解口径：

- 出现次数高，说明这是世界杯常见门槛，不等于它就是“最决定冠军的因素”。
- `伤病风险`、`旅途疲劳`、`提前撞上热门队` 更适合讲成“哪支队特别容易被这个影响”。
- 首页只展示摘要；详细审计链接到 `artifacts/reports/path-card-internal-audit.md` 或后续报告页。

#### Module E: 外界怎么看

目的：把“外部参照”和“公开数据快照”合并，解释 AI、排名、市场这些外界信号怎么看，而不是展示冠军推荐。

内容：

- 6 类外部参照表：平均分给 48 队、卫冕冠军参照、FIFA 排名参照、Elo 参照、市场公开参照、Kimi 公开 AI 参照。
- 每类参照显示：能不能用、从哪来、怎么算、赛后怎么对账、能不能当事实。
- 市场快照状态：数据来源、抓取时间、覆盖多少队/市场、快照有多旧、来源等级。
- 外界分歧：只在 Kimi 和市场快照都存在时展示；只展示“外界看法差多少”，字段仍命名为 `public_consensus_gap`，但页面文案不要叫 `edge`、`value` 或 “tension index”。

可视化：

- 展示“准备好了没有”的表，而不是冠军排行榜。
- 来源标签：可靠事实 / 待核验线索 / 只能参考 / 混合来源。
- 如果 Polymarket API 快照可用：展示 `last_fetched_at`、`teams_covered`、`snapshot_status`，不展示收益、仓位或价值判断。

不允许：

- `buy`, `sell`, `bet`, `edge`, `value`, `profit`, `ROI`, `PnL`, `Sharpe`, `Kelly`。
- “被低估/高估所以值得下注”。
- 把 Kimi、市场或任何外部参照包装成 CDS 结论。

#### Module F: 方法和来源

目的：建立可信度，但保持紧凑。

内容：

- 三类来源：可靠事实、待核验线索、只能参考。
- 账本小规则：看什么数据、什么时候看、怎么判断兑现、来源是谁。
- 链接到 source policy 和 protocol docs。

设计要求：

- 来源标签是常态 UI，不是只在方法区出现。
- 每个具体数据模块都要有来源标签或大白话边界说明。

#### Module G: 后续怎么更新

目的：让访客理解比赛周期中系统如何保持更新。

内容：

```text
source watch -> snapshot -> source ledger -> baseline refresh -> factor candidate queue -> human review -> locked record
```

状态卡面向访客的命名：

- 市场快照
- 官方消息
- 伤病和新闻线索
- 赛程/赛果对账
- 人工复核

展示口径：

- 只展示任务状态、最近更新时间、失败/待审状态。
- 不展示未核验事实为结论。
- 自动化或人工采集输出先进入 Yellow/Red staging，不直接进入 Factor Ledger。
- 不展示具体自动化工具品牌或暗示尚未投入使用的工具已经运行。

#### Module H: 研究报告

目的：把项目从“网页 demo”提升到“注册报告式实验”，但不喧宾夺主。

内容：

- 一段大白话说明：这个研究不是为了神预测世界杯，而是为了把复杂判断变成能复查、能对账的记录。
- 展示三条主线：球队夺冠路、AI 公开参考审计、赛后对账闭环。
- 显示当前锁定状态：赛前设计已锁定/草稿状态；比赛结果等赛事开始后再填。

注意：

- 不直接发布 `docs/references/paper/**` 内容。
- 如需公开论文摘要，应另建 `docs/public/` 或 `site/research.html` 的可发布版本，并人工脱敏。

#### Module I: 更新记录

目的：让首页有实验进行时的时间感，但保持紧凑。

内容：

- 最近 5 条事件用中文展示：48 队路径卡完成、深度卡审计通过、外部参照组设计完成、赛后对账协议验证通过、市场 API 接入状态。
- 每条包含日期、类型、短说明、链接。

数据来源：

- 可先手写到 `site/data/homepage.json`。
- 后续从 `CHANGELOG.md`、wiki memo 或 artifacts reports 自动生成。

## 6. 数据契约

### 6.1 新增首页数据文件

建议新增：

- `site/data/homepage.json`

v1 使用单一首页数据入口。浏览器只读取本地 JSON，不解析 CSV，不直接请求 Polymarket 或其他外部 API。外部数据如需进入首页，必须先由本地构建或 GitHub Actions 定时任务生成快照，并写入 `site/data/homepage.json` 或由它引用的同目录静态 JSON。

字段草案：

```json
{
  "generated_at": "2026-06-11T00:00:00+08:00",
  "build_date": "2026-06-11",
  "source_policy_version": "draft-for-execution",
  "snapshot_generated_at": "2026-06-11T00:00:00+08:00",
  "summary": {
    "total_teams": 48,
    "deep_description_count": 21,
    "thin_slice_count": 27,
    "obstacle_record_count": 109,
    "settleable_condition_count": 89,
    "baseline_count": 6
  },
  "audit": {
    "deep_cards_audited": 21,
    "deep_cards_passed": 21,
    "source_boundary_status": "pass",
    "factor_ledger_schema_status": "pass"
  },
  "team_teasers": [
    {
      "team_slug": "argentina",
      "team_name": "Argentina",
      "display_status": "deep-description",
      "confederation": "CONMEBOL",
      "path_thesis": "One-sentence public teaser generated from the team card.",
      "top_obstacle_types": ["psychological_pressure", "bracket_strength"],
      "source_completeness": "deep",
      "href": "teams.html#argentina"
    }
  ],
  "obstacle_distribution": [
    {"type": "low_scoring_dependency", "count": 18, "classification": "universal_constraint"},
    {"type": "injury_risk", "count": 10, "classification": "differentiating_variable"}
  ],
  "obstacle_matrix_teaser": {
    "status": "available",
    "team_sample": ["Argentina", "France", "Spain", "Morocco"],
    "obstacle_types": ["low_scoring_dependency", "psychological_pressure", "bracket_strength"],
    "cells": [
      {"team_slug": "argentina", "obstacle_type": "psychological_pressure", "active": true}
    ]
  },
  "baselines": [
    {
      "baseline_id": "market_public_baseline",
      "source_level": "Yellow",
      "status": "designed_not_populated",
      "public_display": true,
      "disclaimer": "External consensus only; not betting advice; not CDS input."
    }
  ],
  "public_signal_snapshots": {
    "market_public_baseline": {
      "status": "snapshot_unavailable",
      "last_fetched_at": null,
      "coverage_count": 0,
      "cache_age_seconds": null,
      "source_level": "Yellow",
      "display_rule": "external_consensus_only",
      "missing_reason": "No build-time market snapshot has been published yet."
    },
    "kimi_public_ai": {
      "status": "partial_populated",
      "coverage_count": 21,
      "source_level": "Red",
      "display_rule": "public_ai_baseline_only"
    }
  },
  "public_consensus_gap": {
    "status": "not_available",
    "display_rule": "Only display absolute public baseline differences when both source snapshots exist; never label as investment signal.",
    "items": []
  },
  "monitoring": {
    "review_queue": {
      "status": "planned",
      "last_updated_at": null,
      "pending_review_count": 0,
      "public_display_rule": "show workflow status only; do not display internal tool brands"
    }
  },
  "research_log": [
    {
      "date": "2026-06-11",
      "type": "audit",
      "title": "21 deep path cards passed internal audit",
      "href": "../artifacts/reports/path-card-internal-audit.md"
    }
  ]
}
```

### 6.2 Existing Data Reuse

可直接复用：

- `site/data/meta.json`
- `site/data/teams.json`
- `data/processed/path_card_internal_audit.csv`
- `data/processed/path_card_obstacle_type_matrix.csv`
- `data/processed/baseline_suite_registry.csv`
- `data/processed/kimi_baseline_signals_matrix.csv`

### 6.3 构建期数据流

推荐单向数据流：

```text
processed CSV / team cards / optional external snapshot
-> scripts/build_site_data.py
-> site/data/homepage.json
-> site/index.html + site/js/homepage.js
```

要求：

- `scripts/build_site_data.py` 负责 CSV 清洗、聚合、缺失值规范化和 JSON 输出。
- `site/js/homepage.js` 只做渲染、空状态和轻交互，不做复杂数据清洗。
- GitHub Actions 可选增加定时任务抓取外部市场快照；失败时保留上一版快照或写入 `snapshot_unavailable`，不能让站点构建失败。
- 首页必须显示 `generated_at` 或 `last_fetched_at`，防止访客把静态快照理解为浏览器实时拉取数据。

### 6.4 Missing Data Rules

任何数值面板必须支持以下状态：

- `available`
- `partial`
- `designed_not_populated`
- `missing_with_reason`
- `snapshot_unavailable`
- `deferred`
- `not_applicable`

禁止为了图表完整而编造数值。

### 6.5 访客文案映射

数据字段可以保留英文，页面显示必须优先使用中文大白话。推荐映射：

| 内部字段/术语 | 页面显示 |
|---|---|
| `team_teasers` | 球队入口 / 球队小卡 |
| `obstacle_distribution` | 夺冠难点分布 |
| `low_scoring_dependency` | 太依赖小比分 |
| `psychological_pressure` | 心理压力 |
| `bracket_strength` | 签表太硬 |
| `base_strength_gap` | 硬实力差距 |
| `tactical_mismatch` | 战术对不上 |
| `squad_depth` | 板凳厚度不够 |
| `injury_risk` | 伤病风险 |
| `travel_fatigue` | 旅途消耗 |
| `favorite_collision` | 太早撞热门队 |
| `baseline` | 外部参照 |
| `public_signal_snapshots` | 公开数据快照 |
| `public_consensus_gap` | 外界看法差多少 |
| `source_level` | 这条信息靠不靠谱 |
| `Green Source` | 可靠事实 |
| `Yellow Source` | 待核验线索 |
| `Red Source` | 只能参考 |
| `settlement` | 赛后对账 |
| `Factor Ledger` | 可对账的判断账本 |
| `missing_with_reason` | 暂时没有，原因是... |
| `snapshot_unavailable` | 这次还没有快照 |

公开页面不应直接出现 `baseline readiness`、`public AI baseline`、`source boundary`、`settlement rule`、`Factor Ledger schema` 这类英文味表达；如确需出现，应放在方法区小字说明或链接文档中。

禁用文风：

- 不堆英文名词：例如 `public baseline readiness snapshot` 这类说法不能作为页面文案。
- 不写论文腔：例如“范畴转换”“可校准知识协议”不能放在首屏主文案。
- 不写投资腔：例如“分歧机会”“低估高估”“市场信号”不能引导行动。
- 不写供应商宣传腔：不突出具体工具品牌、额度、模型能力。
- 不写玄学冠军腔：不说“AI 已经算出冠军”“热力榜说明谁稳了”。

## 7. 可视化规格

根据 data-analysis / chart-visualization / consulting-analysis workflow，首页推荐图表如下：

| 模块 | 图表类型 | 数据 | 目的 |
|---|---|---|---|
| 当前进度 | 指标带 | deep vs thin / audit status | 展示覆盖与可验证状态 |
| 夺冠难点 | HTML/CSS 横向条形图 | obstacle counts | 展示夺冠难点结构 |
| 球队 × 难点速览 | CSS Grid 小矩阵 | path_card_obstacle_type_matrix | 展示不同球队卡在哪些关 |
| 外界怎么看 | 状态矩阵 / 紧凑表格 | baseline_suite_registry | 展示外部参照状态与来源等级 |
| AI 参考 | 紧凑状态行 / 热力条 | kimi_baseline_signals_matrix | 展示 Kimi 参考覆盖与集中度 |
| 市场参考 | 状态卡 + 可选对比行 | build-time market snapshot | 展示外部参考，不做建议 |
| 后续怎么更新 | CSS 流程条 / 状态条 | monitoring status | 展示数据更新与人工复核闭环 |

图表设计原则：

- 图表标题必须描述“观察对象”，不要暗示建议。
- 图例必须包含来源等级。
- 悬浮提示中展示数据来源、更新时间、缺失原因。
- 移动端图表优先折叠为 table 或 horizontal scroll，但不得文字重叠。
- v1 不引入 D3、Chart.js、ECharts 或其他外部图表库；柱状图、矩阵 teaser、readiness matrix 均用语义化 HTML + CSS 实现。
- 图表 DOM 必须保留可读文本值，不能只靠颜色表达含义。
- 矩阵在移动端允许横向滚动，但必须有稳定列宽和可见行/列标签。

### 7.1 来源标签系统

所有数据面板都应使用统一来源标记：

| source_level | 展示含义 | 默认视觉 |
|---|---|---|
| `Green` | 可复核事实，可进入 Team Path Card / Factor Ledger | deep green |
| `Yellow` | 候选事实或外部共识，需要核验 | amber |
| `Red` | baseline / Marginalia / seed，不能作为事实输入 | muted red |
| `Mixed` | 同一面板含多个来源等级 | split / neutral |

来源标签必须靠近具体数据，而不是只出现在页面底部。对 Kimi、市场、未核验新闻和待复核队列，标签文案必须说明“不作为 CDS 事实输入”或“需要人工复核”。

## 8. 内容边界

### 8.1 Must Include

- 明确的 anti-betting disclaimer。
- Kimi = 只能参考 / 公开 AI 参照。
- Market = 外界怎么看 / 不是投注建议。
- 判断账本的入账规则摘要。
- 当前数据缺口：27 队还是简版、部分外部参照未填充、比赛结果尚未开始赛后对账。
- 更新时间与快照状态。

### 8.2 Must Not Include

- 投注建议、收益率、仓位、赔率价值判断。
- “CDS 预测冠军是 X”。
- “Kimi/市场证明 X 会赢”。
- `docs/references/**` 原文或敏感路径内容。
- 未核验新闻、伤病、赔率变化作为事实输入。
- 未运行的 Markov / Monte Carlo / Bayesian 引擎结果。
- 具体长程 agent 工具品牌、供应商、额度信息、benchmark 或“已使用”暗示。

## 9. 用户旅程

### Journey 1: 普通球迷

1. 看到“48 条世界线”的首屏。
2. 点击自己关心的球队。
3. 看到这支球队的主要阻力、所需突破、黑天鹅助力。
4. 理解这不是预测，而是条件路径。

### Journey 2: 数据/研究访客

1. 先看到当前进度，确认覆盖、审计和快照状态。
2. 查看夺冠难点分布、外界怎么看和来源标签。
3. 点击方法和来源。
4. 进入 artifacts report 或 wiki 追溯方法。

### Journey 3: 赛事周期复访者

1. 查看公开数据快照更新时间。
2. 查看数据更新与待复核队列状态。
3. 查看哪些线索已经进入人工复核。
4. 在赛后查看对账更新。

## 10. 实施边界

本 spec 不要求立即新增复杂前端框架。推荐继续使用纯静态 HTML/CSS/JS，保持 GitHub Pages 兼容。

静态架构原则：

- 数据复杂性放在构建期，不放在浏览器运行期。
- 浏览器只请求同源静态 JSON，不直接请求外部市场 API。
- 外部快照如通过 GitHub Actions 定时生成，必须可失败、可复现、可显示时间戳。
- v1 不引入 Astro / Next / Jekyll 依赖；当前站点应能通过普通 HTTP server 浏览。

允许后续施工范围：

- 修改 `site/index.html`
- 修改 `site/css/portal.css`
- 新增 `site/js/homepage.js`
- 新增 `site/data/homepage.json`
- 修改 `scripts/build_site_data.py`
- 修改/新增 `tests/test_build_site_data.py`
- 可新增 `src/data/` 或 `src/publish/` 下的数据处理脚本

禁止后续施工范围：

- 修改 `schema/`
- 修改 `templates/`
- 修改 `example/`
- 提交 `docs/references/**`
- 将外部 API key 或敏感数据写入公开站点

## 11. 验收标准

### 11.1 内容验收

- 首屏在 10 秒内可解释“不是猜冠军，是看夺冠要过哪些关”。
- `选球队` 是首屏或首屏后第一个明确主入口，不被驾驶舱或论文说明压到后面。
- 首页至少展示 4 类真实数据资产：球队覆盖、夺冠难点分布、外部参照状态、规则/审计状态。
- 所有 Kimi 和 market 展示均有来源标签与大白话免责声明。
- 页面主文案必须使用中国球迷听得懂的中文；英文术语不能作为主标题、按钮或核心说明。
- 不出现投注建议、ROI、PnL、Sharpe、Kelly、仓位建议等文本。
- 不发布 `docs/references/**` 内容。
- 首页不出现具体长程 agent 工具品牌、供应商、额度信息或“已经使用”暗示。

### 11.2 数据验收

- `site/data/homepage.json` 可由本地数据生成，缺失字段有明确状态。
- Kimi 概率中的 `N/A` 不导致前端崩溃。
- Polymarket API 不可用时，页面显示 `missing_with_reason` 或 `snapshot_unavailable`。
- baseline 未填充时不显示伪造图表。
- 前端不解析 CSV，不直接调用外部 API。
- 页面展示 `generated_at`；外部快照存在时展示 `last_fetched_at`。
- `public_consensus_gap` 只在 Kimi 与 market 两类快照同时存在时显示，否则渲染空状态。
- 数据字段可以是英文；展示给访客的字段名必须经过 6.5 的中文映射。

### 11.3 UI 验收

- Desktop 与 mobile 均无横向溢出。
- 图表、按钮、标签文字不重叠。
- 首页不依赖 Jekyll 或外部构建服务。
- 静态文件可通过本地 HTTP server 直接浏览。
- 不依赖外部图表库；水平柱状图和矩阵 teaser 均可在无第三方 JS 时显示。

### 11.4 验证命令

后续实现完成时至少运行：

```bash
python3 scripts/audit.py --root wiki/
python3 scripts/verify.py --root wiki/
python3 -m unittest discover -s tests -v
python3 scripts/build_site_data.py
```

并用浏览器验证：

- desktop: 1440 × 900
- mobile: 390 × 844

## 12. 推荐实施顺序

这里只记录产品级顺序，不展开代码级计划：

1. 先生成 `homepage.json`，统一首页数据契约。
2. 改造首屏，建立“每队都有一条夺冠路”的叙事钩子。
3. 前置 `选球队`，让球队入口成为主流程。
4. 添加 `当前进度` 指标带。
5. 添加 `夺冠难点` 图表和一个重点观察卡片。
6. 添加 `外界怎么看`，合并外部参照状态与公开数据快照。
7. 添加 `方法和来源`、`后续怎么更新`、`更新记录` 的紧凑区块。
8. 做响应式、source-policy、禁用词和缺失状态审查。

## 13. Open Questions

1. Polymarket API 的当前实现路径、缓存策略和可公开字段需要单独确认；首页 spec 只定义展示边界。
2. 长程 agent 工具是否作为研究期自动化工具使用，需要后续技术决策页记录；在未投入运行前不得进入主页叙事。
3. 论文摘要是否要公开发布，需要先从 `docs/references/paper/**` 派生脱敏版本，不能直接链接敏感目录。
4. 是否需要新增独立 `baselines.html` / `method.html`，还是先用首页锚点承载，留待实现计划决定。

## 14. Spec Self-Review

- Placeholder scan: no `TBD` / `TODO` placeholders retained.
- Scope check: this spec covers homepage optimization only; it does not require full baseline engine, Polymarket ingestion implementation, or match settlement execution.
- Source-policy check: Kimi and market data are explicitly downgraded to public baseline / external consensus; no betting advice is specified.
- Data feasibility check: core homepage can be built from existing static JSON/CSV via build-time preprocessing; market and monitoring modules have missing-state rules.
- Tooling boundary check: homepage must not display specific long-horizon agent brands or imply unused tools are already part of project output.
- Static-site check: browser-side CSV parsing and direct external API calls are explicitly out of scope for v1.
- Language check: public-facing copy should use plain Chinese for football fans; English-heavy technical labels are limited to data contracts and internal implementation notes.

> [!memo] 2026-06-11 首页优化 spec 初稿
>
> 本 spec 根据当前项目能力、路径卡审计、baseline suite、Plan C 验证和 Polymarket API 能力整理。下一步应先由用户审阅信息架构，再进入实现计划。

> [!memo] 2026-06-11 修订长程 agent 工具展示边界
>
> 根据用户反馈，主页不展示具体长程 agent 工具品牌、供应商、额度信息或"已使用"暗示。相关工具仅作为内部可选能力，使用说明另写内部指南，不进入公开主页叙事。

---

## 9. 增量附录 v2（2026-06-12，作者 MiniMax-M3）

> **类型**: homepage-design-spec-increment
> **基础**: 2026-06-11-homepage-optimization-spec.md（v1，811 行）
> **关系**: v1 既有 9 个模块的设计纪律全部保持有效；本文档仅追加 4 类增量需求 + 1 组负向约束；与 v1 冲突时以 v1 为准并在本附录登记偏差。
> **范围**: 本地 wiki 数据层 / 每日自动化 pipeline / 投票档案机制 / 概率全景图模块 / 工具与统计承诺的边界。

### 9.0 增量边界声明

本附录不是 v1 的替代品，而是其上的扩展层。下列约束从 v1 继承且本附录进一步加强：

- 主页不出现具体长程 agent 工具品牌、供应商名、额度信息、benchmark 数字（v1 §3.4）。
- 主页不出现 `buy / sell / bet / edge / value / profit / ROI / PnL / Kelly` 等投注语言（v1 §3.1, §3.2, §3.3）。
- 浏览器不解析 CSV、不直接调用外部 API；一切重数据在构建期完成（v1 §3.0, §6.1）。
- Kimi = Red Source、Market = Yellow Source 的标记必须可见（v1 §5.3, §5.4）。
- 主页文案以中文为主，英文仅作数据字段或括号补充（v1 §4.1）。

**本附录对 v1 的一处状态更新**：v1 §3.4 写明"长程 agent 工具截至本 spec 修订时尚未投入项目运行"。本附录将其更新为"已规划为每日 pipeline 的内部驱动能力，**对外展示口径不变**"。

### 9.1 增量背景与动机

v1 锁定的 9 个模块（A 首屏 / B 选球队 / C 进度 / D 难点 / E 外界怎么看 / F 方法 / G 更新 / H 报告 / I 更新记录）解决的是"页面长什么样"。本附录解决的是"页面下方的数据底座长什么样、数据怎么每天长出来"。

三个用户原话驱动的增量方向：

1. **本地 wiki 要承载比 v1 假设更重的数据资产**：球队、球员、赛程、单场数值预测、市场赔率、Agent 投票、CDS 推演——七类内容需要稳定的可版本化载体，而不是只活在 `site/data/homepage.json` 的扁平字段里。
2. **希望以多模型多轮的方式每天自动跑一次，而不是项目维护者手工启动 sprint**：参考 `policysim-research-Tsinghua` 的 650 跑模式 + 三层分离（Generators / Annotators / Judges），把单次 sprint 拆成每日可调度的研究任务。
3. **最终用户面对的是一张"概率全景图"，可以下钻到球队详情**：v1 Module B 的"球队小卡列表"是列表视图，本附录新增"赛程矩阵 + 概率叠加"是空间视图。

### 9.2 本地 wiki 数据层（v1 未覆盖的新增）

#### 9.2.1 新增 wiki 目录

v1 假设的 wiki 是 Marginalia 协议下的"概念 / 决策 / 批注"三件套。本附录新增一组**事实型 wiki 页面**，与既有概念型 wiki 并列但物理隔离：

```
wiki/
├── concepts/         # 既有：概念解释（v1 范围）
├── decisions/        # 既有：技术决策（v1 范围）
├── annotations/      # 既有：当前状态批注（v1 范围）
└── facts/            # 新增：事实型页面（v1 未覆盖）
    ├── teams/<team_id>.md      # 48 支球队
    ├── players/<player_id>.md  # 关键球员（动态增长，建议 < 200）
    ├── schedule/<match_id>.md  # 单场比赛上下文包
    ├── predictions/<match_id>-<run_id>.md  # 单场预测记录（每日累积）
    └── markets/<market_id>.md  # 市场快照（每日累积）
```

`wiki/facts/` 走 Marginalia 协议，但**禁止使用 `[[wikilink]]` 跨入概念页**——事实页是数据，概念页是叙事，避免链接污染。

#### 9.2.2 球队页 schema（`wiki/facts/teams/<team_id>.md`）

最少字段：

```yaml
---
team_id: fra          # FIFA 三字代码
display_name_zh: 法国
display_name_en: France
fifa_ranking: 2
confederation: UEFA
qualified_via: UEFA Group B winner
path_card_status: deep          # deep | thin
deep_card_path: wiki/facts/teams/fra.path.md
key_players: [mbappe, tchouameni, saliba]
last_updated: 2026-06-12
source_ledger: [wikipedia_…, fifa_ranking_…]
---

## 基础事实
[…从 Green Source 抽取，不写预测…]

## 当前已锁定的阻力记录
[…从 21 队深度卡 cross-link 过来，每条带 obstacle_id…]
```

#### 9.2.3 球员页 schema（`wiki/facts/players/<player_id>.md`）

最少字段：

```yaml
---
player_id: mbappe
display_name_zh: 基利安·姆巴佩
team_id: fra
club: real-madrid
position: FW
age: 27
fitness_status: fit              # fit | doubt | injured | suspended
last_injury_note: 2026-05-30 hamstring — 训练恢复中
yellow_cards_tournament: 0
red_cards_tournament: 0
source_ledger: [news_rss_…, official_…]
last_updated: 2026-06-12
---
```

球员信息是**最易过期**的事实，每日更新窗口由 RSS/官方 RSS 决定；球员页的 `last_updated` 必须小于 24h 才能进入当日主页（v1 §3.4 数据快照原则的具体化）。

#### 9.2.4 赛程页 schema（`wiki/facts/schedule/<match_id>.md`）

```yaml
---
match_id: wc2026-gs-a1-arg-vs-mex
stage: group_stage
group: A
match_number: 1
kickoff_utc: 2026-06-12T03:00:00Z
venue: estadio-azteca
home_team: mex
away_team: arg
status: scheduled        # scheduled | live | final
prediction_window: 14d   # 距开赛 N 天生成的最新预测将被使用
last_updated: 2026-06-12
---
```

每场比赛对应一个唯一 `match_id`，是后续预测、推演、对账的锚点。

#### 9.2.5 预测页 schema（`wiki/facts/predictions/<match_id>-<run_id>.md`）

每次 pipeline 跑出 1 份预测就是 1 个文件：

```yaml
---
match_id: wc2026-gs-a1-arg-vs-mex
run_id: 2026-06-12-daily   # 唯一 run 标识
pipeline_version: v2.1
generated_at: 2026-06-12T01:30:00+08:00
numeric_forecast:
  home_win: 0.42
  draw: 0.28
  away_win: 0.30
  model: ensemble-xg+poisson
  source_level: Green
market_odds_snapshot:
  source: polymarket
  fetched_at: 2026-06-12T01:00:00+08:00
  home_win: 0.45
  draw: 0.26
  away_win: 0.29
  source_level: Yellow
agent_vote_aggregate:
  rounds: 300
  factions: 10
  home_win_median: 0.41
  home_win_p10: 0.30
  home_win_p90: 0.52
  source_level: Red
cds_path_card_link: wiki/facts/teams/arg.path.md
source_ledger: [polymarket_api_…, internal_ensemble_…]
---
```

**注意三档概率必须并列存放，禁止取最大或加权求和**——这与 v1 §5.4 的"外界分歧只展示 gap，不合成单一概率"是一致的设计选择。

#### 9.2.6 事实页 → 主页 JSON 的转换

构建期脚本 `src/data/facts_to_homepage.py` 负责：

- 扫描 `wiki/facts/teams/` → 生成 `site/data/teams_index.json`（v1 Module B 输入）
- 扫描 `wiki/facts/predictions/` → 按 `match_id` 汇总当日最新 run → 生成 `site/data/match_predictions.json`（本附录 §9.4 全景图输入）
- 扫描 `wiki/facts/markets/` → 生成 `site/data/market_snapshots.json`（v1 Module E 增强输入）

**严禁浏览器解析 `wiki/facts/*.md`**：所有 markdown 解析发生在 Python 构建期。

### 9.3 每日自动化 pipeline（v1 §5 G 模块的具体化）

#### 9.3.1 8 步骤设计

每 24 小时（建议 UTC 02:00 / 北京时间 10:00）触发一次完整 pipeline：

| 步骤 | 任务 | 数据源 | 落入路径 | source_level | 预算 |
|---|---|---|---|---|---|
| 1 | 抓取赛程 | FIFA / 官方 RSS | `wiki/facts/schedule/` | Green | < 1 min |
| 2 | 抓取球队新闻 | RSS / News API | `wiki/facts/teams/*.md` 增量段 | Yellow | < 5 min |
| 3 | 抓取球员信息 | RSS / News API | `wiki/facts/players/*.md` | Yellow | < 5 min |
| 4 | 数值预测 | 内部 ensemble 脚本 | `wiki/facts/predictions/<m>-<r>.md` | Green | < 10 min |
| 5 | 市场赔率 | Polymarket API | `wiki/facts/markets/` | Yellow | < 5 min |
| 6 | CDS 夺冠推演 | 多 Agent 辩论（见 §9.3.3） | `wiki/facts/teams/<t>.cds_run.md` | Green（路径卡本身）| < 60 min |
| 7 | Agent 投票赔率 | 300+ 轮多模型多轮 | `wiki/facts/predictions/<m>-<r>.md` 的 `agent_vote_aggregate` | Red | < 90 min |
| 8 | 报告生成 + 发布 | data-analysis / chart-visualization / consulting-analysis 三技能 | `results/2026-MM-DD-report.md` + `site/data/` 增量 | n/a | < 15 min |

**总预算：~3 小时**。建议在 GitHub Actions 单一 workflow 内串行执行，因为步骤 6、7 互相依赖步骤 1-5 的输出。

#### 9.3.2 与 policysim-research-Tsinghua 的 650 跑模式对照

参考 `policysim-research-Tsinghua/CLAUDE.md` 的三层分离：

| policysim | CDS4WorldCup 对应 |
|---|---|
| Generators（生成层） | §9.3.1 步骤 6（CDS 推演） + 步骤 7（Agent 投票） |
| GT Annotators（标注层） | `data/source-ledger/` 的 source_level 标记（v1 既有） |
| Judges（评估层） | §9.3.1 步骤 8 的 consulting-analysis 阶段 |

**对照后新增的设计选择**：

- policysim 跑 650 次是科研对照实验，每跑对应一个 (model, condition) 组合。CDS4WorldCup 每天 300+ 次不是科研对照，而是**群智评估**：300 个 persona × 同一份赛前证据 → 投票分布的稳健性检查。
- 每天 300 次的合理性论证：覆盖 30 个 match × 10 派别 = 300 投票单元，每场每派别约 30 票（中位数估计），符合 `confidence_interval ≤ 5%` 的基本要求。如果出现覆盖率不足的场次（e.g. 冷门对局只有 50 票），应在主页对应卡片显示"低样本"标签。

#### 9.3.3 CDS 夺冠推演（步骤 6 的辩论结构）

本附录不规定具体 prompt 模板（属于 `docs/ops/` 范畴），只规定辩论拓扑：

- **角色**：5 票陪审团 + 2 票书记员 + 1 票仲裁者
  - 陪审团角色：path-analyst / source-auditor / match-context-analyst / settlement-analyst / cognitive-auditor（参考 `institute-one-audit-for-cds4worldcup.md` §3 P3）
  - 书记员：把每轮结论写回 `wiki/facts/teams/<t>.cds_run.md`
  - 仲裁者：在陪审团分歧 > 0.2 时要求重论
- **轮数**：每场比赛 ≤ 4 轮，超过 4 轮强制出结论
- **结论格式**：必须是结构化 `cds_path_update` 提案，标注：
  - 是否新增 obstacle
  - 是否修改 settleable 条件
  - 是否触发 `source_gap` 警报（自动 spawn 步骤 2 补抓）

#### 9.3.4 Agent 投票（步骤 7 的派别与样本）

派别设计参考 `Kimi_Agent_世界杯热力榜 UI 升级.zip/plan.md` 第 2 节"10 个派别"，但做**结构性升级**：

| Kimi 派别 | CDS4WorldCup 派别 | 差异 |
|---|---|---|
| 数据派 | `quant-analyst` | 同 |
| 赔率派 | `market-mirror` | **改名以避免与"投注"语义混淆** |
| 老球迷派 | `tradition-reader` | 同 |
| 玄学派 | `narrative-skeptic` | 改名：弱化"玄学"标签 |
| 主帅视角派 | `tactic-analyst` | 同 |
| 伤病赛程派 | `fitness-watcher` | 强化 RSS 数据依赖 |
| 黑马派 | `upset-spotter` | 同 |
| 阵容年龄派 | `lifecycle-reader` | 同 |
| 心理抗压派 | `pressure-tester` | 同 |
| 建模派 | `ensemble-modeler` | 同 |

**样本量建议**：每派别 30 个 agent × 10 派别 = 300 票/场。每日 30 场赛事 = 9000 票。这是 v1 §3.3 "300 Agent" 的规模化版本，但**对外主页仍按"群智评估"展示，不强调具体数字**（v1 §3.4 工具品牌边界）。

#### 9.3.5 投票档案机制

每次 pipeline 跑出 300 票，每票写一条记录：

```
data/ops/vote_archive/2026-06-12/wc2026-gs-a1-arg-vs-mex.jsonl
```

每行 JSON：

```json
{
  "run_id": "2026-06-12-daily",
  "match_id": "wc2026-gs-a1-arg-vs-mex",
  "agent_id": "tactic-analyst-007",
  "faction": "tactic-analyst",
  "persona_seed": "ex-defensive-midfielder-1990s",
  "evidence_used": ["wiki/facts/teams/arg.md", "wiki/facts/teams/mex.md", "RSS:Marca-2026-06-11"],
  "prediction": {"home_win": 0.35, "draw": 0.30, "away_win": 0.35},
  "confidence": 0.62,
  "reason_short": "阿根廷左路防守缺口被墨西哥边路速度针对",
  "model_id": "mimo-v2.5-flash",
  "latency_ms": 4200,
  "source_level": "Red"
}
```

**档案用途**：

1. **审计追溯**：赛后对账时，谁投了什么、依据什么，可以逐条查证。
2. **派别漂移检测**：连续 7 日同一派别对同队的偏离 > 0.15，触发 `cognitive_auditor` 介入。
3. **训练负样本**：未来 CDS 模型训练时可作为 prompt 池的负反馈（远期用途，本附录不展开）。

**档案保留策略**：

- 30 天内的全量保留
- 30 天后只保留每日聚合（`agent_vote_aggregate`），原始 jsonl 归档到 `data/archive/vote_archive/`
- 1 年后归档进 `archive/`（v1 项目结构约束）

### 9.4 概率全景图模块（v1 Module B 之上的空间视图）

#### 9.4.1 模块定位

v1 Module B 是"48 张球队小卡的列表视图"。本附录新增 **Module J：概率全景图**——以**赛程矩阵**为底图，在每场比赛的格子上叠加多源概率。

为什么需要新模块：列表视图擅长"我认识巴西"，但回答不了"今晚的两场强强对话，我的判断靠不靠谱"。赛程矩阵把"哪些比赛是项目真正在管的"显式化。

#### 9.4.2 信息架构

```
+----------------------------------------------------------+
|  [小组 A]  A1   A2   A3   A4   A5   A6                  |
|  MEX ─── ARG  |   ????  |   ????  |   ????  |   ????   |
|             (0.42/0.45/0.41) (  红色 = 外界分歧大  )     |
|  …                                                      |
+----------------------------------------------------------+
|  [小组 B]  B1   B2   B3   B4   B5   B6                  |
|  ENG ─── CRO  |   ????  |   ????  |   ????  |   ????   |
|             (0.55/0.50/0.58)                              |
|  …                                                      |
+----------------------------------------------------------+
```

每格显示：

- 比赛双方国名/队徽
- 三档概率（数值 / 市场 / Agent 投票）的小数字
- 一个"健康度"指示：若三档概率极差 > 0.2，格子背景染成"分歧大"色

**禁止显示**：

- 单一合成概率（v1 §5.4 纪律）
- 任何"该买谁"的暗示
- 实时比分（赛程页不做 live score，只做赛前概率；live 数据另开 `site/live.html`）

#### 9.4.3 球队详情下钻

点击任意队徽进入球队详情页 `site/team/<team_id>.html`，结构：

1. **基础事实区**（来自 `wiki/facts/teams/<id>.md`）
2. **当前三档概率**（数值 / 市场 / Agent 投票），三档并列
3. **CDS 路径卡链接**（深描版则展开前 3 个 obstacle + 全部 settleable 条件；简版只展示 obstacle 类型分布）
4. **本队所有赛程**（点击格子下钻的逆操作）
5. **该队的 Agent 投票画像**（以"内部参考"标签，不显示具体 300 票）

#### 9.4.4 视觉规范（与 v1 §4.2 兼容）

- 底色：保留 parchment / ink 体系，不引入新主色
- 概率数字字号：clamp(0.7rem, 1.2vw, 0.95rem)，保证 6 格矩阵在小屏可读
- "分歧大"色：使用 v1 §4.2 既有"只能参考：暗红"，避免新色引入
- 数据缺失态：使用 v1 §3.0 既有的"missing-state rules"，明确写"暂无数据"而不是隐藏
- 零图表库依赖：矩阵用 CSS Grid，概率条用 inline flex

#### 9.4.5 触达路径

- 首页 Module B（选球队）保留作为"按队浏览"主入口
- 新增"按赛程浏览"主按钮：`看看本周的 6 场比赛`，跳到 Module J 全景图
- 两个入口互链，不强制顺序

### 9.5 风险与边界（负向增量）

> 本节是用户在原话之外、未明确提出的、但根据 v1 既有约束和项目纪律**必须警告**的事项。

#### 9.5.1 工具品牌对外不可见（强化 v1 §3.4）

用户原话："mimo code 驱动 mimo-v2.5 跑 300 次甚至更多"。

v1 §3.4 已明文禁止"首页不得出现具体长程 agent 工具名、供应商名、额度信息"。如果本附录的 pipeline 落地后，主页出现"由 mimo-v2.5 在 2026-06-12 跑了 300 次"这类表述，即直接违反 v1。

**强化的内部规则**：

- `site/data/*.json` 中不出现模型 ID
- `site/data/*.json` 中不出现"mimo"或具体供应商名
- 投票档案 `data/ops/vote_archive/*.jsonl` 中可记录 `model_id` 字段（内部审计用），但 `wiki/facts/predictions/*.md` 的 frontmatter 不出现该字段
- consulting-analysis 生成的报告，若需公开，先扫描并替换工具名为"多模型群智"

#### 9.5.2 "300 次/天"的统计与承诺

参考 `policysim-research-Tsinghua` 的 H1-H4 假设检验，650 跑是科研项目，有完整 d / IRR / Cohen's kappa 等统计量。

CDS4WorldCup 每天 300 票是**群智评估**，不是对照实验。如果在首页出现"我们每天 300 个 AI 评估"，而没有附：

- 样本稳定性区间（中位数 ± p10/p90）
- 派别间一致性指标
- 至少 7 日的回测一致性

会显得过度承诺。

**强化的内部规则**：

- §9.3.1 步骤 8 报告必须输出三件事：
  1. 当日 30 场比赛的中位数 / p10 / p90
  2. 派别间相关系数（Pearson 或 Spearman）
  3. 与 7 日移动平均的偏离度
- 主页 Module J 只显示"群智评估已运行"的状态灯和当日时间戳，不显示"300"或"v2.5"等数字
- 报告页（`results/`）可以显示"群智评估使用了多模型多轮投票"，但**不显示具体模型版本号**

#### 9.5.3 Polymarket 数据 vs 内部推演的语义边界

用户原话提到 `cds4polymarket` 作为辩论推演的参考。

v1 已锁定 Polymarket 为 **Yellow Source**，只能作 baseline。`cds4polymarket` 作为内部方法论库（不是数据源），与公开 Polymarket API 是不同对象——但容易在叙述中被混淆。

**强化的内部规则**：

- 主页和 wiki facts 页的"市场"区，数据源只能写 `polymarket_api_snapshot`
- `cds4polymarket` 是 wiki 内部方法论的概念（应在 `wiki/concepts/cds4polymarket.md` 单独说明），不可作为数据源字段出现
- 步骤 6 的 CDS 推演不直接读取 Polymarket 价格；它读取 §9.2.5 schema 中的 `market_odds_snapshot`，与"市场赔率"解耦

#### 9.5.4 球员信息源缺失

v1 没有明确球员信息数据源。本附录假设步骤 3 走 RSS / News API。

**未审计风险**：

- RSS 源大多为 Yellow Source（俱乐部官方 RSS 才是 Green）
- 球员伤病的真实性门槛极高，单一 RSS 标题不能进入 wiki facts 页的 fitness_status 字段
- 至少需要两源交叉验证（v1 §3.2 数据纪律的延伸）

**强化的内部规则**：

- `wiki/facts/players/*.md` 的 `fitness_status` 变更必须附带 `source_ledger` 中 ≥ 2 条
- 若 24 小时内无法交叉验证，状态保持上一次确认值，并显示"数据陈旧"标签
- 步骤 3 的输出不直接覆盖球员页；先生成 `data/ops/player_updates_pending/`，经人工 review 后再 merge

#### 9.5.5 每日发布频率与 GitHub Pages 配额的隐性成本

每天一次 8 步 pipeline：

- 单次运行 ~3 小时（如 §9.3.1 所估）
- GitHub Actions 免费额度 2000 分钟/月，每日单 run 180 分钟 = 月消耗 5400 分钟，**超出免费额度**
- 需要迁移到自托管 runner 或付费计划

**强化的内部规则**：

- v1 不约束部署成本，但本附录在执行前需要决策：是否拆分步骤到多个短 workflow（每个 < 30 min）以节省并发配额？是否迁移到自有服务器？
- 这一决策属于 `wiki/decisions/` 范畴，不在本 spec 落地

#### 9.5.6 概率全景图 ≠ 比赛赔率展示

用户原话"用户可以点击每一只球队，来看更详细的内容"——这与博彩站行为高度相似。

**强化的内部规则**：

- Module J 不得显示"赔率"措辞；用"概率"或"评估"或"群智看法"
- 球队详情页不得显示"价值"、"被低估"、"值得"、"买"、"押"等措辞
- 任何"如果你选 X 队"的措辞必须改为"X 队当前三档概率分别为…"

#### 9.5.7 投票档案与 homepage.json 的接口脱钩

投票档案的原始 jsonl 可能非常大（每日 9000 行 × 30 字段 ≈ 5MB）。`site/data/match_predictions.json` 必须**只取聚合结果**，不携带原始票面。

**强化的内部规则**：

- `data/ops/vote_archive/` 不在 `site/` 目录中，永不上 Pages
- `site/data/match_predictions.json` 中 `agent_vote_aggregate` 只含中位数 / p10 / p90 / 派别相关系数
- 任何人手工查档必须通过 `data/ops/`（项目维护者路径），不通过 GitHub Pages URL

### 9.6 与 v1 的衔接

#### 9.6.1 不修改的部分（v1 全部保留）

- v1 §5 的 9 个模块 A-I 设计、字段、文案原则
- v1 §6 的 homepage.json schema 主体
- v1 §3 的"参考产品学习"取舍结论
- v1 §7（隐含的）来源纪律
- v1 §8 的"评估口径"和"已锁定的状态"

#### 9.6.2 升级的部分

| v1 假设 | v2 升级 |
|---|---|
| `site/data/homepage.json` 单入口 | 新增 `site/data/teams_index.json` / `match_predictions.json` / `market_snapshots.json`（v1 §6.1 已有拆分预期，本附录具体化） |
| Module B 仅按"深度版优先 + 队名排序" | 新增"按赛程浏览"作为并列入口（Module J） |
| Module E 6 类外部参照并列展示 | 增加"群智评估（多模型多轮）"作为第 7 类，但仅显示**聚合结果**，不显示模型/次数/品牌 |
| Module G "数据更新状态"是抽象描述 | 落地为 8 步 pipeline 的具体状态灯 |
| wiki 仅承担概念/决策/批注 | 增设 `wiki/facts/` 事实型子目录 |

#### 9.6.3 数据契约扩展

```jsonc
// site/data/match_predictions.json (新增)
{
  "generated_at": "2026-06-12T10:00:00+08:00",
  "build_date": "2026-06-12",
  "pipeline_version": "v2.1",
  "matches": [
    {
      "match_id": "wc2026-gs-a1-arg-vs-mex",
      "kickoff_utc": "2026-06-12T03:00:00Z",
      "venue": "estadio-azteca",
      "home": {"team_id": "mex", "display_name_zh": "墨西哥"},
      "away": {"team_id": "arg", "display_name_zh": "阿根廷"},
      "stage": "group_stage",
      "predictions": {
        "numeric_forecast": {  // 步骤 4
          "home_win": 0.42, "draw": 0.28, "away_win": 0.30,
          "source_level": "Green", "label": "数值预测"
        },
        "market_odds_snapshot": {  // 步骤 5
          "home_win": 0.45, "draw": 0.26, "away_win": 0.29,
          "source_level": "Yellow", "label": "市场参考",
          "fetched_at": "2026-06-12T09:30:00+08:00"
        },
        "agent_vote_aggregate": {  // 步骤 7
          "home_win_median": 0.41,
          "home_win_p10": 0.30, "home_win_p90": 0.52,
          "sample_size_band": "300-vote",  // 离散化带宽，不显示具体数字
          "source_level": "Red", "label": "群智评估"
        },
        "cds_path_link": "wiki/facts/teams/arg.path.md"
      },
      "consensus_gap": 0.04,  // |numeric - market| + |market - agent|
      "data_status": "ok"      // ok | low_sample | stale | missing
    }
  ]
}
```

### 9.7 验收标准（增量）

本附录的 8 步 pipeline 上线需满足以下条件（与 v1 §11 既有验收标准并行）：

1. **数据层**：`wiki/facts/` 4 类页面（teams/players/schedule/predictions）的 schema 模板已建，最少 5 支球队、10 名球员、3 场比赛、2 场预测走通端到端
2. **8 步 pipeline**：单次端到端跑通，预算 ≤ 3 小时，失败步骤可重跑而不污染前序输出
3. **投票档案**：`data/ops/vote_archive/<date>/<match_id>.jsonl` 写入且每日聚合可被 `consulting-analysis` 读取
4. **概率全景图 Module J**：6 组比赛矩阵可在 1024px 桌面和 375px 手机端正确排版，无横向滚动
5. **来源纪律**：所有 `agent_vote_aggregate` 字段 source_level=Red 且在卡片可见；Polymarket 字段 source_level=Yellow 且 `fetched_at` 必填
6. **品牌隔离**：`site/data/*.json` 全量 grep 不含 `mimo`、`mimo-code`、`mimo-v2.5`、`MiMo` 等字串
7. **投注语言隔离**：`site/` 目录下全量 grep 不含 `bet`、`edge`、`value`、`ROI`、`PnL`、`Kelly`（大小写不敏感）
8. **事实页隔离**：浏览器不解析 `wiki/facts/*.md`，仅读取 `site/data/*.json`
9. **统计诚实**：报告页（`results/`）显示"群智评估"时同时显示派别相关系数与 7 日偏离度，不显示模型版本号
10. **保留策略**：30 天前的原始投票档案已归档至 `data/archive/`，主页可访问的 json 不含归档数据

### 9.8 相关页面

- [[decisions/mimo-season-campaign-ops]] — 内部运营节奏
- [[decisions/cds4worldcup2026-path-space-spec]] — 路径空间方法论
- [[decisions/institute-one-audit-for-cds4worldcup]] — Prompt 三明治与角色配置化的来源
- [[concepts/cds]] — CDS 概念
- [[concepts/source-policy]] — 来源分级（v1 引用）

> [!memo] 2026-06-12 增量附录 v2（作者 MiniMax-M3）
>
> 来源：用户要求研究 Kimi UI 升级、institute-one、policysim-research-Tsinghua 三方参考，并把每日多模型 pipeline 想法落到 spec。
> 上下文：在 v1（2026-06-11，811 行）基础上扩展本地 wiki 数据层、8 步每日 pipeline、投票档案机制、概率全景图 Module J；保留 v1 全部 9 个模块与既有约束。加强了 5 条负向约束：工具品牌对外不可见、300 次/天的统计诚实、Polymarket 数据与内部推演解耦、球员信息源审计、概率全景图与赔率展示的语义边界。
> 待办：v1 §6 data contract 与本附录 §9.6.3 新增 contract 的合并；v1 §11 验收标准与本附录 §9.7 增量验收的合并；用户审阅后另写 `wiki/decisions/2026-06-12-homepage-spec-v2-increment.md` 决策页。
