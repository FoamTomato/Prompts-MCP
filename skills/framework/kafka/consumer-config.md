---
name: kafka-consumer-config
description: Kafka 消费者配置 — @KafkaListener、手动 ack（关 auto.commit + ackMode MANUAL）、位移管理、并发、消费组。Use when 写 @KafkaListener / 关自动提交改手动 ack / 调消费并发 / 设计消费组时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 消费者
  - 手动提交
  - '@KafkaListener'
  - ackMode
  - 消费组
  - concurrency
effort: medium
context: inline
version: '1.0'
---
# Kafka · 消费者配置

> 本条只管「怎么收、怎么提交位移、并发多少」。生产端见 [`producer-config.md`](./producer-config.md)；消费失败重试/死信见 [`error-handling.md`](./error-handling.md)。

## 规则

| 配置 | 取值 | 为什么 |
|------|------|-------|
| `enable.auto.commit` | `false` | 自动提交会「先提交后处理」，崩溃即丢消息 |
| `ack-mode` | `MANUAL` / `MANUAL_IMMEDIATE` | 业务处理成功后手动 ack，提交才落地 |
| `group.id` | 每类消费逻辑一个 | 同组分摊分区，不同组各自全量消费 |
| `concurrency` | `≤ 分区数` | 并发线程数，超过分区数的线程空闲 |
| `auto-offset-reset` | `earliest` / `latest` | 新组无位移时从头还是从尾 |

> 关了自动提交 = 至少一次语义（处理完才 ack，崩溃会重投）→ **消费必须幂等**，见 [`idempotent-consumer.md`](./idempotent-consumer.md)。

## 正例：手动 ack

```java
// ✅ 处理成功后才 ack.acknowledge()；抛异常则不提交，下次重投
@KafkaListener(topics = "order-topic", groupId = "order-service", concurrency = "3")
public void onMessage(ConsumerRecord<String, String> record, Acknowledgment ack) {
    handle(record.value());   // 业务处理
    ack.acknowledge();        // 仅成功才提交位移
}
```

```yaml
# ✅ application.yml
spring:
  kafka:
    consumer:
      enable-auto-commit: false
      auto-offset-reset: earliest
    listener:
      ack-mode: manual
```

## 反例

```java
// ❌ 开自动提交：方法刚进就可能已提交位移，handle 崩了消息就丢了
// (enable.auto.commit=true 时根本拿不到 Acknowledgment)
@KafkaListener(topics = "order-topic")
public void onMessage(String value) {
    handle(value);  // 抛异常也已提交 → 丢消息
}
```

```java
// ❌ concurrency 设 10 但 topic 只有 3 个分区 → 7 个线程永远空转
@KafkaListener(topics = "order-topic", concurrency = "10")
```

## 自检

- [ ] `enable.auto.commit=false` 且 `ack-mode=manual`？
- [ ] 业务处理成功后才 `ack.acknowledge()`，失败分支不提交？
- [ ] `concurrency ≤ 该 topic 分区数`？
- [ ] `group.id` 按消费逻辑划分，没有多个无关逻辑共用一个组？
- [ ] 因为是至少一次语义，消费逻辑已做幂等？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`producer-config.md`](./producer-config.md)（生产端配置）
- 兄弟：[`idempotent-consumer.md`](./idempotent-consumer.md)（手动 ack = 至少一次，必须幂等）
- 兄弟：[`error-handling.md`](./error-handling.md)（消费抛异常后的重试与死信）
