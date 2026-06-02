---
name: framework-mysql-ops-index
description: MySQL 上线与扩展 3 个独立决策点 — 大表 Online DDL 改表不锁表、分库分表拆分键选择、分布式有序主键生成。Use when 大表加字段/加索引 / 设计分库分表 / 选分布式主键方案时。
parent: ../index.md
children:
  - { name: mysql-online-ddl-safety, path: online-ddl-safety.md, tag: skill, note: "大表改表用 gh-ost/pt-osc，避免长时间锁表" }
  - { name: mysql-sharding-key-choice, path: sharding-key-choice.md, tag: skill, note: "分库分表拆分键选择，避免跨片 JOIN/分布式事务" }
  - { name: mysql-distributed-id, path: distributed-id.md, tag: skill, note: "分布式有序主键：号段 vs 雪花，勿退回 UUID" }
when_to_descend: 大表在线 DDL、设计分库分表的拆分键、选分布式主键生成方案。
---

# MySQL · 上线与扩展索引

上线/扩展拆成 3 个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 给大表加字段/加索引，怕锁表 | [online-ddl-safety](online-ddl-safety.md) |
| 单表扛不住要分库分表，选拆分键 | [sharding-key-choice](sharding-key-choice.md) |
| 分片后主键不能用自增，选分布式 ID | [distributed-id](distributed-id.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 兄弟维度：[`../index/index.md`](../index/index.md)
- 选型层（要不要分片）：[`../../../tech-selection/database/index.md`](../../../tech-selection/database/index.md)
