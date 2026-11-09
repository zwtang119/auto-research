# docs/SCRIPTS.md — 脚本登记册（按能力分类）

> 最近核对：2026-11-05。本页由 [`index.json`](index.json) 的 `scripts[]` 派生；路径、`capability`、`reusable`、`workdir` 以 `index.json` 为准。
> 建立本页的目的：让 LLM 先按「我要做什么」查能力，再决定复用而非重写，避免每次临时写扫描脚本或凭目录名猜。

## 为什么按 capability 而不是按目录

`analysis/` 下有 **185 个 .py**（`find analysis -maxdepth 3` 口径），分布在 **16 个含 .py 的一级子目录**（磁盘实测 `analysis/` 共 **23 个**一级子目录，其余 7 个在限深 3 内不含 .py），绝大多数是按日期命名的一次性任务副本：`token-1023-append-20261027`、`token-1025-append-20261027`、`token-paper-accounting-20261027`、`token-readiness-audit-20261026`、`tsinghua-*` 等。几乎每个副本都重写同一套骨架，按目录查会看到十几份几乎相同的 `verify.py`；按能力查才能一次看到「所有做 verify 的脚本」。

**只有标 `reusable=true` 的才建议直接复用；当前 185 个里仅 1 个标注为可复用**（`analysis/downloads-pdf-scan/extract.py`）。其余均为一次性副本，建议按能力找到最近的骨架作参考、判断是否值得抽取公共实现，而不是直接复制整个副本。

## 查询顺序

1. 先想「我要做什么」：`freeze_inputs` / `verify` / `release` / `report` / `extract` / `recompute` / `test`。
2. 在本文对应 capability 节查候选脚本。
3. 需要精确字段时查 [`index.json`](index.json) 的 `scripts[]`（`path` / `capability` / `purpose` / `reusable` / `workdir`）。
4. 命中 `reusable=true` 直接复用；否则参照最近副本的骨架，避免从零写。
5. 未命中才做只读扫描，且**必须限深**：`analysis/` 全量约 85000 文件，不限深会导致进程被 SIGTERM。


## 脚本清单（已下移 · 2026-11-09 做梦 D4）

> 185 个脚本按 capability 的逐条清单、重复骨架模式与查找路径，已移至 [`SCRIPTS-DETAILS.md`](SCRIPTS-DETAILS.md)，内容逐字保留。
> 本页只保留查询顺序与 capability 判定规则；精确字段以 [`index.json`](index.json) 的 `scripts[]` 为准。
> 原页字节级备份见 [`backup/`](../analysis/memory-dream-2026-11-09/backup/)。

## capability 判定规则（确定性，可复算）

按文件名小写依次匹配，命中即返回：`test` → 含 `test`；`freeze_inputs` → 含 `freeze` / `pin_`；`recompute` → 含 `recompute/reproduce/replay/score/analyze/compute/statistic/jaccard/benchmark/probe/master_table/design`；`verify` → 含 `verify/check/validate/audit/preflight/gate/acceptance/smoke/readiness/inspection`；`release` → 含 `release/finalize/render/build_report/build_figure/figure`；`report` → 含 `report/summary/adapter/adapt/compare_report/convert`；`extract` → 含 `extract/decode/capture/parse/inspect/recover/restore/relocate/assemble/prepare/public_projection`；其余 `other`。规则源码见 [`tools/build_index.py`](tools/build_index.py) 的 `infer_capability()`。

## 维护约定

- 新增脚本后运行 `python3 docs/tools/build_index.py` 登进 `index.json` 的 `scripts[]`，再人工补 `purpose` / `reusable`（这两个字段脚本不会覆盖）。
- `reusable=true` 只给确实独立于某次任务、可跨任务调用的脚本；按日期命名的一次性副本一律 `false`。
- `analysis/` 深遍历会拖慢甚至被 SIGTERM；本页与 `index.json` 的脚本清单一律限深 3。
- 不写入 `evidence/`、`legacy/`、`papers/`、`framework/`；封存仓库零读写。
