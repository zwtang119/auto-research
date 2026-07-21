# CDS 业务重构设计

> **类型**：decision
> **状态**：approved
> **日期**：2026-06-06
**来源**：archive/cds-business-rebuild-design.md

---

## 背景

CDS 相关资产分散在多个仓库（policysim-research-Tsinghua、Policysim-v0.2、cds4polymarket、cds-keyperson）。商业航天项目已完成签约、交付与回款，需要从单点成功升级为可复制的交付系统。

## 决策结果

**主线重构为：**
- 商业航天：已验证样板（方法论样板、销售证明）
- 应急管理部：下一阶段跨场景复制验证
- 电网项目：高概率并行扩展机会
- CDS-keyperson：机会型分支

## Roadmap

| 阶段 | 时间 | 核心目标 |
|------|------|----------|
| 复制落地期 | 0-3 月 | 应急管理部项目完成第二个样板复制 |
| 并行验证期 | 3-6 月 | 拿下电网项目订单 |
| 产品沉淀期 | 6-9 月 | 共性模块抽象为标准交付底座 |
| 可扩张期 | 9-12 月 | 标准交付包 + 半产品化工作台 |

## 优先级

1. 应急管理部项目（第一优先级）
2. 电网项目订单（第二优先级）
3. CDS-keyperson demo 转单机会（第三优先级）

## 非目标

- 不以"先做通用平台再找市场"为主线
- 不将 cds4polymarket 包装为核心市场方向
- 不将 CDS-keyperson 提前升级为主战场

本决策文档完整版见 archive/cds-business-rebuild-design.md

---

## 相关页面

- [[concepts/cds]]: CDS 计算决策空间
- [[concepts/decision-control-plane]]: 决策控制面
- [[decisions/nlui-decision-workspace-mvp]]: NLUI Decision Workspace MVP
