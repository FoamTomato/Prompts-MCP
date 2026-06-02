---
name: java-threadlocal-cleanup
description: 线程池里用 ThreadLocal 必须在 finally 里 remove — 线程复用导致脏数据残留 + Entry key 弱引用造成 value 内存泄漏。Use when 用 ThreadLocal 传上下文 / 线程池里存 ThreadLocal / 排查脏数据或内存泄漏时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - ThreadLocal
  - ThreadLocal 内存泄漏
  - 线程复用脏数据
  - remove
  - 线程封闭
  - thread local cleanup
  - 上下文传递
effort: medium
context: inline
version: '1.0'
---
# Java · ThreadLocal 清理

> 本条只管「线程池里用 ThreadLocal 为什么 + 怎么 remove」。线程池本身怎么建见 [`thread-pool-config.md`](./thread-pool-config.md)。

## 规则

**用线程池跑的任务里，凡 set 过 ThreadLocal，必须在 `finally` 里 `remove()`。** 两个独立后果，少一个都中招：

| 后果 | 成因 |
|------|------|
| **脏数据** | 线程池线程**复用**，上个任务残留的值被下个任务读到（最常见：用户上下文串号） |
| **内存泄漏** | `ThreadLocalMap` 的 Entry **key 是弱引用、value 是强引用**；线程长期存活（池里就是），不 remove 则 value 永远不被回收 |

## 反例：池里 set 不 remove

```java
// ❌ 线程复用，下一个请求进来 currentUser 还是上一个用户 → 串号 + 泄漏
private static final ThreadLocal<User> CTX = new ThreadLocal<>();

pool.submit(() -> {
    CTX.set(currentUser);
    handle();                  // 用完没清
});
```

## 正例：try-finally remove

```java
private static final ThreadLocal<User> CTX = new ThreadLocal<>();

pool.submit(() -> {
    CTX.set(currentUser);
    try {
        handle();
    } finally {
        CTX.remove();          // ✅ 无论是否异常都清空当前线程的槽
    }
});
```

> 注意：`CompletableFuture` / 线程池切换线程时 ThreadLocal **不会自动跨线程传递**，需要传上下文用 `TransmittableThreadLocal`（TTL）等方案。

## 自检

- [ ] 每个 `ThreadLocal.set()` 都有对应的 `finally { remove() }`？
- [ ] remove 在 `finally` 里（异常路径也能清）？
- [ ] 跨线程池/异步传递的上下文用了 TTL 之类方案，没指望原生 ThreadLocal 自动传？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`thread-pool-config.md`](./thread-pool-config.md)（线程复用正是泄漏前提）
- 兄弟：[`completablefuture.md`](./completablefuture.md)（异步切线程 ThreadLocal 不传递）
- 兄弟：[`lock-choice.md`](./lock-choice.md)（线程封闭 vs 加锁的取舍）
