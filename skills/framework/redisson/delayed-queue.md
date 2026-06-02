---
name: redisson-delayed-queue
description: Redisson RDelayedQueue 延迟队列 — offer(item,delay,unit) 投递延迟消息，到期自动转入目标 RBlockingQueue，消费端 take() 阻塞取。Use when 做延迟取消订单 / 延迟重试 / 定时触发任务时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 延迟队列
  - RDelayedQueue
  - 延迟取消订单
  - 到期触发
  - offer delay
effort: medium
context: inline
version: '1.0'
---
# Redisson · RDelayedQueue 延迟队列

> 本条只管「延迟到期触发任务怎么做」。限流见 [`rate-limiter.md`](./rate-limiter.md)；互斥见 [`distributed-lock.md`](./distributed-lock.md)。

## 规则

| 项 | 约定 |
|----|------|
| 结构 | `RDelayedQueue` 包一个目标 `RBlockingQueue`：到期的 item 由 Redisson 自动转入目标队列 |
| 投递 | `delayedQueue.offer(item, delay, unit)`：delay 后才可被消费 |
| 消费 | 从**目标队列** `take()`（阻塞）取，不是从 delayedQueue 取 |
| 生命周期 | `RDelayedQueue` 用完 `destroy()`；生产中通常全局单例长期持有，不要每次新建 |
| 幂等 | 消费端必须幂等（重复投递/重启重放可能重复），结合业务状态校验 |
| 适用 | 延迟取消未支付订单、延迟重试、N 分钟后提醒 |

## 正例：下单后 30 分钟未支付自动取消

```java
// 启动时初始化（单例）
RBlockingQueue<String> queue = redisson.getBlockingQueue("queue:order:cancel");
RDelayedQueue<String> delayQueue = redisson.getDelayedQueue(queue);

// 下单时投递延迟消息
delayQueue.offer(orderId, 30, TimeUnit.MINUTES);

// 独立消费线程：到期自动转入 queue，take 阻塞取出
String orderId = queue.take();
Order o = orderService.get(orderId);
if (o.getStatus() == UNPAID) {       // 幂等：已支付/已取消则跳过
    orderService.cancel(orderId);
}
```

## 反例

```java
// ❌ 直接从 delayQueue 取：取不到到期元素，应从目标 queue.take()
String id = delayQueue.poll();

// ❌ 每次投递都新建 delayedQueue 又不 destroy：句柄泄漏、监听线程堆积
RDelayedQueue<String> q = redisson.getDelayedQueue(queue); // 放在高频方法里反复 new

// ❌ 消费不做幂等：重启重放 / 重复投递时把已支付订单也取消了
orderService.cancel(orderId);    // 没判状态直接取消
```

## 自检

- [ ] 消费端从**目标 `RBlockingQueue`** `take()`，不是从 `RDelayedQueue` 取？
- [ ] `RDelayedQueue` 是单例长期持有，没在高频路径反复 new？
- [ ] 消费逻辑幂等（按业务状态校验），能容忍重复投递 / 重启重放？
- [ ] 不再使用的 `RDelayedQueue` 调了 `destroy()`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`rate-limiter.md`](./rate-limiter.md)（同为 Redisson 高级原语）
- 兄弟：[`distributed-lock.md`](./distributed-lock.md)（取消时如需互斥可加锁）
