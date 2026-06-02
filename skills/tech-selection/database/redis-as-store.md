---
name: tech-selection-redis-as-store
description: Redis 当主存储还是仅做缓存的边界 — 默认仅缓存（cache-aside+TTL），仅数据小+读极热+有持久化兜底才考虑当主存储。Use when 纠结 Redis 是否当主存储 / 评审 Redis 持久化方案 / 防数据丢失时。
parent: ./index.md
paths:
- '*.java'
- '*.yml'
- '*.xml'
triggers:
  keywords:
  - Redis 主存储
  - Redis 持久化
  - 缓存还是主存储
  - cache-aside
  - RDB
  - AOF
effort: medium
context: inline
version: '1.0'
---
# Redis · 主存储 vs 缓存

> 本条只管「Redis 该当主存储还是只做缓存」。Redis 与其它缓存的对比见 [`../cache/caffeine-vs-redis-vs-memcached.md`](../cache/caffeine-vs-redis-vs-memcached.md)。

## 边界

| 用法 | 何时 |
|------|------|
| **缓存（默认推荐）** | cache-aside + TTL，读多写少的甜区 |
| **主存储（谨慎）** | 数据小 + 读极热 + 可接受内存态 + 有持久化兜底，且已配 RDB+AOF + 高可用 |

## 当主存储的代价

- 必须 RDB + AOF 双持久化，且仍非关系库级别的强持久保证。
- 内存成本高：全量数据常驻内存，数据量大时成本爆炸。
- 需高可用（主从 / Sentinel / Cluster）兜底。

> 反向判据：**数据丢失不可接受 + 数据量远大于内存 + 需复杂查询 → 用关系/文档库当主存储，Redis 仅缓存。**

## 反例

- ❌ 把订单这类「丢了就出事」的核心数据只存 Redis 当主库 —— 持久化保证不足。
- ❌ 数据量远超内存还硬塞 Redis 当主存储 —— 成本与淘汰风险失控。

## 自检

- [ ] 默认就是「Redis 仅缓存」，当主存储是经论证的例外？
- [ ] 若当主存储：RDB+AOF + 高可用都配齐，且数据丢失可接受兜底？
- [ ] 数据量没有远大于内存、不需要复杂查询？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`decision-tree.md`](./decision-tree.md)（关系/文档/KV 总决策树）
- 跨模块：[`../cache/caffeine-vs-redis-vs-memcached.md`](../cache/caffeine-vs-redis-vs-memcached.md)（Redis 作缓存时与谁比）
