# results/ — 预测结果

本目录存放 CDS4WorldCup 的分析结果和预测输出。

## 目录约定

```
results/
├── summary.md          # 最新汇总（自动注入到 GitHub Pages 首页）
├── round-1/            # 第一轮结果
│   ├── group-a.md
│   ├── group-b.md
│   └── ...
├── round-2/            # 淘汰赛结果
└── archive/            # 历史版本（保留回溯）
```

## 规范

- 结果文件使用 Markdown 格式，方便 GitHub Pages 渲染
- 每个结果文件必须包含：生成时间、数据来源、方法论说明
- `summary.md` 是首页展示的入口，由 `src/publish/` 脚本自动生成
- 大型数据文件（CSV、JSON）放在 `data/` 目录，不放在 results/
