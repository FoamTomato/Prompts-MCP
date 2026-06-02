---
name: redisson-rate-limiter
description: Redisson RRateLimiter 分布式限流 — trySetRate 设令牌桶速率（OVERALL 全集群共享 / PER_CLIENT 每实例），acquire 阻塞、tryAcquire 非阻塞快速失败。Use when 做跨进程限流 / 选阻塞还是非阻塞获取令牌时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 分布式限流
  - 令牌桶
  - RRateLimiter
  - tryAcquire
  - 限流速率
effort: medium
context: inline
version: '1.0'
---
# Redisson · RRateLimiter 分布式限流

> 本条只管「跨进程令牌桶限流怎么做」。互斥加锁见 [`distributed-lock.md`](./distributed-lock.md)；延迟执行见 [`delayed-queue.md`](./delayed-queue.md)。

## 规则

| 项 | 约定 |
|----|------|
| 设速率 | `trySetRate(mode, rate, interval, unit)`：每 `interval` 放 `rate` 个令牌 |
| `RateType.OVERALL` | **全集群共享**总速率（所有实例加起来不超），最常用 |
| `RateType.PER_CLIENT` | 每个客户端实例各自限速 |
| `acquire(n)` | **阻塞**直到拿到 n 个令牌；适合后台任务平滑限速 |
| `tryAcquire(n, timeout, unit)` | 拿不到就返回 `false`，**非阻塞快速失败**；适合接口限流，超限直接拒绝 |
| 持久化 | rate 只需 `trySetRate` 一次（重复调用不覆盖），key 建议设 TTL 防遗留脏配置 |

## 正例：接口限流，超限快速拒绝

```java
RRateLimiter limiter = redisson.getRateLimiter("rate:api:order");
// 全集群每秒最多 100 次（trySetRate 幂等，仅首次生效）
limiter.trySetRate(RateType.OVERALL, 100, 1, RateIntervalUnit.SECONDS);

if (!limiter.tryAcquire()) {                 // 非阻塞：拿不到立即 false
    throw new BizException("请求过于频繁，请稍后再试");
}
handleOrder();
```

## 正例：后台任务平滑限速

```java
RRateLimiter limiter = redisson.getRateLimiter("rate:job:push");
limiter.trySetRate(RateType.OVERALL, 50, 1, RateIntervalUnit.SECONDS);

for (Msg msg : batch) {
    limiter.acquire();                       // 阻塞：按 50/s 平滑放行，不打爆下游
    push(msg);
}
```

## 反例

```java
// ❌ 接口限流用 acquire() 阻塞：超限请求被挂住，线程池被占满、响应雪崩
if (limiter.tryAcquire()) ... // 应这样
limiter.acquire();            // ← 错：接口里别阻塞等令牌

// ❌ 每次请求都重设速率：trySetRate 虽幂等，但应只在初始化时配一次
limiter.trySetRate(RateType.OVERALL, 100, 1, RateIntervalUnit.SECONDS); // 放业务方法里反复调
```

## 自检

- [ ] 速率用 `trySetRate` 在初始化时配一次，没放在每次请求里反复调？
- [ ] 集群共享总量用 `RateType.OVERALL`（而非误用 `PER_CLIENT` 导致总量翻倍）？
- [ ] 接口限流用 `tryAcquire` 快速失败，没用 `acquire` 阻塞挂住请求线程？
- [ ] 后台平滑限速才用 `acquire` 阻塞？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`distributed-lock.md`](./distributed-lock.md)（同为 Redisson 分布式协调原语）
- 兄弟：[`delayed-queue.md`](./delayed-queue.md)（延迟任务）
