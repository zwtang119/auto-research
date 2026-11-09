# 记忆「做梦」规划：auto-research 离线整合一次

> 日期：2026-11-09｜状态：**规划 + 单簇 pilot 完成；全仓做梦未执行，待用户放行**
> 依据：Anthropic《The components of agent memory》（Engineering，2026-11-06）
> 交付物：本文（规划）、`analysis/memory-dream-2026-11-09/token-accounting-wiki.md`（pilot wiki）、同目录 `COMPARISON.md`（对比报告）

## 1. 判断（结论先行）

**问题不是「笔记太多」，是四层记忆缺了「离线整合」这一层。**

本仓不缺笔记，也不缺索引，缺的是把索引反过来修正、合并、下移的后台过程。三处硬证据：

1. `docs/INDEX.md` 已经是标准的 memory representation（按主题分组、带 status / verified_at、链到 `index.json`），但自身涨到 **57.0KB / 395 行**，旁边 `docs/SCRIPTS.md` 还有 **48.5KB / 346 行**。Anthropic 给 injected context 的经验上限是 `MEMORY.md` 前 **200 行 / 25KB**；本仓入口链总量约 **118.5KB**。索引正在变成 Borges 那张和帝国一样大的地图——文章里 LAB 任务的反例是 wiki 203KB vs corpus 115KB（1.77×），收益归零。
2. 索引自己登记了 **5 处状态口径冲突 C1–C5**，全部「待裁定」；`CLAUDE.md:23` 自报 `state/progress.json` metadata drift。这正是文章说的「当时写下的 note 会 drift，错误 note 在后续 session 被读取并被信任」。本仓已发现，但没有后台修正机制。
3. 内部链接 636 条，双基准重算后 **209 条真断链（32.9%）**，另有 **128 条只是路径基准写法不一致**（写成仓库根相对路径，按 md 所在目录解析会误判）。文章把「repoint dangling links / 补 index」列为 dreaming 的标准动作。

**所以做梦≠删文件、≠大扫除。** 是加一层：用原始文档当 ground truth 校验上层摘要，按主题簇压出少量 wiki 页，把顶层压回小体积只留链接。

## 2. 文章框架与本仓映射

文章把 agent memory 定义为「从经验中获得、跨 session 保留、以可读取的 context 形式保存的知识」，明确排除 weights / in-context learning / compaction。四层自底向上：

| 层 | 文章定义 | 本仓对应 | 现状 |
|---|---|---|---|
| Transcripts | searchable event log，ground truth | `docs/investigations/`、`docs/plans/`、`analysis/` 原文 + `logs/` | **散、无统一 event log**；讨论文档 171 篇主干 + 数据产物 2268 个混在 `docs/` |
| Memory notes | salient observations / rules / facts / traps | 各篇开头的「结论 / 状态 / 裁定」段 | 有，但无 checked/unconfirmed 标记，撤回信息埋在正文 |
| Memory representations | linked wiki pages，导航用 map | `docs/INDEX.md` + `index.json` + `SCRIPTS.md` | **有但膨胀**，57KB+48.5KB，且只增不修 |
| Injected context | session 开始 preemptively load，必须很小 | `AGENTS.md` → `CLAUDE.md` → `README.md` / `OBSOLETE.md` | 根四件约 13.1KB（合规），但下一步指向 57KB 索引 |

文章对 dreaming 的定义：在 session 之间用 compute 回看 logs，**纠错、生成 notes、构建 representations、把重要内容提升到顶层、按目标重写组织方式、补跨 session 缺口**。明确不做训练、不改权重。

三个关键实验结论，决定本规划的取舍：

- **Representation + search 才有效**：Stainless 语料（35 万文件 / 4.2 亿 token）跑 128 sessions，25 题 graded criteria 13%→48%；`wiki + search` 54%→61%，`search alone` 53%，`wiki alone` 最好 48%，且每题省约 2 万 token。→ **wiki 不能替代原文检索，只做导航层。**
- **Salience 比数量重要**：Pokémon 实验里 indiscriminate 记 413 文件 / 977,930 字符只得 1 badge；只记 strategy / tested rules 的 10 文件 / 43,406 字符得 4 badges。→ **做梦要删掉的是「屏幕上看得到的信息」，不是证据原文。**
- **组织方式要按目标调**：LAB 合同任务把「共享条款表」改成「每合同一页 + 逐字引用」，facts 从 41/57 → 57/57。→ **本仓应按主题簇一页，不要建第二份全文摘要库。**

## 3. 实测基线（2026-11-09，只读脚本，未改任何文件）

| 指标 | 实测值 | 备注 |
|---|---:|---|
| 全仓文件 | 3,279 / 89.10 MB | `docs` 2,473、`evidence` 432、`analysis` 75、`papers` 204、`legacy` 72、其余 23 |
| Markdown 笔记 | 581 篇 / 5.60 MB / 78,428 行 | 全仓，含只读区 |
| 文本/结构化产物 | `.txt` 1,236、`.json` 1,144、`.jsonl` 53 | 主要落在 `docs/papers-closed-portfolio/experiments/`（2,268 个数据产物） |
| 入口链体积 | ~118.5 KB | CLAUDE 6.4 + README 4.5 + OBSOLETE 2.1 + INDEX 57.0 + SCRIPTS 48.5 |
| 已登记状态冲突 | 5 处（C1–C5） | `docs/INDEX.md` §待裁定，全部只标注不改原文 |
| 内部链接 | 636 条 | 双基准（相对当前目录 + 相对仓库根）解析 |
| 真断链 | 209 条 / 32.9% | `docs` 186、`evidence` 19（外部 `file://`，禁区不碰）、`papers` 4 |
| 基准写法不一致 | 128 条 | 可 repoint，不是文件丢失 |
| 完全重复组 | 151 组 / 1,117 冗余文件 / 4.17 MB | 绝大多数是 `.gitkeep` 与实验 prompt 原料，**属数据产物，不删** |
| 同名入口散布 | `README.md` ×24、`index.md` ×10、`CLAUDE.md` ×7、`MEMORY.md` ×5 | 多套入口互相打架，索引已登记 |
| 项目记忆目录 | 不存在 | `.workbuddy/memory/` 未建立 |

**两个测量口径的坑（已排除，勿复用错数字）**：

- 单基准断链率是 **53.0%**，虚高；128 条链接写成仓库根相对路径，按 md 所在目录解析必然失败。真实 32.9%。与用户既有工程经验一致：referenced 存绝对路径却拿相对路径比对，会把孤儿率虚高到 97%。
- 全仓 md 的 mtime 100% 落在 30 天内（worktree 检出时间），**不能用 mtime 判断笔记陈旧**，只能按正文日期与索引 status。

## 4. 做梦设计：D0–D5

### D0 冻结边界（先于任何写操作）

**只读 / 禁改**：`evidence/`（字节级证据快照，含 `.DS_Store`）、`legacy/`、`papers/`、`framework/`、`state/`、外部封存仓库 `/Users/tangzw119/Documents/GitHub/cds4worldcup`（零读写）、`docs/SECRETS.md`、`.env`。

**只标注不改原文**：C1–C5 状态口径冲突、`README.md` / `CLAUDE.md` / `docs/portfolio/project-index.md` / `docs/investigations/INDEX.md` / `analysis/README.md` 的状态正文。用户 2026-11-05 已裁定「状态冲突只标注不改原文」，本规划不推翻。

**不执行**：删除/移动任何既有文件、git commit / push、改写论文数字、自动裁决待裁定项。做梦产物一律写进**新目录**，原文保持可追溯。

### D1 纠错（transcript → notes）

- 输入：171 篇主干讨论文档的「结论 / 状态 / 裁定」段 + `index.json` 的 `status` / `verified_at`。
- 动作：逐条回查原文，标记 `checked / unconfirmed / superseded / 待裁定`；把「撤回」「不再推荐执行」「NO-GO」提升到条目级，不埋在正文。
- 产物：`dream/notes-audit.md`——只列冲突与证据位置 `path:line`，**不裁决**，交用户。
- 闸门：任何断言必须直接计算复核后入档（`CLAUDE.md` 验证纪律；2026-07-20 有 4 条代理断言 2 证伪 1 漏检的先例）。

### D2 合并（notes → representations）

- 按主题簇建 wiki 页，一主题一页、单 agent 写（LAB 反例：共享表并发写会互相擦除）。
- 首批簇：世界杯主线（20 篇）、Decision Co-Scientist（26 篇）、2026-10 token/tsinghua（36 篇）、组合治理（18 篇）。
- 每页固定五节：**当前有效结论 / 权威链（谁取代谁）/ 已验证数字（带 Green Source 位置）/ 撤回与陷阱 / 未决项**，末尾链回原文。只做导航，不复写全文。
- 硬上限：单页 ≤ 8KB、wiki 总量 ≤ 源簇 10%。超过就是没抽象。

### D3 补缺口（repoint + index）

- 重扫全仓链接，双基准判定。128 条基准写法问题登记为「建议统一为仓库根相对路径」清单，**只出清单不批量改写**；209 条真断链逐条分类（目标已删 / 拼写错 / 指向外部只读仓 / `file://` 历史链接）。
- `evidence/` 的 19 条不动，标注「证据快照只读，历史链接保留」。
- 补 wiki index、缺失主题页、跨簇反向链接。

### D4 提升（representations → injected context）

- 目标：把新 session 必读压到 **≤ 25KB / ≤ 200 行**（文章上限）。
- 手法：`docs/INDEX.md` 保留主题表与查询顺序，状态冲突明细、逐篇说明、维护沿革下移到 wiki / `index.json`；`SCRIPTS.md` 保留 capability 索引，细节下移。根四件保持 ≤ 15KB。
- 顶层只留：状态准绳一句话、禁区清单、dream wiki 入口链接、5 处冲突「待裁定」的一行提示。错误 note 不进每次 session。

### D5 验收

| 指标 | 做梦前 | 目标 | 测法 |
|---|---:|---:|---|
| 入口必读体积 | ~118.5 KB | ≤ 25 KB | 字节统计 |
| 入口必读行数 | ~900 行 | ≤ 200 行 | 行数统计 |
| 主题 wiki 覆盖 | 0 页 | 4 页（首批） | 文件计数 |
| 链接真断链 | 209（32.9%） | 分类清单 100%，禁区外修复需另行授权 | 双基准脚本 |
| 状态冲突可见性 | 埋在 5 段正文 | 1 张表 + 顶层 1 行 | 人工核对 |
| 既有原文改动 | — | **0 字节** | md5 前后比对 |
| 关键口径检索跳转 | 3–5 篇 | 1 页 | 见 `COMPARISON.md` |

**回归检查**：`python3 docs/tools/build_index.py --check` 全 path 有效；wiki 所有链接双基准可达；既有 17 个关键文件 md5 不变；`git status` 只有新增文件。

## 5. 不做什么（防止做梦变成新一轮膨胀）

- 不做全仓 wiki：文章明确「单文档 text search 可解时 wiki 无收益」，且 wiki 大于 corpus 等于没有抽象。
- 不删 1,117 个重复文件：绝大多数是实验原料与 `.gitkeep`，是数据产物不是笔记；删了破坏可复算性。
- 不用 mtime 判陈旧（见 §3）。
- 不自动裁决 C1–C5，不替用户二选一。
- 不把 pilot 的压缩比外推成准确率收益：文章 13%→48% 来自 128 sessions / 25 题 graded evaluation，本 pilot 没有评测集，不能类比。
- 不引入定时后台任务；做梦是显式触发的一次性 pass，除非用户另行要求调度。

## 6. 分阶段 go / no-go

| 阶段 | 交付 | 闸门 |
|---|---|---|
| 已完成 | 规划 + 单簇 pilot + 对比报告 | 本文 + `COMPARISON.md`，既有原文 0 改动 |
| 待放行 P1 | D1 notes-audit（171 篇结论校验） | 用户确认「按规划执行」；只读，产出新文件 |
| 待放行 P2 | D2 四簇 wiki | P1 无争议断言 ≤ 0；单页 ≤ 8KB |
| 待放行 P3 | D3 链接清单 + D4 顶层瘦身 | **需单独授权**：D4 会改 `docs/INDEX.md` / `SCRIPTS.md` 正文，触及用户「只标注不改原文」边界的历史裁定范围，先列完整改动清单再执行 |
| 待放行 P4 | D5 验收 + 是否纳入常规节奏 | 用户复核后决定 |

## 7. 后续执行可用 Prompt

```
在 auto-research 仓库执行 dreaming pass <P1/P2/P3>，严格按
docs/plans/memory-dream-2026-11-09.md 的 D0 边界：
- 输入：docs/investigations/、docs/plans/、docs/INDEX.md、docs/index.json
- ground truth 是原文，任何断言回查 path:line 后入档
- 产物只写 analysis/memory-dream-2026-11-09/ 下新文件，不改任何既有文件
- evidence/ legacy/ papers/ framework/ state/ 只读，封存仓库零读写
- 状态冲突只标注不裁决，不写回 README/CLAUDE/各 INDEX 正文
- 每页 wiki ≤ 8KB，固定五节：有效结论 / 权威链 / 已验证数字 / 撤回与陷阱 / 未决项
- 结束前报告：新增文件清单、既有文件 md5 变化数、断链双基准数字
```

## 8. 已知限制与待裁定

- 本仓**没有统一 transcript / event log**，`logs/` 与 `state/` 规模极小。文章把 transcript search 列为可能的 memory foundation，本规划暂以讨论文档原文充当 ground truth；是否补建 session log 是独立决策。
- 209 条真断链中，指向外部 `file://` 的 19 条属于证据快照原始内容，**永不修改**，会永久留在断链清单里；验收指标应写「分类 100%」而非「清零」。
- 顶层瘦身（D4）与用户 2026-11-05「状态冲突只标注不改原文」裁定可能冲突：需用户明确「瘦身是否允许改索引正文的结构、但不改状态口径文字」。
- 文章自身列的开放问题同样适用：dreaming cadence、如何防止 representation 累积 hallucination、是否以 transcript search 为 foundation——本规划不预设答案。
