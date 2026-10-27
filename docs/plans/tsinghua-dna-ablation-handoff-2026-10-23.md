# DNA 配套消融：执行 Agent 交接文档

日期：2026-10-23；交接者：gpt-6-astra。

## 1. 裁定与任务

**研究方向及服务兼容性允许进入正式启动阶段（conditional GO）；当前旧命令不能原样启动。** 下一位Agent完成下述有限工程接入、离线验收和一次隔离端到端小试后，可按用户“准备换Agent开始实验”的意图推进正式阶段。不再反复调查五月不可考细节，不把小试成功解释为历史等价。预算不足时报告所需充值，不擅自扩大支出。

本交接文件是最新执行状态说明；旧v3计划仍有“未授权/未实施”、生成2048及评分8192等过时表述。以本文件描述的当前状态和后续用户指示为准。当前没有修改正式采样配置，正式生成0/630，交接本身没有模型调用。

## 2. 路径与优先阅读

工作目录 `/Users/tangzw119/Documents/GitHub/auto-research`。

- `D` = `analysis/tsinghua-baseline-audit-20261022/D-dna-ablation-20261023`。
- 项目规则：`CLAUDE.md`、`AGENTS.md`。
- 原设计：`docs/plans/tsinghua-dna-ablation-2026-10-23.md`（原则沿用，状态/预算参数过时）。
- 最新实证：`D/compatibility-omit-max-tokens/supplement-02/REPORT.md`、`FINAL-SUMMARY.json`；配对资料`D/compatibility-omit-max-tokens/paired-01/`。
- 当前入口：`D/scripts/run_stage.py`；原调用：`D/scripts/api_client.py`；离线验证：`D/scripts/verify_protocol.py`。
- 原件：`D/frozen/`、`D/source-manifest.json`；原pilot：`D/runs/pilot/`（失败原样保留）。
- 无GT建表：`D/scripts/build_no_gt_dataset.py`，是函数模块，不是现成CLI。
- 变更记录：`analysis/tsinghua-baseline-audit-20261022/CHANGELOG.md`。

禁止读写封存cds4worldcup；证据快照与历史源只读；不碰其他既存wiki、legacy、.mimosa改动。不提交/推送，除非用户另行要求。凭证仅进程加载分析副本父目录.env供认证，不打印/写入日志。

## 3. 已确定协议

- 新增无DNA：SASR315、MAMR315。每条件3模型×3企业×35次。只整体移除五项显式企业属性，身份、政策、输出格式及交互机制保留。
- 原MAMR三轮、每轮三企业、两次中央摘要、Jaccard内容重试规则、prompt随机化及原聚合口径不变；每条件入口seed42，不声称复原历史随机序列。
- **下一步正式接入目标：所有生成、摘要和A/B评分保留temperature=0.7，不发送max_tokens，不指定推理强度。** 这是兼容性调整，不是证实五月没有设置上限。
- 不新增top_p、API seed、结构化输出模式、搜索工具。生成与评分不启用浏览/检索，允许模型API通信。
- 生成：OpenRouter `openai/gpt-oss-120b`、`deepseek/deepseek-v4-flash`；Paratera `Qwen3.5-122B-A10B`。
- A：Paratera `GLM-5.1`；B：OpenRouter `moonshotai/kimi-k2.5`与Paratera `MiniMax-M2.7`。
- 正式沿既定路由，不把控制实验的provider锁定自动带入正式。记录可见上游；不自动替换模型，尤其不换DeepSeek0731。
- 五月历史作为对照，不重跑有DNA、不重评历史、无GT。主指标SO+TO；B双判官沿用原聚合。跨期run_id不是配对数据。
- 用户已接受路由变化、随机/启动恢复差异与正常技术失败重跑；历史SDK/服务内部细节未知不再单独阻止运行。

## 4. 已完成验证及正确解释

Green Source：`D/compatibility-omit-max-tokens/supplement-02/FINAL-SUMMARY.json:1`；父代理直接执行`run.py verify`通过。历史/旧小试及冻结输入哈希未变；新增9请求各一次、无pending。

- DeepSeek企业新诊断793字符、stop、格式通过。旧APIConnectionError缺cause链，根因不可追溯；新成功不解释旧失败。
- Qwen企业YAML不规范，但原管线把正文作为text保存/传给评分，不以解析企业YAML作为前置条件。此前“因此不能运行”判断过严。
- DeepSeek摘要278字符、stop，超过prompt200字要求；Qwen179字符、stop。超字数是遵循度标记，不新增截断/重抽条件。
- GPT同Venice配对：2048空/length，省略上限174字符/stop；省略臂completion1441，低于2048，说明随机推理长度仍影响结果。
- DeepSeek同Relace配对：两臂均成功，不能全归因于删除上限。
- GLM同endpoint：8192空/length，省略后15071 completion并得到25项评分；后端版本不可核验。
- 上述为诊断覆盖，不是完整MAMR端到端执行通过，也不证明长期稳定/历史等价。

## 5. 正式启动前必须完成的有限工程接入

### A. 实际请求省略max_tokens（尚未实现）

Green Source：`D/scripts/api_client.py:26–35`仍显式发送max_tokens，且删除配置键会回落2048；评分还显式传8192。因此**只删YAML配置不够**。

建议在当前执行适配层统一省略该字段，使journal指纹记录实际发送参数；不改frozen。对生成/摘要/A/B分别离线截获最终请求，证明temperature=.7、无max_tokens/max_completion_tokens/reasoning/tools，其他字段/prompt未变。记录版本、diff、依赖与启动参数。更新旧计划顶部的状态和兼容性覆盖说明，避免后继Agent误用。

### B. 日志与恢复

已修复`run_stage.py:91–105`HTTP hook累积：finally移除本次hook。外层重试2次记[1,1]、SDK内3次记[3]、日志Pause后清理已离线验证。

剩余限制：`:71`遇历史error会暂停，不能自动重放失败后成功轨迹；command目前只保存首启（`:138–139`）。不把它描述成无人值守完整恢复。正式可分阶段有人监督执行，遇此限制保留记录并确定恢复方案；若实现自动恢复，必须离线验证原失败/成功序列与随机消费，不重发已成功或发送状态不确定的请求。记录每次启动/恢复而不覆盖旧记录。

技术失败按正常恢复处理，但必须区分超时/无响应、空正文、模型有效输出不遵循格式。原API重试与Jaccard重试是两回事。不得因评分低、正文格式或摘要超字数重抽。若空正文/空摘要/空评分再次出现，保留全响应并暂停对应工作单元；正常技术失败重跑须明确编号与采用规则，不能将空评分当有效负例，也不能悄悄改原评分器或补分。

### C. 验收与隔离端到端小试

1. 离线请求参数检查及`verify_protocol.py`；任何旧测试只因新增省略max_tokens断言变化，单独解释，不能削弱prompt/评分等价检查。
2. 用新的独立运行目录执行一个小型完整流程，覆盖三个模型MAMR轮次与摘要消费、SASR、三评委。旧pilot包含已知失败，不在旧目录恢复。当前run_stage.py默认pilot固定目录，应先加入隔离运行标识或等效安全入口。
3. 按原文本管线验收，不添加严格企业YAML/200字/全维度内容筛样规则。评分缺项旁路标记，沿原解析统计；空响应和API失败单独记录。执行完成与有效指标覆盖分开。
4. 小试用于接线检查，不计入正式630。通过后无需再重复做参数因果研究，进入正式阶段。

## 6. 余额与费用

最后查询2026-10-23余额为OpenRouter **$6.601414439**，不是实时余额；每个OpenRouter阶段前提醒用户并查询最新余额。Paratera费用未返回，不能记为零。

此前正式OpenRouter估算25.36–36.52美元是在旧预算条件下的粗估；省略max_tokens后不可用作新费用保证。当前余额不足以按旧估算覆盖全程。先利用新小试usage及当时价格重新估算，确认充值/阶段支出预算再发正式批次。原`--cap 40`是操作性阈值，不是已充值、不等于硬费用上限；无max_tokens单次费用无法严格封顶。

保留已知费用、余额变动、未知费用分别列账。未知每笔1美元是工程预留而非实际账单，不能无限累计成永久阻塞，也不能直接清零；调整记账需说明。

## 7. 阶段执行与交付

完成第5、6节后，在D目录使用经接入验收的入口，依次SASR、MAMR、A、B-kimi、B-minimax；不要并发启动共享日志入口。现有命令形态为`python3 scripts/run_stage.py --stage <阶段> --cap <已确认操作阈值>`，**仅示意，当前旧版本不可直接照跑**。

验收键：生成630；A630；Kimi630；MiniMax630。另报请求尝试数、传输失败、空输出、部分解析、有效指标覆盖，不用文件齐全代替有效性。

调用无GT建表函数`build_no_gt_dataset.build_dataset(exp_dir)`并显式落盘CSV；补齐阶段覆盖报告、主比较及限制说明。保留历史最终评分作为既定对照，不擅自给新臂照抄历史4份D4补5。历史12份parser差异为已记录限制，不在此任务重做历史评分。

最终交付包括630原始样本、三套评分、无GT表、各格覆盖与失败清单、请求/响应与成本日志、冻结配置与依赖、主比较和跨期混杂说明。全部更改记CHANGELOG。

## 8. 给下一位Agent的启动指令

> 读取本交接文档与CLAUDE.md。先完成第5节的正式请求适配及离线检查，再查询余额并告知用户资金缺口。资金/阶段预算明确后运行隔离端到端小试，通过即按阶段推进630正式输出与A/B评分。保留temperature=.7、不指定reasoning，统一省略max_tokens；不改prompt、原Jaccard与计分、不运行GT、不重评历史、不重抽有效但格式不完美的输出。不要将旧pilot/兼容性样本混入正式数据。遇异常保留证据、明确恢复，不因历史不可考再次无限调查。
## 9. 交接进度：第5节工程接入与离线验收（2026-10-23 晚，工程接入子代理，待父代理复核）

> 本节由执行接入的子代理写入；所有断言来自其离线运行产物，**属子代理结果，须经父代理直接复核后方可视为确认**。本轮零模型请求、零小试/正式启动，正式生成仍 0/630。

### 已完成（对应第5节条目）

- **§5A 实际请求省略 max_tokens**：`D/scripts/run_stage.py` 执行适配层新增 `official_request_profile`，在 `Journal.client.create` 顶部统一净化：temperature=0.7，剥离 max_tokens/max_completion_tokens/reasoning_effort/reasoning；净化先于 journal 记录 → journal 指纹=实际发送参数。生成/摘要/A/B 全部经此单一拦截点。未改 frozen/、YAML 配置、prompt/重试/评分语义；`api_client.py` 等四个平移文件与 frozen 字节一致。
- **§5B 日志与恢复**：`launches.jsonl` 逐次追加每次启动（含 resume 标记），不覆盖旧记录；`command-<stage>.json` 保持首启语义并新增 request_profile 摘要。恢复限制保留：recorded error → Pause、fingerprint mismatch → Pause，均经离线断言；未实现也不宣称无人值守自动恢复。
- **§5C1 离线验收**：新增 `python3 scripts/verify_request_profile.py`（`D/request-profile-checks/report.json`，PASS）——MockTransport 截获最终 HTTP 请求体，基线臂↔接入臂 29 请求逐条 diff，唯一差异=删除 max_tokens（生成/摘要 2048、评分 8192）；接入臂全部 temp .7、无 max_tokens/max_completion_tokens/reasoning*/tools；journal 与线上参数逐条相等；回放臂零发送输出一致。`python3 scripts/verify_protocol.py` 原样通过（480 prompt/23 Jaccard/630 行/0 mismatch），旧断言未弱化、无因新断言而变化的旧测试。
- **§5C2 隔离入口**：`--run-id` 就绪（`runs/<run-id>`，保留名/非法名拒绝；`pilot` 无 `--run-id` 直接 Pause 保护 `runs/pilot`）。**隔离端到端小试本身未运行**（按指令待资金/预算确认）。

### 验收命令（可复跑，均零网络）

```bash
cd analysis/tsinghua-baseline-audit-20261022/D-dna-ablation-20261023
python3 scripts/verify_request_profile.py   # 结果 PASS；产物 request-profile-checks/report.json
python3 scripts/verify_protocol.py          # 480/23/4/630/0 mismatch
python3 scripts/run_stage.py --stage pilot  # 预期 PAUSED: pilot stage requires --run-id（保护 runs/pilot）
```

### 关键位置

- 适配与净化：`D/scripts/run_stage.py`（`official_request_profile`、`Journal.client.create` 首行、`--run-id`/launches 记录在 `main()`）。
- 离线截获门：`D/scripts/verify_request_profile.py`；机器报告：`D/request-profile-checks/report.json`（含版本、脚本 sha256、冻结一致性、请求清单）。
- 变更记录：`analysis/tsinghua-baseline-audit-20261022/CHANGELOG.md` 2026-10-23 条目；旧计划顶部状态更新：`docs/plans/tsinghua-dna-ablation-2026-10-23.md`。

### Oracle review 状态（一次，2026-10-23 晚）

- 结论：拦截/日记/回放核心成立（净化先于指纹、同参数上网络、journal==线上逐条相等）；未发现 prompt/重试/评分语义漂移。
- 明确问题两条均已处理并回归：①保留名守卫改显式 `.lower()` 于 mkdir 前拦截 + `samefile` 别名二次检查（APFS 大小写不敏感/符号链接）；②验证器改用生产接线 `install_journal`（与 `main()` 单一来源），新增 `resolve_run_dir` 守卫回归（fakeroot 隔离）。
- 遗留政策点（未改行为，待父代理/用户裁定）：非 pilot 阶段不带 `--run-id` 仍默认 `runs/formal`（正式设计入口）；隔离小试必须显式 `--run-id`。review 期间测试副作用 `runs/FORMal` 空目录已确认空并删除。
- **父直接复核（2026-10-23 晚）**：两验证器父执行均 PASS；并发现子代理与 oracle 均漏检的回归——别名守卫原为无条件执行，导致无 `--run-id` 的正式默认路径（`runs/formal` 自指）必定 Pause，正式入口被阻断。已修复（守卫仅对显式 `run_id` 执行）并新增离线回归 `formal_default_without_run_id_ok`（临时 ROOT，不写真实 `runs/formal`）与 `formal_symlink_alias_blocks`，验证器重跑 PASS。
- **预算父查询时间戳修正**：父余额核验为会话实测 GET（2026-10-23T14:53:41.629738+00:00，HTTP 200，balance $6.601414439）；`budget-preflight-20261023/balance-parent-verification.json` 已按父指示更正（原「未提供时间戳」记载有误；父原始 GET 工件已被 explore 代理覆盖、不再存在，文件内更正为父报告的重建记录）。

### 预算预检（另一 explore 代理，父代理已独立复核）

- 来源：`D-dna-ablation-20261023/budget-preflight-20261023/REPORT.md`（explore 代理，2026-10-23，仅 GET 与离线算术，零付费请求）。
- 实时余额 $6.601414439（父 GET 独立确认）；正式 OpenRouter 分阶段 S1 $7.84 / S2 $9.81 / S3 $11.47（父逐阶段求和确认）；Qwen 摘要 1470 已父证伪更正为 490。Paratera 费用未知不记零。**当前余额不足以覆盖正式全程；资金未明确，本轮离线验收后停止。**

### 待办（不在本代理范围）

- 资金确认后的隔离端到端小试（建议 `--run-id` 如 `pilot-e2e-<date>`）→ 按第7节分阶段正式执行。
- 可选（父代理裁定）：正式阶段显式 opt-in 入口（如 `--formal`），替代当前非 pilot 阶段默认 `runs/formal` 的隐式行为。


## 10. 2026-10-24 隔离小试执行进度

最新用户授权覆盖仅小试，正式另派父验收后执行（覆盖本文件旧“通过即正式”的表述）。Paratera人民币1000元已确认；OpenRouter新run实际费用$1阶段停查，非硬单次上限。

有限入口已接入96基准调用：三模型各SASR三企业+MAMR一批，18输出全部交三评委。pilot专用 `--pilot-stop-usd 1` 替代旧全runs/SDK预留cap，不以默认40作授权；新run为 `pilot-e2e-20261024-1100`。OpenRouter未知费暂停，Paratera未知费单列继续。API失败/空正文保存后Pause，小试关闭SDK自动重试；正式原协议保留。三个离线验证器父直接执行PASS。一次Oracle review及父复核见CHANGELOG。

执行命令（已启动，勿重复启动）：
`python3 scripts/run_stage.py --stage pilot --run-id pilot-e2e-20261024-1100 --pilot-stop-usd 1`

验收产物将写入 `D/runs/pilot-e2e-20261024-1100/{REPORT.md,acceptance.json}`；日志 `D/pilot-e2e-20261024-1100.log`。新run包含源码哈希及依赖快照。正式仍未启动。

### §10 最终状态：异常退出，部分验收，未通过完整小试

PID88339已退出，系统无其他小试进程；退出原因和退出码未知，未重启/重发。64笔请求中63笔完整非空响应，最后`calls/pilot/000064.json`为Paratera MiniMax pending（已发送一次，响应未知，不是空正文）。输出12/18、评分31/54：GPT两条件全部，DeepSeek A/Kimi全部及MiniMax MAMR首企业；Qwen未开始。已落盘31评分全部完整解析。真实Jaccard追加4笔已直接复核，摘要消费与生成正文匹配通过。

OpenRouter已知实际费$0.106732955296；退出后GET余额$6.494681490。Paratera20笔费用未知（含pending），不是零。部分数据正式条件外推约$5.4203，30%余量$7.0463、当前缺$0.5517；Qwen覆盖缺失，不能当完整阶段预算保证。正式未启动。

最终报告：`D/runs/pilot-e2e-20261024-1100/REPORT.md`；机器结果`acceptance.json`、`direct-audit.json`，进程核验`process-exit-audit.json`，原口径部分无GT表`no-gt-partial.csv`。

复算：先`python3 scripts/report_pilot.py pilot-e2e-20261024-1100`，再`python3 scripts/audit_pilot_exit.py pilot-e2e-20261024-1100`（均离线）。

**恢复阻塞**：第64笔状态不明，禁止重发。先由平台核查并优先取回原响应；有权威响应后另存证据并批准恢复接入。若只确认请求终结但响应不可取，父验收裁定明确技术替代编号及采用规则后另做恢复适配；状态不明继续暂停。成功前缀必须缓存回放并校验随机消费。尚待解决37个请求位置（含pending、其后36基准调用），原Jaccard可能追加。父验收后再派恢复/正式，不自行启动。

### 2026-10-24 · 第64笔窄恢复检查（gpt-6-astra）
父报告直接复核64/63/1、单发、指纹/正文、4 Jaccard及费用投影通过。检查原journal、执行日志与实际HTTP hook：000064未保存request ID/response ID/HTTP状态/响应头；本地指纹不是平台ID。官方useApi/apiKeys/text三页只读文档快照已保存，未发现支持文本completion取回的文档；已文档化控制台费用→账单明细不保证能取回正文。无推理请求、无重启，PID88339不存在。恢复仍阻塞；用户/平台最小需以账户团队/密钥非秘密名称、2026-10-24 11:58:18.204540+08:00、MiniMax-M2.7及相邻response ID定位，提供目标ID、终态、usage/费用以及原始响应或官方只读恢复文档。详见 D-dna-ablation-20261023/runs/pilot-e2e-20261024-1100/recovery-check/REPORT.md。未取得权威响应，未修改pending，等待父审批。

## 2026-10-24 持久托管恢复：TCC阻塞，真实补齐未启动

执行者gpt-6-astra；来源用户本轮授权、原journal、launchd/TCC实测。新增scripts/host_job.py、verify_recovery_host.py及hosting-checks证据；run_stage.py加入固定64-tech01授权/采用与STOP边界。原64保持pending且原63成功文件哈希全不变。四项离线门通过，63缓存+37模拟达18/54，但launchd在脚本open被macOS Documents权限提示阻塞，托管退出码/锁/停止整体未验收；两个测试服务已卸载。一次oracle review及直接复核修复授权异常被外层重试绕过问题，八项负测PASS。GET余额$6.494681490，已知累计$0.106732955296，本轮completion零；真实仍12/18、31/54。需要用户允许Python访问Documents后继续验收；正式未启动。详见D-dna-ablation-20261023/hosting-checks/REPORT.md。

最新授权覆盖旧“状态未知不得技术替代”：允许一次另编号tech01，不代表平台确认终结。当前阻塞为独立launchd Python的Documents TCC授权，未发tech01；须先补完托管离线验收，再小试补齐监督到完成或明确暂停。不得启动正式。

## 2026-10-24 19:05 持久托管验收PASS；小试87超时暂停

执行者gpt-6-astra；来源用户权限确认、launchd新job实测、真实journal与直接离线复算。新增host_boundary_probe.py及host-pass/launchctl证据，report_pilot.py区分逻辑/物理调用及tech01采用，修正不完整Kimi预算为12均值外推630。新job退出7/host锁73/实验锁2/在途STOP后退出2通过；真实恢复监督到exit2，tech01成功，原64pending保持，原63哈希全不变。24新增尝试23成功1超时（87 APITimeoutError单发），最终18生成40评分（40完整），88物理/87逻辑。真实86缓存回放零发送、18/40产物等价通过。GET余额$6.494681490，累计OpenRouter$0.106732955296、本次新增$0；Paratera44笔未知。停止，无tech02，三个新job确认退出后卸载。详细证据D-dna-ablation-20261023/hosting-checks/REPORT.md和run/acceptance.json；正式未启动，等父裁定87。

## 2026-10-24 19:23 小试最终完整验收（待父最终复核）

执行者gpt-6-astra；用户授权87唯一tech01，父已确认原87单发超时/host exit2无signal。run_stage有限扩展64/87显式恢复映射，另增87授权，保留64授权、原journal与预算基线；verify_recovery87离线失败停止/成功补14/预算与哈希不变PASS。launchd pilot-recovery87-01监督到exit0，无新异常，已确认退出并卸载。最终18生成54评分全部完整有效；102物理/100逻辑，原64pending及87error保持服务端未知，2个tech01明确采用；最终两次真实缓存回放零发送且18/54等价PASS。report_pilot修复逻辑/物理计数及摘要索引；no-gt-final.csv18行主指标无缺失。累计OpenRouter$0.133496266296、本轮$0.026763311；最终GET余额$6.467918179；Paratera52笔费用未知。正式估计$4.67237，30%余量$6.07408非保证，正式仍未启动。最终可复跑命令及父复核边界见D-dna-ablation-20261023/runs/pilot-e2e-20261024-1100/FINAL-RECOVERY.md。

## 2026-10-24 正式 SASR315 启动授权与离线门

执行者 gpt-6-astra；Green Source：本轮直接离线验证与用户转述父直接复核。父已运行 verify_recovery87.py --final / report_pilot.py，通过18生成54有效评分、102物理/100逻辑、64/87各tech01采用，原记录保留。

本轮仅正式SASR315，runs/formal隔离pilot。启动前进程/launchctl为空、执行锁空闲、正式目录不存在。限定入口 --stage SASR --formal-sasr；正式run累计已知OpenRouter与账户增量分别监督：总$6.07、SASR$0.30停查，余额保留$0.39；非单次硬上限。Paratera1000元用户确认，未知费用单列。启动前GET余额$6.467918179，正式已知费0。Red Source预测源pilot-e2e-20261024-1100：SASR .11138/MAMR .25508/Kimi4.30592，总4.67237，30%6.07408，非保证。

覆盖旧§10重试描述：正式SDK retries=0，API错误/空正文原样保存后Pause，禁止自动技术替代；达到阈值或错误即本次授权停查，须父验收/新裁定。原prompt/Jaccard、temperature .7、省略输出cap/reasoning保持。host_job默认正式STOP接线，launchd单次托管监督到exit。

直接离线门：verify_formal_sasr.py 315截获/315输出/回放0发送、费用与账户增量/余额/空正文/超时门PASS；verify_request_profile.py PASS；verify_protocol.py 480/23/4/630、0 mismatch。报告在D/formal-entry-checks/。一次Oracle review三路返回两路服务失败：无代码启动阻塞；直接确认非数字cost在未知费用Pause前float解析问题并修复，复跑PASS；接受错误/阈值停查而非扩预算。Oracle提及SASR Jaccard追加属不准确，直接函数核对SASR单调用、Jaccard仅MAMR。冻结30源码/输入文件哈希、解释器和pip依赖见runs/formal/execution-source-snapshot.json；旧frozen未改。

## 2026-10-24 23:26 SASR315 收尾：覆盖完整，CONDITIONAL

执行者 gpt-6-astra（ses_e9181cbb9ffefr3gH9LmgwI8eU）。Green Source：直接检查 launchctl、进程、原始 journal/raw、启动及冻结哈希，并执行独立离线 `D/scripts/audit_formal_sasr.py`；机器报告 `D/runs/formal/sasr-acceptance.json:1`，详情 `D/runs/formal/SASR-CLOSEOUT.md:1`（D 定义见本交接/原计划）。

- 接管时唯一worker50775/run_stage50783，launchd runs=1；续记 supervision.jsonl 至退出。2026-10-24T23:26:00+08:00 host exit0、signal null，两个PID均已退出。未重启或重发，未启动MAMR。
- 315 journal completed、315 raw、315次HTTP单发；3模型×3企业各35，全部非空且正文逐笔对应，参数temperature=.7、仅model/messages/temperature，指纹及路由通过；30启动源码/输入哈希与9冻结哈希一致。
- **不是315全部有效成功**：314 finish_reason=stop；000054（GPT/SPACETIMETECH/run019）正文627字符，但finish_reason=error、choice.error=502 Network connection lost / provider_unavailable。现运行入口只拦API异常/空正文/tools，未拦该非空provider错误，因此exit0不能代表响应全通过。原件保持；不自动重抽或排除，异常采用/技术处理由父裁定。结构验收PASS，总体CONDITIONAL；内容/评分有效性未验收。
- OpenRouter已知$0.06827449496；起始$6.467918179→结束GET余额$6.399643723，account usage delta $0.068274456，差$0.00000003896；低于SASR$0.30/总$6.07，余额高于$0.39。Paratera105笔费用未知，单列，人民币1000元确认不等于实际花费。
- 新增独立audit脚本及JSON/收尾报告；未改运行源码/原journal/raw/frozen。一次Oracle review部分服务失败，主路未取得新audit全文，不能称完整审阅通过；其指出completed/exit0不等于有效性，经直接代码核对确认，audit对全部响应检查finish_reason及error字段。
- 父复算：在仓库根运行 `python3 analysis/tsinghua-baseline-audit-20261022/D-dna-ablation-20261023/scripts/audit_formal_sasr.py`，零网络，仅重写验收JSON；预期structural_checks=PASS、status=CONDITIONAL、唯一异常000054。脚本退出0仅表示结构检查通过。MAMR由另派代理处理，本任务到SASR收尾停止。


## 2026-10-24 正式SASR退出与验收保留意见

Green Source：D/runs/formal/acceptance-SASR.json:1、REPORT-SASR.md:1；执行者gpt-6-astra直接复算。launchd formal-sasr-01已监督到exit0/no signal，进程消失并卸载。315物理/逻辑请求、9格各35、315非空；**314正常stop，000054内嵌provider error（502 Network connection lost.）带部分正文，SASR未通过315有效验收**。对应gpt-oss-120b/SPACETIMETECH/run_019。执行器未识别HTTP200的choice.error，未即时暂停而继续完成；离线测试与Oracle也漏检，最终逐条验收发现。原响应/输出/冻结版本原样保存，STOP阻止后续发送，未自动重跑。父下一步先裁定该异常及有限错误闸门修复/负测，再决定唯一技术替代；禁止重跑成功314或直接MAMR。

315参数/原prompt seed42重建/正文对应/指纹及30冻结文件哈希PASS。OpenRouter已知$0.06827449496、账户增量$0.068274456、余额$6.399643723；差3.896e-8分别保留。Paratera105费用未知不记零。父复算：在D运行python3 scripts/report_formal_sasr.py（零网络，输出REQUIRES_PARENT_REVIEW及唯一错误）。原小试父复核18/54、102/100、64/87各tech01通过已按用户报告记录。本次仅SASR，MAMR/评分未启动，无提交推送。

## 2026-10-24 SASR000054 唯一tech01恢复完成

执行者gpt-6-astra；来源用户本轮授权、原journal、直接MockTransport/真实launchd执行。Green Source：D-dna-ablation-20261023/runs/formal/recovery-000054-tech01-v1/REPORT.md:1、acceptance.json:1。父原SASR复核按用户报告记录，并修改前直接复算确认315/315/9×35/30+9hash、唯一627字符provider error。新增错误保存后Pause及回放检查，独立54-tech01单发入口/显式采用评分视图/七场景离线验证/恢复audit；host STOP有限接线。旧启动快照原样保留，新版执行快照26文件；647原证据hash不变。tech01正常stop1267字符，host exit0/no signal且卸载；315采用/316物理/314成功未重发。总已知OpenRouter$0.06858898396（新增.000314489），最新GET$6.399643723尚未体现新增费，差额.00031452796保留；Paratera105未知。一次Oracle因新文件上下文缺失未完整审阅，具体断言直接复核记录于REPORT。未启动MAMR/评分、不提交；后续使用recover_sasr54.py verify与audit_sasr54.py零网络验收。

最新评分须走run_stage的scoring_row采用适配；原raw保持异常证据，不能直接用于54评分。旧audit_formal_sasr.py保留历史口径，恢复后源码hash/最后checkpoint检查不再适用；父验收改用D/scripts/audit_sasr54.py。详细版本/费用差额/Oracle复核与命令见上述REPORT。


## 2026-10-25 正式MAMR v1：第18笔provider error，已暂停

执行者gpt-6-astra；Green Source：D/runs/formal/mamr-execution-v1/REPORT.md:1、acceptance.json:1。用户授权仅MAMR315。本会话启动前直接audit_sasr54 PASS并归档；GET余额6.399329234已含tech01。有限扩展--formal-mamr、阶段.60/原总6.07、独立阶段baseline与STOP-MAMR；原prompt/Jaccard/seed42/temp.7无cap/reasoning。完整离线1155/315/210摘要/630消费/回放0及错误门PASS，一次Oracle partial review已逐项直接复核。版本化36文件启动快照未覆盖SASR。

launchd formal-mamr-v1持续监督到exit2/no signal并卸载。MAMR18单发17成功，第18 GPT run002 round2 ISPACE，DekaLLM 502 provider_unavailable/Connection closed，finish_reason error、正文null，响应全保留且即时Pause，无自动重发。MAMR3/315完整raw，总SASR315+MAMR3=318/630；3摘要，8成功后续消费，0内容重试。STOP-MAMR已写，等父裁定技术恢复，不启动评分。已知MAMR OR .005318233、正式.07390721696，GET余额6.394328521；正式账户delta.073589658，与known差.00031755896单列。Paratera正式105未知，本阶段0。

975既存文件hash全不变，launches只追加一条且旧前缀hash相等；原647保护中646不变、launches前缀不变，SASR原件/adoption不变。旧audit_sasr54及verify_adoption全文件日志锁无法适配新阶段追加，旧文件未改；新audit显式前缀验证后复用adoption检查。后续评分需父处理scoring_row同一日志锁兼容点。父复算：在D运行 python3 scripts/audit_formal_mamr.py，预期PAUSED_PREFIX_VERIFIED/3raw/18请求/唯一error18。未提交推送。


## 2026-10-25 MAMR18唯一tech01恢复：315生成验收PASS，结束账户闸门暂停

执行者gpt-6-astra。Green Source：D/runs/formal/mamr-recovery18-tech01-v1/{REPORT.md,acceptance.json,final-closeout.json}:1。父初始复核经本代理直接重跑确认。固定tech01原路由/原request，真实17缓存零重发；离线失败两次启动仅1send，成功接续315/回放0send，39项新版本快照。一次Oracle partial review与直接复核记录保留。

原launchd host10892/child10910持续监督到exit2/no signal并卸载（无重启）；MAMR315+SASR315=630采用。1206物理/1205逻辑，唯一原18error保留，tech01正常采用；全部1205采用请求正常stop。210摘要、680实际消费含50原Jaccard内容重试，315raw重建完全一致。975初始既存文件及恢复前1010文件hash不变，launches仅追加且旧前缀不变，原SASR/adoption/baseline不变。

MAMR OR已知.356322175708，正式生成累计.424911159668；Paratera490未知。结束GET余额4.894422258，正式账户delta1.573495921、MAMR账户delta1.504906976触发.60阶段账户闸门，故无complete-MAMR.json，但315生成已完成验收。账户delta减生成known=1.148584761332，期间另代理获授权并行评分，须按独立评分账本归因，不当MAMR费用。总6.07及两条原baseline未改。Qwen后期16–18请求/30min与原16–17基线相近，无新限流/持续减速。

本代理只监督/验收生成，未启动评分。父复算在D运行python3 scripts/audit_formal_mamr.py，预期PASS/315/630/1206物理1205逻辑/tech01 adopted/210摘要680消费50重试；物理原error18另见final-closeout.json。315 raw hashes和9格覆盖已固定，可供独立评分冻结消费。未提交推送。
