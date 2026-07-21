# Public Site AI + Market Upgrade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 CDS4WorldCup 的 GitHub Pages 首页和球队详情页升级成“看得出是 AI 多视角分析、也看得懂足球”的公开网站，同时补上市场快照能力，删除访客不该看到的开发说明。

**Architecture:** 继续保持纯静态站：Python 在构建期生成 `site/data/*.json` 和兜底 JS 数据文件，浏览器只负责渲染。Polymarket 作为 Yellow Source 快照，外部模型群体作为 Red Source 参考，二者都不能变成事实依据或投注建议。

**Tech Stack:** Python 3.10+ zero dependency scripts, `unittest`, vanilla HTML/CSS/JS, GitHub Pages static hosting, optional GitHub Actions scheduling.

---

## 0. 执行前先读

- `CLAUDE.md`
- `wiki/index.md`
- `docs/source-policy.md`
- `docs/design/specs/2026-06-12-public-site-ai-market-upgrade-spec.md`
- `AGENTS.md`
- 需要时再读：
  - `/Users/tangzw119/.trae-cn/skills/chart-visualization/SKILL.md`
  - `/Users/tangzw119/.trae-cn/skills/consulting-analysis/SKILL.md`
  - `/Users/tangzw119/.cc-switch/skills/frontend-design/SKILL.md`

执行中不要修改：

- `docs/references/**`
- `schema/**`
- `templates/**`
- `example/**`

不要 stage / commit：

- `AGENTS.md`
- `.playwright-mcp/**`
- `docs/references/**`
- 下载目录中的 zip / pdf / xlsx 原始文件

## 1. 技能与素材使用规则

### 1.1 必用技能

| 场景 | 技能 | 具体要求 |
|---|---|---|
| 页面视觉升级 | `frontend-design` | 做一个“浅色、克制、但明显有 AI 工作台感”的界面；不要营销落地页，不要炫技盖过内容。 |
| 图表选择 | `chart-visualization` | 先用它判断图表类型；最终实现优先用 HTML/CSS 图表，避免引入 D3/ECharts/Chart.js。 |
| 球队分析文案 | `consulting-analysis` | 借它的“结论先行、证据、看球抓手”结构，但输出必须是球迷听得懂的大白话。 |
| 本地/线上验证 | Browser / Playwright | 改完必须检查首页、球队详情页、移动端、GitHub Pages 线上页。 |
| 完成前检查 | `superpowers:verification-before-completion` | 先跑命令、看输出，再说完成。 |

### 1.2 可选技能

| 场景 | 技能 | 触发条件 |
|---|---|---|
| 读取 `/Users/tangzw119/Downloads/2026世界杯数据全景工作簿.xlsx` | `data-analysis` 或 `xlsx` | 只有当执行者决定抽取表格指标时使用。 |
| 读取 `/Users/tangzw119/Downloads/2026_World_Cup_White_Paper.pdf` | `pdf` | 只有当执行者需要校对公开模型说明或视觉参考时使用。 |
| 生成新图片/视频 | `imagegen` | 本轮非优先。除非明确要做 hero 背景，不要先做视频。 |

### 1.3 素材使用矩阵

| 素材 | 允许用途 | 禁止用途 | 来源级别 |
|---|---|---|---|
| `data/processed/kimi_agent_inventory.csv` | 生成公开的“AI 多视角推演”统计、派别卡片、球队相关片段。公开命名用“外部模型群体”或“300 个独立视角”。 | 不能在公开页面写 Kimi / 小米 / MiMo；不能把 reason 当事实。 | Red |
| `/Users/tangzw119/Downloads/Kimi_Agent_世界杯热力榜 UI 升级.zip` | 借鉴 300 点阵、莫兰迪色、浅色纸感、交互节奏。 | 不复制品牌名、源码文案、供应商说明；不提交 zip。 | 视觉参考 |
| `/Users/tangzw119/Downloads/Kimi_Agent_世界杯球迷人格测试.zip` | 借鉴球迷化中文语气。 | 不照搬页面结构或品牌表达。 | 视觉/文案参考 |
| `/Users/tangzw119/Downloads/Kimi_Agent_为什么有些国家足球就是强.zip` | 借鉴“讲人话”的解释方式。 | 不把其中说法当 Green Source。 | 叙事参考 |
| `/Users/tangzw119/Downloads/2026_World_Cup_White_Paper.pdf` | 用于理解公开模型材料的叙事结构。 | 不发布原文；不把最终概率当事实。 | Red |
| `/Users/tangzw119/Downloads/2026世界杯数据全景工作簿.xlsx` | 可抽取已能核验的数据字段，进入待核验资料包。 | 不直接把未核验表格数据当 Green Source。 | Yellow/Red，视字段而定 |
| `docs/references/**` | 本地理解项目背景。 | 绝不上库、绝不复制到 `site/`。 | 敏感内部资料 |

## 2. 文件结构与职责

计划完成后，相关文件职责如下：

- `scripts/fetch_market_snapshot.py`  
  新增。调用 Polymarket Gamma public search，生成 `data/processed/market_public_snapshot.json`。

- `scripts/build_site_data.py`  
  扩展。继续生成 `site/data/homepage.json`、`team-details.json` 和对应 `*-data.js`，新增 AI 多视角公开 payload，移除公开 JSON 中的 `update_contract`。

- `tests/test_build_site_data.py`  
  修改。更新公共词禁用规则：允许“AI 多视角推演”，继续禁止 Kimi / 小米 / MiMo / 投注语言；新增 market snapshot helper 测试。

- `tests/test_fetch_market_snapshot.py`  
  新增。用本地 fixture 测解析逻辑，不依赖真实网络。

- `site/index.html`  
  修改。加 AI 多视角模块容器和外部参考图容器。

- `site/team.html`  
  修改。删除“后续更新”开发者说明区，加球队 AI 多视角模块容器。

- `site/js/homepage.js`  
  修改。渲染 AI 派别卡、外部参考 Top 8 对比、市场快照状态。

- `site/js/team-detail.js`  
  修改。删除 `renderUpdateContract`，渲染单队 AI 多视角和市场快照。

- `site/css/portal.css`  
  修改。新增浅色 AI 工作台视觉、莫兰迪派别色、CSS bars、点阵、移动端样式。

- `docs/guides/public-site-update-flow.md`  
  新增。给维护者写更新流程，页面上不展示。

- `wiki/decisions/cds4worldcup2026-path-space-spec.md`  
  追加 memo。记录公开站升级边界：AI 可说，厂商不说，市场只作外部参考。

## 3. 公开语言边界

公开页面可以出现：

- `AI 多视角推演`
- `300 个独立视角`
- `外部模型群体`
- `公开模型群体参考`
- `市场快照`
- `只代表外界怎么看，不是投注建议`

公开页面和 `site/data/*.json` 不可以出现：

- `Kimi`
- `kimi`
- `小米`
- `Xiaomi`
- `MiMo`
- `MiMo Code Long-Horizon`
- `买`
- `卖`
- `投注建议`
- `ROI`
- `PnL`
- `Sharpe`
- `Kelly`
- `仓位`
- `低估`
- `高估`
- `正期望`
- `value bet`

注意：为了让网站有 AI 感，本轮允许公开出现 `AI` 和 `Agent`，但建议优先用中文：

- 首页模块标题可用：`300 个视角，不是一个声音。`
- 详情页模块标题可用：`AI 多视角怎么看这队？`
- 如果用 `Agent`，只在解释“300 个独立 Agent”时少量使用，正文尽量说“视角”。

## 4. Task 1: 先写失败测试，锁住公共边界

**Files:**

- Modify: `tests/test_build_site_data.py`
- Create: `tests/test_fetch_market_snapshot.py`

- [ ] **Step 1: 修改公共词测试规则**

在 `tests/test_build_site_data.py` 中，把当前禁止 `AI` / `Agent` 的断言改成允许 AI 表达、禁止厂商和投注语言。

新增 helper：

```python
PUBLIC_VENDOR_FORBIDDEN = [
    "Kimi", "kimi", "小米", "Xiaomi", "MiMo", "MiMo Code Long-Horizon",
]

PUBLIC_BETTING_FORBIDDEN = [
    "投注建议", "ROI", "PnL", "Sharpe", "Kelly", "仓位",
    "低估", "高估", "正期望", "value bet",
]

def assert_public_payload_clean(testcase, payload):
    text = json_dump(payload)
    for term in PUBLIC_VENDOR_FORBIDDEN + PUBLIC_BETTING_FORBIDDEN:
        testcase.assertNotIn(term, text)
```

把所有旧的 `forbidden_terms` / `forbidden_positive_terms` 中的 `AI`、`Agent`、`agent`、`智能体` 删除，改用上面的 helper。

- [ ] **Step 2: 添加 AI 多视角 payload 期望**

在 `test_build_homepage_json_has_plain_chinese_public_contract` 里增加：

```python
self.assertIn("ai_perspectives", homepage)
self.assertEqual(homepage["ai_perspectives"]["perspective_count"], 300)
self.assertEqual(homepage["ai_perspectives"]["faction_count"], 10)
self.assertEqual(homepage["ai_perspectives"]["covered_team_count"], 21)
self.assertEqual(homepage["ai_perspectives"]["source_label"], "只能参考")
self.assertGreaterEqual(len(homepage["ai_perspectives"]["factions"]), 10)
assert_public_payload_clean(self, homepage)
```

- [ ] **Step 3: 删除 update_contract 的公开 JSON 期望**

把 `test_public_team_details_have_reader_facing_analysis_and_update_contract` 改名为：

```python
def test_public_team_details_have_reader_facing_analysis_without_update_contract(self):
```

把：

```python
self.assertIn("update_contract", details)
self.assertIn("after_match", details["update_contract"])
```

改成：

```python
self.assertNotIn("update_contract", details)
text = json_dump(details)
for leaked in ["后续更新", "每场比赛后", "artifacts/team-cards", "data/processed", "scripts/build_site_data.py"]:
    self.assertNotIn(leaked, text)
assert_public_payload_clean(self, details)
```

- [ ] **Step 4: 新增市场快照解析测试文件**

创建 `tests/test_fetch_market_snapshot.py`：

```python
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "fetch_market_snapshot.py"

spec = importlib.util.spec_from_file_location("fetch_market_snapshot", SCRIPT)
fetch_market_snapshot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fetch_market_snapshot)


class FetchMarketSnapshotTests(unittest.TestCase):
    def test_extract_team_from_question(self):
        self.assertEqual(
            fetch_market_snapshot.extract_team_name("Will Spain win the 2026 FIFA World Cup?"),
            "Spain",
        )
        self.assertEqual(
            fetch_market_snapshot.extract_team_name("Will USA win the 2026 FIFA World Cup?"),
            "USA",
        )

    def test_build_snapshot_from_public_search_payload(self):
        payload = {
            "events": [
                {
                    "title": "World Cup Winner",
                    "slug": "world-cup-winner",
                    "markets": [
                        {
                            "question": "Will Spain win the 2026 FIFA World Cup?",
                            "slug": "will-spain-win-the-2026-fifa-world-cup-963",
                            "outcomes": "[\"Yes\", \"No\"]",
                            "outcomePrices": "[\"0.1695\", \"0.8305\"]",
                        },
                        {
                            "question": "Will Any Other Team win the 2026 FIFA World Cup?",
                            "slug": "will-any-other-team-win-the-2026-fifa-world-cup",
                            "outcomes": "[\"Yes\", \"No\"]",
                            "outcomePrices": "[\"0.5\", \"0.5\"]",
                        },
                    ],
                }
            ]
        }
        name_map = {"Spain": "spain"}
        snapshot = fetch_market_snapshot.build_snapshot_from_search(payload, name_map, event_slug="world-cup-winner")

        self.assertEqual(snapshot["status"], "available")
        self.assertEqual(snapshot["event_slug"], "world-cup-winner")
        self.assertAlmostEqual(snapshot["teams"]["spain"]["probability"], 16.95)
        self.assertEqual(len(snapshot["unmapped_markets"]), 1)
        self.assertIn("只代表外界怎么看", snapshot["display_rule"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 5: 运行测试，确认失败**

Run:

```bash
python3 -m unittest tests/test_build_site_data.py tests/test_fetch_market_snapshot.py
```

Expected:

- `tests/test_fetch_market_snapshot.py` 因 `scripts/fetch_market_snapshot.py` 不存在而失败。
- `tests/test_build_site_data.py` 因 `ai_perspectives` 不存在、`update_contract` 仍存在而失败。

## 5. Task 2: 移除访客页里的开发说明

**Files:**

- Modify: `site/team.html`
- Modify: `site/js/team-detail.js`
- Modify: `scripts/build_site_data.py`
- Modify: `tests/test_build_site_data.py`

- [ ] **Step 1: 删除 HTML 区块**

从 `site/team.html` 删除整个：

```html
<section class="section detail-panel update-contract">
  ...
</section>
```

- [ ] **Step 2: 删除 JS DOM 引用和渲染函数**

在 `site/js/team-detail.js` 中删除 `detailEls` 里的：

```js
updateRule: document.querySelector("[data-update-rule]"),
updateSteps: document.querySelector("[data-update-steps]"),
```

删除 `initTeamDetail()` 里的：

```js
renderUpdateContract(payload.update_contract || {});
```

删除整个函数：

```js
function renderUpdateContract(contract) {
  ...
}
```

- [ ] **Step 3: 公共 JSON 不再输出 update_contract**

在 `scripts/build_site_data.py` 的 `build_public_team_details_json()` 中，把：

```python
details = {
    "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "source_policy_version": "draft-for-execution",
    "teams": {},
    "update_contract": _build_update_contract(),
}
```

改成：

```python
details = {
    "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "source_policy_version": "draft-for-execution",
    "teams": {},
}
```

在 `_validate_team_details_json()` 中删除：

```python
if "after_match" not in details.get("update_contract", {}):
    errors.append("team details missing update_contract.after_match")
```

- [ ] **Step 4: 运行边界测试**

Run:

```bash
python3 -m unittest tests/test_build_site_data.py
```

Expected:

- 与 `update_contract` 相关的新断言通过。
- `ai_perspectives` 相关断言仍失败，留给后续任务。

## 6. Task 3: 写市场快照脚本

**Files:**

- Create: `scripts/fetch_market_snapshot.py`
- Create/Modify: `data/processed/market_public_snapshot.json`
- Test: `tests/test_fetch_market_snapshot.py`

- [ ] **Step 1: 创建脚本骨架**

创建 `scripts/fetch_market_snapshot.py`，包含这些函数：

```python
#!/usr/bin/env python3
"""Fetch a public Polymarket World Cup winner snapshot for static site display."""

import csv
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEAM_NAME_MAP = ROOT / "data" / "processed" / "team_name_map.csv"
TEAM_REGISTRY = ROOT / "data" / "processed" / "team_registry.csv"
DEFAULT_OUT = ROOT / "data" / "processed" / "market_public_snapshot.json"
DEFAULT_SEARCH_QUERY = "FIFA World Cup 2026 winner"
DEFAULT_EVENT_SLUG = "world-cup-winner"


ALIASES = {
    "USA": "united-states",
    "United States": "united-states",
    "Turkiye": "turkey",
    "Türkiye": "turkey",
    "Turkey": "turkey",
    "Ivory Coast": "côte-divoire",
    "Côte d'Ivoire": "côte-divoire",
    "South Korea": "south-korea",
    "Korea Republic": "south-korea",
}
```

- [ ] **Step 2: 实现球队名解析**

加入：

```python
def extract_team_name(question):
    match = re.match(r"^Will\s+(.+?)\s+win\s+the\s+2026\s+FIFA\s+World\s+Cup\??$", str(question or "").strip())
    if not match:
        return None
    name = match.group(1).strip()
    if name.lower() in {"any other team", "team am", "team ai"}:
        return None
    return name


def slugify(value):
    text = str(value or "").strip().lower()
    text = text.replace("'", "").replace(".", "")
    text = re.sub(r"\s+", "-", text)
    return re.sub(r"[^a-z0-9\-à-ž]", "", text)
```

- [ ] **Step 3: 实现本地球队映射**

加入：

```python
def load_team_name_map():
    mapping = {}
    if TEAM_NAME_MAP.exists():
        with TEAM_NAME_MAP.open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                slug = slugify(row.get("canonical_team") or row.get("en_name"))
                for key in [row.get("canonical_team"), row.get("en_name"), row.get("zh_name")]:
                    if key:
                        mapping[key] = slug
                for alias in str(row.get("aliases", "")).split("|"):
                    if alias.strip():
                        mapping[alias.strip()] = slug
    if TEAM_REGISTRY.exists():
        with TEAM_REGISTRY.open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                slug = slugify(row.get("canonical_team"))
                for key in [row.get("canonical_team"), row.get("en_name"), row.get("zh_name")]:
                    if key:
                        mapping[key] = slug
    mapping.update(ALIASES)
    return mapping
```

- [ ] **Step 4: 实现 market 解析**

加入：

```python
def parse_jsonish(value):
    if isinstance(value, list):
        return value
    if value in (None, ""):
        return []
    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, list) else []
    except (TypeError, json.JSONDecodeError):
        return []


def yes_price_from_market(market):
    outcomes = parse_jsonish(market.get("outcomes"))
    prices = parse_jsonish(market.get("outcomePrices"))
    for index, outcome in enumerate(outcomes):
        if str(outcome).lower() == "yes" and index < len(prices):
            try:
                return float(prices[index])
            except (TypeError, ValueError):
                return None
    return None
```

- [ ] **Step 5: 实现 snapshot 构造**

加入：

```python
def iter_events(search_payload):
    if isinstance(search_payload, dict):
        for key in ("events", "results", "data"):
            value = search_payload.get(key)
            if isinstance(value, list):
                yield from value
        if search_payload.get("slug"):
            yield search_payload
    elif isinstance(search_payload, list):
        yield from search_payload


def build_snapshot_from_search(search_payload, name_map, event_slug=DEFAULT_EVENT_SLUG):
    target = None
    for event in iter_events(search_payload):
        if isinstance(event, dict) and event.get("slug") == event_slug:
            target = event
            break
    if not target:
        raise ValueError(f"Polymarket event not found: {event_slug}")

    teams = {}
    unmapped = []
    for market in target.get("markets", []) or []:
        if not isinstance(market, dict):
            continue
        team_name = extract_team_name(market.get("question"))
        price = yes_price_from_market(market)
        if team_name is None or price is None:
            unmapped.append({
                "question": market.get("question", ""),
                "market_slug": market.get("slug", ""),
                "reason": "unmapped_or_missing_yes_price",
            })
            continue
        slug = name_map.get(team_name) or name_map.get(team_name.replace("’", "'"))
        if not slug:
            unmapped.append({
                "question": market.get("question", ""),
                "market_slug": market.get("slug", ""),
                "reason": "team_name_not_in_registry",
            })
            continue
        teams[slug] = {
            "probability": round(price * 100, 2),
            "market_slug": market.get("slug", ""),
            "question": market.get("question", ""),
            "raw_yes_price": price,
        }

    return {
        "status": "available" if teams else "snapshot_unavailable",
        "source": "polymarket_gamma_public_search",
        "event_slug": target.get("slug", event_slug),
        "event_title": target.get("title", "World Cup Winner"),
        "last_fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "display_rule": "只代表外界怎么看，不作为事实依据，也不是投注建议。",
        "teams": dict(sorted(teams.items())),
        "unmapped_markets": unmapped,
    }
```

- [ ] **Step 6: 实现网络获取和 CLI**

加入：

```python
def fetch_public_search(query):
    encoded = urllib.parse.urlencode({"q": query, "limit": 20})
    url = f"https://gamma-api.polymarket.com/public-search?{encoded}"
    request = urllib.request.Request(url, headers={"User-Agent": "cds4worldcup-static-site/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def main():
    query = os.environ.get("POLYMARKET_SEARCH_QUERY", DEFAULT_SEARCH_QUERY)
    event_slug = os.environ.get("POLYMARKET_EVENT_SLUG", DEFAULT_EVENT_SLUG)
    out_path = Path(os.environ.get("MARKET_SNAPSHOT_OUT", DEFAULT_OUT))
    payload = fetch_public_search(query)
    snapshot = build_snapshot_from_search(payload, load_team_name_map(), event_slug=event_slug)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out_path} with {len(snapshot['teams'])} mapped teams")
    return 0 if snapshot["teams"] else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"market snapshot fetch failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
```

- [ ] **Step 7: 运行市场脚本测试**

Run:

```bash
python3 -m unittest tests/test_fetch_market_snapshot.py
```

Expected:

- PASS.

- [ ] **Step 8: 手动抓一次快照**

Run:

```bash
python3 scripts/fetch_market_snapshot.py
```

Expected:

- 输出 `data/processed/market_public_snapshot.json`
- mapped teams 数量大于 0
- 如果网络失败，记录错误，不要手写假数据。

## 7. Task 4: 构建 AI 多视角公开 payload

**Files:**

- Modify: `scripts/build_site_data.py`
- Modify: `tests/test_build_site_data.py`

- [ ] **Step 1: 增加常量**

在 `scripts/build_site_data.py` 顶部增加：

```python
AGENT_INVENTORY_CSV = ROOT / "data" / "processed" / "kimi_agent_inventory.csv"

FACTION_COLORS = {
    "数据派": "#6E8499",
    "赔率派": "#A85F50",
    "老球迷派": "#7E9070",
    "玄学派": "#C2A75F",
    "主帅视角派": "#97768F",
    "伤病赛程派": "#5E807A",
    "黑马派": "#C07E55",
    "阵容年龄派": "#B27D7E",
    "心理抗压派": "#76729A",
    "建模派": "#B59A6B",
}
```

- [ ] **Step 2: 调整 sanitize，不再全局替换 AI**

在 `_sanitize_public_text()` 中删除这些替换：

```python
"AI": "模型",
"Agent": "模型样本",
"agent": "模型样本",
"智能体": "模型样本",
```

保留并扩展厂商替换：

```python
"kimi": "外部模型",
"Kimi": "外部模型",
"小米": "外部模型",
"Xiaomi": "外部模型",
"MiMo Code Long-Horizon": "外部模型",
"MiMo": "外部模型",
```

- [ ] **Step 3: 增加 public forbidden validation**

在 `scripts/build_site_data.py` 中新增：

```python
PUBLIC_VENDOR_FORBIDDEN = [
    "Kimi", "kimi", "小米", "Xiaomi", "MiMo", "MiMo Code Long-Horizon",
]

PUBLIC_BETTING_FORBIDDEN = [
    "投注建议", "ROI", "PnL", "Sharpe", "Kelly", "仓位",
    "低估", "高估", "正期望", "value bet",
]


def _validate_public_text_boundary(payload, label):
    text = json.dumps(payload, ensure_ascii=False)
    leaked = [term for term in PUBLIC_VENDOR_FORBIDDEN + PUBLIC_BETTING_FORBIDDEN if term in text]
    if leaked:
        raise ValueError(f"{label} contains forbidden public terms: {', '.join(leaked)}")
```

把 `_validate_homepage_json()` 和 `_validate_team_details_json()` 里重复的 forbidden 检查改为调用它。

- [ ] **Step 4: 增加 AI payload 函数**

新增函数：

```python
def _build_ai_perspectives(teams):
    if not AGENT_INVENTORY_CSV.exists():
        return {
            "status": "snapshot_unavailable",
            "status_label": STATUS_LABELS["snapshot_unavailable"],
            "perspective_count": 0,
            "faction_count": 0,
            "covered_team_count": 0,
            "source_level": "Red",
            "source_label": SOURCE_LABELS["Red"],
            "display_rule": "外部模型群体参考暂时没有生成。",
            "factions": [],
            "teams": {},
        }

    rows = load_csv(AGENT_INVENTORY_CSV)
    team_by_zh = {team["zh_name"]: team for team in teams.values() if team.get("zh_name")}
    faction_rows = {}
    team_rows = {}
    covered_teams = set()
    for row in rows:
        faction = row.get("faction", "").strip()
        champion = row.get("champion", "").strip()
        if not faction:
            continue
        faction_rows.setdefault(faction, []).append(row)
        team = team_by_zh.get(champion)
        if team:
            covered_teams.add(team["slug"])
            team_rows.setdefault(team["slug"], []).append(row)

    factions = []
    for faction, items in faction_rows.items():
        champion_counts = Counter(row.get("champion", "").strip() for row in items if row.get("champion"))
        representative = _representative_agent_row(items)
        factions.append({
            "name": faction,
            "count": len(items),
            "color": FACTION_COLORS.get(faction, "#6E8499"),
            "top_champions": [
                {"team_name": name, "count": count}
                for name, count in champion_counts.most_common(3)
            ],
            "representative": representative,
        })

    team_payload = {}
    for slug, items in team_rows.items():
        faction_counts = Counter(row.get("faction", "").strip() for row in items if row.get("faction"))
        snippets = []
        for row in items[:4]:
            snippets.append(_representative_agent_row([row]))
        team_payload[slug] = {
            "count": len(items),
            "faction_counts": dict(faction_counts.most_common()),
            "snippets": snippets,
            "source_label": SOURCE_LABELS["Red"],
            "display_rule": "这些只是外部模型群体的看法，不能当事实。",
        }

    return {
        "status": "available",
        "status_label": "已有外部视角",
        "perspective_count": len(rows),
        "faction_count": len(faction_rows),
        "covered_team_count": len(covered_teams),
        "source_level": "Red",
        "source_label": SOURCE_LABELS["Red"],
        "display_rule": "这是外部模型群体参考，只代表不同视角怎么想，不作为事实依据。",
        "factions": factions,
        "teams": team_payload,
    }


def _representative_agent_row(rows):
    row = rows[0] if rows else {}
    return {
        "persona": _short_public_text(row.get("persona", ""), 26),
        "champion": _short_public_text(row.get("champion", ""), 18),
        "reason": _short_public_text(row.get("reason", ""), 90),
    }


def _short_public_text(value, limit):
    text = strip_markdown_public(value)
    return text if len(text) <= limit else text[: limit - 1].rstrip("，。；;、 ") + "…"
```

- [ ] **Step 5: 接入 homepage 和 team detail**

在 `build_homepage_json()` 中：

```python
ai_perspectives = _build_ai_perspectives(teams)
```

并加入：

```python
"ai_perspectives": {
    key: value
    for key, value in ai_perspectives.items()
    if key != "teams"
},
```

在 `build_public_team_details_json()` 中：

```python
ai_perspectives = _build_ai_perspectives(teams)
```

并传给 `_build_public_team_detail(team, market_snapshot, ai_perspectives)`。

把 `_build_public_team_detail` 的签名改为：

```python
def _build_public_team_detail(team, market_snapshot, ai_perspectives):
```

在每个 team detail payload 中增加：

```python
"ai_perspective": ai_perspectives.get("teams", {}).get(team["slug"], {
    "count": 0,
    "faction_counts": {},
    "snippets": [],
    "source_label": SOURCE_LABELS["Red"],
    "display_rule": "这支队还没有外部模型群体参考。我们先保留路径拆解，等后续数据补齐。",
}),
```

- [ ] **Step 6: 运行测试**

Run:

```bash
python3 -m unittest tests/test_build_site_data.py
```

Expected:

- `ai_perspectives` 相关断言通过。
- 如果失败，多半是 sanitize 后仍有 `低估` 等词，先修 sanitize。

## 8. Task 5: 改市场快照展示和 build 集成

**Files:**

- Modify: `scripts/build_site_data.py`
- Modify: `site/js/homepage.js`
- Modify: `site/js/team-detail.js`
- Modify: `tests/test_build_site_data.py`

- [ ] **Step 1: 扩展 `_sanitize_market_snapshot` 输出**

在 `scripts/build_site_data.py` 的 `_sanitize_market_snapshot(payload)` 中保留：

```python
"event_slug": payload.get("event_slug"),
"event_title": payload.get("event_title"),
```

在每支队里保留：

```python
"market_slug": row.get("market_slug", ""),
"question": _sanitize_public_text(row.get("question", "")),
```

公共展示继续只用 `probability`、`source_label`、`last_fetched_at`，不要展示交易术语。

- [ ] **Step 2: 生成数据**

Run:

```bash
python3 scripts/fetch_market_snapshot.py
python3 scripts/build_site_data.py
```

Expected:

- `site/data/homepage.json` 中 `public_signal_snapshots.market_public_baseline.status == "available"`，除非网络失败。
- 网络失败时，运行 `python3 scripts/build_site_data.py` 仍能生成站点，显示 `snapshot_unavailable`。

- [ ] **Step 3: 测试 build**

Run:

```bash
python3 -m unittest tests/test_build_site_data.py tests/test_fetch_market_snapshot.py
```

Expected:

- PASS.

## 9. Task 6: 首页加 AI 多视角模块和外部参考图

**Files:**

- Modify: `site/index.html`
- Modify: `site/js/homepage.js`
- Modify: `site/css/portal.css`

- [ ] **Step 1: 加 HTML 容器**

在 `site/index.html` 中，放在“选球队”附近，建议在 `id="choose-team"` 后面或前面加：

```html
<section class="section ai-perspective-section" id="ai-perspectives">
  <div class="section-head">
    <div>
      <p class="eyebrow">AI 多视角推演</p>
      <h2>300 个视角，不是一个声音。</h2>
      <p>数据、赔率、老球迷、主帅、伤病赛程、黑马、年龄结构、心理抗压、建模和娱乐向玄学一起看。它们只提供参考，不替我们下结论。</p>
    </div>
    <span class="source-badge source-red">只能参考</span>
  </div>
  <div data-ai-perspectives></div>
</section>
```

在外部参考区加：

```html
<div data-external-reference-chart></div>
```

如果已经有相近容器，复用，不重复堆模块。

- [ ] **Step 2: 增加 JS 渲染入口**

在 `site/js/homepage.js` 的元素集合中加入：

```js
aiPerspectives: document.querySelector("[data-ai-perspectives]"),
externalReferenceChart: document.querySelector("[data-external-reference-chart]"),
```

在初始化成功后调用：

```js
renderAiPerspectives(data.ai_perspectives);
renderExternalReferenceChart(data.public_signal_snapshots);
```

- [ ] **Step 3: 实现 AI 派别卡渲染**

加入：

```js
function renderAiPerspectives(ai) {
  if (!homeEls.aiPerspectives) return;
  const factions = Array.isArray(ai?.factions) ? ai.factions : [];
  if (!factions.length) {
    homeEls.aiPerspectives.innerHTML = `<div class="empty-state">AI 多视角数据还在整理。</div>`;
    return;
  }
  homeEls.aiPerspectives.innerHTML = `
    <div class="ai-summary-row">
      <strong>${escapeHtml(ai.perspective_count)} 个独立视角</strong>
      <span>${escapeHtml(ai.faction_count)} 个派别</span>
      <span>${escapeHtml(ai.covered_team_count)} 支球队有参考</span>
    </div>
    <div class="faction-grid">
      ${factions.map((faction) => renderFactionCard(faction)).join("")}
    </div>
    <p class="source-note">${escapeHtml(ai.display_rule)}</p>
  `;
}

function renderFactionCard(faction) {
  const dots = Array.from({ length: Number(faction.count || 0) || 30 }, (_, index) =>
    `<span class="agent-dot" style="--dot-index:${index};--faction-color:${escapeAttr(faction.color || "#6E8499")}"></span>`
  ).join("");
  const top = (faction.top_champions || []).map((item) =>
    `<span>${escapeHtml(item.team_name)} ${escapeHtml(item.count)}票</span>`
  ).join("");
  const rep = faction.representative || {};
  return `
    <article class="faction-card" style="--faction-color:${escapeAttr(faction.color || "#6E8499")}">
      <div class="faction-card-head">
        <strong>${escapeHtml(faction.name)}</strong>
        <span>${escapeHtml(faction.count)} 个视角</span>
      </div>
      <div class="agent-dot-grid" aria-label="${escapeAttr(faction.name)}">${dots}</div>
      <div class="faction-topline">${top}</div>
      <p><b>${escapeHtml(rep.persona || "代表视角")}</b>：${escapeHtml(rep.reason || "暂无代表理由。")}</p>
    </article>
  `;
}
```

- [ ] **Step 4: 实现外部参考 Top 8 图**

优先用 CSS 条形图。市场缺失时显示：

```text
市场快照待更新
```

不要在 UI 里写 `snapshot_unavailable`。

- [ ] **Step 5: CSS 设计要求**

在 `site/css/portal.css` 加：

- `.ai-perspective-section`
- `.ai-summary-row`
- `.faction-grid`
- `.faction-card`
- `.agent-dot-grid`
- `.agent-dot`
- `.external-reference-chart`

关键样式约束：

```css
.faction-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 14px;
}

.agent-dot-grid {
  display: grid;
  grid-template-columns: repeat(6, 10px);
  gap: 6px;
}

.agent-dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  background: color-mix(in srgb, var(--faction-color), transparent 55%);
  animation: dotPulse 900ms ease both;
  animation-delay: calc(var(--dot-index) * 18ms);
}

@media (prefers-reduced-motion: reduce) {
  .agent-dot {
    animation: none;
  }
}
```

如果 `color-mix` 兼容性担心，用 opacity 实心点替代：

```css
background: var(--faction-color);
opacity: .42;
```

- [ ] **Step 6: 本地打开首页检查**

Run:

```bash
python3 -m http.server 8000 --directory site
```

Browser:

- `http://localhost:8000/`
- mobile `390 x 844`

Expected:

- 首页看得出“AI 多视角推演”。
- 没有 Kimi / 小米 / MiMo。
- 点阵不是空心灰圈。
- 图表移动端不横向撑爆。

## 10. Task 7: 球队详情页加单队 AI 模块

**Files:**

- Modify: `site/team.html`
- Modify: `site/js/team-detail.js`
- Modify: `site/css/portal.css`

- [ ] **Step 1: 加 HTML 容器**

在 `site/team.html` 的 `analysis-stack` 后或 `chart-grid` 前加入：

```html
<section class="section detail-panel team-ai-panel">
  <div class="section-head compact">
    <div>
      <p class="eyebrow">AI 多视角</p>
      <h2>AI 多视角怎么看这队？</h2>
    </div>
    <span class="source-badge source-red">只能参考</span>
  </div>
  <div data-team-ai-perspective></div>
</section>
```

- [ ] **Step 2: 加 JS DOM 引用**

在 `detailEls` 中加入：

```js
aiPerspective: document.querySelector("[data-team-ai-perspective]"),
```

在 `initTeamDetail()` 中调用：

```js
renderAiPerspective(team);
```

- [ ] **Step 3: 实现单队 AI 模块**

加入：

```js
function renderAiPerspective(detail) {
  if (!detailEls.aiPerspective) return;
  const ai = detail.ai_perspective || {};
  const snippets = Array.isArray(ai.snippets) ? ai.snippets : [];
  if (!snippets.length) {
    detailEls.aiPerspective.innerHTML = `
      <div class="empty-state">${escapeHtml(ai.display_rule || "这支队还没有外部模型群体参考。我们先保留路径拆解，等后续数据补齐。")}</div>
    `;
    return;
  }
  detailEls.aiPerspective.innerHTML = `
    <div class="team-ai-summary">
      <strong>${escapeHtml(ai.count || snippets.length)} 个视角提到这队</strong>
      <span>${escapeHtml(ai.display_rule || "只能参考，不能当事实。")}</span>
    </div>
    <div class="team-ai-snippets">
      ${snippets.map((item) => `
        <article>
          <span class="label">${escapeHtml(item.persona || "代表视角")}</span>
          <p>${escapeHtml(item.reason || "")}</p>
        </article>
      `).join("")}
    </div>
  `;
}
```

- [ ] **Step 4: 检查阿根廷页**

Browser:

- `http://localhost:8000/team.html?team=argentina`

Expected:

- 页面只显示阿根廷。
- 有 “AI 多视角怎么看这队？”
- 没有“后续更新”和任何开发文件路径。
- 市场快照如果缺失，显示人话，不显示技术状态码。

## 11. Task 8: 写维护者更新流程文档

**Files:**

- Create: `docs/guides/public-site-update-flow.md`

- [ ] **Step 1: 创建文档**

内容：

```markdown
# Public Site Update Flow

> 面向维护者。不要把本页内容复制到公开网站。

## 什么时候更新

- 每场比赛后：更新赛果、路径卡或赛中观察项。
- 市场看法需要刷新时：重新抓一次市场快照。
- 外部模型群体重跑后：更新处理后的 CSV，再重建站点数据。

## 常规更新命令

```bash
python3 scripts/fetch_market_snapshot.py
python3 scripts/build_site_data.py
python3 -m unittest tests/test_build_site_data.py tests/test_fetch_market_snapshot.py
python3 scripts/verify.py --root wiki/
python3 scripts/audit.py --root wiki/
```

## 市场快照失败怎么办

市场快照失败不阻塞站点发布。站点会显示“市场快照待更新”。不要手写假概率。

## 公开页面边界

- 可以说 AI 多视角。
- 不说 Kimi / 小米 / MiMo。
- 市场数据只代表外界怎么看，不是投注建议。
- 外部模型群体是参考，不是事实来源。
```

- [ ] **Step 2: 确认该文档不被站点页面引用**

Run:

```bash
rg "public-site-update-flow|后续更新|每场比赛后，不用重写页面|scripts/build_site_data.py" site
```

Expected:

- no matches for developer-facing text in `site/`.

## 12. Task 9: 更新 wiki memo

**Files:**

- Modify: `wiki/decisions/cds4worldcup2026-path-space-spec.md`

- [ ] **Step 1: 追加 memo**

在文件末尾追加：

```markdown

> [!memo] 2026-06-12 公开站升级边界：允许在访客页面说“AI 多视角推演”，让用户知道这是 AI 辅助分析；但不公开 Kimi / 小米 / MiMo 等厂商品牌。Polymarket 只作为 Yellow Source 市场快照，外部模型群体只作为 Red Source 参考，二者都不进入事实判断，也不输出投注建议。
```

- [ ] **Step 2: 跑 wiki 检查**

Run:

```bash
python3 scripts/verify.py --root wiki/
python3 scripts/audit.py --root wiki/
```

Expected:

- `verify.py` PASS。
- `audit.py` 可能仍报告已有 7 个 P2 orphan pages；只要没有新增 P0/P1，不阻塞。

## 13. Task 10: 重建、验证、浏览器检查

**Files:**

- Generated: `site/data/homepage.json`
- Generated: `site/data/homepage-data.js`
- Generated: `site/data/team-details.json`
- Generated: `site/data/team-details-data.js`
- Generated: `site/data/teams.json`
- Generated: `site/data/teams-data.js`
- Generated: `site/data/meta.json`

- [ ] **Step 1: 重建数据**

Run:

```bash
python3 scripts/build_site_data.py
```

Expected:

- 命令 0 exit。
- `site/data/homepage.json` 存在 `ai_perspectives`。
- `site/data/team-details.json` 不存在 `update_contract`。

- [ ] **Step 2: 跑完整测试**

Run:

```bash
python3 -m unittest tests/test_build_site_data.py tests/test_fetch_market_snapshot.py
```

Expected:

- PASS.

- [ ] **Step 3: 搜索公开禁词**

Run:

```bash
rg "Kimi|kimi|小米|Xiaomi|MiMo|MiMo Code Long-Horizon|ROI|PnL|Sharpe|Kelly|仓位|低估|高估|正期望|value bet|后续更新|每场比赛后|artifacts/team-cards|scripts/build_site_data.py" site
```

Expected:

- no matches.

- [ ] **Step 4: 本地浏览器验证**

Run server:

```bash
python3 -m http.server 8000 --directory site
```

Check:

- `http://localhost:8000/`
- `http://localhost:8000/team.html?team=argentina`
- `http://localhost:8000/team.html?team=spain`
- mobile viewport `390 x 844`

Expected:

- 首页加载无 `Failed to fetch`。
- 选择球队后进入单队详情，不显示一批球队。
- 首页有 AI 多视角模块。
- 球队详情有单队 AI 多视角模块。
- 市场快照显示概率或“市场快照待更新”。
- 图表不挤、不溢出。
- 页面没有开发者说明。

- [ ] **Step 5: Git 检查**

Run:

```bash
git status --short --branch
git diff --stat
```

Expected:

- 不 stage `AGENTS.md`。
- 不 stage `.playwright-mcp/**`。
- 不 stage `docs/references/**`。

## 14. Task 11: 提交与线上验证

**Files:**

- Only stage files changed by this plan.

- [ ] **Step 1: stage 安全文件**

示例命令：

```bash
git add \
  docs/design/plans/2026-06-12-public-site-ai-market-upgrade-plan.md \
  docs/guides/public-site-update-flow.md \
  scripts/fetch_market_snapshot.py \
  scripts/build_site_data.py \
  tests/test_build_site_data.py \
  tests/test_fetch_market_snapshot.py \
  site/index.html \
  site/team.html \
  site/js/homepage.js \
  site/js/team-detail.js \
  site/css/portal.css \
  site/data/homepage.json \
  site/data/homepage-data.js \
  site/data/team-details.json \
  site/data/team-details-data.js \
  site/data/teams.json \
  site/data/teams-data.js \
  site/data/meta.json \
  data/processed/market_public_snapshot.json \
  wiki/decisions/cds4worldcup2026-path-space-spec.md
```

如果某些文件没有改，不要强行 stage。

- [ ] **Step 2: 再检查 staged diff**

Run:

```bash
git diff --cached --stat
git diff --cached --name-only
```

Expected:

- 没有 `AGENTS.md`
- 没有 `.playwright-mcp/`
- 没有 `docs/references/`

- [ ] **Step 3: commit**

Run:

```bash
git commit -m "feat: add AI perspectives and market snapshot to public site"
```

- [ ] **Step 4: push**

注意：当前本地分支可能显示 `main...origin/main [ahead 2]`，因为之前曾通过 GitHub API 更新远端，local/remote commit graph 可能不完全同步。执行者必须先确认：

```bash
git fetch origin
git log --oneline --decorate --graph --max-count=8 --all
```

如果正常 fast-forward 可推：

```bash
git push origin main
```

如果发现远端包含本地没有的历史，先停下来说明情况，不要 `--force`。

- [ ] **Step 5: 线上验证**

拿到 commit SHA 后访问：

```text
https://zwtang119.github.io/cds4worldcup/?v=<commit>
https://zwtang119.github.io/cds4worldcup/team.html?team=argentina&v=<commit>
```

Expected:

- GitHub Pages 可公开访问。
- 私有仓库不影响 Pages 公网访问。
- 页面与本地验证一致。

## 15. 验收标准

全部满足才算完成：

- [ ] 首页点击球队进入 `team.html?team=<slug>`，详情页只展示单队分析。
- [ ] 详情页不再出现“后续更新”、开发路径、构建命令。
- [ ] 首页明确有“AI 多视角推演”的感觉，但不出现 Kimi / 小米 / MiMo。
- [ ] 球队详情页有单队 AI 多视角模块。
- [ ] 市场快照可以由 `scripts/fetch_market_snapshot.py` 生成。
- [ ] 市场快照失败时站点仍可构建，并显示人话缺失状态。
- [ ] 图表使用轻量 HTML/CSS，不引入重图表库。
- [ ] 公开页面不输出投注建议、收益率、仓位或“低估/高估/正期望”。
- [ ] 公开文案是中国球迷听得懂的大白话。
- [ ] 维护者更新流程写在 `docs/guides/public-site-update-flow.md`，不出现在访客页面。
- [ ] `python3 -m unittest tests/test_build_site_data.py tests/test_fetch_market_snapshot.py` PASS。
- [ ] `python3 scripts/verify.py --root wiki/` PASS。
- [ ] 浏览器本地和线上验证通过。

