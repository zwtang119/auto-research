# Public Site Update Flow

> 面向维护者。不要把本页内容复制到公开网站。

## 什么时候更新

- 每场比赛后：更新赛果、路径卡或赛中观察项。
- 市场看法需要刷新时：重新抓一次市场快照。
- 外部模型群体重跑后：更新处理后的 CSV，再重建站点数据。

## 常规更新命令

```bash
python3 scripts/fetch_market_snapshot.py
python3 scripts/build_site_data.py
python3 -m unittest tests/test_build_site_data.py tests/test_fetch_market_snapshot.py
python3 scripts/verify.py --root wiki/
python3 scripts/audit.py --root wiki/
```

## 市场快照失败怎么办

市场快照失败不阻塞站点发布。站点会显示"市场快照待更新"。不要手写假概率。

## 公开页面边界

- 可以说 AI 多视角。
- 不说 Kimi / 小米 / MiMo。
- 市场数据只代表外界怎么看，不是投注建议。
- 外部模型群体是参考，不是事实来源。
