---
name: kafka-producer-config
description: Kafka 生产者可靠性配置 — acks=all 不丢、enable.idempotence 幂等、retries、批量，及 KafkaTemplate 发送回调。Use when 配生产者 / 保证消息不丢 / 调批量吞吐 / 处理发送回调时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 生产者
  - 消息不丢
  - acks=all
  - enable.idempotence
  - KafkaTemplate
  - linger.ms
effort: medium
context: inline
version: '1.0'
---
# Kafka · 生产者可靠性配置

> 本条只管「生产端怎么发、怎么不丢」。消费端配置见 [`consumer-config.md`](./consumer-config.md)。

## 规则

| 配置 | 取值 | 为什么 |
|------|------|-------|
| `acks` | `all`（=-1） | 等所有 ISR 副本确认才算成功，挂主不丢 |
| `enable.idempotence` | `true` | broker 去重，避免 retry 导致重复写入 |
| `retries` | `Integer.MAX_VALUE` | 配合幂等，瞬时失败自动重试不丢 |
| `max.in.flight.requests.per.connection` | `≤5` | 开幂等时超 5 会乱序，必须 ≤5 |
| `batch.size` / `linger.ms` | 如 `16384` / `5~20ms` | 攒批提吞吐；linger 给一点等待窗口 |

> 开了 `enable.idempotence=true`，broker 只保证**单生产者会话内**不重复；跨会话 / 消费侧重复仍要消费幂等，见 [`idempotent-consumer.md`](./idempotent-consumer.md)。

## 正例：发送回调必须处理失败

```java
// ✅ 异步发送 + 回调，失败要 log/补偿，不能默默丢
kafkaTemplate.send("order-topic", order.getId(), payload)
    .whenComplete((result, ex) -> {
        if (ex != null) {
            log.error("发送失败, key={}", order.getId(), ex);
            // 落本地消息表 / 告警，等待补偿重发
        }
    });
```

```yaml
# ✅ application.yml 可靠性配置
spring:
  kafka:
    producer:
      acks: all
      retries: 2147483647
      properties:
        enable.idempotence: true
        max.in.flight.requests.per.connection: 5
      batch-size: 16384
      properties.linger.ms: 10
```

## 反例

```java
// ❌ 发完不管返回值——broker 没收到也无感知，消息静默丢失
kafkaTemplate.send("order-topic", payload);
```

```yaml
# ❌ acks=1 只等 leader，leader 挂在副本同步前就丢
acks: 1
```

## 自检

- [ ] `acks=all` 且 `enable.idempotence=true`？
- [ ] 开幂等时 `max.in.flight.requests.per.connection ≤ 5`？
- [ ] `send()` 返回的 future 接了回调处理失败（log / 补偿），没有发完不管？
- [ ] 需要顺序的 key 走同一 partition（用相同 message key）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`consumer-config.md`](./consumer-config.md)（消费端配置）
- 兄弟：[`idempotent-consumer.md`](./idempotent-consumer.md)（即使生产幂等，消费侧仍需去重）
