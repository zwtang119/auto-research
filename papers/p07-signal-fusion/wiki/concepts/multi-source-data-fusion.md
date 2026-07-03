# 多源数据融合

> **定义**：12 个外部数据源的信息通过 SignalFusionEngine 融合为镜头权重 + 三情景预测的统一结构化信号。

## 12 Active Datasources

从 cds-keyperson 的 14 领域 19 核心源的子集：

| 类别 | 数据源 |
|------|------|
| 金融市场 | finance.py, energy.py |
| 地缘政治 | geopolitics.py, sanctions.py |
| 宏观经济 | macro.py |
| 新闻舆情 | news.py |
| 学术 | academic.py |
| 预测市场 | polymarket.py |
| 通用百科 | wikipedia.py |
| 其他 | weather.py, aviation.py, sports.py |

## 融合输出

- **镜头权重（Lens Weight）**：每个数据源对当前决策的相对重要性
- **三情景预测**：乐观/基准/悲观三种情景的概率化描述
- **偏差诊断**：当前信息是否存在系统性偏见（偏乐观/偏悲观）

## 相关页面

- [[concepts/signal-fusion-pipeline]]: 融合管线技术细节
- [[decisions/datasource-selection]]: 数据源选择决策
