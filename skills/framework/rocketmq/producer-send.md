---
name: rocketmq-producer-send
description: RocketMQ 发送方式选型 — 重要消息用同步 syncSend 且校验 SendStatus，异步 asyncSend 回调处理，日志类用单向 sendOneway。Use when 用 RocketMQTemplate 发消息 / 选同步异步单向 / 判断发送是否成功时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 消息发送
  - syncSend
  - sendOneway
  - SendStatus
  - RocketMQTemplate
effort: medium
context: inline
version: '1.0'
---
# RocketMQ · 发送方式

> 本条只管「怎么把消息发出去、怎么确认发成功」。消息要顺序/事务/延迟见 [`message-types.md`](./message-types.md)；消费端见 [`consumer-mode.md`](./consumer-mode.md)。

## 规则

| 发送方式 | API | 用于 | 可靠性 |
|---------|-----|------|--------|
| 同步 | `syncSend` | 重要消息（订单、扣款），需确认结果 | 高，阻塞等 broker ACK |
| 异步 | `asyncSend` + 回调 | 对吞吐敏感、可接受回调处理结果 | 高，不阻塞主线程 |
| 单向 | `sendOneway` | 日志、埋点等丢了无所谓的 | 低，不等结果、不重试 |

同步/异步发送后**必须校验 `SendStatus`**：只有 `SEND_OK` 才算成功，其余（`FLUSH_DISK_TIMEOUT` / `FLUSH_SLAVE_TIMEOUT` / `SLAVE_NOT_AVAILABLE`）说明未完全落盘或同步，需告警或补偿。

## 正例

```java
// 同步：重要消息，校验 SendStatus
SendResult result = rocketMQTemplate.syncSend("order-topic", orderMsg);
if (result.getSendStatus() != SendStatus.SEND_OK) {
    log.error("发送未成功 status={}", result.getSendStatus());
    throw new BusinessException("MQ 发送失败");   // 触发上游补偿
}

// 异步：回调里处理成功/失败
rocketMQTemplate.asyncSend("notify-topic", msg, new SendCallback() {
    @Override public void onSuccess(SendResult r) { /* 标记已发 */ }
    @Override public void onException(Throwable e) { log.error("异步发送失败", e); }
});

// 单向：日志类，发完即走，不关心结果
rocketMQTemplate.sendOneway("log-topic", logMsg);
```

## 反例

```java
// ❌ 同步发送后不看 SendStatus，broker 刷盘超时也当成功
rocketMQTemplate.syncSend("order-topic", orderMsg);   // 返回值丢弃

// ❌ 重要消息用 sendOneway，丢了完全无感知
rocketMQTemplate.sendOneway("pay-topic", payMsg);
```

## 自检

- [ ] 重要消息用 `syncSend` 并校验 `SendStatus == SEND_OK`？
- [ ] 高吞吐场景用 `asyncSend` 且在回调里处理异常，不在主线程阻塞？
- [ ] `sendOneway` 只用于丢失无影响的日志/埋点？
- [ ] 没有「发完丢弃返回值」当成功的写法？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`message-types.md`](./message-types.md)（顺序/事务/延迟消息怎么发）
- 兄弟：[`consumer-mode.md`](./consumer-mode.md)（消费端怎么收）
- 兄弟：[`idempotent.md`](./idempotent.md)（重试导致重复，消费端去重）
