---
name: java-lock-choice
description: 锁选型 — synchronized（简单互斥）vs ReentrantLock（要 tryLock/超时/可中断）vs ReadWriteLock（读多写少），且 Lock 必须 try-finally 里 unlock。Use when 多线程共享可变状态 / 选锁 / 评审锁泄漏时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 锁选型
  - synchronized
  - ReentrantLock
  - ReadWriteLock
  - 读写锁
  - tryLock
  - lock unlock
effort: medium
context: inline
version: '1.0'
---
# Java · 锁选型

> 本条只管「该用哪种锁 + 锁怎么释放」。无锁的线程池/异步编排见 [`index.md`](./index.md) 其他叶子。

## 规则

| 场景 | 选 | 理由 |
|------|-----|------|
| 简单临界区，无高级需求 | `synchronized` | JVM 自动释放，最不易出错，JIT 优化好 |
| 要超时 / 可中断 / 可轮询获取 | `ReentrantLock` + `tryLock` | synchronized 拿不到锁只能死等 |
| 要公平锁 / 多个条件队列 | `ReentrantLock` + `Condition` | synchronized 只有一个等待集 |
| 读远多于写 | `ReentrantReadWriteLock` | 读读不互斥，并发读吞吐高 |

优先级：能用 `synchronized` 解决就别上 `Lock`——后者多一份手动 unlock 的出错面。

## 反例：unlock 没进 finally

```java
// ❌ 临界区抛异常，unlock 永远执行不到 → 锁泄漏，其他线程全部死锁
lock.lock();
doWork();              // 抛异常
lock.unlock();
```

## 正例：lock 在 try 外，unlock 在 finally

```java
// ✅ lock() 写在 try 之外，unlock() 必进 finally
lock.lock();
try {
    doWork();
} finally {
    lock.unlock();
}

// ✅ tryLock 拿到才进 try，没拿到不能 unlock
if (lock.tryLock(2, TimeUnit.SECONDS)) {
    try {
        doWork();
    } finally {
        lock.unlock();
    }
} else {
    // 降级 / 抛超时
}
```

## 自检

- [ ] 只是互斥的优先 `synchronized`，没有为用而用 `ReentrantLock`？
- [ ] 读多写少考虑了 `ReadWriteLock`？
- [ ] 每个 `lock.lock()` 都有对应的 `finally { unlock() }`？
- [ ] `lock()` 写在 `try` 块之外（避免 lock 失败也 unlock）？
- [ ] `tryLock` 仅在返回 true 时才 unlock？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`thread-pool-config.md`](./thread-pool-config.md)（多线程从哪来）
- 兄弟：[`threadlocal-cleanup.md`](./threadlocal-cleanup.md)（线程封闭是另一种避免共享的手段）
