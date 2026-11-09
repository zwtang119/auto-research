#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
docs/tools/build_index.py — auto-research 仓库级索引再生脚本

用途
----
生成 / 更新 docs/index.json。目标是让 LLM 会话开始时不必临时写扫描脚本，也不必凭
记忆或 README.md 断言主线状态：先读 docs/INDEX.md（人读导航），再精确命中
docs/index.json（机器可查清单），命中即用，未命中才做只读扫描。

字段分工（关键约定）
--------------------
* 骨架字段（每次再生按磁盘实况刷新）：
    docs[]    : path, mtime, size, heading, kind
    scripts[] : path, mtime, size, heading, capability, workdir
* 人工维护字段（脚本绝不覆盖；仅在条目首次出现时填默认值）：
    docs[]    : id, title, topic, status, verified_at, supersedes,
                related_scripts, related_docs
    scripts[] : purpose, reusable
  人工可直接编辑 docs/index.json 修改这些字段，再次运行本脚本不会被抹掉。
  顶层 scope / data_zones / readonly_zones / status_conflicts 同样「已存在即保留」。

扫描范围（只读，刻意保守）
--------------------------
* docs/ 各主干子目录下的 *.md；排除 docs/ 顶层 *.md（索引自身、SECRETS.md）、
  docs/tools/、docs/papers-closed-portfolio/experiments/（2268 个数据产物）、隐藏目录。
* analysis/ 下 *.py，限深 3（与 `find analysis -maxdepth 3 -type f -name '*.py'` 等价）；
  analysis/ 全量约 85000 文件，不限深会导致进程被 SIGTERM。
* 不扫描 evidence/、legacy/、papers/、framework/ 内部文件：这些区只在
  counts / readonly_zones 里做摘要登记（字节级只读，禁区零写入）。

幂等性
------
generated_at 取到「日」而非「秒」；同一天、磁盘未变时重复运行，输出字节一致。
所有 path 均来自磁盘扫描，因此天然真实存在。

用法
----
    python3 docs/tools/build_index.py              # 默认：写回（幂等，保留人工字段）
    python3 docs/tools/build_index.py --dry-run    # 不写回，只打印将要发生的变更
    python3 docs/tools/build_index.py --check      # 只校验现有 index.json 所有 path 是否仍存在

无第三方依赖，macOS / Python 3 直接可跑。
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------- 基础常量

REPO_ROOT = Path(__file__).resolve().parents[2]  # docs/tools/ -> repo root
INDEX_PATH = REPO_ROOT / "docs" / "index.json"
TODAY = datetime.now().strftime("%Y-%m-%d")

GENERATOR = "docs/tools/build_index.py"

# os.walk 剪枝目录名（只作用于 docs/ 扫描）
DOC_PRUNE_DIRS = {"tools", "experiments", ".obsidian", ".git"}
# find analysis -maxdepth 3 的等价实现：文件所在目录相对 analysis 的深度 <= 2
SCRIPT_MAX_FILE_DEPTH = 3

KIND_VOCABULARY = [
    "plan", "investigation", "review", "roadmap", "progress", "portfolio", "other",
]
CAPABILITY_VOCABULARY = [
    "freeze_inputs", "verify", "release", "report",
    "extract", "recompute", "test", "other",
]

# 骨架字段：每次再生按磁盘刷新
DOC_SKELETON_FIELDS = ("path", "mtime", "size", "heading", "kind")
SCRIPT_SKELETON_FIELDS = ("path", "mtime", "size", "heading", "capability", "workdir")

# ---------------------------------------------------------------- 盘点快照
# 2026-11-05 实测。三层口径不一致是「查资料不准」的机制性根因：
# 只依据其中一层会系统性低估 / 找不到 analysis/、legacy/、evidence/。
# 这些数字是「盘点快照」，刻意不随每次再生深遍历重算，以免扫描禁区拖慢。
COUNTS_SNAPSHOT = {
    "measured_at": "2026-11-05",
    "basis_note": (
        "三种统计口径并存且互相不一致。① disk_full = 磁盘全量（find -type f）；"
        "② git_tracked = git ls-files 已跟踪文件数；③ session_injected_snapshot = 会话上下文"
        "注入的目录快照数值（口径未确认，与主理人 Phase 1 移交记录一致）。"
        "LLM 只看上下文快照或只跑 git ls-files 会系统性低估 / 找不到 analysis/、legacy/、"
        "evidence/。查资料请以本索引的 docs[]/scripts[] 逐条 path 为准，不要把任何一层"
        "总数当作文件是否存在或内容是否权威的依据。"
    ),
    "disk_full": {
        "basis": "find <dir> -type f（磁盘全量）",
        "docs": 2474, "docs_md": 173, "docs_py": 5,
        "docs_md_baseline": 173, "docs_md_current": 176,
        "docs_md_note": (
            "docs_md 与 docs_md_baseline 同为 2026-11-05 索引建立前的磁盘基线"
            "（find docs -name '*.md' | wc -l = 173）；新增 docs/INDEX.md 与 "
            "docs/SCRIPTS.md 两篇后实测为 175（均位于 docs/ 顶层，属索引机制自身，"
            "按扫描约定不计入 docs[]）；2026-11-05 再新增 "
            "docs/progress/2026-11-05-repo-index-mechanism-progress.md 一篇后实测为 176"
            "（docs_md_current），该篇计入 docs[]（现为 171 篇主干讨论文档）。"
            "disk_full 内其余数值（docs=2474、docs_py=5 等）亦为索引建立前基线口径，"
            "当前值见 docs/INDEX.md「数字口径」。"
        ),
        "analysis_py_depth3": 185, "analysis_dirs_depth1": 23,
        "evidence": 850, "evidence_md": 337, "evidence_py": 37,
        "legacy": 11723, "legacy_md": 2322, "legacy_py": 39,
        "papers": 213, "papers_md": 76, "papers_py": 22,
        "framework": 20, "framework_md": 8, "framework_py": 3,
        "state": 6, "research": 6, "prompt_exports": 20,
        "docs_experiments_datazone": 2268,
    },
    "git_tracked": {
        "basis": "git ls-files <dir>（已跟踪口径）",
        "docs": 2468, "evidence": 432, "legacy": 74,
        "papers": 204, "framework": 17,
    },
    "session_injected_snapshot": {
        "basis": "会话上下文注入的目录快照，具体口径未确认",
        "legacy": 7546, "evidence": 548,
    },
    "docs_indexed": 0,     # 每次再生按实际扫描重算
    "scripts_indexed": 0,  # 每次再生按实际扫描重算
}

SCOPE = {
    "repo": "auto-research",
    "in_scope": [
        "docs/ 主干讨论文档（investigations / plans / portfolio / roadmaps / progress / "
        "reviews / autoresearch / compose / analysis / papers-closed-portfolio 的非数据区）",
        "analysis/ 下 .py 脚本（限深 3，185 个）",
        "papers/ 与 framework/（受控只读登记，不逐条深挖）",
    ],
    "readonly_registration_only": [
        "evidence/（证据快照，字节级只读）",
        "legacy/（2322 篇历史 md，仅做目录级摘要，不深挖、不写入）",
    ],
    "excluded_from_scan": [
        "docs/papers-closed-portfolio/experiments/（2268 个数据产物，非讨论文档，见 data_zones）",
        "docs/ 顶层 *.md（docs/INDEX.md、docs/SCRIPTS.md 等索引自身，以及 docs/SECRETS.md）",
        "docs/tools/（索引机制自身代码，避免自指循环）",
        "隐藏目录 .obsidian / .git 等",
        "封存仓库 /Users/tangzw119/Documents/GitHub/cds4worldcup（零读写）",
    ],
    "naming_convention": "沿用仓库既有英文路径命名 <topic>-<YYYY-MM-DD>.md；新增 Markdown 正文用中文；相对路径互链。不强制中文文件名、不改名既有文件。",
    "kind_vocabulary": KIND_VOCABULARY,
    "kind_note": "前 6 类与 docs/ 子目录一一对应；other 用于 autoresearch/、compose/specs/、papers-closed-portfolio/ 等无法归入 6 类的文档，保证每篇文档都被登记而不丢条目。",
    "capability_vocabulary": CAPABILITY_VOCABULARY,
    "field_policy": {
        "skeleton_refreshed_each_run": {
            "docs": list(DOC_SKELETON_FIELDS),
            "scripts": list(SCRIPT_SKELETON_FIELDS),
        },
        "manual_never_overwritten": {
            "docs": ["id", "title", "topic", "status", "verified_at", "supersedes",
                     "related_scripts", "related_docs"],
            "scripts": ["purpose", "reusable"],
            "top_level": ["scope", "data_zones", "readonly_zones", "status_conflicts"],
        },
    },
    "status_authority": "状态以 CLAUDE.md『当前活跃主线』表为准；README.md:5 与 CLAUDE.md:7 于 2026-11-05 由外部改动补挂起标注，与 CLAUDE.md:11 趋一致；剩余为主线版本口径分歧，见 C1（待裁定）。index.json 的 status 为索引维护初判，遇冲突以 docs/INDEX.md『待裁定』节为准，不擅自二选一。",
}

DATA_ZONES = [
    {
        "path": "docs/papers-closed-portfolio/experiments/",
        "files": 2268,
        "kind": "历史实验数据产物（.txt / .json 为主）",
        "is_discussion_doc": False,
        "access": "只读登记，不写入、不逐条索引、不参与 docs[] 扫描",
        "note": "占 docs/ 2474 个文件的绝大多数。若不单列隔离，会把讨论文档索引淹没在数据噪声里。",
    },
]

READONLY_ZONES = [
    {
        "path": "evidence/",
        "disk_files": 850, "md": 337, "py": 37, "git_tracked": 432,
        "access": "字节级只读：禁止任何修改（含删 .DS_Store、格式化、重命名）；深遍历会拖慢，索引只做摘要登记",
        "note": "证据快照。引用其内部文件时须注明「证据快照」字样。",
    },
    {
        "path": "legacy/",
        "disk_files": 11723, "md": 2322, "py": 39, "git_tracked": 74,
        "access": "只读登记；不深挖 2322 篇历史 md、不写入、不重命名/移动内部文件",
        "note": "磁盘全量 11723 但仅 74 个入 git，是三层口径差异最大的区域。",
    },
    {
        "path": "papers/",
        "disk_files": 213, "md": 76, "py": 22, "git_tracked": 204,
        "access": "高引用区，只读；禁止重命名/移动内部文件",
        "note": "含 4 个 papers/*/wiki/index.md 已有索引，均为历史副本，未纳入本索引的 docs[]。",
    },
    {
        "path": "framework/",
        "disk_files": 20, "md": 8, "py": 3, "git_tracked": 17,
        "access": "只读",
        "note": "跨论文可复用 schemas/ + knowledge/。",
    },
    {
        "path": "state/",
        "disk_files": 6, "md": 2, "py": 0,
        "access": "高引用区，只读；约 478 处引用",
        "note": "state/progress.json:3 的 status 停在 W6 备忘录阶段，见待裁定冲突 5。",
    },
    {
        "external_ref": "封存仓库 /Users/tangzw119/Documents/GitHub/cds4worldcup",
        "access": "零读写，无一例外（任何进程不得碰）",
        "note": "外部禁区，非仓库相对路径，不参与 path 存在性校验。",
    },
]

# ---------------------------------------------------------------- 待裁定冲突
STATUS_CONFLICTS = [
    {
        "id": "C1",
        "title": "世界杯主线口径：双论文路线 v1.7 / 开题 v2.1 vs 单篇开题 v1.3 + 已挂起",
        "claims": [
            {
                "path": "README.md", "line": 5,
                "quote": "▶ 当前主线（2026-09-25 已挂起、投稿暂停）：世界杯双论文路线（2026-07-21 用户裁定拆分；v1.7 路线图 2026-07-26）……开题 v2.1",
            },
            {
                "path": "CLAUDE.md", "line": 7,
                "quote": "当前主线（2026-09-25 起挂起、投稿暂停）：世界杯算法比较实证论文（用户裁定 2026-07-20，以开题报告为主线）",
                "head_quote": "当前活跃主线：世界杯算法比较实证论文（用户裁定 2026-07-20，以开题报告为主线）",
                "source_note": "引文于 2026-11-05 随外部改动同步；HEAD 旧版见 head_quote，可经 git show HEAD:CLAUDE.md | sed -n '7p' 回溯",
            },
            {
                "path": "CLAUDE.md", "line": 11,
                "quote": "⏸ 2026-09-25 用户决定：世界杯双论文研究挂起、投稿暂停（无限期）",
            },
        ],
        "observed_change": "2026-11-05 本次任务期间 README.md:5 发生外部改动，新增「2026-09-25 已挂起、投稿暂停」标注；该改动为工作区 pre-existing M，非本团队产生，未触碰。",
        "why": "活跃/挂起表述已趋一致（README.md:5 于 2026-11-05 由外部补上「2026-09-25 已挂起、投稿暂停」，与 CLAUDE.md:11 的无限期挂起一致；CLAUDE.md:7 亦于同期改为「2026-09-25 起挂起、投稿暂停」）；剩余分歧为主线版本口径（双论文 v1.7 / 开题 v2.1 vs 单篇开题 v1.3），仍待用户裁定。CLAUDE.md:7 引文于 2026-11-05 随外部改动同步，HEAD 旧引文保留在 head_quote，未静默删除。",
        "resolution": "待裁定",
        "action": "只标注，不修改 README.md / CLAUDE.md 正文；状态准绳以 CLAUDE.md「当前活跃主线」表为准。",
    },
    {
        "id": "C2",
        "title": "组合主线状态：P12「新建，短期优先」活跃任务顺序 vs 2026-07-18 已关闭",
        "claims": [
            {
                "path": "docs/portfolio/project-index.md", "line": "3-4",
                "quote": "更新日期：2026-07-03 / 用途：让根目录一眼看清每条实验线的角色、状态和下一步",
            },
            {
                "path": "docs/portfolio/project-index.md", "line": 27,
                "quote": "papers/p12-judge-calibration | P12 Judge 校准 | 新建，短期优先 | 从 P11 抽 sample manifest",
            },
            {
                "path": "docs/portfolio/project-index.md", "line": 36,
                "quote": "1. P12 Judge Calibration：新建目录，作为短期主任务。",
            },
            {
                "path": "CLAUDE.md", "line": 7,
                "quote": "组合主线已于 2026-07-18 关闭（docs/portfolio/project-closure-2026-07-18.md），当前处于关闭后孵化期",
            },
        ],
        "why": "project-index.md 停留在 2026-07-03 的活跃任务顺序，CLAUDE.md 记录组合主线已于 2026-07-18 关闭。",
        "resolution": "待裁定",
        "action": "只标注，不修改 docs/portfolio/project-index.md 正文。",
    },
    {
        "id": "C3",
        "title": "investigations 索引停在 2026-07-08，未收录 2026-10 的 token-* / tsinghua-* 系列",
        "claims": [
            {
                "path": "docs/investigations/INDEX.md", "line": 3,
                "quote": "Last cleaned: 2026-07-08. 6 canonical docs kept current; 22 stale verdict-chain / intermediate docs archived under archive/.",
            },
            {
                "path": "docs/investigations/INDEX.md", "line": 6,
                "quote": "## Canonical (read these first — current state)",
            },
            {
                "path": "docs/investigations/token-report-2026-10-27.md", "line": 1,
                "quote": "（2026-10 新增报告，未被 INDEX.md 的 6 canonical 收录；此处以文件存在性为证）",
                "kind": "existence_evidence",
            },
        ],
        "why": "INDEX.md 的 canonical 列表（第 8–17 行）不含 2026-10 约 20 篇 token-* / tsinghua-* 讨论与报告，例如 docs/investigations/token-report-2026-10-27.md、docs/investigations/tsinghua-1025-vs-may-2026-10-27.md。",
        "resolution": "待裁定",
        "action": "只标注，不修改 docs/investigations/INDEX.md 正文；新文档逐条登记进本索引 docs[]。",
    },
    {
        "id": "C4",
        "title": "analysis/README.md 称 worldcup-2026/ 待建，实际已存在并运行到 2026-09-11",
        "claims": [
            {
                "path": "analysis/README.md", "line": 17,
                "quote": "| worldcup-2026/（待建） | evidence/cds4worldcup-snapshot-2026-07-20/ | 计划 W1 建立，见 docs/plans/worldcup-algorithms-comparison-paper-2026-07-20.md |",
            },
            {
                "path": "analysis/worldcup-2026/CHANGELOG.md", "line": 1,
                "quote": "# CHANGELOG — analysis/worldcup-2026/",
            },
            {
                "path": "analysis/worldcup-2026/CHANGELOG.md", "line": 5,
                "quote": "## 2026-09-11（Paper A 连贯工作稿 · 不改证据）",
            },
        ],
        "why": "README 说「待建」，但该目录已存在且含 CHANGELOG.md、2 个 .py、多篇工作稿；analysis/ 另有 23 个一级子目录、185 个 .py。",
        "resolution": "待裁定",
        "action": "只标注，不修改 analysis/README.md 正文。",
    },
    {
        "id": "C5",
        "title": "state/progress.json 的 status 停在 W6 备忘录阶段（metadata drift）",
        "claims": [
            {
                "path": "CLAUDE.md", "line": 23,
                "quote": "⚠️ 状态口径警告（2026-07-20）：state/progress.json 的 status 字段停在 W6 备忘录阶段，未同步 v1.3 主线裁定（metadata drift）。课题状态以本表为准",
            },
            {
                "path": "state/progress.json", "line": 3,
                "quote": "\"status\": \"PAUSED_2026_07_20_worldcup_paper_topic_W6_GO_with_8_gates_pending_A0_final_settlement\"",
            },
            {
                "path": "CLAUDE.md", "line": 7,
                "quote": "当前主线（2026-09-25 起挂起、投稿暂停）：世界杯算法比较实证论文（用户裁定 2026-07-20，以开题报告为主线）",
                "head_quote": "当前活跃主线：世界杯算法比较实证论文（用户裁定 2026-07-20，以开题报告为主线）",
                "source_note": "引文于 2026-11-05 随外部改动同步；HEAD 旧版见 head_quote，可经 git show HEAD:CLAUDE.md | sed -n '7p' 回溯",
            },
        ],
        "why": "CLAUDE.md:23 自报 metadata drift；state/progress.json:3 仍为 W6 备忘录阶段 status，与 CLAUDE.md:7 的 v1.3 主线裁定不同步。",
        "resolution": "待裁定",
        "action": "只标注，不修改 CLAUDE.md / state/progress.json 正文；state/ 为高引用只读区。",
    },
]

# ---------------------------------------------------------------- 人工标注种子
# 仅在条目「首次出现」时用于填充人工字段；之后 docs/index.json 是权威，脚本不覆盖。

MANUAL_DOCS = {
    "docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms.md": {
        "title": "世界杯算法比较实证论文开题（v1.3，CLAUDE.md 列为主线）",
        "topic": "世界杯主线", "status": "挂起", "verified_at": "2026-11-05",
    },
    "docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms-v2.md": {
        "title": "世界杯开题 v2.1（W5 后定位，README 列为主线）",
        "topic": "世界杯主线", "status": "挂起", "verified_at": "2026-11-05",
    },
    "docs/plans/worldcup-algorithms-comparison-paper-2026-07-20.md": {
        "title": "世界杯算法比较论文计划（2026-07-20 裁定）",
        "topic": "世界杯主线", "status": "挂起", "verified_at": "2026-11-05",
    },
    "docs/roadmaps/worldcup-two-paper-roadmap-2026-07-21.md": {
        "title": "世界杯双论文路线图 v1.7",
        "topic": "世界杯主线", "status": "挂起", "verified_at": "2026-11-05",
    },
    "docs/roadmaps/worldcup-two-paper-roadmap-2026-07-21-working.md": {
        "title": "世界杯双论文路线图工作稿",
        "topic": "世界杯主线", "status": "挂起", "verified_at": "2026-11-05",
        "supersedes": ["docs/roadmaps/worldcup-two-paper-roadmap-2026-07-21.md"],
    },
    "docs/investigations/worldcup-paper-topic-2026-07-19.md": {
        "title": "W6 终裁备忘录（用户裁定降为参考）",
        "topic": "世界杯主线", "status": "superseded", "verified_at": "2026-11-05",
    },
    "docs/investigations/decision-coscientist-proposal/proposal-decision-coscientist.md": {
        "title": "Decision Co-Scientist 开题主文档",
        "topic": "Decision Co-Scientist", "status": "dormant", "verified_at": "2026-11-05",
    },
    "docs/investigations/decision-coscientist-proposal/PROJECT-BRIEF.md": {
        "title": "Decision Co-Scientist 陌生人入口单文档简报",
        "topic": "Decision Co-Scientist", "status": "dormant", "verified_at": "2026-11-05",
    },
    "docs/plans/decision-coscientist-experiment-2026-07-19.md": {
        "title": "Decision Co-Scientist 实验计划",
        "topic": "Decision Co-Scientist", "status": "dormant", "verified_at": "2026-11-05",
    },
    "docs/portfolio/project-closure-2026-07-18.md": {
        "title": "组合主线关闭记录（当前权威关闭名单）",
        "topic": "组合治理", "status": "active", "verified_at": "2026-11-05",
    },
    "docs/portfolio/aliases.md": {
        "title": "论文代号映射（P7 / P8 / P12 / P1+P2）",
        "topic": "组合治理", "status": "active", "verified_at": "2026-11-05",
    },
    "docs/portfolio/project-index.md": {
        "title": "旧版项目组合索引（2026-07-03，状态已知过时）",
        "topic": "组合治理", "status": "superseded", "verified_at": "2026-11-05",
        "supersedes": [],
    },
    "docs/investigations/INDEX.md": {
        "title": "旧版 investigations 索引（停在 2026-07-08）",
        "topic": "已有索引", "status": "superseded", "verified_at": "2026-11-05",
    },
    "docs/investigations/meta-uncertainty-and-blindspot-2026-07-07.md": {
        "title": "元诊断：LLM-on-LLM 自指循环与人类盲点",
        "topic": "AutoResearch 框架", "status": "active", "verified_at": "2026-11-05",
    },
    "docs/investigations/karpathy-loop-harness-2026-07-07.md": {
        "title": "Karpathy autoresearch / evaluator-lock 外部 prior art 核查",
        "topic": "AutoResearch 框架", "status": "active", "verified_at": "2026-11-05",
    },
    "docs/autoresearch/README.md": {
        "title": "AutoResearch 框架与运行材料入口",
        "topic": "AutoResearch 框架", "status": "active", "verified_at": "2026-11-05",
    },
    "docs/portfolio/FRAMEWORK-RULES.md": {
        "title": "框架规则（含 R7 cite-restoration，归档不得删的依据）",
        "topic": "组合治理", "status": "active", "verified_at": "2026-11-05",
    },
    "docs/investigations/dmo-uncertainty-decision-reading-2026-07-22.md": {
        "title": "DMO 不确定性决策文献精读（已关闭 2026-07-22）",
        "topic": "世界杯主线", "status": "archived", "verified_at": "2026-11-05",
    },
    "docs/roadmaps/topic5-research-directions.md": {
        "title": "课题五全量方向规划（历史基线）",
        "topic": "组合治理", "status": "superseded", "verified_at": "2026-11-05",
    },
    "docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md": {
        "title": "2026-07-03 路线图（旧版执行准绳）",
        "topic": "组合治理", "status": "superseded", "verified_at": "2026-11-05",
    },
}

MANUAL_SCRIPTS = {
    "analysis/downloads-pdf-scan/extract.py": {
        "purpose": "通用 PDF 文本抽取，独立于任何按日期命名的任务副本",
        "reusable": True,
    },
    "analysis/tsinghua-1024-dna-value/frozen/jaccard.py": {
        "purpose": "Jaccard 相似度实现；与 tsinghua-factorial-ablation-20261025/frozen/jaccard.py 构成重复骨架，可作为抽取公共实现的参考",
        "reusable": False,
    },
    "analysis/worldcup-2026/fig6_and_metrics_2026-07-26.py": {
        "purpose": "世界杯图 6 与指标复算（绑定 2026-07-26 冻结数据，一次性）",
        "reusable": False,
    },
}

# 主题键：用于「一个任务散落三处」的自动交叉引用（首次生成时填入，之后不覆盖）
TAG_RULES = [
    ("token-1023", r"token-1023"),
    ("token-1025", r"token-1025"),
    ("token-consumption", r"token-consumption|consumption-handoff"),
    ("token-readiness", r"token-readiness|final-readiness|readiness-recheck"),
    ("token-imputation", r"token-imputation|imputation"),
    ("token-paper-accounting", r"token-paper-accounting|paper-accounting"),
    ("token-report", r"token-report|token-adoption|token-1023-handoff|handoff-confirmation"),
    ("tsinghua-1024", r"tsinghua-1024|1024-dna|1024-clean"),
    ("tsinghua-1025", r"tsinghua-1025|1025-vs-may"),
    ("tsinghua-factorial", r"factorial"),
    ("tsinghua-clean-release", r"clean-release|clean_release"),
    ("tsinghua-dna-ablation", r"dna-ablation|dna-value|dna_value|dna-final"),
    ("tsinghua-baseline", r"baseline-audit|baseline_audit"),
    ("reprompt", r"reprompt"),
    ("worldcup", r"worldcup|paper-a|paper-b|two-paper|evidence-roadmap|kimi-reasoning"),
    ("decision-coscientist", r"decision-coscientist|coscientist"),
    ("topic-selection", r"topic-selection"),
]
COMPILED_TAGS = [(tag, re.compile(pat, re.I)) for tag, pat in TAG_RULES]


# ---------------------------------------------------------------- 扫描与推断

def file_stat(rel, full):
    """返回骨架字段：mtime / size / heading。"""
    try:
        st = full.stat()
        mtime = datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%dT%H:%M:%S")
        size = st.st_size
    except OSError:
        mtime, size = "", 0
    return mtime, size, read_heading(full)


def read_heading(full):
    """首段标题：md 取首个 '# ' 行；py 取首个注释或 docstring 首行。"""
    try:
        with open(full, "r", encoding="utf-8", errors="replace") as fh:
            lines = []
            for i, line in enumerate(fh):
                if i > 40:
                    break
                lines.append(line.rstrip("\n"))
    except OSError:
        return ""
    is_py = str(full).endswith(".py")
    if not is_py:
        for line in lines:
            s = line.strip()
            if s.startswith("# "):
                return s[2:].strip()
        return ""
    in_doc = False
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith('"""') or s.startswith("'''"):
            if not in_doc:
                in_doc = True
                inner = s.strip('"\'').strip()
                if inner:
                    return inner[:120]
                continue
            in_doc = False
            continue
        if in_doc:
            return s[:120]
        if s.startswith("#!") or (s.startswith("#") and "coding" in s):
            continue
        if s.startswith("#"):
            return s.lstrip("#").strip()[:120]
        return ""  # 代码行不作为「首段标题」
    return ""


def scan_docs():
    base = REPO_ROOT / "docs"
    out = []
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = sorted(
            d for d in dirnames
            if not d.startswith(".") and d not in DOC_PRUNE_DIRS
        )
        for fn in sorted(filenames):
            if not fn.endswith(".md") or fn == "SECRETS.md":
                continue
            full = Path(dirpath) / fn
            rel = full.relative_to(REPO_ROOT).as_posix()
            if len(Path(rel).parts) <= 2:  # 排除 docs/ 顶层 *.md
                continue
            out.append((rel, full))
    return sorted(out, key=lambda x: x[0])


def scan_scripts():
    base = REPO_ROOT / "analysis"
    out = []
    limit_dir_depth = SCRIPT_MAX_FILE_DEPTH - 1  # = 2
    for dirpath, dirnames, filenames in os.walk(base):
        depth = len(Path(dirpath).relative_to(base).parts)
        if depth >= limit_dir_depth:
            dirnames[:] = []
        if depth > limit_dir_depth:
            continue
        for fn in sorted(filenames):
            if not fn.endswith(".py"):
                continue
            full = Path(dirpath) / fn
            rel = full.relative_to(REPO_ROOT).as_posix()
            out.append((rel, full))
    return sorted(out, key=lambda x: x[0])


def infer_kind(rel):
    if "/plans/" in rel or "/compose/plans/" in rel:
        return "plan"
    if "/investigations/" in rel:
        return "investigation"
    if "/reviews/" in rel:
        return "review"
    if "/roadmaps/" in rel:
        return "roadmap"
    if "/progress/" in rel:
        return "progress"
    if "/portfolio/" in rel:
        return "portfolio"
    return "other"


def infer_capability(rel):
    n = rel.rsplit("/", 1)[-1].lower()
    if "test" in n:
        return "test"
    if "freeze" in n or "pin_" in n:
        return "freeze_inputs"
    if any(k in n for k in ("recompute", "reproduce", "replay", "score",
                            "analyze", "compute", "statistic", "jaccard",
                            "benchmark", "probe", "master_table", "design")):
        return "recompute"
    if any(k in n for k in ("verify", "check", "validate", "audit",
                            "preflight", "gate", "acceptance", "smoke",
                            "readiness", "inspection")):
        return "verify"
    if any(k in n for k in ("release", "finalize", "render", "build_report",
                            "build_figure", "figure")):
        return "release"
    if any(k in n for k in ("report", "summary", "adapter", "adapt",
                            "compare_report", "convert")):
        return "report"
    if any(k in n for k in ("extract", "decode", "capture", "parse",
                            "inspect", "recover", "restore", "relocate",
                            "assemble", "prepare", "public_projection")):
        return "extract"
    return "other"


def infer_topic(rel):
    low = rel.lower()
    ordered = [
        ("decision-coscientist", "Decision Co-Scientist"),
        ("coscientist", "Decision Co-Scientist"),
        ("token-", "2026-10 token 系列"),
        ("tsinghua", "2026-10 tsinghua 系列"),
        ("reprompt", "2026-10 reprompt 会话调查"),
        ("papers-closed-portfolio", "已关闭组合论文产出"),
        ("/archive/", "历史归档调查"),
        ("topic-selection", "课题终裁链"),
        ("worldcup", "世界杯主线"),
        ("paper-a", "世界杯主线"),
        ("paper-b", "世界杯主线"),
        ("two-paper", "世界杯主线"),
        ("evidence-roadmap", "世界杯主线"),
        ("/portfolio/", "组合治理"),
        ("/roadmaps/", "路线图"),
        ("/reviews/", "评审"),
        ("/progress/", "进度"),
        ("/autoresearch/", "AutoResearch 框架"),
        ("/compose/", "跨项目编排"),
        ("/analysis/", "元评审"),
        ("/plans/", "研究计划"),
        ("/investigations/", "调查与开题"),
    ]
    for key, topic in ordered:
        if key in low:
            return topic
    return "其他"


def default_status(rel):
    if "/archive/" in rel or "papers-closed-portfolio" in rel:
        return "archived"
    low = rel.lower()
    if "worldcup" in low or "paper-a" in low or "paper-b" in low \
            or "two-paper" in low or "evidence-roadmap" in low:
        return "挂起"
    if "decision-coscientist" in low or "coscientist" in low:
        return "dormant"
    if rel.startswith("docs/roadmaps/") or rel.startswith("docs/portfolio/"):
        return "superseded"
    return "active"


def short_id(rel):
    return "doc-" + hashlib.sha1(rel.encode("utf-8")).hexdigest()[:10]


def tag_of(rel):
    """返回最具体的主题键，用于跨三处关联；无匹配返回 None。"""
    for tag, rx in COMPILED_TAGS:
        if rx.search(rel):
            return tag
    return None


def build_relations(doc_paths, script_paths):
    """按主题键把 docs/plans/ 计划、docs/investigations/ 报告、analysis/ 脚本互链。"""
    doc_tags = {}
    for p in doc_paths:
        t = tag_of(p)
        if t:
            doc_tags.setdefault(t, []).append(p)
    script_tags = {}
    for p in script_paths:
        t = tag_of(p)
        if t:
            script_tags.setdefault(t, []).append(p)
    rel_docs, rel_scripts = {}, {}
    for p in doc_paths:
        t = tag_of(p)
        if not t:
            rel_docs[p], rel_scripts[p] = [], []
            continue
        rel_docs[p] = [q for q in doc_tags.get(t, []) if q != p][:8]
        rel_scripts[p] = list(script_tags.get(t, []))[:10]
    return rel_docs, rel_scripts


# ---------------------------------------------------------------- 索引合并

def load_index():
    if not INDEX_PATH.exists():
        return {}
    try:
        with open(INDEX_PATH, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError) as exc:
        print("[错误] 无法解析现有 %s：%s" % (INDEX_PATH.relative_to(REPO_ROOT), exc))
        sys.exit(2)


def merge_docs(scan, existing, rel_docs, rel_scripts, stale_map):
    old = {d.get("path"): d for d in existing.get("docs", []) if d.get("path")}
    out = []
    for rel, full in scan:
        mtime, size, heading = file_stat(rel, full)
        seed = dict(MANUAL_DOCS.get(rel, {}))
        prior = old.get(rel) or stale_map.get(rel)
        if prior:
            entry = dict(prior)  # 人工字段一律沿用
        else:
            entry = {
                "id": short_id(rel),
                "title": heading or rel.rsplit("/", 1)[-1],
                "topic": infer_topic(rel),
                "status": default_status(rel),
                "verified_at": TODAY,
                "supersedes": [],
                "related_scripts": rel_scripts.get(rel, []),
                "related_docs": rel_docs.get(rel, []),
            }
            entry.update(seed)  # 种子只用于首次生成
        # 补齐缺失字段（不覆盖已有值）
        entry.setdefault("id", short_id(rel))
        entry.setdefault("title", heading or rel.rsplit("/", 1)[-1])
        entry.setdefault("topic", infer_topic(rel))
        entry.setdefault("status", default_status(rel))
        entry.setdefault("verified_at", TODAY)
        entry.setdefault("supersedes", [])
        entry.setdefault("related_scripts", rel_scripts.get(rel, []))
        entry.setdefault("related_docs", rel_docs.get(rel, []))
        # 骨架字段刷新
        entry["path"] = rel
        entry["mtime"] = mtime
        entry["size"] = size
        entry["heading"] = heading
        entry["kind"] = infer_kind(rel)
        out.append(entry)
    return out


def merge_scripts(scan, existing, stale_map):
    old = {s.get("path"): s for s in existing.get("scripts", []) if s.get("path")}
    out = []
    for rel, full in scan:
        mtime, size, heading = file_stat(rel, full)
        prior = old.get(rel) or stale_map.get(rel)
        if prior:
            entry = dict(prior)
        else:
            entry = {}
            entry.update(MANUAL_SCRIPTS.get(rel, {}))
        entry.setdefault(
            "purpose", "%s 能力脚本：%s" % (
                infer_capability(rel), rel.rsplit("/", 1)[-1]))
        entry.setdefault("reusable", False)
        entry["path"] = rel
        entry["mtime"] = mtime
        entry["size"] = size
        entry["heading"] = heading
        entry["capability"] = infer_capability(rel)
        entry["workdir"] = rel.rsplit("/", 1)[0]
        out.append(entry)
    return out


def collect_stale(existing, docs, scripts, stale_prior):
    live = set(d["path"] for d in docs) | set(s["path"] for s in scripts)
    old_entries = []
    for key, kind in (("docs", "doc"), ("scripts", "script")):
        for e in existing.get(key, []):
            if e.get("path") and e["path"] not in live:
                old_entries.append({"kind": kind, "entry": e})
    seen = set()
    merged = []
    for item in stale_prior + old_entries:
        p = item.get("entry", {}).get("path")
        if p and p not in seen and p not in live:
            seen.add(p)
            merged.append(item)
    return merged


def compose(existing, docs, scripts, stale):
    top = {}
    # 顶层人工/配置区块：已存在即保留，绝不覆盖
    constants = {
        "scope": SCOPE,
        "data_zones": DATA_ZONES,
        "readonly_zones": READONLY_ZONES,
        "status_conflicts": STATUS_CONFLICTS,
    }
    for key, default in constants.items():
        top[key] = existing.get(key) or default
    top["generated_at"] = TODAY
    top["generator"] = existing.get("generator") or GENERATOR
    counts = dict(existing.get("counts") or COUNTS_SNAPSHOT)
    counts["docs_indexed"] = len(docs)
    counts["scripts_indexed"] = len(scripts)
    top["counts"] = counts
    top["docs"] = docs
    top["scripts"] = scripts
    top["stale_paths"] = stale
    return top


def write_index(data):
    text = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False)
    with open(INDEX_PATH, "w", encoding="utf-8") as fh:
        fh.write(text + "\n")


# ---------------------------------------------------------------- 三种模式

def mode_check(existing):
    print("=== --check：校验 docs/index.json 全部 path 是否仍存在 ===")
    if not existing:
        print("[错误] docs/index.json 不存在或为空，请先运行默认模式生成。")
        return 2
    missing = []
    checked = 0
    for key in ("docs", "scripts"):
        for e in existing.get(key, []):
            p = e.get("path")
            if not p:
                continue
            checked += 1
            if not (REPO_ROOT / p).exists():
                missing.append((key, p))
    for key in ("data_zones", "readonly_zones"):
        for z in existing.get(key, []):
            p = z.get("path")
            if p:
                checked += 1
                if not (REPO_ROOT / p).exists():
                    missing.append((key, p))
    print("已校验 path 总数：%d" % checked)
    print("docs[] 条目：%d，scripts[] 条目：%d" % (
        len(existing.get("docs", [])), len(existing.get("scripts", []))))
    if missing:
        print("失效清单（%d 条）：" % len(missing))
        for key, p in missing:
            print("  - [%s] %s" % (key, p))
        return 1
    print("失效清单：0 条 —— 全部 path 均能在磁盘解析到真实文件。")
    print("（只读校验，未写回任何文件）")
    return 0


def main():
    ap = argparse.ArgumentParser(description="auto-research 仓库级索引再生脚本")
    ap.add_argument("--dry-run", action="store_true", help="不写回，只打印将要发生的变更")
    ap.add_argument("--check", action="store_true", help="只校验现有 index.json 所有 path 是否存在")
    args = ap.parse_args()

    if args.check:
        return mode_check(load_index())

    existing = load_index()
    doc_scan = scan_docs()
    script_scan = scan_scripts()
    doc_paths = [p for p, _ in doc_scan]
    script_paths = [p for p, _ in script_scan]
    rel_docs, rel_scripts = build_relations(doc_paths, script_paths)

    stale_prior = existing.get("stale_paths", [])
    stale_map = {}
    for item in stale_prior:
        e = item.get("entry", {})
        if e.get("path"):
            stale_map[e["path"]] = e

    docs = merge_docs(doc_scan, existing, rel_docs, rel_scripts, stale_map)
    scripts = merge_scripts(script_scan, existing, stale_map)
    stale = collect_stale(existing, docs, scripts, stale_prior)
    data = compose(existing, docs, scripts, stale)

    old_doc_paths = set(d.get("path") for d in existing.get("docs", []))
    old_script_paths = set(s.get("path") for s in existing.get("scripts", []))
    new_docs = [p for p in doc_paths if p not in old_doc_paths]
    new_scripts = [p for p in script_paths if p not in old_script_paths]

    print("=== 扫描结果 ===")
    print("docs/ 讨论文档（已排除数据区/顶层/隐藏目录）：%d 篇" % len(doc_scan))
    print("analysis/ 脚本（限深 %d）：%d 个" % (SCRIPT_MAX_FILE_DEPTH, len(script_scan)))
    print("将新增 docs[]：%d 条；将新增 scripts[]：%d 条" % (
        len(new_docs), len(new_scripts)))
    for p in new_docs[:5]:
        print("  + doc  %s" % p)
    if len(new_docs) > 5:
        print("  ... 其余 %d 条略" % (len(new_docs) - 5))
    for p in new_scripts[:5]:
        print("  + py   %s" % p)
    if len(new_scripts) > 5:
        print("  ... 其余 %d 条略" % (len(new_scripts) - 5))
    print("失效（stale_paths）：%d 条" % len(stale))
    print("人工字段保护：docs[] 的 id/title/topic/status/verified_at/supersedes/"
          "related_scripts/related_docs 与 scripts[] 的 purpose/reusable 均不会被覆盖。")

    if args.dry_run:
        print("[--dry-run] 未写回任何文件。")
        return 0

    write_index(data)
    print("已写回 %s（generated_at=%s）" % (
        INDEX_PATH.relative_to(REPO_ROOT).as_posix(), TODAY))
    print("counts.docs_indexed=%d，counts.scripts_indexed=%d" % (
        len(docs), len(scripts)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
