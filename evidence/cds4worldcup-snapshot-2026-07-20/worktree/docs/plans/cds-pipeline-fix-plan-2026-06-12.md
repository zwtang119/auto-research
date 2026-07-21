# CDS Pipeline 修复执行计划

基于深度调查报告 `docs/investigations/cds-pipeline-deep-investigation-2026-06-12.md` 执行修复。

## 基线
- 43/43 测试通过（执行前确认）

## Work Items

### WI-1: Quick Python Fixes（简单修复）
- [x] F-01: championship.py:215 `t != t` → `t != team` ✅
- [x] F-06: qualification.py:324 添加 `if team_pos is None: continue` ✅
- [x] F-17: championship.py:453 Elo 缺失 fallback 改为全局平均值 ✅
- [x] F-16: championship.py `_collect_teams_for_slot()` 添加 max_depth=10 ✅
- **完成标准**: ✅ 43 测试通过 + 手动验证完成

### WI-2: CDS Engine Probability Model（概率模型修复）
- [x] F-05: championship.py cache key 加入 team ✅
- [x] F-03: championship probability clamp 到 [0,1] ✅
- [x] F-04: qualification.py 保留 `qual_prob_top2` 字段 ✅
- [x] F-12: third_place_qual_prob 模型改进（小组平均实力） ✅
- **完成标准**: ✅ 44 测试通过（含新增概率边界测试）

### WI-3: Frontend Fixes（前端修复）
- [x] F-07: team-detail.js 夺冠概率条加 `Math.min(100, ...)` ✅
- [x] F-09: team-detail.js / panorama.js 比分加 escapeHtml ✅
- [x] F-10: match.js:125 renderError 加 escapeHtml ✅
- [x] F-15: panorama.js / team-detail.js round 加 escapeHtml ✅
- [x] F-11: 概率条百分比校正（largest remainder） ✅
- [x] panorama.js renderDateView 数据突变修复 ✅
- **完成标准**: ✅ 所有 innerHTML 动态数据均已转义

### WI-4: Build Pipeline Fixes（构建管线修复）
- [x] F-11b: build_site_data.py `_write_data_script()` 添加 `</script>` 转义 ✅
- [x] F-07b: `_write_data_script()` global_name 合法性校验 ✅
- [x] F-06b: `build_cds_paths_json()` 缺失字段默认值 ✅
- [x] F-08: `_validate_site_data()` 硬编码值提取为常量 ✅
- **完成标准**: ✅ 44 测试通过 + 构建输出无 None 字段

## 执行顺序
- Wave 1: WI-1（快速，独立）
- Wave 2: WI-2（复杂，依赖 WI-1 的基线）
- Wave 3: WI-3 + WI-4（可并行，独立于 WI-2 的代码区域）
- 最终: 运行全量测试 + 验证
