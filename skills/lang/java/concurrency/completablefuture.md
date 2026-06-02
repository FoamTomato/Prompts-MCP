---
name: java-completablefuture
description: CompletableFuture 异步编排 — supplyAsync 必传自定义线程池、thenCompose vs thenCombine、exceptionally 兜异常。Use when 写异步任务 / 编排多个异步调用 / 处理异步异常时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - CompletableFuture
  - 异步编排
  - supplyAsync
  - thenCompose
  - thenCombine
  - exceptionally
  - ForkJoinPool commonPool
effort: medium
context: inline
version: '1.0'
---
# Java · CompletableFuture 编排

> 本条只管「CompletableFuture 怎么编排」。线程池本身怎么建见 [`thread-pool-config.md`](./thread-pool-config.md)。

## 规则

| 决策点 | 规则 |
|--------|------|
| 跑在哪个池 | `*Async` 方法**必须传第二个参数（自定义线程池）**，禁用默认 `ForkJoinPool.commonPool()` |
| 串行依赖（B 用 A 的结果） | `thenCompose`（扁平化，避免 `CF<CF<T>>` 嵌套） |
| 并行合并（A、B 互不依赖再汇总） | `thenCombine` |
| 异常处理 | `exceptionally`（只兜异常）或 `handle`（成功失败都接） |
| 阻塞取结果 | `get(timeout)` / `join`，**必须带超时**，别裸 `get()` |

## 反例：用默认 commonPool

```java
// ❌ commonPool 是 JVM 全局共享、线程数≈核数-1，一个慢 IO 任务就拖垮整个进程的所有并行流
CompletableFuture.supplyAsync(() -> rpc.call());
```

## 正例：传自定义池 + 编排 + 兜异常

```java
ExecutorService pool = bizPool;   // 见 thread-pool-config.md

// 串行依赖：拿到 user 再去查 order —— 用 thenCompose 避免嵌套
CompletableFuture<List<Order>> f = CompletableFuture
        .supplyAsync(() -> userService.find(id), pool)
        .thenCompose(user -> CompletableFuture.supplyAsync(
                () -> orderService.listByUser(user), pool))
        .exceptionally(ex -> {                       // 异常兜底
            log.warn("load orders failed: {}", id, ex);
            return List.of();
        });

// 并行合并：user 和 stock 互不依赖，并行后 thenCombine 汇总
CompletableFuture<Dto> g = userFuture.thenCombine(stockFuture,
        (user, stock) -> new Dto(user, stock));
```

## 自检

- [ ] 所有 `supplyAsync` / `thenXxxAsync` 都传了自定义线程池，没用默认 commonPool？
- [ ] 串行依赖用 `thenCompose`（不是 `thenApply` 套出 `CF<CF<T>>`）？
- [ ] 并行无依赖用 `thenCombine`，没有人为串行化？
- [ ] 有 `exceptionally` / `handle` 兜异常，且 `get` 带超时？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`thread-pool-config.md`](./thread-pool-config.md)（传进去的池怎么建）
- 兄弟：[`thread-pool-types.md`](./thread-pool-types.md)（同样禁用无界/默认池）
- 兄弟：[`threadlocal-cleanup.md`](./threadlocal-cleanup.md)（异步切线程时 ThreadLocal 不会自动传递）
