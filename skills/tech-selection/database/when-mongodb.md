---
name: tech-selection-when-mongodb
description: 文档库 MongoDB 何时合适、何时误用 — 天然聚合/嵌套/Schema多变才合适，多实体强事务+复杂 join 应回到关系库。Use when 考虑用 MongoDB / 评审文档模型选型 / 排查 MongoDB 误用时。
parent: ./index.md
paths:
- '*.java'
- '*.yml'
- '*.xml'
- '*.json'
triggers:
  keywords:
  - 文档数据库
  - 文档模型
  - MongoDB
  - 嵌套文档
  - 多文档事务
  - Schema 多变
effort: medium
context: inline
version: '1.0'
---
# 文档库 · MongoDB 何时用

> 本条只管「该不该用文档模型」。关系库内部 MySQL/PG 之选见 [`mysql-vs-postgresql.md`](./mysql-vs-postgresql.md)；三类总决策见 [`decision-tree.md`](./decision-tree.md)。

## 合适 vs 误用

| 真合适 | 误用（应回关系库） |
|---|---|
| 数据天然聚合/嵌套：商品详情、用户档案、CMS、IoT 事件 | 当成 SQL 表建模 + 频繁 `$lookup` join |
| Schema 多变、字段不固定 | 强多表/多文档事务 |
| 按文档自然分片 | 单文档逼近 16MB 上限 |

## 关键约束

- **多文档事务有硬约束**：建议 ≤1000 文档 / 60s 内完成，跨分片事务成本高。
- **单文档上限约 16MB**：无限往一个文档塞嵌套数组会撞墙。

> 核心判据：**多实体强事务 + 复杂 join → 回到 PostgreSQL / MySQL**；文档库的甜区是「一个聚合根读写一整篇文档」。

## 反例

- ❌ 把订单/用户/商品拆成多个集合，再用 `$lookup` 模拟外键 join —— 这是关系建模，选错了库。
- ❌ 依赖跨多个文档的强一致事务 —— MongoDB 多文档事务约束多，应选关系库。

## 自检

- [ ] 数据是「天然聚合的一整篇」还是「需要拆表 join」？后者别用文档库。
- [ ] 不存在「多实体强一致事务」的核心诉求？
- [ ] 单文档不会逼近 16MB、不依赖海量跨文档事务？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`mysql-vs-postgresql.md`](./mysql-vs-postgresql.md)（关系库内部之选）
- 兄弟：[`decision-tree.md`](./decision-tree.md)（关系/文档/KV 总决策树）
