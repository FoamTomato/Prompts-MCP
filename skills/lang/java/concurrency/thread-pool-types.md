---
name: java-thread-pool-types
description: 禁用 Executors.newFixedThreadPool/newCachedThreadPool 工厂 — 无界队列或无界线程都会 OOM，必须手写 ThreadPoolExecutor。Use when 看到 Executors 调用 / 创建线程池时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - Executors
  - newFixedThreadPool
  - newCachedThreadPool
  - 无界队列
  - 线程池 OOM
  - 阿里规约
  - unbounded queue
effort: medium
context: inline
version: '1.0'
---
# Java · 禁用 Executors 工厂方法

> 本条只管「为什么不能用 `Executors` 工厂」。具体七参数怎么填见 [`thread-pool-config.md`](./thread-pool-config.md)。

## 规则

**禁止用 `Executors` 的工厂方法创建线程池，一律手动 `new ThreadPoolExecutor(...)`。**（《阿里巴巴 Java 开发手册》强制条款。）

理由：工厂方法把危险参数藏在了默认值里，编译期看不出风险，线上才 OOM。

| 工厂方法 | 隐藏的雷 | 后果 |
|----------|----------|------|
| newFixedThreadPool | 用 `LinkedBlockingQueue` **无界队列**（容量 `Integer.MAX_VALUE`） | 任务堆积撑爆内存 → OOM |
| newSingleThreadExecutor | 同上，无界队列 | 同上 |
| newCachedThreadPool | maxPoolSize = `Integer.MAX_VALUE`，**线程无上限** | 突发流量创建海量线程 → OOM |
| newScheduledThreadPool | 用无界的 `DelayedWorkQueue` | 任务堆积撑爆内存 |

## 反例：工厂方法

```java
// ❌ 无界队列：积压任务无上限，内存被任务对象吃光
ExecutorService pool = Executors.newFixedThreadPool(8);

// ❌ 无界线程：每来一个任务没空闲线程就 new，瞬时几万线程
ExecutorService pool = Executors.newCachedThreadPool();
```

## 正例：手写，参数全部显式可见

```java
// ✅ 队列容量、最大线程、拒绝策略全暴露在眼前，没有隐藏的无界
ExecutorService pool = new ThreadPoolExecutor(
        8, 16, 60L, TimeUnit.SECONDS,
        new ArrayBlockingQueue<>(1000),                 // 有界
        new ThreadFactoryBuilder().setNameFormat("biz-%d").build(),
        new ThreadPoolExecutor.AbortPolicy());          // 显式拒绝
```

参数取值与命名细节见 [`thread-pool-config.md`](./thread-pool-config.md)。

## 自检

- [ ] 代码里没有任何 `Executors.newXxx(...)` 调用？
- [ ] 线程池都是 `new ThreadPoolExecutor(...)` 显式构造？
- [ ] 队列有界、maxPoolSize 有上限，不存在无界堆积或无界扩线程？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`thread-pool-config.md`](./thread-pool-config.md)（手写时七参数怎么填）
- 兄弟：[`completablefuture.md`](./completablefuture.md)（同理禁用默认 commonPool）
