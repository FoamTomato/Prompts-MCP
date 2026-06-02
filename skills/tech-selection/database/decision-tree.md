---
name: tech-selection-db-decision
description: 数据库三类（关系/文档/KV）选型决策树 — 强事务复杂关系→PostgreSQL，天然聚合Schema多变→MongoDB，读极热结构简单→Redis。Use when 还没定用关系/文档/KV / 做主存储选型 / 评审数据库架构时。
parent: ./index.md
paths:
- '*.java'
- '*.yml'
- '*.xml'
- '*.sql'
triggers:
  keywords:
  - 数据库选型决策树
  - 关系库
  - 文档库
  - KV 存储
  - PostgreSQL
  - MongoDB
effort: medium
context: inline
version: '1.0'
---
# 数据库 · 三类选型决策树

> 本条只管「先定关系 / 文档 / KV 哪一类」。定了关系再选 MySQL/PG 见 [`mysql-vs-postgresql.md`](./mysql-vs-postgresql.md)；文档库细节见 [`when-mongodb.md`](./when-mongodb.md)；Redis 当主存储边界见 [`redis-as-store.md`](./redis-as-store.md)。

## 决策树

| 你的数据特征 | 选哪一类 |
|-----------|---------|
| 强事务 + 复杂关系/分析/GIS/向量 | 关系库（默认 PostgreSQL） |
| 天然聚合/嵌套 + Schema 多变 + 无强跨实体事务 | 文档库（MongoDB） |
| 读极热 + 低延迟 + 结构简单 | KV（Redis，默认缓存） |

## 默认与提醒

> 多数中小系统「**一个 PostgreSQL + 一个 Redis**」即可覆盖主存储 + 缓存。引入 MongoDB / 其它库前先确认数据形态真不适合关系建模。

## 反例

- ❌ 核心是多实体强一致事务，却为「Schema 灵活」上 MongoDB —— 应回关系库。
- ❌ 数据要复杂查询/分析，却选 Redis 当主存储 —— KV 不擅复杂查询。
- ❌ 一上来就堆 PG+Mongo+Redis 三套 —— 中小系统过度复杂，先收敛。

## 自检

- [ ] 按「事务+关系强度 / 聚合形态 / 读热度」三条特征定了大类，而非凭喜好？
- [ ] 默认从「PostgreSQL + Redis」起步，额外库是经论证的例外？
- [ ] 没有为单一灵活字段需求就放弃关系库的事务保证？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`mysql-vs-postgresql.md`](./mysql-vs-postgresql.md) · [`when-mongodb.md`](./when-mongodb.md) · [`redis-as-store.md`](./redis-as-store.md)
