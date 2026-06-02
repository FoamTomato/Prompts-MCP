---
name: tech-selection-db-index
description: 数据库选型索引 — 关系（MySQL/PostgreSQL）/ 文档（MongoDB）/ KV（Redis）该选谁 + 主存储决策树。Use when 选主存储 / 对比关系库与文档库与KV / 评审数据库选型时。
parent: ../index.md
children:
  - { name: mysql-vs-postgresql, path: mysql-vs-postgresql.md, tag: skill, note: PG 何时更优 vs MySQL 何时够用 }
  - { name: when-mongodb, path: when-mongodb.md, tag: skill, note: 文档模型何时合适、何时误用 }
  - { name: redis-as-store, path: redis-as-store.md, tag: skill, note: Redis 当主存储 vs 仅缓存的边界 }
  - { name: decision-tree, path: decision-tree.md, tag: skill, note: 关系/文档/KV 选型决策树 }
when_to_descend: 任务涉及「主存储用关系库 / 文档库 / KV」的选型。
---

# Database · 选型索引

> 默认建议：多数中小系统「一个 PostgreSQL + 一个 Redis」即可，先别堆库。

按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 关系库在 MySQL 和 PostgreSQL 之间纠结 | [mysql-vs-postgresql](mysql-vs-postgresql.md) |
| 在考虑用文档库（MongoDB），想知道合不合适 | [when-mongodb](when-mongodb.md) |
| 想把 Redis 当主存储而不只是缓存 | [redis-as-store](redis-as-store.md) |
| 还没定用关系 / 文档 / KV 哪一类 | [decision-tree](decision-tree.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../message-queue/index.md`](../message-queue/index.md) · [`../cache/index.md`](../cache/index.md) · [`../search-olap/index.md`](../search-olap/index.md)
