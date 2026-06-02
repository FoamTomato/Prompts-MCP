---
name: fundamentals-jvm-index
description: JVM 工程决策四件事 — GC 选型 / 堆参数规约 / OOM 排查 / 类加载与 SPI。Use when 配置 JVM 启动参数 / 选 GC / 排查 OOM / 处理类加载冲突时。
parent: ../index.md
children:
  - { name: jvm-gc-selection, path: gc-selection.md, tag: skill, note: G1/ZGC/Parallel 何时换哪个 }
  - { name: jvm-heap-params, path: heap-params.md, tag: skill, note: "-Xmx=-Xms / 元空间 / HeapDumpOnOutOfMemoryError 必加" }
  - { name: jvm-oom-troubleshooting, path: oom-troubleshooting.md, tag: skill, note: 按 OOM 类型分流的排查决策树 }
  - { name: jvm-class-loading, path: class-loading.md, tag: skill, note: 双亲委派 / SPI 打破 / 自定义 ClassLoader }
when_to_descend: 调 JVM 参数、选 GC、线上 OOM、类加载冲突时下钻
---

# JVM · 子项索引

JVM 内功拆成四个**独立工程决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 给服务选 GC，或现有 GC 停顿/吞吐不达标想换 | [gc-selection](gc-selection.md) |
| 写 `-Xmx`/`-Xms`/元空间等堆启动参数 | [heap-params](heap-params.md) |
| 线上抛 `OutOfMemoryError`，要定位是哪种 OOM | [oom-troubleshooting](oom-troubleshooting.md) |
| 遇到 `ClassNotFound`/`NoClassDefFound`/SPI 加载不到，或要自定义 ClassLoader | [class-loading](class-loading.md) |
