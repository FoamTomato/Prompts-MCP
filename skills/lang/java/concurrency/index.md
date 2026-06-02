---
name: lang-java-concurrency-index
description: Java 并发五件事 — 线程池怎么配 / 为什么禁 Executors 工厂 / CompletableFuture 编排 / 锁怎么选 / ThreadLocal 怎么清。Use when 建线程池 / 写异步编排 / 选锁 / 排查并发内存泄漏的 PR 时。
parent: ../index.md
children:
  - { name: thread-pool-config, path: thread-pool-config.md, tag: skill, note: ThreadPoolExecutor 七参数、拒绝策略、线程数估算、命名 ThreadFactory }
  - { name: thread-pool-types, path: thread-pool-types.md, tag: skill, note: 禁 Executors 工厂方法（无界队列/无界线程 OOM），手写 ThreadPoolExecutor }
  - { name: completablefuture, path: completablefuture.md, tag: skill, note: CompletableFuture 编排、传自定义线程池、thenCompose vs thenCombine、异常处理 }
  - { name: lock-choice, path: lock-choice.md, tag: skill, note: synchronized vs ReentrantLock vs ReadWriteLock 选型、try-finally unlock }
  - { name: threadlocal-cleanup, path: threadlocal-cleanup.md, tag: skill, note: 线程池场景 ThreadLocal 必 remove，try-finally 清理 }
when_to_descend: 写 / 评审任何用到线程池、异步任务、锁、ThreadLocal 的 Java 代码
---

# Concurrency · 子项索引

并发拆成五个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 要 new 一个线程池，纠结七个参数、拒绝策略、线程数、线程命名 | [thread-pool-config](thread-pool-config.md) |
| 想用 `Executors.newFixedThreadPool` / `newCachedThreadPool` 图省事 | [thread-pool-types](thread-pool-types.md) |
| 用 CompletableFuture 做异步编排（supplyAsync / thenCompose / 异常） | [completablefuture](completablefuture.md) |
| 多线程共享可变状态，纠结用 synchronized 还是 Lock | [lock-choice](lock-choice.md) |
| 在线程池里用了 ThreadLocal，担心内存泄漏或脏数据 | [threadlocal-cleanup](threadlocal-cleanup.md) |
