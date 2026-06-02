---
name: tech-selection-cache-index
description: 缓存选型索引 — Caffeine（本地）/ Redis（分布式）/ Memcached 三者对比 + 多级缓存（Caffeine L1 + Redis L2）。Use when 选缓存方案 / 对比本地与分布式缓存 / 设计多级缓存时。
parent: ../index.md
children:
  - { name: caffeine-vs-redis-vs-memcached, path: caffeine-vs-redis-vs-memcached.md, tag: skill, note: 三者对比 + 多级缓存 L1/L2 组合 }
when_to_descend: 任务涉及「缓存放本地还是分布式、要不要多级」的选型。
---

# Cache · 选型索引

> Redis 当「缓存 vs 主存储」的边界另见 [`../database/redis-as-store.md`](../database/redis-as-store.md)。

按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 在 Caffeine / Redis / Memcached 之间选，或设计多级缓存 | [caffeine-vs-redis-vs-memcached](caffeine-vs-redis-vs-memcached.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../message-queue/index.md`](../message-queue/index.md) · [`../database/index.md`](../database/index.md) · [`../search-olap/index.md`](../search-olap/index.md)
