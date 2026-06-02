---
name: framework-kafka-index
description: Kafka（Spring Kafka 视角）使用约定 — 生产者可靠性/消费者手动 ack/消费幂等/错误处理四个独立决策点。Use when 配生产者保证不丢 / 配 @KafkaListener 手动 ack / 做消费幂等去重 / 设计重试与死信队列时。
parent: ../index.md
children:
  - { name: kafka-producer-config, path: producer-config.md, tag: skill, note: "acks=all+幂等+批量+KafkaTemplate 回调" }
  - { name: kafka-consumer-config, path: consumer-config.md, tag: skill, note: "@KafkaListener+手动 ack+并发+消费组" }
  - { name: kafka-idempotent-consumer, path: idempotent-consumer.md, tag: skill, note: 至少一次语义下消费去重 }
  - { name: kafka-error-handling, path: error-handling.md, tag: skill, note: 重试+死信队列 DLQ+毒丸隔离 }
when_to_descend: 写 / 改 Java 里收发 Kafka 消息的代码：配生产者、写 @KafkaListener 消费、做幂等去重或设计重试与死信。
---

# Kafka · 框架使用约定索引

四个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 配生产者、保证消息不丢、发送回调处理 | [producer-config](producer-config.md) |
| 写 @KafkaListener、关自动提交改手动 ack、设并发与消费组 | [consumer-config](consumer-config.md) |
| 至少一次语义下做消费去重、防重复消费 | [idempotent-consumer](idempotent-consumer.md) |
| 消费失败重试、死信队列、隔离毒丸消息 | [error-handling](error-handling.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../spring-boot/index.md`](../spring-boot/index.md) · [`../redis/index.md`](../redis/index.md)
- 相关：[`../../lang/java/error-handling/index.md`](../../lang/java/error-handling/index.md)
