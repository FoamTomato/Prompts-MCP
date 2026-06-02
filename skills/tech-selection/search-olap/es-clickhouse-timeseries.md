---
name: tech-selection-search-olap
description: ES/ClickHouse/InfluxDB/TDengine 定位对比 — 全文检索→ES，海量聚合→ClickHouse，监控时序→InfluxDB，工业IoT→TDengine，含何时引入决策树。Use when 选搜索引擎/OLAP/时序库 / 评审检索或聚合或时序选型时。
parent: ./index.md
paths:
- '*.java'
- '*.yml'
- '*.xml'
- '*.sql'
triggers:
  keywords:
  - 搜索分析选型
  - 全文检索
  - 时序数据库
  - Elasticsearch
  - ClickHouse
  - InfluxDB
effort: medium
context: inline
version: '1.0'
---
# 搜索/分析/时序 · ES vs ClickHouse vs InfluxDB vs TDengine

> 本条管「四类系统定位 + 何时引入」。这四类是关系库的补充而非替代。
> 性能数字（如压缩比）为量级参考，落地前必须按真实负载压测。

## 定位对比

| 系统 | 定位 | 强项 | 不适用 |
|---|---|---|---|
| Elasticsearch | 全文检索 + 日志 | 倒排 / BM25 / 模糊 / 日志聚合 | 大规模数值聚合慢、存储贵 |
| ClickHouse | OLAP 列式 | 海量聚合亚秒级、压缩比高（省 ES 12-19x） | 无事务、点更新弱、不擅全文检索 |
| InfluxDB | 实时时序 | IoT/监控指标、写后即查、Grafana 生态 | 高基数软肋 |
| TDengine | 工业 IoT 时序 | 超高写入、强压缩、工业协议、保留 SQL | 通用分析/搜索生态窄 |

## 何时引入（决策树）

| 你的硬需求 | 选谁 |
|-----------|------|
| 全文检索 / 相关性排序 | Elasticsearch |
| 海量交互式聚合分析 / BI（可无事务） | ClickHouse |
| 通用监控时序、基数可控 | InfluxDB |
| 工业 IoT 海量设备 + 想保留 SQL | TDengine |

## 常见组合

- InfluxDB 实时告警 + ClickHouse 历史分析。
- ES 做检索 + ClickHouse 做日志聚合（省存储）。

## 反例

- ❌ 只是要几个数值聚合报表却上 ES —— 数值聚合慢且存储贵，ClickHouse 更合适。
- ❌ 没有真实检索/聚合/时序硬需求就引入这些系统 —— 关系库索引可能已够，徒增运维。

## 自检

- [ ] 需求是「检索」「聚合分析」还是「时序」？三者对应不同系统，没混淆？
- [ ] 引入前确认关系库的索引/物化视图确实扛不住？
- [ ] 选 ClickHouse 时接受「无事务、点更新弱」的代价？

## 相关

- 父：[`./index.md`](./index.md)
- 跨维度：[`../database/decision-tree.md`](../database/decision-tree.md)（主存储仍走关系/文档/KV）
