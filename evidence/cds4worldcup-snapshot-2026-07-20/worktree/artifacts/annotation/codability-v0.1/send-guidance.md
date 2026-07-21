# Codability 标注发送指南

## 推荐发送对象

- 对足球有基本理解，但不需要是专家。
- 能认真按选项标注，不会自行查资料或改规则。
- 最好至少 2 人：一人标 `A-full300`，另一人标 `B-kappa100`。

## 不要发送

- 不要发送 `private/` 目录。
- 不要发送 `codability-id-map-private.csv`。
- 不要发送包含 faction / champion / confidence 的原始表。

## 发送附件

主标注者：

1. `codability-calibration-20.xlsx`
2. `codability-annotation-A-full300.xlsx`
3. `codability-rubric-v0.1.md`

第二标注者：

1. `codability-calibration-20.xlsx`
2. `codability-annotation-B-kappa100.xlsx`
3. `codability-rubric-v0.1.md`

如果对方不熟悉 Markdown，可以直接让对方只看 Excel 里的 `instructions` 工作表。

## 发送话术

你好，我在做一个世界杯 AI 预测理由的可审计性研究，需要你帮忙标注一批很短的中文 reason。

请注意：

1. 不需要查资料。
2. 不判断这句话是真是假。
3. 只判断它是否“原则上可被事实审计/结算”。
4. 请优先使用下拉选项，备注只在不确定时填写。
5. 先做 `calibration-20.xlsx`，我确认规则理解一致后，再做正式文件。

预计耗时：

- calibration 20 条：10-15 分钟。
- kappa 100 条：45-75 分钟。
- full 300 条：2-3 小时。

完成后请把 Excel 原文件发回，不要导出 PDF，也不要改文件名里的版本号。

## 回收后处理

1. 保存原始回收文件，不覆盖。
2. 先检查是否有空列、非法选项、漏标行。
3. 计算 100 条双标注一致性。
4. 生成 disagreement report。
5. 仲裁后再生成最终 `adjudicated` 版本。
