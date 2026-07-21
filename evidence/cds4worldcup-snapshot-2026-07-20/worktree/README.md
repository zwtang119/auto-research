# CDS4WorldCup

> 计算决策空间 × 2026 FIFA 世界杯 — 让复杂决策先在机器中运行，再在现实中执行。

[![CI](https://github.com/tangzw119/cds4worldcup/actions/workflows/ci.yml/badge.svg)](https://github.com/tangzw119/cds4worldcup/actions/workflows/ci.yml)
[![Pages](https://github.com/tangzw119/cds4worldcup/actions/workflows/pages.yml/badge.svg)](https://tangzw119.github.io/cds4worldcup)

## 这是什么？

CDS4WorldCup 是一个**路径空间与可校准知识实验**项目：

- **方法论**：基于 CDS（计算决策空间）对世界杯进行结构化路径分析
- **知识管理**：使用 Marginalia 边注系统管理项目知识（`wiki/`）
- **公开结果**：预测结果通过 [GitHub Pages](https://tangzw119.github.io/cds4worldcup) 自动发布

**这不是一个预测冠军的项目。** 我们关注路径、因子和不确定性，而非单一结论。

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/tangzw119/cds4worldcup.git
cd cds4worldcup

# 知识库健康检查
python3 scripts/audit.py --root wiki/
python3 scripts/verify.py --root wiki/
```

## 目录结构

```
cds4worldcup/
├── src/                # 开发代码
│   ├── analysis/       #   分析脚本
│   ├── data/           #   数据处理
│   ├── publish/        #   结果发布
│   └── utils/          #   公共工具
├── data/               # 数据文件（raw/ 不上库）
├── results/            # 预测结果（自动发布到 GitHub Pages）
├── site/               # GitHub Pages 站点源文件
├── wiki/               # Marginalia 知识库
├── schema/             # Marginalia 协议规范
├── scripts/            # 知识库工具脚本（零依赖 Python）
├── templates/          # 页面模板
├── example/            # 示例知识库
├── docs/               # 项目文档（references/ 不上库）
├── docs/design/        # 设计规格与执行计划
└── archive/            # 历史内容（不上库）
```

## 核心概念

| 术语 | 定义 |
|------|------|
| **CDS** | Computational Decision Space，计算决策空间 |
| **NLUI** | Natural Language User Interface，自然语言用户界面 |
| **路径空间** | 每支球队从当前状态到可能终态的所有路径集合 |
| **因子账本** | 可观测、可结算的影响因子记录 |
| **来源分级** | Green/Yellow/Red 三级来源可信度管理 |

## 许可证

MIT — 详见 [LICENSE](LICENSE)

## 参与贡献

欢迎！请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。
