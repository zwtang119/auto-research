# analysis/ — 分析副本根目录

> 命名约定（2026-07-20 用户裁定，详见 `evidence/cds4worldcup-snapshot-2026-07-20/MANIFEST.md`）：
> **封存仓库**（零读写证据原体）→ **证据快照**（`evidence/`，字节级原始，永不修改）→ **分析副本**（本目录，可写）。

## 规则

- 本目录是**分析副本**的唯一存放位置：从证据快照派生的可写工作区。
- 每个分析副本一个子目录（如 `analysis/worldcup-2026/`），根目录内必须维护 `CHANGELOG.md`，逐条登记所有增补（赛果补齐、ex-ante 版本提取、复算产物）及其来源。
- 禁止把增补信息回写到 `evidence/` 下的证据快照。
- 本目录内容默认不入 git（在 `.gitignore` 中排除）；需要共享的产物（结算表、图表）提炼后放入 `docs/` 或对应论文目录。

## 当前分析副本

| 目录 | 来源 | 状态 |
|---|---|---|
| `worldcup-2026/`（待建） | `evidence/cds4worldcup-snapshot-2026-07-20/` | 计划 W1 建立，见 `docs/plans/worldcup-algorithms-comparison-paper-2026-07-20.md` |
