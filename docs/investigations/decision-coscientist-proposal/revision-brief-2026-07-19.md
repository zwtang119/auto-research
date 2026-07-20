# 文档修订简报（2026-07-19 晚）

> **用途**：本轮文档修订的统一事实基准与风格规范。每位修订代理先读本文件，再修指定目标文档。
> **总原则**：外科手术式修订——不动骨架、不动已通过的终裁（NeurIPS D&B 首选 / MVE 第一优先 / G2 go/no-go / 四层评估 / 诚实边界）、不重写实验设计（H1/H2/统计方案）；只吸收下列已核实事实。每份文档按自身惯例追加版本记录或修订注记（日期 2026-07-19）。

## 一、风格规范（以 `proposal-decision-coscientist.md` 为基准）

- 正式学术中文，措辞精确克制；与开题报告同 register。
- 事实主张附证据（URL 或文件路径）；查不到的如实写「未能核实」；禁止编造。
- 重大修改写入该文档的版本记录/修订记录（若有），注明「2026-07-19：……」。
- 沿用各文档既有术语（Factor Ledger、锚分离、宽类、深案、检验侧/生成侧、可结算/settleable）。
- 英文术语首次出现括注中文或原文（如：可结算（settleable））。

## 二、事实基准（已核实，含证据）

**F1 宽案例类轨道**：检验结构可从「2 深案（古雷+郑州）」升级为「**2 深案 + 1 宽类**」。宽类首选**台风**（备选地震）：IBTrACS v04r01（1842–至今，免 key bulk，https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/ ，每周 3 更，引用 Knapp 2010/Gahtan 2024；HDX 镜像 CC BY-IGO）+ CMA 最佳路径（1949–，2017 起登陆前 24h 加密 3h；**非商用**；原站 tcdata.typhoon.org.cn 挂 WAF 拦脚本（468），**可用 IBTrACS 内置 CMA 序列替代**）+ 省级响应通告（决策侧，见 F2）+ EM-DAT 后果（注册免费，无 API，行动字段已弃用）。地震轨道：USGS FDSN（https://earthquake.usgs.gov/fdsnws/event/1/ ，免 key，PAGER 警级+ShakeMap）。宽类用于强化 H3 旁证的统计效力（N≥60），不改 H1/H2 设计。

**F2 决策行动锚源（已核实）**：
- mem.gov.cn 国家防总响应通告：/xw/yjyw/（123 页归档，2018-01 起）、/xw/yjglbgzdt/（88 页，2020-07 起），日时级时间戳，静态 HTML 可爬；**2018 年前无官方机读归档（2018 断档）**。
- 调查报告栏目 /gk/sgcc/tbzdsgdcbg/：2003–2026 逐年归档，全文级自 2011 甬温线起。
- 省厅：广东 yjgl.gd.gov.cn（实测 2020–2025）、福建 yjt.fujian.gov.cn（2019 起）、浙江 yjt.zj.gov.cn（**境内直连可爬**，栏目 /col/col1229565103/index.html 实测 200；**限境外 IP**——「只能走媒体源」的旧结论作废）。
- JMA 防灾信息 XML（Digital Typhoon）：2012–2026 台风报文/警报发布时间线，CC BY 4.0。
- IFRC GO API（goadmin.ifrc.org/api/v2/）：免 key，field-report 5,107 条含 `actions_taken`（主体×行动编码）；中国 69 事件多为 GDACS 自动同步条目；cds4polymarket 已接 event 端点。
- NWS api.weather.gov：CAP 预警（含 Evacuation Immediate），免 key（需 UA）。
- NTSB CAROL（CSV/JSON）；CSB 全本 PDF（BP Texas City，与古雷同灾种，公有领域，https://www.csb.gov/assets/1/20/csbfinalreportbp.pdf ）。
- ReliefWeb API：**2025-11 起需预审批 appname**（未审批返回 410）。

**F3 指定锚实测存活（2026-07-19）**：郑州 7·20 报告 PDF（https://www.mem.gov.cn/gk/sgcc/tbzdsgdcbg/202201/P020220121639049697767.pdf ，667 KB 文本型）；古雷 4·6 报告 HTML（https://yjt.fj.gov.cn/zwgk/sgxxgk_gb/sgdcbg/202501/t20250102_6601366.htm ）。

**F4 事实修正**：① Buncefield——HSE 官方直链已 **404**；改用英国国家档案馆 webarchive（buncefieldinvestigation.gov.uk 归档）或 FABIG 镜像（Vol.1 https://www.fabig.com/media/tpuaseey/buncefield-incident-miib-final-report-volume-1-dec2008.pdf ；Vol.2 https://www.fabig.com/media/jkvgpiv3/buncefield-incident-miib-final-report-volume-2-dec2008.pdf ），**Crown copyright 非商用限制**，六源中最贴应急指挥决策。② 2018 断档（见 F2）。③ 中国气象历史预警报文**无机读存档**（中央气象台台风公报过季不可追溯）。④ pm25.in 已死。

**F5 settleability 切割**：LLM4TyphoonKG（github.com/2BAIHAO/LLM4TyphoonKG）证明 disaster-KG 线已存在（LLM 抽取台风演化/灾情三元组、**无抽取评测、无结算语义**、CoT 蒸馏 7B）。本项目锚数据集的新颖性表述统一为：**首个可结算（settleable）的灾害决策因子集**——因子=带判定规则、阈值区间、反证信号、盲评字段、来源分级的可裁定断言；与描述性三元组显式区分。表述场合：novelty/定位陈述、预期成果、资产价值、pipeline 契约。

**F6 media 流水线**：公共卫生媒体监测报告（report_20260604_1200_media.html 系列）的生成端不在本机（云端 agent 定时任务），**不可改造**；可按报告自含规范（L1/L3 分级+滞后天数两张表）重建灾害采集端，约 1–2 天。前瞻锚协议（季前注册、事后盲结算）的采集基础设施=mem.gov.cn/省厅逐日爬取。

**F7 数据可行性附件**：`source-inventory-2026-07-19.md`（本目录，含 §8/§9 两轮网络复测）。**最终网络指引：采集走境内直连，勿挂 VPN**（政务站限境外 IP）。

## 三、分工（修订矩阵摘要，详细版见扫描结论）

- **Item 1 `proposal-decision-coscientist.md`**（v1.3.1→v1.4）：① §2.7 与 §9 创新点 2 按 F5 切割（可结算因子 vs disaster-KG，补 LLM4TyphoonKG 一句）；② §5.1 按 F1 增补宽类轨道（作为 H3 旁证的统计强化层，写明不改 H1 设计；台风首选、地震备选、源见 F1/F2）；③ §7 风险 8 按 F4① 修正 Buncefield，并补 2018 断档、历史预警报文无机读存档、ReliefWeb appname 三条硬约束；④ §4 M5 与 §6.1 按 F2 补决策行动锚源清单（一句总括+源名）；⑤ §6.1 按 F3 把「公开全文」升级为「2026-07-19 实测存活（附 URL）」；⑥ 附录 C 版本记录加 v1.4 条目。
- **Item 2 `PROJECT-BRIEF.md`**（v1.3→v1.4）：① §7 入口 3 按 F4① 修 Buncefield；② §6.4/§3 新颖性表述按 F5 切割；③ §7 按 F1 增补宽类锚轨道入口（与 topic-eval 一致）；④ §6.3 锚可建证据按 F3 升级；⑤ 版本记录。
- **Item 3 `topic-eval-top-journal-2026-07-19.md` + `topic-eval-explained-em-audience-2026-07-19.md`**（后者 v1.1→v1.2）：① 修正清单 #3（锚≥3 且跨辖区）升级为「2 深案 + 1 宽类（N≥60）」（F1+F2 源）；② explained §6 语料基础：事故档案侧按 F2/F3 追加行动锚源与实测证据、Buncefield 按 F4① 改写、附注按 F6 补前瞻采集基础设施；③ explained §3/§5/§9 与 top-journal 相关段按 F5 切割措辞；④ explained §6 浙江相关若有「走媒体源」表述按 F2 作废改写；⑤ 版本记录。
- **Item 4 `anchors/anchor-pool-pipeline.md` + `README.md`**：① anchor-pool §1 候选列增宽类样本候选（F1）；§3/§4 金矿源与筛选准入按 F1/F2 扩充；§5 已有资产登记 source-inventory；Buncefield 行按 F4① 修正。② README：登记 source-inventory-2026-07-19.md（数据可行性附件）；文件地图相关行同步 F1/F2/F4 变化；修订记录追加。
- **Item 5 `asset-mapping-2026-07-19.md` + `pipeline-design-spec-2026-07-19.md` + `adjacent-work-positioning-2026-07-19.md`**：① asset-mapping §3 检索步骤按 F2 补行动锚源（含 actions_taken 字段）；§3.3 登记宽类数据流扩展点。② pipeline-design-spec §2.1 步骤 3 契约可增 `decision_actions[]`（origin 枚举扩 ifrc_go/nws_cap/ntsb/csb 等）；步骤 5 calibration_status 注释按 F5 明确「可结算性」要件。③ adjacent-work §1.2 按 F2 补「机器可读行动锚新兴来源」一句及与 8 步流水线 decision_actions 的对齐。④ 各文档加修订注记。
- **Item 6 `q5-second-case-selection.md` + `ruling-memo-2026-07-19.md`**（过程存档，仅顶部注记，不改正文）：各在文首（标题下）插入一行「> **2026-07-19 更正注记**：……」。q5：Buncefield 直链 404→归档/镜像+非商用（F4①）、ReliefWeb 需 appname（F2）、宽类轨道可与零污染锚并行（F1）。ruling-memo：宽类 N≥60 路径补充（F1）、决策行动锚源可使检索不为空（F2）。

## 四、禁止事项

- 不改正文骨架与既有结论；不改 q1–q4、redteam-review、reviews/、sources/、idea-decision-pipeline。
- 不把「宽类」写成替代深案；表述为「2 深案 + 1 宽类」的增补层。
- 不删除「横州六蓝零污染锚」任何内容（前瞻线与宽类并行）。
- 引用 URL 一律用本简报 F 区给出的实测链接，不要自行发明新链接。
