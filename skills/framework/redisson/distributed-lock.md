---
name: redisson-distributed-lock
description: Redisson RLock 分布式锁 — lock() 看门狗自动续期（默认 30s），tryLock(wait,lease,unit) 控等待+租期，释放必须放 finally。Use when 用 RLock 加锁 / 选 lock 还是 tryLock / 防止忘了 unlock 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 分布式锁
  - 看门狗续期
  - RLock
  - tryLock
  - finally unlock
effort: high
context: inline
version: '1.0'
---
# Redisson · RLock 分布式锁

> 本条只管「RLock API 怎么用对」。Redisson 凭什么比手写 SETNX 好、RedLock 要不要用见 [`lock-vs-setnx.md`](./lock-vs-setnx.md)；SETNX/Lua 命令本身见 [`../redis/distributed-lock.md`](../redis/distributed-lock.md)。

## 规则

| 项 | 约定 |
|----|------|
| `lock()` | 阻塞获取，**不传 leaseTime** 才触发看门狗（默认每 10s 续到 30s），适合执行时长不确定 |
| `tryLock(wait,lease,unit)` | 最多等 `wait` 拿锁，拿到后持有 `lease`；**传了 lease 即关闭看门狗**，到点自动释放 |
| 选哪个 | 怕死锁、要快速失败 → `tryLock` 带超时；执行时长不可控、必须跑完 → `lock()` 靠看门狗 |
| 释放 | `unlock()` **必须放 `finally`**，且先判 `isHeldByCurrentThread()`，否则抛 `IllegalMonitorStateException` |
| 可重入 | 同线程可重复 `lock`，按次数计；加几次就要解几次 |

## 正例：tryLock 带等待+租期（快速失败）

```java
RLock lock = redisson.getLock("lock:order:" + orderId);
boolean locked = false;
try {
    locked = lock.tryLock(3, 30, TimeUnit.SECONDS); // 等 3s，持锁 30s
    if (!locked) {
        throw new BizException("系统繁忙，请重试");   // 没抢到锁，快速失败
    }
    doBusiness();
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
} finally {
    if (locked && lock.isHeldByCurrentThread()) {
        lock.unlock();                              // 只释放自己持有的
    }
}
```

## 正例：lock() 靠看门狗（执行时长不确定）

```java
RLock lock = redisson.getLock("lock:job:" + jobId);
lock.lock();                                        // 不传 leaseTime → 看门狗自动续期
try {
    runLongTask();                                  // 跑多久看门狗续多久，不会中途锁过期
} finally {
    lock.unlock();
}
```

## 反例

```java
// ❌ unlock 不在 finally：业务抛异常 → 锁永不释放
RLock lock = redisson.getLock(key);
lock.lock();
doBusiness();        // 抛异常就漏 unlock
lock.unlock();

// ❌ tryLock 传了 leaseTime 又指望看门狗续期：传 lease 即关闭看门狗，到点照样过期
lock.tryLock(3, 10, TimeUnit.SECONDS);   // 业务跑 20s → 第 10s 锁已被自动释放

// ❌ 不判持有就 unlock：锁已超时被别人拿走，这里抛 IllegalMonitorStateException
lock.unlock();
```

## 自检

- [ ] `unlock()` 放在 `finally` 里，业务异常也能释放？
- [ ] `unlock` 前判了 `isHeldByCurrentThread()`，不会误释放/抛异常？
- [ ] 想靠看门狗续期，用的是**不带 leaseTime** 的 `lock()`（而非 `tryLock(wait,lease,...)`）？
- [ ] 怕死锁的场景用了 `tryLock` 带超时，没抢到就快速失败？
- [ ] 锁粒度是单个业务键（如 `lock:order:{id}`），不是一把大锁锁全表？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`lock-vs-setnx.md`](./lock-vs-setnx.md)（为什么用 Redisson 不手写 SETNX）
- 相关：[`../redis/distributed-lock.md`](../redis/distributed-lock.md)（Redis 视角：SETNX/Lua 释放命令）
