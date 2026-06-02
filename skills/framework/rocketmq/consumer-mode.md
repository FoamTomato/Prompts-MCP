---
name: rocketmq-consumer-mode
description: RocketMQ 消费者配置 — @RocketMQMessageListener 选集群/广播、并发/顺序消费，依赖重试 reconsumeTimes 与自动 ACK，正常返回即确认。Use when 写消费者监听器 / 选集群广播或并发顺序 / 处理消费重试时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 消费模式
  - RocketMQMessageListener
  - 集群广播
  - 顺序消费
  - reconsumeTimes
effort: high
context: inline
version: '1.0'
---
# RocketMQ · 消费模式

> 本条只管「消费者怎么配、怎么确认与重试」。重复消费的业务去重见 [`idempotent.md`](./idempotent.md)；消息类型怎么发见 [`message-types.md`](./message-types.md)。

## 规则

| 维度 | 选项 | 怎么选 |
|------|------|--------|
| 消费组模式 | `CLUSTERING`（默认） vs `BROADCASTING` | 一条只消费一次用集群；每个实例都要收用广播 |
| 消费顺序 | `CONCURRENTLY`（默认） vs `ORDERLY` | 要严格顺序用 ORDERLY（单线程串行该队列） |
| 确认 | 方法正常返回 = 自动 ACK | 抛异常 = NACK 触发重试 |
| 重试 | 集群模式自动重试，`maxReconsumeTimes` 控制次数 | 超次进死信队列 `%DLQ%group` |

`@RocketMQMessageListener` 的 `consumeMode` / `messageModel` / `maxReconsumeTimes` 在注解上声明；当前重试次数从 `MessageExt.getReconsumeTimes()` 读。**广播模式不重试**（重试是 broker 行为，广播由各实例自己消费）。

## 正例

```java
@Service
@RocketMQMessageListener(
    topic = "order-topic",
    consumerGroup = "order-consumer",
    messageModel = MessageModel.CLUSTERING,        // 集群：组内只消费一次
    consumeMode = ConsumeMode.CONCURRENTLY,        // 并发消费
    maxReconsumeTimes = 3)                          // 超 3 次进死信
public class OrderListener implements RocketMQListener<MessageExt> {
    @Override
    public void onMessage(MessageExt msg) {
        if (msg.getReconsumeTimes() >= 3) {
            saveToDeadLetterTable(msg);             // 末次兜底，避免直接丢
            return;                                  // 正常返回 = ACK，不再重试
        }
        handle(msg);                                 // 抛异常 = NACK 自动重试
    }
}
```

## 反例

```java
// ❌ catch 掉所有异常后正常返回 → 失败消息被 ACK 丢掉，重试机制失效
@Override public void onMessage(Order o) {
    try { handle(o); } catch (Exception e) { log.error("err", e); }
}

// ❌ 顺序消费场景却用 CONCURRENTLY，同一订单多线程乱序处理
consumeMode = ConsumeMode.CONCURRENTLY  // 应为 ORDERLY
```

## 自检

- [ ] `messageModel` 按「只消费一次/每实例都收」选对集群或广播？
- [ ] 要顺序的场景 `consumeMode = ORDERLY`，且发送端已用顺序消息？
- [ ] 处理失败时**抛异常触发重试**，没有 catch 后正常返回吞掉？
- [ ] 设了 `maxReconsumeTimes`，末次重试有死信兜底，不直接丢消息？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`idempotent.md`](./idempotent.md)（重试会重复投递，必须业务去重）
- 兄弟：[`message-types.md`](./message-types.md)（顺序消息的发送端配合）
- 相关：[`../../lang/java/error-handling/index.md`](../../lang/java/error-handling/index.md)（消费异常处理）
