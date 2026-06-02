---
name: framework-rocketmq-index
description: Apache RocketMQ（Spring 视角）约定 — 发送方式 / 消息类型 / 消费模式 / 消费幂等去重。Use when 用 RocketMQTemplate 发消息 / 选顺序-事务-延迟消息 / 写消费监听 / 做消费幂等时。
parent: ../index.md
children:
  - { name: rocketmq-producer-send, path: producer-send.md, tag: skill, note: "发送方式：syncSend/asyncSend/sendOneway 选型 + SendStatus 判断" }
  - { name: rocketmq-message-types, path: message-types.md, tag: skill, note: "消息类型：顺序/事务半消息回查/延迟 delayLevel/Tag 过滤" }
  - { name: rocketmq-consumer-mode, path: consumer-mode.md, tag: skill, note: "消费模式：集群vs广播/并发vs顺序/重试 reconsumeTimes/ACK" }
  - { name: rocketmq-idempotent, path: idempotent.md, tag: skill, note: "消费幂等：不保证不重复，业务唯一键 + Redis/DB 去重表" }
when_to_descend: 写 / 改 Java 里收发 RocketMQ 消息的代码：发消息、选消息类型、写消费者监听器或做幂等去重。
---

# Apache RocketMQ · 子项索引

RocketMQ（Spring 视角）使用拆成 4 个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 发消息选同步/异步/单向、判断 SendStatus 是否成功 | [producer-send](producer-send.md) |
| 要顺序、事务、延迟消息，或按 Tag 过滤订阅 | [message-types](message-types.md) |
| 写消费者监听器（集群/广播、并发/顺序、重试与 ACK） | [consumer-mode](consumer-mode.md) |
| 防止重复消费、做消费幂等去重 | [idempotent](idempotent.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../redis/index.md`](../redis/index.md)（去重表常用 Redis）
- 相关：[`../../lang/java/error-handling/index.md`](../../lang/java/error-handling/index.md)
