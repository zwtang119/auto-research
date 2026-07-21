# Mimo Goal 模式任务集

> **用途**：每个 Goal 是一个可以直接发给 Mimo 的 `/goal` 指令。
> **原理**：Goal 模式下，独立的验证模型会审查 Mimo 的全部工作历史，判断停止条件是否真正满足。满足才停，不满足就反馈差距继续。
> **前提**：Phase 1 交叉验证已完成，人类已看过验证结果。

---

## 任务编排

```
Goal A（修复已确认的问题）  ← 可以最先跑
   ↓
Goal B（修复后视觉回归验证）  ← 依赖 A 完成
   ↓
Goal C（全站 CI 绿灯）  ← 依赖 A 完成，可与 B 并行
   ↓
Goal D（站点部署就绪检查）  ← 依赖 B + C 都完成
```

---

## Goal A：修复已确认的问题

### 停止条件

```
/goal 以下条件全部满足：

1. cdspath.json 中所有球队的 qualification.scenarios[].trigger 字段全部为中文（
   不包含 "Win all"、"guaranteed"、"Losing to"、"Lose all"、"Qualification depends" 等英文模板）
2. cdspath.json 中所有球队的 championship.bracket_dependency 字段使用中文轮次名
   （16强/八强/半决赛/决赛，不使用 R16/QF/SF/Final）
3. python3 scripts/build_site_data.py 以 exit code 0 完成
4. python3 -m pytest tests/ -q 全部通过
5. git status 显示的变更文件仅在 site/data/、src/cds/、scripts/ 范围内（无越界修改）
6. results/ops/ 中存在本次修复的变更日志，记录了改了什么、为什么改
```

### 给 Mimo 的上下文（随 Goal 一起发）

```
## 背景
视觉验证确认：球队详情页的"CDS 路径分析"→"关键情景"区域，
scenario 的 trigger 字段全部为英文（如 "Win all remaining matches → guaranteed top 2"），
bracket_dependency 也为英文（如 "R16 opponent: W85; QF opponent: W95"）。
这违反了 Spec 1.1 "Use plain Chinese that football fans understand"。

## 修改指引
1. 找到生成 site/data/cds-paths.json 的源头脚本（可能在 scripts/ 或 src/cds/ 中）
2. 将 scenario trigger 的英文模板翻译为中文，映射如下：
   - "Win all remaining matches → guaranteed top 2" 
     → "赢下全部剩余比赛 → 确保前二出线"
   - "Already guaranteed qualification (all outcomes → top 2)" 
     → "已确保出线（所有结果都是前二）"
   - "Losing to {team} → qualification at risk ({n} of {total} scenarios in danger zone)" 
     → "输给 {team} → 出线危险（{total} 种情况中有 {n} 种不利）"
   - "Lose all 3 group matches → eliminated" 
     → "小组赛三场全负 → 淘汰"
   - "Qualification depends on specific match results" 
     → "出线取决于具体赛果"
3. 将 bracket_dependency 中的轮次名映射：
   - R32 → 32强, R16 → 16强, QF → 八强, SF → 半决赛, Final → 决赛
   - "opponent" → "对手"
4. 重新运行 build_site_data.py 生成新的 site/data/cds-paths.json
5. 跑测试确认没有破坏
6. 写变更日志到 results/ops/

## 约束
- 不要修改 site/js/ 中的渲染代码，只改数据生成层
- 不要修改 wiki/、schema/、templates/
- 保持所有概率数字不变
```

---

## Goal B：修复后视觉回归验证

### 停止条件

```
/goal 以下条件全部满足：

1. 本地服务器已启动，以下页面截图已保存到 dogfood-output/screenshots/postfix/：
   - 首页桌面端 (1280×800)
   - 首页移动端 (390×844)
   - 阿根廷详情页桌面端
   - 巴拿马详情页桌面端（简版队）
   - 全景页桌面端
2. 每张截图中确认：
   - 情景描述（trigger）全部为中文
   - Bracket 依赖全部为中文
   - 概率数字与修复前一致（未因翻译而改变）
3. 首页桌面端 Hero 区域为双列布局（未被破坏）
4. 浏览器 Console 无红色 JavaScript 错误
5. dogfood-output/reports/postfix-regression-{日期}.md 已写入，
   包含每页对比结果和"无新回归"确认
```

### 给 Mimo 的上下文

```
## 背景
Goal A 修复了路径分析中的英文文本。现在需要视觉确认：
a) 修复生效（英文→中文）
b) 没有引入新问题

## 修复前的基线截图
对比基准在 dogfood-output/screenshots/crossval/ 目录下：
- crossval-issue002-scenarios.png（修复前的英文情景）
- crossval-issue002-bracket.png（修复前的英文 Bracket）
- crossval-issue003-desktop.png（修复前的首页布局）

## 检查步骤
1. python3 scripts/build_site_data.py
2. cd site && python3 -m http.server 8000
3. 对比修复前后截图，确认：
   - trigger 从英文变为了中文
   - bracket_dependency 从 R16/QF 变为了 16强/八强
   - 概率数字（如 20.9%、47.9%）没有变化
   - 首页布局还是双列，没有被破坏
   - Console 无 JS 错误
4. 写回归报告
```

---

## Goal C：全站 CI 绿灯

### 停止条件

```
/goal 以下条件全部满足：

1. python3 -m pytest tests/ -q 全部通过（0 failed）
2. python3 scripts/build_site_data.py 以 exit code 0 退出
3. python3 scripts/verify.py --root wiki/ 无新增 P0/P1 问题
4. grep -rn "ROI\|PnL\|Sharpe\|仓位" site/data/ 无命中
   （或在 grep 命中时，确认命中的内容不渲染在用户可见的页面上）
5. grep -rn "Kimi\|小米\|Xiaomi\|MiMo" site/ 无命中
6. grep -rn "投注建议\|低估\|高估\|value bet" site/ 无命中
```

### 给 Mimo 的上下文

```
## 背景
站点经过多轮修改，需要确认所有测试和合规检查通过。

## 检查清单
1. 运行全部测试
2. 运行站点数据构建
3. 运行 wiki 验证
4. 禁词扫描（品牌泄露 + 投注语言）
5. 如果发现问题，修复它，然后重新检查
6. 如果 baselines-data.js 的 description 字段含禁词但 UI 不渲染，
   在 results/ops/ 中记录为"数据卫生问题，不影响用户"

## 约束
- 不要删除或跳过测试来让它们通过
- 不要用 --ignore 跳过失败的测试文件
- 如果某个测试确实需要跳过，在 results/ops/ 中记录原因
```

---

## Goal D：站点部署就绪检查

### 停止条件

```
/goal 以下条件全部满足：

1. git status 显示所有变更已 commit（working tree clean）
2. commit message 遵循 conventional commit 格式
3. site/ 目录下不包含 AGENTS.md、.playwright-mcp/、docs/references/ 的内容
4. git diff --staged 不包含以下敏感路径：
   AGENTS.md、.playwright-mcp/、docs/references/、.mimocode/
5. python3 -m http.server 8000 --directory site 启动后，
   以下页面均可正常加载（HTTP 200，无白屏）：
   - /
   - /panorama.html
   - /teams.html
   - /team.html?team=argentina
   - /match.html
6. dogfood-output/reports/deploy-readiness-{日期}.md 已写入，
   包含：commit hash、变更文件清单、5 个页面状态、合规扫描结果
```

### 给 Mimo 的上下文

```
## 背景
Goal A 修复 + Goal B 视觉验证 + Goal C CI 绿灯都已完成。
现在做最后一道部署门控。

## 检查项
1. 所有变更已 commit，无未暂存文件
2. commit message 格式正确
3. 敏感文件没有被误 commit
4. 站点所有页面可访问
5. 写部署就绪报告

## 注意
- 这个 Goal 不负责 push，只负责确认"可以 push"
- 最终 push 由人类执行
```

---

## 如何使用

### 方式一：逐个 Goal 执行（推荐）

等 Phase 1 完成后，按顺序发给 Mimo：

```
Phase 1 完成（正在跑）
    ↓
复制 Goal A 的停止条件 + 上下文 → 发给 Mimo → /goal ...
    ↓ 等 Mimo 自己完成
复制 Goal B 的停止条件 + 上下文 → 发给 Mimo → /goal ...
    ↓ Goal C 可以和 B 并行
    ↓
Goal D → 最后确认 → 人类 push
```

### 方式二：合并为一个长 Goal

如果想让 Mimo 一次跑完全部：

```
/goal Goal A 的 6 个条件全部满足，
AND Goal B 的 5 个条件全部满足，
AND Goal C 的 6 个条件全部满足，
AND Goal D 的 6 个条件全部满足
```

风险：如果中途某个条件卡住，整个 Goal 会持续运行。建议只在时间充裕时使用。

### 方式三：融入 Campaign 体系

在 `task_queue.json` 中新增任务，每个 Goal 作为一个任务：

```json
{
  "id": "T007",
  "type": "goal_mode_fix",
  "title": "Goal A: 修复路径分析英文文本",
  "goal_condition": "...（复制上面的停止条件）...",
  "priority": "high",
  "status": "pending",
  "safe_if_blocked": false
}
```

然后在 `docs/ops/mimo-season-campaign.md` 中补充 Goal 模式的执行规则。
