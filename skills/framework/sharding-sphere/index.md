---
name: framework-sharding-sphere-index
description: ShardingSphere 分库分表中间件规范 5 项 — 分片策略 / 分片键选择 / 读写分离 / 广播绑定表 / 分布式限制。Use when 配 ShardingSphere 分片规则 / 排查跨片查询慢 / 评审分片 YAML 与 Service 时。
parent: ../index.md
children:
  - { name: sharding-sphere-sharding-strategy, path: sharding-strategy.md, tag: skill, note: "分片策略：标准/复合/Hint，inline 表达式 vs 自定义算法" }
  - { name: sharding-sphere-sharding-key-choice, path: sharding-key-choice.md, tag: skill, note: "分片键选择：高频查询条件做分片键，避免跨片" }
  - { name: sharding-sphere-read-write-split, path: read-write-split.md, tag: skill, note: "读写分离：主写从读，主从延迟读不到刚写数据" }
  - { name: sharding-sphere-broadcast-binding-table, path: broadcast-binding-table.md, tag: skill, note: "广播表/绑定表：避免分片 JOIN 笛卡尔积" }
  - { name: sharding-sphere-distributed-limitations, path: distributed-limitations.md, tag: skill, note: "分布式限制：跨库 JOIN/分页/聚合/事务的规避" }
when_to_descend: 用 ShardingSphere 配分片/读写分离规则、写或评审分片场景的 Service 与分片 YAML
---

# ShardingSphere · 子项索引

ShardingSphere 分库分表中间件拆成 5 个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 配分片算法（按 mod/range 分，inline 还是自定义类） | [sharding-strategy](sharding-strategy.md) |
| 选用哪个列做分片键（避免每次广播全片） | [sharding-key-choice](sharding-key-choice.md) |
| 配主从、写完立刻读却读到旧数据 | [read-write-split](read-write-split.md) |
| 小表到处 join（字典/配置表），或主从表关联 join | [broadcast-binding-table](broadcast-binding-table.md) |
| 跨库 JOIN / 分页 / 聚合 / 事务报错或结果不对 | [distributed-limitations](distributed-limitations.md) |

> 分工：本模块是 **ShardingSphere 中间件视角**（怎么配规则、中间件能不能做）。数据库层「要不要分、拆分键的 DB 原理」见 [`../mysql/ops/sharding-key-choice.md`](../mysql/ops/sharding-key-choice.md)。
