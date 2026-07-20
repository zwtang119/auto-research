# 灾害决策推演数据源盘点（定向核查版）

> **日期**：2026-07-19 ｜ **性质**：定向盘点（6 路并行实测核查，全部关键判断附 URL/路径证据）
> **范围**：检验侧锚源（灾害参数/后果/决策行动三层）+ 生成侧素材源 + 已有资产复核
> **背景文档**：PROJECT-BRIEF.md、topic-eval-explained-em-audience-2026-07-19.md（本文为其数据可行性附件）
> **方法说明**：WebSearch+FetchURL 实测与本地仓库侦察；未能一手核实的项均如实标注。

---

## 0. 一句话总结论

- **检验侧三层锚全部落实**：灾害参数锚（IBTrACS/CMA/Digital Typhoon）、后果锚（EM-DAT/USGS）、**决策行动锚**（mem.gov.cn 2018+ 响应通告、省厅防风响应、JMA-XML、IFRC GO `actions_taken`、NWS CAP、NTSB/CSB 报告）均有实测可用的源。
- **两个指定锚今日实测存活**：郑州 7·20 调查报告 PDF（mem.gov.cn，HTTP 200）✅；古雷 4·6 调查报告全文 HTML（福建省应急管理厅）✅。
- **三个硬约束**：① 中国国家防总响应通告机读归档仅 **2018 年起**（此前断档）；② 中国气象**历史预警报文无机读存档**；③ Buncefield 的 HSE 官方直链已 **404**（须改用国家档案馆/镜像）。
- **宽案例类（台风/地震）证据路径成立**：台风 1949 起参数全、2020+ 省级响应时间线可爬；地震 USGS FDSN 全球免 key。H3 可由「2 深案 8 因子」升级为「2 深 + 1 宽类（N≥60）」。
- **media 监测流水线生成端不在本机**（云端 agent 定时任务），不可改造、只能按报告自含规范重建（约 1–2 天）。

---

## 1. 检验侧：灾害参数锚

| 源 | 可得性 | 机读性 | 时间覆盖 | 决策行动记录 | 许可 | 结论 |
|---|---|---|---|---|---|---|
| **IBTrACS v04r01**（NOAA/NCEI） | 免 key 免注册，[bulk 直连](https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/) 实测 200；另有 HDX 镜像（周更） | CSV/netCDF/shapefile bulk，无 REST API | 1842 至今，每周 3 更 | 无 | 开放（引用 Knapp 2010、Gahtan 2024；HDX 镜像 CC BY-IGO） | **台风路径/强度锚首选**；DOI: 10.25921/82ty-9e16 |
| **CMA 最佳路径**（上海台风所 tcdata.typhoon.org.cn） | 免费；2025-08 Wayback 快照显示免登录直链；当前站点挂 WAF（脚本访问 468），现行门槛未完全核实 | 逐年定宽 TXT + 整包 RAR，无 API | 1949 至今（至 2024）；**2017 起登陆前 24h 加密为 3h** | 无 | **非商用**，须注明出处并引用 Ying 2014、Lu 2021 | 中国登陆台风权威锚（登陆段 3h 加密对裁定关键）；论文涉商用风险用 IBTrACS 兜底 |
| **Digital Typhoon**（NII 北本朝展） | 免注册 | 网页/CGI + ML 数据集（H5） | 最佳路径 1951–；**JMA 防灾信息 XML 库 2012–2026**（全般台風情報+警報・注意報，含发布时间线，实测个例页链接存活） | **有（日本）**：JMA 报文/警报发布时间线；不含地方避难指示 | 数据集与 XML 相关 CC BY 4.0 | 路径与 IBTrACS 重复；**独有价值=日本决策时间线锚（2012 起、CC BY）** |
| **中央气象台台风网**（typhoon.nmc.cn） | 免 key，JSON 接口实测（`list_YYYY` 1949–2026 逐年、`view_<id>` 逐 6h） | 非官方 JSON 接口（前端 JS 中确认地址） | 路径 1949–；**报文仅当期，无历史存档** | 无历史决策记录 | www.nmc.cn 页脚「未经授权禁止下载使用」 | 路径可当免费实时素材（生成侧）；**历史预警报文确认没有，勿依赖** |
| **USGS Earthquake FDSN** | 免 key | REST/GeoJSON/CSV | 全球目录级历史 | 无决策记录；有 PAGER 量化后果警级、ShakeMap | 美国政府公开数据 | **地震宽类首选事件锚**（检验侧） |
| **USGS Water Services** | 免 key | REST/tab-delimited | 实时+百年级日值（美国） | 无决策记录；有量化水位/流量 | 美国政府公开数据 | 美国洪水量化后果锚 |
| **INPE Queimadas**（巴西火点） | 免 key（旧域名已失效，迁至 terrabrasilis.dpi.inpe.br/queimadas/） | WebGIS/下载 | 逐小时+历史 | 无 | 巴西官方开放 | 野火发生事实锚 |

## 2. 检验侧：后果锚（量化伤亡/损失）

| 源 | 可得性 | 机读性 | 时间/地理 | 行动字段 | 许可 | 结论 |
|---|---|---|---|---|---|---|
| **EM-DAT**（CRED/UCLouvain） | 注册免费（非商用；商用 €6,000/年）；机构邮箱是否强制未核实；另有 Dataverse Archive（CC-BY-NC-ND）与 HDX 国家年度汇总 | **无公开 API**，登录后导出 xlsx | 1900–，27,000+ 事件；国家级（2023.09 起含次国家级 Admin Units）；中国事件有覆盖但有收录门槛（死亡≥10 等） | **无**（仅有的 3 个响应二元字段 2025.12 起官方弃用） | 非商用署名 | **伤亡/经济损失金标准后果锚**；校准「伤亡与损失」，不校准「决策」 |
| **DesInventar**（UNDRR） | 开放下载免注册 | 网页查询导出，无统一 API | 因国而异（1970s–）；73 国，**无中国库** | 无 | 数据归各国机构，署名 | 粒度最细（次国家级）但对中国零覆盖，本项目排除 |
| **GDACS**（EC-JRC/OCHA） | 免 key | REST API（GeoJSON）+RSS/KML 实测 | 地震/洪水 2004–、TC 2011–、野火 2021–；中国覆盖好 | 无（模型化影响估计，非核实损失） | 免费署名 | **生成侧**（灾害参数供给器），不可当检验锚 |
| **NOAA NCEI Storm Events** | 未专项核查（public-apis 黄页列为缺口，美国官方灾情损失库） | — | — | — | — | 待补查（美国后果锚候选） |

## 3. 检验侧：决策行动锚（本项目最稀缺层，本次核查最大收获）

### 3.1 中国源

| 源 | 可得性/机读性 | 时间覆盖 | 内容 | 结论 |
|---|---|---|---|---|
| **应急管理部官网新闻栏目**（mem.gov.cn/xw/yjyw/ 123 页归档 + /xw/yjglbgzdt/ 88 页归档） | 免 key；静态 HTML 可爬（带 UA+gzip） | **2018-01 建站至今**（此前无官方归档；gov.cn 2009 样本已 404） | 国家防总响应启动/提升/终止通告，**日时级时间戳**（「X 月 X 日 X 时启动 X 级」）+ 派工作组等行动 | **中国响应时间线主力源**；2018 断档须在设计中明示 |
| **应急管理部「事故及灾害查处→调查报告」栏目**（/gk/sgcc/tbzdsgdcbg/） | 免 key；HTML 列表+全文 HTML/PDF | 2003–2026 逐年归档；**全文级报告约自 2011 甬温线起**（响水 3·21、泉州欣佳、长沙 4·29 等） | 特别重大事故完整处置经过，可逐条裁定 | **检验侧金标准**（深案） |
| **郑州 7·20 调查报告 PDF** | [全文直链](https://www.mem.gov.cn/gk/sgcc/tbzdsgdcbg/202201/P020220121639049697767.pdf) 实测 200（667 KB，文本型） | 2022-01-21 发布 | 7·17–7·23 逐日/逐时处置、响应滞后认定 | ✅ 指定锚，今日存活 |
| **古雷 4·6 调查报告 HTML** | [福建省应急厅全文](https://yjt.fj.gov.cn/zwgk/sgxxgk_gb/sgdcbg/202501/t20250102_6601366.htm) 实测完整（2015 首发，2025 迁移路径） | 2015 | 4·6 18:56 起爆至 4·9 逐罐扑灭完整时间线 | ✅ 指定锚，今日存活（省级报告须到省厅找，不在国家栏目） |
| **广东省应急管理厅**（yjgl.gd.gov.cn，gkmlpt+「防汛进行时」专题） | 免 key；静态页可爬 | 实测 2020–2025（防风/防汛/防冻三类） | 省防总响应启动/调整/结束，日时级时间戳+防御指令 | **省级锚样例充足**（台风宽类决策侧来源） |
| **福建省应急管理厅**（yjt.fujian.gov.cn 应急要闻） | 免 key；HTML | 2019 建站后为主 | 省防指响应通告+具体指令（渔船回港时限等） | 与古雷同站，福建案例一站取齐 |
| 浙江省防指通告 | 决策存在且带时间戳（新华网/潮新闻），**省厅官网归档栏目未定位** | — | — | ⚠️ 需走媒体源，不适合批量 |
| **应急管理部新闻发布会实录**（/xw/xwfbh/） | 免 key；HTML | 2018– | 问答式决策解释 | 「决策理由」语料 |
| 地方志/《中国应急管理年鉴》 | 华师地方志库（注册免费，扫描为主）；年鉴仅付费纸质/CNKI | — | 叙事体 | 生成侧背景，不适合裁定 |

### 3.2 国际源

| 源 | 可得性/机读性 | 时间覆盖 | 决策行动含量 | 结论 |
|---|---|---|---|---|
| **IFRC GO API**（goadmin.ifrc.org/api/v2/） | **免 key 读取实测**；REST 全端点 | 2018 上线+历史迁移；field-report 实测 **5,107 条** | **五源中唯一结构化行动锚**：`actions_taken`（主体×行动分类编码）、官方口径伤亡分列、ERU 部署；DREF 挂 EPoA 行动计划 | **行动锚首选**；中国 69 事件多为 GDACS 自动同步条目、人工报告薄——中文区密度靠 GDACS 条目兜底；cds4polymarket 已接入 event 端点 |
| **NWS api.weather.gov** | 免 key（需 UA）；REST/GeoJSON/**CAP** | 预警在效+7 天，档案走 NCEI | **有**——CAP 官方预警（含 Evacuation Immediate 等类型） | 美国气象/飓风预警行动锚；许可开放（官网明示任意用途） |
| **US NTSB（CAROL）** | 免 key；查询页 CSV/JSON 下载+航空月度 bulk+报告 PDF 直链（实测 MAR2103 200） | 航空 1962–，其他运输 2010– | 海事/铁路/管道重大报告含分钟级事件史+伤情/损失 | 英文检验侧语料机读性最好；公有领域 |
| **US CSB** | 免 key；无 API，逐案 PDF（第三方 CSB Incident Wiki 116 案可助爬取清单） | 1998– | **化工爆炸决策链刻画最细**（实测 BP Texas City 全本：p.43 时间线表、分钟级时间戳、15 死 180 伤、>$1.5B、4.3 万人就地避难令） | **古雷同灾种检验侧首选**；[全文 PDF 实测 200](https://www.csb.gov/assets/1/20/csbfinalreportbp.pdf)；公有领域 |
| **UK Buncefield（MIIB 2008）** | ⚠️ **HSE 官方直链已 404（实测）**；[国家档案馆归档](https://webarchive.nationalarchives.gov.uk/) 200；[FABIG Vol.1](https://www.fabig.com/media/tpuaseey/buncefield-incident-miib-final-report-volume-1-dec2008.pdf)/[Vol.2](https://www.fabig.com/media/jkvgpiv3/buncefield-incident-miib-final-report-volume-2-dec2008.pdf) 镜像实测 200 | 单案（2005-12-11） | 六源中最贴**应急指挥决策**（应急准备专项建议卷+消防局 26 天灭火编年复盘） | 第三锚候选可用，但引用须改归档/镜像 URL；Crown copyright 非商用限制注意 |
| **UK MAIB** | gov.uk 免费；⚠️ 本机 DNS 受限未直接核实（第三方权威引用间接确认） | 约 1990s– | VDR/AIS 重建分钟级航行决策 | OGL v3；换网络环境复核 |
| **ATSB（澳）** | 免 key；逐案网页+PDF（QF32 案实测）+ 航空事件库可导出 | 2003 为主 | sequence of events 带时间戳 | CC BY 4.0；检验侧 |
| **JTSB（日）** | 免 key；逐年 HTML 表+PDF | 英文子集（航空 2001–、海事 2008–），日文全量更深 | 分钟级事故经过 | 英文子集可小批量；规模化需日文；优先级最低 |
| **ReliefWeb API v2** | ⚠️ **2025-11-01 起需预审批 appname**（未审批实测 403） | 报告 1970s–；灾害名录 1981– | situation report 正文含响应行动叙述（需 NLP 抽取） | 时间线文本锚（需加工+先申请） |

## 4. 生成侧素材源（择要）

- **GDACS**（§2）：灾害参数供给器（类型/强度/暴露人口/GLIDE 键）。
- **Open-Meteo**（已在 cds 19 源）、**NOAA CPC/PSL**（ENSO 文本产品，机读友好、公有领域）、**Oikolab/Visual Crossing**（70+ 年逐小时历史气象重建，apiKey 免费层）：灾害期气象参数重建。
- **HKO 开放数据**（免 key JSON/CSV：台风最佳路径+天气预警+地震速报）：华南台风生成侧+有限检验侧，中国相关最强官方源。
- **QWeather 和风 / 彩云**（apiKey 付费）：中国天气实况唯一现实选项。
- **data.gov.tw**（免 key，含灾害应变数据集）：中国相关政务数据唯一入口（台湾）。
- **地方志/省级地情网**：历史灾害背景。
- **public-apis 黄页本地克隆**（`~/Documents/GitHub/0ref/skill/public-apis`，1597 条，2026-07-01 更新）：已筛出上述条目；**中国大陆官方源全目录缺席**（无应急管理部/地震局/水利部）——中国源须专项接入，本盘点 §3.1 即补齐。

## 5. 已有资产复核（两个仓库 + 四个候选位置）

- **cds4polymarket**：`docs/decisions/data-source-selection-2026-05-05.md` 19 源通用盘点（含 IFRC GO/HDX）；格式（端点/免 key/特色/弃用理由）可复用为本盘点模板；`experiments/worldcup-2026-factor-calibration/data/source_ledger.md` Green/Red/黑名单三级源门控 = Factor Ledger 源门控前身。
- **Policysim-v0.2**：KB 侧五件套（三级源分级 SOP `wiki/concepts/kb-source-verification-sop.md`、辰安 API 文档、emergency-kb 盘点、17 GB 国标索引 `kb-standards-index.yaml`、辰安 28 篇 manifest SHA256 锁定）；OSINT spec Phase 2 规划源未实施。
- **知识库获取接口文档.pdf** = 辰安 KB 取数通道（2 端点、X-User-API-Key、无 kbId 枚举；kbId=1 可用、2–20 无权限）。生成侧素材管道。
- **DMO PDF 参考文献**：数据源均军事/海事，无贡献；方法借鉴（环境因子概率化）。
- **CLIProxyAPI**：LLM 代理服务器，无关。
- **media 监测报告**（`report_20260604_1200_media.html`）：云端 agent 定时任务产物（四班制），**生成端不在本机、本机无配置文件**；L1/L3 分级+滞后天数规范内嵌于报告 HTML（两张表即规范实例）；重建为灾害采集端约 1–2 天（提示词改写半天+调度 1–2h+采集增强可选）。

## 6. 缺口与硬约束（设计须吸收）

1. **2018 断档**：国家防总通告机读归档自 2018 起；此前事件靠调查报告栏目（2011+ 全文）+ 新华社通稿 + web archive，标注低置信。
2. **中国气象历史预警报文无机读存档**（台风公报过季不可追溯）→ 预警发布时间线须用省级响应通告替代，或限定日本个例用 JMA-XML。
3. **EM-DAT 无 API**（xlsx 导出）；ReliefWeb 需 appname 审批；CMA 站 WAF 拦脚本（468）且**非商用**；Buncefield HSE 直链 404。
4. **疏散令/转移人数**在官方源中最稀：省级发布会实录（媒体转录）与地方媒体为主补充。
5. 中国事件在 IFRC GO 以 GDACS 自动同步条目为主，人工行动报告薄。

## 7. 对研究的含义（详见当日文档进化讨论）

- **宽案例类成立**：台风（IBTrACS 1949– 参数 + CMA 登陆段 3h + 省厅 2020– 响应时间线 + EM-DAT 后果）与地震（USGS FDSN + PAGER）两条宽类轨道证据齐备，H3 可升级为「2 深案 + 1 宽类（N≥60）」。
- **前瞻锚协议成本大幅下降**：mem.gov.cn/省厅通告逐日可爬，常设采集（≈media 流水线重建 1–2 天）即可把「季前注册、事后盲结算」机械化。
- **D&B 数据集切割点**： disaster-KG 线（如 LLM4TyphoonKG，LLM 抽取三元组、无评测、无结算语义）已存在；本资产须以「**可结算（settleable）因子**」与之区分——因子=带判定规则/阈值/反证信号/盲评字段/来源分级的可裁定断言，非描述性三元组。

---

## 8. 网络复测记录（2026-07-19，更换 VPN 后对本机直连复测）

| 端点 | 原状态 | 复测结果 | 结论与对策 |
|---|---|---|---|
| `www.gov.uk/maib-reports`（UK MAIB） | DNS 受限，未能直接核实 | **200 ✅**（报告索引页与个案例页均通） | MAIB 升级为已核实检验侧源（OGL v3） |
| `tcdata.typhoon.org.cn`（CMA 最佳路径） | WAF 468 | **仍 468**（完整浏览器头重测同） | 非网络问题，SafeLine 反爬按客户端指纹拦截。对策：① 浏览器/Playwright 人工下载；② **IBTrACS v04r01 本身即含 CMA 最佳路径序列**，可不经原站获取 |
| `api.reliefweb.int` | 403（无 appname） | **410 Gone**（无 appname 亦然） | 网络可达，纯权限门：须先申请预审批 appname，与 VPN 无关 |
| `chroniclingamerica.loc.gov` | 403 | **仍 403** | 机器人防护，非地理问题；生成侧低优先，搁置 |
| `pm25.in` | 疑似失效 | **连接超时，确认死亡** | 从候选清单移除 |
| `yjt.zj.gov.cn`（浙江省应急厅） | 归档栏目未定位 | **连接超时（换路径同）** | 疑对境外 IP 限制——**此类中国政务站建议走境内直连而非 VPN**；浙江决策时间线暂走媒体源 |
| `public.emdat.be` | 可达 | 200（不变） | 注册表单为 JS 应用，邮箱要求仍未能机读核实 |

**复测第 1 轮总结论**（VPN 开，境外出口）：换 VPN 只解锁了 **MAIB** 一项；其余「未能核实」均为反爬指纹（CMA、LoC）、权限门（ReliefWeb）、站点死亡（pm25.in）或政务站境外 IP 限制（浙江），与网络出口无关。CMA 数据可由 IBTrACS 内置序列替代，不构成硬阻塞。

## 9. 网络复测第 2 轮（2026-07-19，关闭 VPN，境内直连，出口北京 CERNET）

| 端点 | 结果 | 结论 |
|---|---|---|
| `yjt.zj.gov.cn`（浙江省应急厅） | **200 ✅**（首页与 `/col/col1229565103/index.html` 栏目页均通） | 证实该站限制境外 IP；**浙江升级为官网可爬**（此前结论「走媒体源」作废） |
| `tcdata.typhoon.org.cn`（CMA） | **仍 468** | 境内 IP 也拦 → 确证为客户端指纹反爬，与地理无关；用浏览器/Playwright 或 IBTrACS 内置 CMA 序列 |
| `mem.gov.cn` 郑州报告 PDF | 200 ✅ | 境内直连正常 |
| `yjt.fj.gov.cn` 古雷报告 HTML | 200 ✅ | 境内直连正常 |
| `www.gov.uk/maib-reports` | 200 ✅ | 境内直连亦通（最早失败应归因于当时子代理网络环境，非 MAIB 本身限制） |
| `ncei.noaa.gov` IBTrACS bulk | 200 ✅ | 境内直连可批量下载 |
| `goadmin.ifrc.org/api/v2` | 200 ✅ | 正常 |
| `earthquake.usgs.gov` FDSN | 200 ✅ | 正常 |
| `public.emdat.be` | 200 ✅ | 正常 |
| `api.reliefweb.int` | 410 | 不变：appname 权限门，与网络无关 |
| `chroniclingamerica.loc.gov` | 403 | 不变：机器人防护，搁置 |

**复测第 2 轮总结论（最终网络指引）**：**境内直连即可覆盖全部关键源**（IBTrACS、USGS、IFRC GO、EM-DAT、MAIB、mem.gov.cn、福建/浙江省厅），采集工作无需 VPN；唯二遗留：① CMA 原站需浏览器级访问或走 IBTrACS 替代；② ReliefWeb 需申请 appname。中国政务站（浙江已证实）对境外 IP 有限制，挂 VPN 反而有害。

---

*盘点执行：6 路并行子代理（WebSearch+FetchURL 实测、本地仓库侦察），全部只读；各节「未能核实」项已就地标注。*
