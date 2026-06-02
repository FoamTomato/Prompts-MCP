---
name: fundamentals-distributed-theory-index
description: 分布式理论选型四件事 — CAP 取舍（CP/AP）/ 分布式事务方案选型 / 幂等设计 / 分布式 ID 选型。Use when 选注册中心一致性模型 / 选分布式事务方案 / 设计幂等 / 选分布式 ID 算法时。
parent: ../index.md
children:
  - { name: distributed-cap-tradeoff, path: cap-tradeoff.md, tag: skill, note: "CAP：P 必选，CP（ZK/etcd）vs AP（Eureka/Nacos AP）怎么取舍" }
  - { name: distributed-transaction-solutions, path: transaction-solutions.md, tag: skill, note: "2PC/TCC/Saga/本地消息表/最大努力通知 的方案选型" }
  - { name: distributed-idempotent-design, path: idempotent-design.md, tag: skill, note: "幂等：唯一键/去重表/Token/状态机/乐观锁，接口+消息" }
  - { name: distributed-id, path: distributed-id.md, tag: skill, note: "分布式 ID 算法选型：雪花/号段/Redis incr/UUID 取舍" }
when_to_descend: 做分布式架构选型——选一致性模型、事务方案、幂等手段、ID 算法时下钻
---

# 分布式理论 · 子项索引

分布式理论拆成四个**独立选型决策点**，按你正在做的取舍下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 选注册中心/存储的一致性模型，纠结要一致性还是可用性 | [cap-tradeoff](cap-tradeoff.md) |
| 跨服务/跨库要保证一致，选哪种分布式事务方案 | [transaction-solutions](transaction-solutions.md) |
| 接口可能被重试/消息可能重投，要保证执行一次效果 | [idempotent-design](idempotent-design.md) |
| 给分布式系统选全局唯一 ID 的生成算法 | [distributed-id](distributed-id.md) |
