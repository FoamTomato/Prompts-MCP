---
name: concurrency-synchronized-vs-lock
description: 用锁升级原理指导 synchronized vs ReentrantLock 选型 — 简单同步靠 JVM 优化选 synchronized，要 tryLock/公平/可中断/多条件才上 Lock。Use when 选锁 / 评审同步代码 / 纠结用哪种锁时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 锁升级
  - synchronized 原理
  - ReentrantLock
  - 偏向锁
  - 轻量级锁
  - AQS
effort: medium
context: inline
version: '1.0'
---
# Java · 锁升级原理与 synchronized/Lock 选型

> 本条只回答「凭原理该用 synchronized 还是 ReentrantLock」。**怎么写** try-finally unlock、ReadWriteLock 用法见 [`../../lang/java/concurrency/lock-choice.md`](../../lang/java/concurrency/lock-choice.md)。

## 原理：synchronized 的锁升级（为什么它不再"重"）

JVM 对 `synchronized` 做了**单调升级**优化，无竞争时几乎零成本，这是选型的核心依据：

| 状态 | 触发 | 成本 |
|------|------|------|
| 偏向锁 | 始终单线程进入（JDK15 后默认废弃，不可依赖） | 一次 CAS 记录线程 ID，后续无开销 |
| 轻量级锁 | 多线程**交替**、无实际竞争 | CAS 自旋抢锁，不阻塞 |
| 重量级锁 | 真正并发竞争、自旋失败 | 升级为 monitor，线程进内核态阻塞 |

结论：**临界区短、竞争不激烈时 synchronized 多停在轻量级，不比 Lock 慢**——别为"性能"而无脑换 Lock。

## 规则：按需求选，不按性能臆测

| 需求 | 选 | 原理依据 |
|------|-----|---------|
| 只要互斥，竞争不高 | `synchronized` | 锁升级 + JIT 锁消除/粗化，自动释放不漏锁 |
| 要 `tryLock`(非阻塞/超时) | `ReentrantLock` | AQS 暴露可轮询获取，synchronized 只能死等 |
| 要可中断地等锁 | `ReentrantLock.lockInterruptibly` | synchronized 阻塞期间不响应中断 |
| 要公平锁 | `new ReentrantLock(true)` | AQS 维护 FIFO 队列，synchronized 只能非公平 |
| 要多个等待条件队列 | `ReentrantLock` + 多个 `Condition` | synchronized 只有一个 wait set |

## 正例：默认 synchronized，有明确高级需求才上 Lock

```java
// ✅ 简单计数互斥：synchronized 足够，JVM 自动管理锁，无遗漏 unlock 风险
private final Object lock = new Object();
synchronized (lock) { count++; }

// ✅ 需要"拿不到锁就降级"，这是 synchronized 做不到的，才用 ReentrantLock
if (reentrantLock.tryLock(2, TimeUnit.SECONDS)) {
    try { doWork(); } finally { reentrantLock.unlock(); }
} else {
    fallback();   // synchronized 没有这个能力
}
```

## 反例：为"性能"把 synchronized 换成 Lock

```java
// ❌ 临界区只是 count++，无竞争场景 synchronized 走轻量级锁本就不慢；
//    换 ReentrantLock 不仅没收益，还多出"忘记 finally unlock 即死锁"的出错面
ReentrantLock lock = new ReentrantLock();
lock.lock();
count++;          // 后面若漏写 finally unlock，整条线程链全锁死
lock.unlock();
```

## 自检

- [ ] 没有"为了性能"把 synchronized 换 Lock？（轻量级锁阶段并不慢）
- [ ] 用 Lock 的理由是 tryLock / 超时 / 可中断 / 公平 / 多 Condition 之一，而非感觉？
- [ ] 不依赖偏向锁（JDK15+ 已默认关闭）做性能假设？
- [ ] 选了 Lock 就确认按 lock-choice.md 写了 try-finally unlock？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`volatile-boundary.md`](./volatile-boundary.md)（不需要互斥、只需可见性时用 volatile）
- 兄弟：[`happens-before.md`](./happens-before.md)（synchronized 提供的 happens-before 保证）
- 用法（怎么写 unlock / ReadWriteLock）：[`../../lang/java/concurrency/lock-choice.md`](../../lang/java/concurrency/lock-choice.md)
- 线程从哪来：[`../../lang/java/concurrency/thread-pool-config.md`](../../lang/java/concurrency/thread-pool-config.md)
