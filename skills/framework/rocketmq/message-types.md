---
name: rocketmq-message-types
description: RocketMQ 消息类型选型 — 顺序消息发同一 MessageQueue、事务消息半消息+回查、延迟消息 delayLevel、Tag 过滤订阅。Use when 要保证消息顺序 / 做分布式事务消息 / 发延迟消息 / 按 Tag 过滤时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 顺序消息
  - 事务消息
  - 延迟消息
  - delayLevel
  - Tag 过滤
effort: high
context: inline
version: '1.0'
---
# RocketMQ · 消息类型

> 本条只管「选哪种消息类型怎么发」。发送方式（同步/异步/单向）见 [`producer-send.md`](./producer-send.md)；顺序消息的消费端配置见 [`consumer-mode.md`](./consumer-mode.md)。

## 规则

| 类型 | 怎么做 | 用于 |
|------|--------|------|
| 顺序 | 同一业务键 hash 到**同一 MessageQueue**，用 `syncSendOrderly(topic, msg, hashKey)` | 同一订单的状态流转 |
| 事务 | 半消息 + 本地事务 + broker 回查，`sendMessageInTransaction` | DB 操作与发消息最终一致 |
| 延迟 | 设 `delayLevel`（1~18 对应 1s/5s.../2h，非任意秒） | 订单超时关闭、定时提醒 |
| Tag 过滤 | 发送 `topic:tag`，消费端 `selectorExpression` 订阅指定 tag | 一个 topic 区分多业务 |

## 正例

```java
// 顺序：同一 orderId 进同一队列，保证该订单消息有序
rocketMQTemplate.syncSendOrderly("order-topic", statusMsg, orderId);

// 事务：半消息对消费者不可见，本地事务成功才 COMMIT，超时未决则回查
rocketMQTemplate.sendMessageInTransaction("tx-topic",
        MessageBuilder.withPayload(payload).build(), arg);
// 监听器实现 executeLocalTransaction + checkLocalTransaction

// 延迟：delayLevel=3 → 延迟 10s 投递（不是任意秒数）
Message<String> msg = MessageBuilder.withPayload(body).build();
rocketMQTemplate.syncSend("delay-topic", msg, 3000, 3);

// Tag：发到 topic 的 create tag
rocketMQTemplate.syncSend("order-topic:create", createMsg);
```

事务消息须实现 `RocketMQLocalTransactionListener`：`executeLocalTransaction` 执行本地事务并返回 COMMIT/ROLLBACK/UNKNOWN，`checkLocalTransaction` 供 broker 回查兜底未决状态。

## 反例

```java
// ❌ 想要顺序却用普通 syncSend：消息分散到多队列，并发消费乱序
rocketMQTemplate.syncSend("order-topic", statusMsg);

// ❌ 把 delayLevel 当任意秒数（如填 30 想延迟 30 秒）
rocketMQTemplate.syncSend("t", msg, 3000, 30);   // 超出 1~18 范围无效
```

## 自检

- [ ] 顺序消息用 `syncSendOrderly` 且 hashKey 是同一业务键？
- [ ] 事务消息实现了 `checkLocalTransaction` 回查，不只依赖 executeLocalTransaction？
- [ ] 延迟用合法 `delayLevel`（1~18），没当成任意秒数？
- [ ] 用 Tag 区分业务时，发送带 `:tag`、消费端按 tag 订阅？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`producer-send.md`](./producer-send.md)（同步/异步/单向发送方式）
- 兄弟：[`consumer-mode.md`](./consumer-mode.md)（顺序消费 / Tag 订阅的消费端配置）
