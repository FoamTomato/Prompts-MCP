---
name: rocketmq-idempotent
description: RocketMQ 消费幂等 — 不保证不重复（重试/重平衡会重投），msgId 不可靠，必须用业务唯一键 + Redis/DB 去重表保证只生效一次。Use when 防止重复消费 / 做消费幂等去重 / 处理消息重复投递时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 消费幂等
  - 去重表
  - 重复消费
  - 业务唯一键
  - idempotent
effort: high
context: inline
version: '1.0'
---
# RocketMQ · 消费幂等去重

> 本条只管「重复投递了怎么保证只生效一次」。重试/ACK 机制本身见 [`consumer-mode.md`](./consumer-mode.md)。

## 规则

| 项 | 约定 |
|----|------|
| 前提 | RocketMQ 是 **at-least-once**，不保证不重复；重试、消费者重平衡都会重投 |
| 去重键 | 用**业务唯一键**（订单号、流水号），**不要用 msgId** |
| 为何不用 msgId | 重试时 msgId 可能变；生产端重发是新 msgId；不能跨业务等价 |
| 去重存储 | Redis `SETNX`（高频、可加 TTL）或 DB 唯一索引/去重表（强一致） |
| 原子性 | 「判重 + 业务写入」要在同一事务或同一原子操作内，避免判重通过后写入失败留下空洞 |

## 正例

```java
// DB 去重表：唯一索引兜底，插入冲突即视为重复
@Transactional
public void onMessage(OrderMsg msg) {
    String bizKey = msg.getOrderNo();                 // 业务唯一键，非 msgId
    try {
        dedupMapper.insert(bizKey);                   // 表上 biz_key 有唯一索引
    } catch (DuplicateKeyException e) {
        return;                                        // 已处理过，直接 ACK
    }
    orderService.process(msg);                         // 与插入同一事务
}

// 或 Redis SETNX：高频场景，带 TTL
Boolean first = redis.opsForValue()
        .setIfAbsent("mq:dedup:" + bizKey, "1", Duration.ofHours(24));
if (Boolean.FALSE.equals(first)) return;              // 重复，跳过
process(msg);
```

## 反例

```java
// ❌ 用 msgId 去重：重试/重发的 msgId 不同，去重直接失效
if (redis.hasKey("dedup:" + msg.getMsgId())) return;

// ❌ 先判重再单独写业务，两步非原子：判重过了但 process 失败，
//    重试时已标记"处理过"被跳过 → 业务丢失
if (dedupMapper.exists(bizKey)) return;
dedupMapper.insert(bizKey);
process(msg);   // 这步失败就再也不会执行
```

## 自检

- [ ] 去重键用业务唯一键（订单号/流水号），不是 `msgId`？
- [ ] 去重用 Redis SETNX（带 TTL）或 DB 唯一索引，不靠内存 Set？
- [ ] 「判重 + 业务处理」原子（同事务/插入冲突即跳过），不会判重过却处理失败？
- [ ] 接受 RocketMQ at-least-once，没有假设"不会重复"？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`consumer-mode.md`](./consumer-mode.md)（重试与 ACK 是重复的来源）
- 相关：[`../redis/distributed-lock.md`](../redis/distributed-lock.md)（Redis 去重/互斥）
- 通用方案（先看）：[`../../fundamentals/distributed-theory/idempotent-design.md`](../../fundamentals/distributed-theory/idempotent-design.md)（去重表/唯一索引/Token/状态机的通用选择，本条只是 RocketMQ 落地）
- 同类对照：[`../kafka/idempotent-consumer.md`](../kafka/idempotent-consumer.md)（Kafka 消费幂等，方案应与本条一致）
