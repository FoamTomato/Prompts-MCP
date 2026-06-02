---
name: kafka-error-handling
description: Kafka 消费错误处理 — DefaultErrorHandler 重试、死信队列 DLQ、阻塞 vs 非阻塞重试、毒丸消息隔离。Use when 消费抛异常要重试 / 配死信队列 / 隔离卡死分区的毒丸消息时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 错误处理
  - 死信队列
  - 重试
  - DLQ
  - 毒丸消息
  - DefaultErrorHandler
effort: high
context: inline
version: '1.0'
---
# Kafka · 消费错误处理

> 本条只管「消费抛异常后怎么重试、怎么进死信」。手动 ack 见 [`consumer-config.md`](./consumer-config.md)；重试会放大重复消费，去重见 [`idempotent-consumer.md`](./idempotent-consumer.md)。

## 规则

| 概念 | 说明 |
|------|------|
| `DefaultErrorHandler` | 替代旧 `SeekToCurrentErrorHandler`，配重试退避 + 最终 recoverer |
| `DeadLetterPublishingRecoverer` | 重试耗尽后把消息投到 DLQ（默认 `<topic>.DLT`） |
| 阻塞重试 | 在当前 partition 原地重试，**会卡住后续消息**，适合短暂故障 |
| 非阻塞重试 `@RetryableTopic` | 失败消息转入重试 topic 延迟再投，**不阻塞主分区** |
| 毒丸消息 | 永远失败的消息（如反序列化失败）；阻塞重试下会**卡死整个分区**，必须靠 DLQ 隔离 |

**选型**：故障是瞬时的（网络抖动）→ 阻塞重试几次即可；故障可能持久、不能卡后续消息 → 非阻塞重试 + DLQ。反序列化类毒丸用 `ErrorHandlingDeserializer` 直接转 DLQ，别进重试。

## 正例：重试退避 + DLQ

```java
// ✅ 退避重试 3 次，仍失败投到 <topic>.DLT，不无限阻塞
@Bean
public DefaultErrorHandler errorHandler(KafkaTemplate<Object, Object> template) {
    var recoverer = new DeadLetterPublishingRecoverer(template);
    var backoff = new FixedBackOff(1000L, 3);   // 间隔 1s，最多重试 3 次
    return new DefaultErrorHandler(recoverer, backoff);
}
```

```java
// ✅ 非阻塞重试：失败转入重试 topic，4 次后入 DLT，主分区不被卡
@RetryableTopic(attempts = "4", backoff = @Backoff(delay = 2000, multiplier = 2.0))
@KafkaListener(topics = "order-topic")
public void onMessage(String value) { handle(value); }
```

## 反例

```java
// ❌ catch 后吞掉：失败消息既不重试也不进 DLQ，静默丢失
@KafkaListener(topics = "order-topic")
public void onMessage(String value, Acknowledgment ack) {
    try { handle(value); }
    catch (Exception e) { /* 吞掉 */ }
    ack.acknowledge();   // 照样提交 → 丢消息
}
```

```java
// ❌ 无限阻塞重试且无 DLQ：一条毒丸消息卡死整个 partition，后面全堵住
new DefaultErrorHandler(new FixedBackOff(1000L, Long.MAX_VALUE));
```

## 自检

- [ ] 配了 `DefaultErrorHandler`，重试次数**有上限**（不是无限阻塞）？
- [ ] 重试耗尽后有 `DeadLetterPublishingRecoverer` 投 DLQ，没有静默丢消息？
- [ ] 区分了阻塞（卡分区）与非阻塞重试，按故障是否持久选对？
- [ ] 反序列化失败用 `ErrorHandlingDeserializer` 直接进 DLQ，没让毒丸卡死分区？
- [ ] 重试可能放大重复消费，消费逻辑已幂等？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`idempotent-consumer.md`](./idempotent-consumer.md)（重试放大重复消费，必须配合幂等）
- 兄弟：[`consumer-config.md`](./consumer-config.md)（手动 ack 下抛异常才触发重试）
- 相关：[`../../lang/java/error-handling/catch-block-rules.md`](../../lang/java/error-handling/catch-block-rules.md)（禁吞异常）
