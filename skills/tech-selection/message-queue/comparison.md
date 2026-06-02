---
name: tech-selection-mq-comparison
description: Kafka/RocketMQ/RabbitMQ/Pulsar 四款消息队列的吞吐/延迟/顺序/事务/回溯/运维多维对比 + 各自优缺点。Use when 对比 MQ 能力 / 选消息队列 / 评审 MQ 选型时。
parent: ./index.md
paths:
- '*.java'
- '*.yml'
- '*.xml'
triggers:
  keywords:
  - 消息队列对比
  - 消息队列选型
  - Kafka
  - RocketMQ
  - RabbitMQ
  - Pulsar
effort: medium
context: inline
version: '1.0'
---
# 消息队列 · 四款对比

> 本条只管「四款 MQ 逐项能力差异」。已知场景直接选谁见 [`decision-tree.md`](./decision-tree.md)。
> TPS/延迟为**量级参考**，受消息体大小/副本数/刷盘策略/硬件影响，落地前必须压测。

## 多维对比

| 维度 | Kafka | RocketMQ | RabbitMQ | Pulsar |
|---|---|---|---|---|
| 吞吐量 | 最高，百万级 TPS / 600+ MB/s | 十万级 TPS（双十一级） | 万级 TPS / ~30K msg/s | 十万级 / ~300 MB/s |
| 延迟 | 低 ~5ms | 低 几十ms | 最低 单数字ms（高吞吐下劣化） | 低 几十ms |
| 消息顺序 | 分区内有序；全局需单分区 | 强：全局+分区顺序 | 弱 | 分区内有序(Key_Shared) |
| 事务消息 | 支持(exactly-once) | 强：两阶段+本地事务回查(金融级) | 不支持(仅 confirm) | 有限 |
| 延迟/定时消息 | 原生不支持 | 强：内置延迟级别+任意定时 | 插件/TTL+DLX | 有限 |
| 消息回溯 | 极强(offset 重置) | 强(时间/offset) | 弱(消费即删) | 强(分层存储) |
| 运维复杂度 | 高(分区/再均衡/KRaft) | 中 | 中 | 较高(Broker+BookKeeper+ZK) |

## 各自优缺点

| MQ | 优 | 缺 |
|---|---|---|
| Kafka | 吞吐天花板、回溯极强、大数据流生态（Flink/Spark） | 无原生定时/延迟消息、运维门槛高、单数字 ms 延迟做不到 |
| RocketMQ | 金融级事务消息、强顺序、内置定时延迟 | 吞吐不及 Kafka、生态偏国内 |
| RabbitMQ | 延迟最低、路由灵活（exchange）、上手快 | 万级吞吐封顶、回溯弱、无事务消息 |
| Pulsar | 存算分离弹性、多租户、冷热分层 | 组件多（Broker+BookKeeper+ZK）运维重 |

## 自检

- [ ] 对比的维度覆盖了本场景真正在意的那几项（吞吐 / 顺序 / 事务 / 回溯）？
- [ ] 没有只看吞吐就选，忽略了顺序 / 事务 / 定时消息的硬约束？
- [ ] 性能数字按真实负载压测过，而非直接抄表里量级？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`decision-tree.md`](./decision-tree.md)（已知场景直接选谁）
