---
name: behavioral-observer
description: 观察者模式 — 事件发布订阅解耦发布方与多个下游，Spring 用 ApplicationEvent 发布、@EventListener 监听。Use when 一个动作后要通知多个不相关下游 / 想解耦主流程与副作用 / 用 Spring 事件时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 观察者
  - Observer
  - 事件发布
  - 发布订阅
  - ApplicationEvent
  - EventListener
effort: medium
context: inline
version: '1.0'
---
# Behavioral · 观察者（Spring 事件）

## 何时用

| 信号 | 用观察者/事件 |
|------|--------------|
| 主动作完成后要触发**多个互不相关**的副作用（发短信/积分/日志） | ✅ |
| 想让主流程不感知下游，下游可随意增删 | ✅ |
| 副作用是主流程的强依赖、失败必须回滚 | ❌ 直接同步调用，别用事件 |

## 正例：Spring ApplicationEvent

```java
// 事件对象
public class OrderPaidEvent {
    private final Long orderId;
    public OrderPaidEvent(Long orderId) { this.orderId = orderId; }
    public Long getOrderId() { return orderId; }
}

// 发布方：只管发事件，不知道有谁在听
@Service
public class OrderService {
    private final ApplicationEventPublisher publisher;
    public OrderService(ApplicationEventPublisher publisher) { this.publisher = publisher; }
    public void pay(Long orderId) {
        // 主流程：改订单状态...
        publisher.publishEvent(new OrderPaidEvent(orderId));   // 通知下游
    }
}

// 订阅方：各自独立，增删一个监听不影响发布方
@Component
public class PointListener {
    @EventListener
    public void onPaid(OrderPaidEvent e) { /* 加积分 */ }
}
```

## 同步 / 异步 / 事务边界

- `@EventListener` **默认同步**，跑在发布方线程、同一事务里。
- 加 `@Async`（需 `@EnableAsync`）异步执行，副作用不阻塞主流程。
- 想等事务提交后再触发用 `@TransactionalEventListener(phase = AFTER_COMMIT)`，避免主事务回滚了通知却已发出。

## 反例：主流程硬编码所有下游

```java
// ❌ 发布方耦合每一个下游，加一个通知就改 pay()
public void pay(Long orderId) {
    // 改状态...
    pointService.add(orderId);
    smsService.send(orderId);
    logService.record(orderId);   // 新下游继续往这堆
}
```

## 自检

- [ ] 副作用是「弱依赖、可独立失败」才用事件；强一致依赖用同步调用？
- [ ] 发布方只发事件，不 import 任何监听方？
- [ ] 异步监听加了 `@Async` + `@EnableAsync`，没误以为默认异步？
- [ ] 需要事务提交后触发的，用了 `@TransactionalEventListener(AFTER_COMMIT)`？

## 相关

- 父：[`./index.md`](./index.md)
- 异步线程池：[`../../lang/java/concurrency/thread-pool-config.md`](../../lang/java/concurrency/thread-pool-config.md)
