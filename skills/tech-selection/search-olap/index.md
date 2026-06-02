---
name: tech-selection-search-olap-index
description: 搜索/分析/时序选型索引 — Elasticsearch / ClickHouse / InfluxDB / TDengine 的定位对比 + 何时引入决策树。Use when 选搜索引擎/OLAP/时序库 / 评审检索或聚合或时序选型时。
parent: ../index.md
children:
  - { name: es-clickhouse-timeseries, path: es-clickhouse-timeseries.md, tag: skill, note: 四系统定位对比 + 何时引入决策树 }
when_to_descend: 任务涉及「要全文检索 / 海量聚合分析 / 时序」的引擎选型。
---

# Search-OLAP · 选型索引

> 引入前提醒：先确认真有检索/聚合/时序硬需求，否则一个关系库的索引可能就够，别过度复杂。

按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 在 ES / ClickHouse / InfluxDB / TDengine 之间定位与选型 | [es-clickhouse-timeseries](es-clickhouse-timeseries.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../message-queue/index.md`](../message-queue/index.md) · [`../database/index.md`](../database/index.md) · [`../cache/index.md`](../cache/index.md)
