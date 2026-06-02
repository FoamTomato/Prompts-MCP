---
name: virtual-threads-vs-thread-pool
description: 虚拟线程与线程池的关系 — 创建极廉价不需池化，用 newVirtualThreadPerTaskExecutor 而非固定大小池；海量虚拟线程下慎用 ThreadLocal。Use when 给虚拟线程建 Executor / 纠结要不要池化 / 处理 ThreadLocal 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 虚拟线程池化
  - newVirtualThreadPerTaskExecutor
  - ThreadLocal
  - 不需要池化
  - 线程池关系
  - thread pool
effort: medium
context: inline
version: '1.0'
---
# Java · 虚拟线程与线程池的关系

> 本条只回答「虚拟线程要不要池化、怎么建 Executor、ThreadLocal 怎么办」。该不该用见 [`when-to-use.md`](./when-to-use.md)；pinning 见 [`pinning-pitfall.md`](./pinning-pitfall.md)。

## 原理 → 为什么不池化

线程池存在的根本理由是**平台线程创建昂贵**（每个映射一个 OS 线程、约 1MB 栈），所以复用。虚拟线程创建极廉价（栈在堆上、按需增长，可同时有百万个），那条理由不成立——**池化虚拟线程是反模式**：用固定大小池反而人为给它设了并发上限，丢掉了"一任务一线程"的全部好处。

## 规则

| 需求 | 做法 |
|------|------|
| 跑一批 IO 任务 | `Executors.newVirtualThreadPerTaskExecutor()`，每个任务一条新虚拟线程 |
| 临时起一条 | `Thread.ofVirtual().start(runnable)` / `Thread.startVirtualThread(r)` |
| **限流**（保护下游，如 DB 连接数） | 不靠线程池大小限流，用 `Semaphore` 显式控制并发数 |
| CPU 重活 | 仍用**固定大小平台线程池**（见 [`thread-pool-config.md`](../../lang/java/concurrency/thread-pool-config.md)） |

ThreadLocal 注意：海量虚拟线程下，每条线程一份 ThreadLocal 副本会**放大内存占用**；且虚拟线程生命周期短，缓存型 ThreadLocal 收益消失。优先用方法传参或 JDK21 的 `ScopedValue` 替代。

## 正例

```java
// ✅ 不池化：每个任务一条虚拟线程，try-with-resources 自动 join
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    tasks.forEach(t -> executor.submit(t::run));
}

// ✅ 要保护下游就用 Semaphore 限并发，而不是缩小线程池
Semaphore permits = new Semaphore(50);   // 最多 50 个并发打到 DB
executor.submit(() -> {
    permits.acquire();
    try { db.query(...); } finally { permits.release(); }
});
```

## 反例

```java
// ❌ 把虚拟线程塞进固定大小池 —— 人为设并发上限，废掉虚拟线程的意义
ExecutorService pool = Executors.newFixedThreadPool(200,
        Thread.ofVirtual().factory());

// ❌ 海量虚拟线程里大量用 ThreadLocal 做缓存 —— 每线程一份副本，内存膨胀
private static final ThreadLocal<HeavyCtx> CTX = ThreadLocal.withInitial(HeavyCtx::new);
```

理由：虚拟线程廉价到无需复用，固定池只会限制并发；限流应交给 `Semaphore` 语义化表达；ThreadLocal 副本数随虚拟线程数线性膨胀，海量场景改用 `ScopedValue` 或显式传参。

## 自检

- [ ] 虚拟线程用 `newVirtualThreadPerTaskExecutor`，没塞进固定大小池？
- [ ] 限流用 `Semaphore` 等显式手段，而非缩小线程池？
- [ ] CPU 密集仍走固定大小平台线程池？
- [ ] 海量虚拟线程下没有滥用 ThreadLocal（改 `ScopedValue` / 传参）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`when-to-use.md`](./when-to-use.md)（先确认 IO 密集才谈 Executor）
- 兄弟：[`pinning-pitfall.md`](./pinning-pitfall.md)（载体线程被钉住时池化也救不了）
- 平台线程池配置：[`lang/java/concurrency/thread-pool-config.md`](../../lang/java/concurrency/thread-pool-config.md)
