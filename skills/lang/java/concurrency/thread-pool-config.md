---
name: java-thread-pool-config
description: ThreadPoolExecutor 七参数配置 — 核心/最大线程、有界队列、命名 ThreadFactory、拒绝策略，含 CPU/IO 密集线程数估算。Use when 新建线程池 / 调参 / 选拒绝策略时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 线程池参数
  - ThreadPoolExecutor
  - 拒绝策略
  - RejectedExecutionHandler
  - ThreadFactory
  - 线程数估算
  - corePoolSize
effort: medium
context: inline
version: '1.0'
---
# Java · 线程池参数配置

> 本条只管「ThreadPoolExecutor 七参数怎么填」。为什么不能用 `Executors` 工厂见 [`thread-pool-types.md`](./thread-pool-types.md)。

## 规则

| 参数 | 含义 | 怎么填 |
|------|------|--------|
| corePoolSize | 常驻核心线程数 | 按下方公式估 |
| maximumPoolSize | 最大线程数 | 队列满后才扩到此值 |
| keepAliveTime | 非核心线程空闲存活 | 60s 起步 |
| workQueue | 任务队列 | **必须有界**（如 `new ArrayBlockingQueue<>(1000)`） |
| threadFactory | 线程工厂 | **必须自定义、给线程命名** |
| handler | 拒绝策略 | 见下表四选一 |

## 拒绝策略四选一

| 策略 | 行为 | 何时用 |
|------|------|--------|
| AbortPolicy（默认） | 抛 `RejectedExecutionException` | 默认，任务不可丢 |
| CallerRunsPolicy | 提交线程自己执行 | 要削峰、不丢任务、可接受变慢 |
| DiscardPolicy | 静默丢弃 | 任务可丢且无需感知 |
| DiscardOldestPolicy | 丢队头最老任务 | 只关心最新任务 |

## 线程数估算

- **CPU 密集型**（计算为主）：`核数 + 1`，线程多了只增加上下文切换。
- **IO 密集型**（等 DB / RPC / 磁盘）：`核数 × (1 + 平均等待时间 / 平均计算时间)`，工程上常取 `核数 × 2` 起步，再压测调。

## 正例：完整配置 + 命名 ThreadFactory

```java
ThreadFactory factory = new ThreadFactoryBuilder()   // guava，或 Spring 的 CustomizableThreadFactory
        .setNameFormat("order-async-%d")
        .build();

ExecutorService pool = new ThreadPoolExecutor(
        8, 16, 60L, TimeUnit.SECONDS,
        new ArrayBlockingQueue<>(1000),               // 有界队列
        factory,
        new ThreadPoolExecutor.CallerRunsPolicy());    // 显式拒绝策略
```

## 反例：线程不命名

```java
// ❌ 默认线程名 pool-1-thread-3，线上 jstack / 日志根本认不出是哪个池
ExecutorService pool = new ThreadPoolExecutor(
        8, 16, 60L, TimeUnit.SECONDS, new ArrayBlockingQueue<>(1000));
```

## 自检

- [ ] workQueue 是**有界**队列（带容量参数）？
- [ ] 传了自定义 `ThreadFactory` 且线程名有业务语义（`xxx-%d`）？
- [ ] 显式指定了拒绝策略，没用裸构造让它走默认 Abort 还不自知？
- [ ] 线程数按 CPU / IO 密集型估算，而非拍脑袋？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`thread-pool-types.md`](./thread-pool-types.md)（为什么禁用 Executors 工厂）
- 兄弟：[`completablefuture.md`](./completablefuture.md)（异步编排要传这里建的池）
- 兄弟：[`threadlocal-cleanup.md`](./threadlocal-cleanup.md)（池里用 ThreadLocal 要清理）
