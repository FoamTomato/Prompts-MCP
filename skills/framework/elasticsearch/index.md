---
name: framework-elasticsearch-index
description: Elasticsearch 用法规范 6 项 — Mapping 设计 / 中文 IK 分词 / bool 查询 DSL / 聚合 / 与 MySQL 同步 / 深分页。Use when 设计 ES 索引 Mapping / 写检索或聚合 DSL / 配中文分词 / 排查深分页与同步问题时。
parent: ../index.md
children:
  - { name: elasticsearch-mapping-design, path: mapping-design.md, tag: skill, note: "Mapping：text 分词 vs keyword 精确/聚合/排序，别全 text" }
  - { name: elasticsearch-analyzer-ik, path: analyzer-ik.md, tag: skill, note: "中文 IK：ik_max_word 索引 / ik_smart 查询" }
  - { name: elasticsearch-query-dsl, path: query-dsl.md, tag: skill, note: "bool：must/should/filter/must_not，filter 不算分可缓存" }
  - { name: elasticsearch-aggregation, path: aggregation.md, tag: skill, note: "聚合：terms / date_histogram / metrics" }
  - { name: elasticsearch-sync-from-mysql, path: sync-from-mysql.md, tag: skill, note: "与 MySQL 同步：Canal binlog / 双写 / Logstash" }
  - { name: elasticsearch-deep-paging, path: deep-paging.md, tag: skill, note: "深分页：search_after 不用 from+size，>10000 报错" }
when_to_descend: 设计 / 评审 ES 索引 Mapping、检索或聚合 DSL、中文分词、深分页或 MySQL 同步
---

# Elasticsearch · 子项索引

> 这里是 ES 的**用法**规范。要不要引入 ES（vs ClickHouse/时序库）的**选型**对比在 [`../../tech-selection/search-olap/index.md`](../../tech-selection/search-olap/index.md)。

ES 用法拆成 6 个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 建索引、定字段类型（哪些 text 哪些 keyword） | [mapping-design](mapping-design.md) |
| 中文字段配分词器（建索引 / 查询用哪个） | [analyzer-ik](analyzer-ik.md) |
| 写检索 DSL（多条件组合 / 算分 vs 过滤） | [query-dsl](query-dsl.md) |
| 做聚合统计（分组计数 / 时间直方图 / 指标） | [aggregation](aggregation.md) |
| 把 MySQL 数据同步进 ES（实时 / 批量） | [sync-from-mysql](sync-from-mysql.md) |
| 翻页很深、`from+size` 报错或越来越慢 | [deep-paging](deep-paging.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 选型（是否该用 ES）：[`../../tech-selection/search-olap/index.md`](../../tech-selection/search-olap/index.md)
