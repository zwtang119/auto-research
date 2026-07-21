# Investigation: GitHub Pages Site Showing Old Version

## Summary
本地 `main` 分支有 **7 个未推送的 commit**，所有近期升级（WI-2.1 ~ WI-2.5 + CDS pipeline 修复）都在本地，从未 push 到 `origin/main`。GitHub Pages 部署的是 remote 的 `0caf8e8`，而不是本地的 `875748b`。

## Symptoms
- 用户访问 https://zwtang119.github.io/cds4worldcup/index.html 看到的是旧版内容
- 近期的大量升级工作（panorama 页面、match 详情页、球队详情增强、CDS pipeline 修复等）没有反映在线上

## Background / Prior Research

### 本地 vs Remote 状态
- **Local HEAD**: `875748b` — fix: P0-1 Elo display + P0-2 championship probability normalization
- **Remote HEAD**: `0caf8e8` — feat: populate 3 baselines (FIFA ranking proxy, Elo proxy, market public)
- **差距**: 7 个 commit

### 未推送的 7 个 commit（从旧到新）
1. `574a5da` feat(site): add panorama match schedule page (WI-2.1)
2. `6b3a99b` feat(site): add match detail page (WI-2.2)
3. `f9fc5cd` WI-2.3: 球队详情增强 — 小组赛程 + 夺冠概率对比 + 导航更新
4. `9e9b274` WI-2.4 + WI-2.5: navigation integration + build pipeline verification
5. `d44e211` fix: P0+P1 code quality fixes from investigation
6. `ef30658` feat: CDS pipeline + panoramic upgrade + deep investigation fixes
7. `875748b` fix: P0-1 Elo display + P0-2 championship probability normalization

### GitHub Actions 部署记录
最后一次成功部署：`2026-06-12T11:07:22Z`，对应 commit `0caf8e8`
之后无新的 Pages 部署触发（因为没有新的 push 事件）

### 部署流程确认
`.github/workflows/pages.yml` 配置正确：
- 触发条件：`push` to `main` + `workflow_dispatch`
- 构建流程：checkout → Python build_site_data.py → 复制 site/ 到 _publish/ → upload-pages-artifact → deploy-pages
- 流程本身没有问题

## Investigation Log

### Phase 1 - 检查部署工作流
**Hypothesis:** 部署 workflow 可能配置错误
**Findings:** workflow 配置正确，触发条件和构建流程均正常
**Conclusion:** 消除 — 问题不在 workflow

### Phase 2 - 检查 Remote 部署记录
**Hypothesis:** 部署可能失败了
**Findings:** 最后一次部署成功但对应的 commit 是 `0caf8e8`，不是最新的本地 commit
**Evidence:** `gh run list` 显示最近一次 Pages deploy 是 2026-06-12T11:07:22Z，commit 为 `0caf8e8`
**Conclusion:** 部署成功但内容旧

### Phase 3 - 对比 Local vs Remote
**Hypothesis:** 本地 commit 未 push 到 remote
**Findings:** 确认 — `git log origin/main..HEAD` 显示 7 个 commit 只存在于本地
**Evidence:** 
- `git rev-parse HEAD` → `875748b`
- `git rev-parse origin/main` → `0caf8e8`
- `git log origin/main..HEAD` → 7 commits listed
**Conclusion:** **根因确认**

## Root Cause

**7 个 commit 从未被 push 到 `origin/main`。**

GitHub Pages 的部署依赖于 push 事件触发 `.github/workflows/pages.yml`。由于这 7 个 commit 只在本地，remote 的 `main` 分支仍然停留在 `0caf8e8`，Pages 从未被触发重新部署。

这导致线上站点仍然是 `0caf8e8` 时期的内容，缺少以下功能：
- Panorama 比赛日程页面 (WI-2.1)
- 比赛详情页面 (WI-2.2)
- 球队详情增强 (WI-2.3)
- 导航集成与构建验证 (WI-2.4/2.5)
- CDS pipeline 修复与全景升级
- Elo 显示与冠军概率归一化修复

## Recommendations

1. **立即推送**：执行 `git push origin main` 将 7 个 commit 推送到 remote
   - 这会自动触发 Pages 部署（concurrency 配置会取消正在运行的旧部署）
   - 预计 20-40 秒完成部署

2. **验证部署**：推送后在 Actions 页面确认 Deploy Pages workflow 成功运行

3. **可选 — 手动触发**：如果不想立即推送所有 commit，可以通过 `gh workflow run pages.yml` 手动触发部署（但需要 remote 上有最新代码）

## Preventive Measures
- 工作完成后养成 `git push` 的习惯，或者设置 `git config --global push.autoSetupRemote true`
- 可以在 CLAUDE.md 的 "完成工作后" 部分增加 "确认 git push 已执行" 的步骤
- 考虑使用 `gh pr create` 流程，PR 合并会自动触发部署
