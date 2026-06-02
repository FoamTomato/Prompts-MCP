---
name: tech-selection-mq-index
description: 消息队列选型索引 — Kafka/RocketMQ/RabbitMQ/Pulsar 的四维对比表 + 决策树速查。Use when 选消息队列 / 对比 MQ 吞吐顺序事务能力 / 评审 MQ 选型时。
parent: ../index.md
children:
  - { name: comparison, path: comparison.md, tag: skill, note: 四款 MQ 吞吐/延迟/顺序/事务四维对比表 }
  - { name: decision-tree, path: decision-tree.md, tag: skill, note: "选谁的决策树 + 场景速查（日志→Kafka，订单事务→RocketMQ）" }
when_to_descend: 任务涉及「要不要上 MQ、上哪个 MQ」的选型。
---

# Message-Queue · 选型索引

> 性能数字均为量级参考，落地前必须按真实负载压测。

按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 想看四款 MQ 在吞吐/延迟/顺序/事务/运维上的逐项差异 | [comparison](comparison.md) |
| 已知场景（日志 / 订单事务 / 任务队列 / 多租户），要直接定一个 | [decision-tree](decision-tree.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../database/index.md`](../database/index.md) · [`../cache/index.md`](../cache/index.md) · [`../search-olap/index.md`](../search-olap/index.md)
