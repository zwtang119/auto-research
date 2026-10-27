# 三样张视觉/PDF预检设计 review

日期：2026-10-27；执行者：gpt-6.1-sol。

**结论：3份预备PDF已交付，离线构建、CJK实际字体与完整可见正文检查通过；视觉未确认，不能称视觉通过、Kami READY或最终交付。暂不据此锁版/启动630批量。**

## Context / Scope

仅检查旧冻结的SASR×1、MAMR×2，每份含三评委。来源为 `analysis/tsinghua-baseline-audit-20261022/report-adapter-prep-20261026/samples/` 的三HTML及对应JSON，不读取活跃D、不消费最终1890数据、不输出统计结论。来源README明确样张非PDF且未视觉验收：`analysis/tsinghua-baseline-audit-20261022/report-adapter-prep-20261026/README.md:53-54`。

本报告中的 **Green Source** 为本轮直接运行的浏览器DOM、PDF字体/文本及hash检查；样张模型回答/评分/思考仍为 **Red Source**，冻结manifest版本 `cead1b0ecdbd9a3424b027713bdf578a7f181824f4fe714b827ef176043e5c08`，不据此判断现实事实或统计效应。

为缩短路径，以下 **P** 仅指完整路径 `analysis/tsinghua-baseline-audit-20261022/report-visual-preflight-20261027/`；例如 `P/checks/run4/SUMMARY.md:5` 是该目录下的同名文件。没有修改兄弟适配器/统计目录或 historical-acceptance-20261027，未使用git、oracle/子代理、外部字体请求、模型/API或实验启停。

### 原要求与本次交付边界

- 父计划允许独立轻量模板、无GT不展示、仅呈现原文/轮次/评分/诊断：`docs/plans/tsinghua-dna-ablation-2026-10-23.md:123`。因此保留现有轻模板，不顺手迁移模板或计分。
- 适配方案要求先三样张、CJK实际绘制、逐页看图；不能看图必须称视觉未确认：`docs/plans/tsinghua-dna-ablation-report-adapter-2026-10-26.md:90-94`。本次满足三样张构建/字体证据，**未满足实际看图**。
- 方案默认思考折叠、另设全文版，正文要求保留prompt/可见输出/评分/诊断/来源：`docs/plans/tsinghua-dna-ablation-report-adapter-2026-10-26.md:100-105`。本次PDF明确不含折叠思考正文；完整留痕仅JSON/HTML，不冒称完整PDF。
- 原门槛写“页数符合合同”但未给具体页数：`docs/plans/tsinghua-dna-ablation-report-adapter-2026-10-26.md:115`。**合同待裁定**，23/26/35不是人为制定的页数目标或PASS上限。

## Findings

### F1 · 阻断锁版：图像未实际呈现，不能给视觉PASS

**Green Source：**本机Chromium 149.0.7827.55实际加载三HTML，生成1440×1000桌面、print媒体、回答区和长思考展开截图；PDF全部84页已栅格化，另有放大页与逐页联系表。流程在 `P/scripts/preflight.py:64` 起；最终证据索引 `P/evidence-gallery.html:1`，文件清单 `P/checks/artifact-manifest.json:1`。

MCP浏览器也实际导航MAMR001、完成截图，但工具输出仅含图片文件链接，未向本会话提供可见图像。没有可用的本地图片查看返回通道；没有安装/下载或以额外模型绕过。**没有一页可以记作“已目视确认”**。这里不是“有截图所以通过”，而是“已生成图像证据，等待父实际看图”。

未确认项：模板占位符专项扫描（未建立词表，不能据文本完整性声称无占位符）、CJK字形外观/缺字方框、标题悬挂与孤行、长pre跨页美观、屏幕/打印对比度、折叠展开后阅读舒适性。自动字体/文字完整性/越界检查不能替代这些。

### F2 · 已在新副本修复：默认PDF的思考省略提示不足

源HTML的 `<details>` 均默认关闭，打印只留下summary；原版内存PDF无明确“本PDF未收录”提示（`P/checks/run4/results.json:189`、`:629`、`:1021`）。源尾部“未截断reasoning”用于JSON/HTML语境，不能被误读为PDF已完整交付。

修复仅新副本：首屏增加预备范围及“PDF不含思考正文、非完整留痕版”，打印每处summary追加明确省略提示；不折叠/删去回答。见 `P/scripts/preflight.py:10-26`，实际样张 `P/samples/MAMR--deepseek-v4-flash--ISPACE--001.html:7-24`；逐份差异 `P/patches/MAMR--deepseek-v4-flash--ISPACE--001.diff:1`，另外两份同名diff。JSON/所有pre原文不变。

默认HTML仍允许展开完整reasoning；PDF是明确标识的正文预备版，而非全文思考版。父须裁定是否需要 `--with-reasoning` 全文PDF；本轮未额外生成该版本。

### F3 · 已在新副本修复：自动字体回退产生Type3，Poppler重排文本

**Green Source：**初次样张原文pre采用系统monospace，浏览器实测CJK回退PingFang；`P/checks/run2/results.json:213`、`P/checks/run2/MAMR--deepseek-v4-flash--ISPACE--001--fonts.txt:1` 显示嵌入Type3。PyMuPDF完整抽取，但Poppler部分回答有数字/文字重排，不把此误报为数据丢失。

显式将pre设为 `Courier,"Songti SC",monospace` 后，最终三PDF的CJK实际span仅使用 `STSongti-SC-Regular/Bold`，不是只检查font-family声明。三份 `pdffonts` 均为嵌入CID TrueType、有Unicode映射、无Type3；全部可见pre块在两引擎中完整匹配。证据：`P/scripts/preflight.py:14`、`P/checks/run4/SUMMARY.md:5-33` 及对应 `--fonts.txt`。没有外部字体请求，均为本机既有字体。

这确认“实际用CJK字体绘制并可抽取”，但不替代逐页目视字形验收。跨机器字体可用性、WeasyPrint表现未验证。

### F4 · 内容检查通过：JSON关联、完整回答、无新增GT

**Green Source：**全部三样张的生成YAML字节hash与JSON来源hash匹配；每轮生成回答与JSON调用message.content唯一精确匹配；三评委canonical key及evaluation.input_sha256与样张输入一致；JSON六源文件hash终检均未变。源文件路径/hash见 `P/checks/source-manifest.json:1`，源未改复核 `P/checks/run4/source-unchanged.json:1`。

生成回答、三评委API可见回答、完整request/prompt、原evaluation逐项与HTML pre关联；只允许HTML解析规范去掉pre开头一个LF（MiniMax原回答有三个起始LF）。PDF检查仅NFKC＋去空白，不允许删改正文字符：三样张46个可见pre块全部可从PyMuPDF和Poppler完整找回。见 `P/checks/run4/SUMMARY.md:5-33`、`P/scripts/verify_delivery.py:1`。这是**可见正文**完整性，不包括折叠思考，不声称PDF原字节等同JSON。

无GT JSON键/展示标题、未新增GT栏位。源SASR样张已有tech01采用映射与“原请求服务端终态未知”诊断，保持展开、不删除：`P/original/SASR--gpt-oss-120b--SPACETIMETECH--019.html:51-387`。

限制：只检这些bundle的内部一致性与源样张hash，未回查blob、外部冻结inventory或630/1890全覆盖；不能替代并行历史验收，也不对评分正确性/模型事实做判断。

### F5 · 长文本分页自动检查通过，表格不适用；设计可读性仍待看图

**Green Source：**最终PDF分别23、26、35页（`P/checks/run4/SUMMARY.md:7,17,27`）；无空白页、无页面外文字框、无U+FFFD；1440×1000 screen/print媒体DOM未发现水平溢出。逐页原始文字与字体命令输出在 `P/checks/run4/`，84页缩略图在 `P/raster/`。

源样张没有HTML table，评分/采用映射以pre JSON展示：**表格溢出N/A，不是表格模板通过**。PDF长文本未抽取丢失，不等于分页美观通过。SASR的view_sha256大映射、完整request和JSON转义换行造成长篇正文；不为压页擅自折叠回答或删减溯源。是否另做评分速览/采用映射附录应由父作为后续设计裁定，本轮未扩范围。

## 交付清单与复核命令

三份PDF完整仓库路径：

1. `analysis/tsinghua-baseline-audit-20261022/report-visual-preflight-20261027/pdf/MAMR--deepseek-v4-flash--ISPACE--001.pdf` — 23页。
2. `analysis/tsinghua-baseline-audit-20261022/report-visual-preflight-20261027/pdf/MAMR--deepseek-v4-flash--ISPACE--002.pdf` — 26页。
3. `analysis/tsinghua-baseline-audit-20261022/report-visual-preflight-20261027/pdf/SASR--gpt-oss-120b--SPACETIMETECH--019.pdf` — 35页。

仓库根：

```sh
P=analysis/tsinghua-baseline-audit-20261022/report-visual-preflight-20261027
python3 -B "$P/scripts/verify_delivery.py"
open "$P/evidence-gallery.html"
open "$P/pdf/SASR--gpt-oss-120b--SPACETIMETECH--019.pdf"
pdffonts "$P/pdf/MAMR--deepseek-v4-flash--ISPACE--001.pdf"
pdfinfo "$P/pdf/MAMR--deepseek-v4-flash--ISPACE--001.pdf"
pdftotext -layout "$P/pdf/MAMR--deepseek-v4-flash--ISPACE--001.pdf" -
```

只读检查应输出 `CONTENT_CHECK_PASS_VISUAL_UNCONFIRMED`。渲染复现命令/覆盖警告、环境版本、证据目录与所有限制见 `P/README.md:1`。`run1/2/3`仅过程留痕，最终权威为 `checks/run4/`。Chromium作为本轮预检引擎；**未执行Kami doctor/check-content/deliver或WeasyPrint链路，不能称该原计划构建路径已通过**。

## Recommendations / 待父裁定

1. **先闭合视觉闸门**：在可见图像环境打开离线gallery，逐页查看三份PDF全部84页，并核对桌面/print/回答/展开reasoning截图；逐项记录页号与结果后才能锁版。当前只可接收为“构建通过、视觉未确认”。
2. 审批 `patches/*.diff` 是否合入父适配器。本轮只改新副本，未代替父作合并。优先保留明确省略提示与显式CJK字体回退。
3. 裁定默认正文PDF＋HTML/JSON附件是否为足够交付，还是需另做全文思考PDF；任何选择都不能把折叠思考当成已完整打印，也不能折叠/省掉回答来压页。
4. 页数合同仍未定，暂只记实测。裁定渲染引擎（本机Chromium vs 原方案WeasyPrint）和目标字体环境后再做验收；不要按本轮23/26/35页倒推合同。
5. 不从三个旧样张外推最终1890数据或630报告可交付；保持与历史/统计并行项解耦。
