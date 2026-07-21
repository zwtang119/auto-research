# CDS4WorldCup

计算决策空间 × 2026 FIFA 世界杯路径分析实验。基于 Marginalia 协议管理知识。

## 项目概述

CDS4WorldCup 是面向 2026 FIFA 世界杯的路径空间与可校准知识实验项目。
使用 CDS（计算决策空间）方法论进行结构化路径分析，通过 GitHub Pages 自动发布结果。

- **一句话**：让复杂决策先在机器中运行，再在现实中执行。
- **方法论**：路径空间 + 因子账本 + 来源分级
- **知识管理**：Marginalia 边注系统
- **发布**：GitHub Pages 自动部署

## 项目结构

```
cds4worldcup/
├── src/                # 开发代码（analysis/、data/、publish/、utils/）
├── data/               # 数据文件（raw/ 不上库）
├── results/            # 预测结果（发布到 GitHub Pages）
├── site/               # GitHub Pages 站点源文件
├── wiki/               # 知识库（Marginalia 协议）
├── docs/               # 项目文档（references/、design/ 不上库）
├── schema/             # Marginalia 协议规则
├── scripts/            # 知识库工具脚本
├── templates/          # 页面模板
├── example/            # Marginalia 示例知识库
└── archive/            # 历史归档（不上库）
```

## AI 助手工作流

### 进入项目时
1. 读 `wiki/index.md` 了解知识库全貌
2. 读 `docs/source-policy.md` 了解来源分级规则
3. 读当前正在执行的 `specs/` 文件

### 执行 spec 时
1. 读 `specs/` 下对应的 spec 文件
2. 按任务顺序执行，每完成一个任务更新 wiki
3. 在相关 wiki 页面添加批注：`> [!memo] YYYY-MM-DD 内容`

### 开发代码时
- 代码放在 `src/` 下对应子目录
- 结果输出到 `results/`
- 大数据文件放 `data/raw/`（不上库）
- 处理后数据放 `data/processed/`（上库）

### 完成工作后
- 更新 `wiki/index.md`（如有新页面）
- 运行 `python3 scripts/audit.py --root wiki/` 检查知识库健康
- 提交 PR，CI 会自动验证

## 约束

- 知识库使用纯 Markdown，不引入第三方依赖
- 批注必须包含日期
- spec 文件是只读参考，不要直接修改
- `docs/references/` 下的文件是敏感文档，绝不上库
- 不输出投注建议，不报告收益率（见 source-policy.md）

## 批注格式

> [!memo] YYYY-MM-DD 内容
