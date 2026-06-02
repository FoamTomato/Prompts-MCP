---
name: fundamentals-virtual-threads-index
description: JDK21 虚拟线程（Project Loom）三件事 — 何时该用/不用、pinning 陷阱、与线程池的关系。Use when 评估上虚拟线程 / 改 synchronized 防钉住 / 用 newVirtualThreadPerTaskExecutor 时。
parent: ../index.md
children:
  - { name: virtual-threads-when-to-use, path: when-to-use.md, tag: skill, note: "IO 密集一请求一虚拟线程，CPU 密集无收益" }
  - { name: virtual-threads-pinning-pitfall, path: pinning-pitfall.md, tag: skill, note: "synchronized 内阻塞钉住载体线程，改 ReentrantLock" }
  - { name: virtual-threads-vs-thread-pool, path: vs-thread-pool.md, tag: skill, note: "创建极廉价不需池化，用 newVirtualThreadPerTaskExecutor" }
when_to_descend: 在 JDK21+ 项目里评估或落地虚拟线程，需要从 Loom 原理做决策时
---

# Virtual Threads · 子项索引

> 内功定位：**原理 → 实践决策**。虚拟线程（Project Loom，JDK21 正式）是 2025-26 高频考点，但用错（CPU 密集、synchronized 钉住、误池化）反而有害。每条回答一个独立决策。

按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 评估某段逻辑/某个服务该不该上虚拟线程，IO 密集还是 CPU 密集 | [when-to-use](when-to-use.md) |
| 担心 synchronized 块里阻塞把载体线程钉住（pinning），想改 ReentrantLock | [pinning-pitfall](pinning-pitfall.md) |
| 不知道虚拟线程要不要池化、怎么建 Executor、ThreadLocal 还能不能用 | [vs-thread-pool](vs-thread-pool.md) |
