---
name: tech-selection-index
description: 技术选型对比维度 — 跨语言/跨框架的「选哪个技术」决策（消息队列 / 数据库 / 缓存 / 搜索分析时序）。Use when 选 MQ/数据库/缓存/搜索引擎 / 评审技术选型 / 做架构选型对比时。
parent: ../index.md
children:
  - { name: message-queue, path: message-queue/index.md, tag: folder, note: Kafka/RocketMQ/RabbitMQ/Pulsar 选型 }
  - { name: database, path: database/index.md, tag: folder, note: MySQL/PostgreSQL/MongoDB/Redis 选型 }
  - { name: cache, path: cache/index.md, tag: folder, note: Caffeine/Redis/Memcached 缓存选型 }
  - { name: search-olap, path: search-olap/index.md, tag: folder, note: ES/ClickHouse/InfluxDB/TDengine 选型 }
when_to_descend: 任务是「在多个候选技术里选一个」而非「某框架怎么用」时进本维度。
---

# Tech-Selection · 技术选型对比

> 本维度回答「**选哪个技术**」，不回答「某技术怎么用」（用法见 `lang/` / `framework/`）。
> 所有性能数字是**量级参考**，受消息体大小/副本数/刷盘策略/硬件影响，落地前必须压测。
> 提醒：多数中小系统「一个 PostgreSQL + 一个 Redis」即可；引入 MQ/ES/ClickHouse/时序库前先确认真有重放/检索/聚合/时序硬需求，避免过度复杂。

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| message-queue | 文件夹 | Kafka / RocketMQ / RabbitMQ / Pulsar 四选一 |
| database | 文件夹 | 关系（MySQL/PG）/ 文档（MongoDB）/ KV（Redis）选型 |
| cache | 文件夹 | Caffeine / Redis / Memcached + 多级缓存 |
| search-olap | 文件夹 | ES / ClickHouse / InfluxDB / TDengine 定位 |

## 何时下钻

| 你在选什么 | 进哪个 |
|-----------|-------|
| 要不要上 MQ、上哪个 MQ | [message-queue](message-queue/index.md) |
| 主存储用关系库 / 文档库 / KV | [database](database/index.md) |
| 缓存放本地还是分布式、要不要多级 | [cache](cache/index.md) |
| 要全文检索 / 海量聚合分析 / 时序 | [search-olap](search-olap/index.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行维度：[`../lang/index.md`](../lang/index.md) · [`../framework/index.md`](../framework/index.md) · [`../design-pattern/index.md`](../design-pattern/index.md) · [`../habit/index.md`](../habit/index.md) · [`../ai/index.md`](../ai/index.md) · [`../fundamentals/index.md`](../fundamentals/index.md)
