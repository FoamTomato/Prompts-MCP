---
name: virtual-threads-when-to-use
description: 虚拟线程何时用何时不用 — IO 密集（调 DB/RPC/外部 API）一请求一虚拟线程收益大，CPU 密集计算无收益甚至更差。Use when 评估上虚拟线程 / 区分 IO 与 CPU 密集 / JDK21 并发选型时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 虚拟线程适用场景
  - virtual thread
  - IO 密集
  - CPU 密集
  - 一请求一线程
  - Project Loom
effort: medium
context: inline
version: '1.0'
---
# Java · 虚拟线程何时用 / 何时不用

> 本条只回答「该不该上虚拟线程」。pinning 陷阱见 [`pinning-pitfall.md`](./pinning-pitfall.md)；要不要池化、怎么建 Executor 见 [`vs-thread-pool.md`](./vs-thread-pool.md)。

## 原理 → 收益从哪来

虚拟线程（JDK21 正式）由 JVM 调度，阻塞时**自动从载体（平台）线程上卸载**，让出 OS 线程去跑别的虚拟线程。所以它的收益**只来自把"阻塞等待"的时间还给 CPU**——等待越多，收益越大。纯计算没有阻塞点可卸载，自然没有收益。

## 规则

| 工作负载 | 用不用 | 原因 |
|---------|--------|------|
| **IO 密集**：调 DB / RPC / 外部 API / 读写文件，大量阻塞等待 | ✅ 用，**一请求一虚拟线程** | 阻塞时自动卸载载体线程，可同时承载百万级并发 |
| **CPU 密集**：加解密、压缩、大量计算、纯内存运算 | ❌ 不用 | 没有阻塞点可卸载，受限于核数，反而多一层调度开销 |
| 混合型 | 拆分：IO 部分走虚拟线程，CPU 重活提交到固定大小平台线程池 | 各取所长 |

判据一句话：**这段代码大部分时间在"等"还是在"算"？等 → 虚拟线程；算 → 平台线程池（核数级别）。**

## 正例

```java
// ✅ IO 密集 Web 处理：一请求一虚拟线程，阻塞调用直接写同步代码
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (Request req : requests) {
        executor.submit(() -> {
            var user = userRpc.fetch(req.userId());   // 阻塞 RPC，自动卸载载体线程
            var order = orderDb.query(req.orderId());  // 阻塞 DB
            return assemble(user, order);
        });
    }
}
```

## 反例

```java
// ❌ 把 CPU 密集计算丢给虚拟线程 —— 无阻塞点可卸载，受限核数，徒增调度开销
Executors.newVirtualThreadPerTaskExecutor().submit(() -> {
    return heavyMatrixMultiply(bigMatrix);   // 纯计算，该用核数级平台线程池
});
```

理由：虚拟线程的全部优势是阻塞时归还载体线程，CPU 密集任务没有阻塞可归还，并发度仍受物理核数限制，还白加一层 JVM 调度成本。性能数字为量级参考，落地需自测。

## 自检

- [ ] 确认这段是 IO 密集（大量等待外部资源）才上虚拟线程？
- [ ] CPU 密集计算仍用核数级别的固定平台线程池？
- [ ] 采用"一请求一虚拟线程"模型，没有反过来限制并发数？
- [ ] 混合负载已把 CPU 重活与 IO 等待拆开？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`pinning-pitfall.md`](./pinning-pitfall.md)（用之前先确认没有 synchronized 钉住）
- 兄弟：[`vs-thread-pool.md`](./vs-thread-pool.md)（确认要用后，怎么建 Executor）
