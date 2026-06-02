---
name: virtual-threads-pinning-pitfall
description: 虚拟线程 pinning 陷阱 — synchronized 块内执行阻塞调用会把虚拟线程钉死在载体线程上无法卸载，改用 ReentrantLock。Use when 虚拟线程里有 synchronized / 排查载体线程耗尽 / 改锁防 pinning 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - pinning
  - 钉住载体线程
  - synchronized 阻塞
  - ReentrantLock
  - 虚拟线程陷阱
  - carrier thread
effort: high
context: inline
version: '1.0'
---
# Java · 虚拟线程 pinning 陷阱

> 本条只回答「为什么 synchronized 会害了虚拟线程，怎么改」。该不该用虚拟线程见 [`when-to-use.md`](./when-to-use.md)；池化与 Executor 见 [`vs-thread-pool.md`](./vs-thread-pool.md)。

## 原理 → 什么是 pinning

虚拟线程正常情况下阻塞时会从载体线程卸载。但当它在 `synchronized` 块/方法**内部**执行阻塞操作时，JDK21 会把它**钉住（pin）**在当前载体线程上——载体线程被独占、无法去跑其他虚拟线程。若大量虚拟线程同时被钉住，**少量载体线程被耗尽**，并发能力直接退回平台线程水平，虚拟线程的意义荡然无存，严重时表现为吞吐骤降甚至假死。

## 规则

| 场景 | 做法 |
|------|------|
| 需要锁 + 锁内有阻塞（IO / 等待） | 用 `ReentrantLock` 的 `lock()`/`unlock()`，**不要** `synchronized` |
| 锁内是纯内存的极短临界区，无阻塞 | `synchronized` 仍可（钉住时间极短，影响小） |
| 第三方库/驱动内部用 synchronized 阻塞 | 升级到已改用 Lock 的版本，或对该调用退回平台线程池 |
| 想定位线上钉住 | 加 `-Djdk.tracePinnedThreads=full` 打印 pinning 栈 |

注：JDK24+（JEP 491）已让 synchronized 内阻塞不再钉住，但 JDK21 LTS 仍有此问题——生产多数跑 21，按本条规避。

## 正例

```java
// ✅ 锁内有阻塞调用：用 ReentrantLock，虚拟线程仍可正常卸载
private final ReentrantLock lock = new ReentrantLock();

void update() {
    lock.lock();
    try {
        remoteCall();          // 阻塞 IO，不会钉住载体线程
    } finally {
        lock.unlock();
    }
}
```

## 反例

```java
// ❌ synchronized 块内阻塞 —— 虚拟线程被钉死在载体线程，载体线程耗尽
synchronized (this) {
    remoteCall();              // 阻塞期间载体线程被独占，无法调度别的虚拟线程
}
```

理由：`synchronized` 在 JDK21 下与虚拟线程的卸载机制冲突，锁内阻塞会钉住载体线程；`ReentrantLock` 不触发 pinning，阻塞时虚拟线程照常卸载。性能影响为量级描述，需结合 `-Djdk.tracePinnedThreads` 实测。

## 自检

- [ ] 虚拟线程会执行到的代码路径上，没有「synchronized 块内做阻塞 IO」？
- [ ] 这类锁已从 `synchronized` 换成 `ReentrantLock`（且 unlock 在 finally）？
- [ ] 排查时加了 `-Djdk.tracePinnedThreads=full` 确认无意外 pinning？
- [ ] 知道 JDK24+ 已修复，但当前 JDK21 仍需规避？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`when-to-use.md`](./when-to-use.md)（大量 synchronized 也是"不该用虚拟线程"的信号）
- 兄弟：[`vs-thread-pool.md`](./vs-thread-pool.md)（钉住严重时退回平台线程池）
- 锁选型细节：[`lang/java/concurrency/lock-choice.md`](../../lang/java/concurrency/lock-choice.md)
