# src/ — 项目源代码

本目录存放 CDS4WorldCup 的所有开发代码。

## 目录约定

```
src/
├── analysis/       # 分析脚本（因子提取、路径计算等）
├── data/           # 数据处理（清洗、转换、导入）
├── publish/        # 结果发布脚本（生成 results/ 下的报告）
└── utils/          # 公共工具函数
```

## 规范

- 代码语言：Python 3.12+（零依赖优先，必要依赖记入 requirements.txt）
- 每个子目录应有 `__init__.py` 和独立的 `README.md`
- 运行入口统一放在根目录 `Makefile` 或 `scripts/` 下
