---
name: kafka-idempotent-consumer
description: Kafka 消费幂等 — 至少一次语义下必须去重（业务唯一键 / 去重表 / Redis setnx），应对重平衡、重试、补偿导致的重复消费。Use when 手动 ack 后做消费去重 / 防止消息重复处理 / 设计幂等键时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 消费幂等
  - 重复消费
  - 去重表
  - 幂等键
  - 至少一次
  - Redis setnx
effort: high
context: inline
version: '1.0'
---
# Kafka · 消费幂等

> 本条只管「同一条消息被投递多次时怎么不重复处理」。手动 ack 配置见 [`consumer-config.md`](./consumer-config.md)；失败重试/死信见 [`error-handling.md`](./error-handling.md)。

## 规则

Kafka 默认是**至少一次**（手动 ack、重平衡、重试、补偿重发都会导致同一条消息被消费 ≥1 次），所以**消费逻辑必须幂等**——重复执行结果不变。

| 方案 | 适用 | 要点 |
|------|------|------|
| 业务唯一键 | DB 写入类 | 唯一索引 + `INSERT ... ON DUPLICATE` / 插入冲突即跳过 |
| 去重表 | 通用 | 用消息唯一 ID 当主键，插入成功才处理，已存在则跳过 |
| Redis `setnx` | 高频、可容忍极端边界 | `setnx(msgId, 1, ttl)` 抢到才处理 |

**幂等键**优先用业务自带的唯一 ID（如订单号），没有再用生产者侧生成的 messageId 放进消息体；不要用 Kafka 的 offset 当幂等键（重平衡后会变）。

## 正例：去重表

```java
// ✅ 唯一 msgId 当主键，插得进才处理；重复消费时插入冲突直接跳过
@KafkaListener(topics = "order-topic", groupId = "order-service")
public void onMessage(ConsumerRecord<String, String> record, Acknowledgment ack) {
    Order msg = parse(record.value());
    if (!dedupDao.tryInsert(msg.getMsgId())) {  // 已处理过
        ack.acknowledge();
        return;
    }
    handle(msg);
    ack.acknowledge();
}
```

```java
// ✅ DB 写入直接靠唯一索引兜底，天然幂等
// orders 表对 order_no 建唯一索引
orderMapper.insertIgnore(order);  // 冲突即忽略
```

## 反例

```java
// ❌ 直接累加/插入，没有任何去重 —— 重投一次就多扣一次款
@KafkaListener(topics = "pay-topic")
public void onMessage(PayMsg msg, Acknowledgment ack) {
    account.deduct(msg.getAmount());  // 重复消费 → 重复扣款
    ack.acknowledge();
}
```

## 自检

- [ ] 消费逻辑是幂等的（同一消息处理 N 次结果等于 1 次）？
- [ ] 幂等键用业务唯一 ID 或消息体里的 messageId，**不是** offset？
- [ ] 去重判断与业务写入在同一事务 / 同一唯一约束内，没有「查了再写」的并发窗口？
- [ ] 重复消息走「已处理」分支后仍 `ack.acknowledge()`，不会卡住？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`consumer-config.md`](./consumer-config.md)（手动 ack = 至少一次，是幂等的前提）
- 兄弟：[`error-handling.md`](./error-handling.md)（重试也会放大重复消费，与幂等配合使用）
- 相关：[`../redis/cache-patterns.md`](../redis/cache-patterns.md)（Redis 去重）
- 通用方案（先看）：[`../../fundamentals/distributed-theory/idempotent-design.md`](../../fundamentals/distributed-theory/idempotent-design.md)（去重表/唯一索引/Token/状态机的通用选择，本条只是 Kafka 落地）
- 同类对照：[`../rocketmq/idempotent.md`](../rocketmq/idempotent.md)（RocketMQ 消费幂等，方案应与本条一致）
