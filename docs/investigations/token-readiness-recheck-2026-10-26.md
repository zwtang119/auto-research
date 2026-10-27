# Token 复核更正说明与有限接入准备

日期：2026-10-26；执行者：OpenCode gpt-6.1-sol；范围：计划 Item2。

## 结论

**新版本离线准备包已建立，最终发布仍 NO-GO；不宣称实验完成或端到端 ready。**
新包 `analysis/token-final-readiness-20261026/README.md:1` 为操作入口；冻结审计依据是 `analysis/token-readiness-audit-20261026/REPORT.md:7`，尤其其 §7（`:90`）。旧暂行报告与旧包不覆盖、不改写；本说明是新的更正入口。

### 取代关系（明确撤回旧流程）

旧 `analysis/token-imputation-audit-20261026/append-1023-1025-checklist.md` 的整批 ADD-only 接入流程由本说明及新包 **replacement-view 完全取代，不再推荐执行**。旧4,498条1023/1025快照必须superseded；只保留五月4,319+benchmark3,446=7,765行，再由新最终冻结实验替代两实验。此次replacement-preview只演示审计快照替代，不能充当最终冻结发布。五月锚点迁移估算仍是五月Red Source / item1-v1，不与1023原生行混删。

## 更正旧暂行版

Green Source：Item1冻结审计的字段/请求记录复算，不是计费协议或完整物理发送全集。

1. 撤回旧 `docs/investigations/token-report-2026-10-26.md:119-129` 中确定provider mode及五月外推。保留原生prompt/completion/total/reasoning；语义unknown。reasoning>completion只标冲突，不证明独立计费或应相加；相反不等式也不证明包含协议。completion−reasoning仅算术差额，不是实测可见输出。reasoning=0不证明无隐藏思考。字段级旧/新值见新包 `field-corrections.csv:1`；旧S0–S4历史估算保留原身份，不升级测量。
2. 更正旧报告 `:141-147` 的SASR均值1,194/1,299/4,326及35条分母：冻结1023正式SASR各模型均为105条，总315条企业×run请求。

| 模型 | 五月原生completion和 / n / 均值 | 1023冻结completion和 / n / 均值 |
|---|---|---|
| Qwen | 452057 / 105 / 4305.3048 | 443310 / 105 / **4222** |
| DeepSeek | 84045 / 105 / 800.4286 | 128107 / 105 / **1220.0667** |
| GPT-OSS | 85430 / 105 / 813.6190 | 132639 / 105 / **1263.2286** |

来源：审计 `REPORT.md:65-75`；编排者直接复核记录见下节。不是本轮新API测量。nemotron五月05-05为85条，05-06另85条；400=315+85只对应首批，全集485=315+170，不能混分子/分母。MAMR各模型35个joint episodes，不能混为SASR请求数。
3. **五月原生头条不变**：matched生成SASR808076、MAMR3101262，主比3.8378×、episode比11.5135×；全部评估9300054。MAMR共享usage不能三份重复计。来源：审计 `REPORT.md:59-63`。迁移编排锚点749705为1023原生；用于五月仍是Red Source / item1-v1 / ORCH-MEAN，不是五月实测。
4. 撤回“两个config同2048，故排除上限影响”的因果结论。**操作者确认（2026-10-26）：1023/1025无限制，五月既往也未执行限制。** 此为操作者说明，与历史请求原件证据分栏：归档1023正式请求和1025 prepared request_json省略max_tokens（审计 `REPORT.md:77-83`）；五月逐HTTP请求/实际执行完整历史证据不足。保持原生usage不截断、不补齐；不以新API探针验证，也不从配置值或超限现象推出全时期因果关系。

## 复核记录与离线验证

**编排者直接核验（用户提供，非本执行者新增断言）：** 已运行 `python3 analysis/token-readiness-audit-20261026/audit.py audit`，得到 `AUDIT PASS; completion NO-GO`；独立zipfile循环旧thinking-inputs.zip正式SASR得到GPT105/132639、DeepSeek105/128107、Qwen105/443310；独立csv.Counter得到may4319、benchmark3446、1023 3231、1025 1267，保留7765、替代4498。此记录按提供者署名入档，未冒称本轮重新执行了审计脚本。

本执行者直接离线验证：新工具只读Item1归档，校验完整zip集合/源hash，再校验其中旧thinking-inputs.zip与manifest。新投影逐行原生四字段未变；historical keep视图逐行相等；2条pending→completed记录只有hash/状态修订，不增加同源发送。19项unittest通过，覆盖 §7 最小集及hash/manifest、冻结改内容、symlink越界、未闭合coverage等；测试日志见新包 `test-results.txt:1`。

命令：
```sh
PYTHONDONTWRITEBYTECODE=1 python3 analysis/token-final-readiness-20261026/readiness.py dry-run
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s analysis/token-final-readiness-20261026 -p 'test_*.py' -v
PYTHONDONTWRITEBYTECODE=1 python3 analysis/token-final-readiness-20261026/readiness.py verify-release
```

## 已实现与未实现边界

已实现安全ledger/master投影、字段更正登记、replacement-view离线核心、源文件集合/hash严格校验、换call_id拒绝、run/attempt命名空间、pending替代、coverage与已知小计、双遍完整集合/内容/链接目标验证（库函数，合成夹具验证）、发布哈希清单。

**未实现生产可信完成凭据审批与scope/adoption验证；不自动决定pilot/technical/config-invalidated、独立重复实验与恢复重发分类。** 1025 prepared/pending/complete不等于发送收据，缺usage不填0。此次5346条新观察含未闭合和待分类来源，不作正式全集/项目最终量。没有对活动实验执行冻结，双遍库测试不升级原非原子审计快照为final。工具发布gate始终NO-GO，直至另行实现可信审批集成；未来即使槽位满也需双方整体可接受终态、退出凭据、停写与无补跑确认、新冻结输入及scope/adoption映射。详见新包 `README.md:32` 起。

未修改旧包、Item1审计包、活动实验或历史源仓；无API、进程控制、代理或oracle调用。既有工作区改动保持原样。
