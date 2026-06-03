---
name: fundamentals-index
description: 程序员内功维度（规约+决策非八股）— Java/JVM + 前端浏览器/HTTP/构建原理。Use when 做 GC 调优 / 选锁 / 排查线上问题 / 分布式决策 / 前端性能原理决策时。
parent: ../index.md
children:
  - { name: jvm, path: jvm/index.md, tag: folder, note: "GC 选型 / 堆参数 / OOM 排查 / 类加载" }
  - { name: concurrency-internals, path: concurrency-internals/index.md, tag: folder, note: "synchronized vs Lock / volatile 边界 / CAS-LongAdder / happens-before" }
  - { name: collection-internals, path: collection-internals/index.md, tag: folder, note: "HashMap 预设容量 / 并发 Map 选型 / 树化与负载因子" }
  - { name: virtual-threads, path: virtual-threads/index.md, tag: folder, note: "虚拟线程何时用 / pinning 陷阱 / 与线程池关系（JDK21）" }
  - { name: troubleshooting, path: troubleshooting/index.md, tag: folder, note: "CPU 高 / 内存泄漏 / Arthas / 排查决策树" }
  - { name: distributed-theory, path: distributed-theory/index.md, tag: folder, note: "CAP 取舍 / 分布式事务选型 / 幂等 / 分布式 ID" }
  - { name: frontend, path: frontend/index.md, tag: folder, note: "浏览器渲染 / 事件循环 / HTTP 缓存 / 跨域 / 防抖节流 / 模块化 / 构建 / 状态管理思想" }
when_to_descend: |
  Java/JVM 侧：选 GC / 调堆参数 / 排查 OOM、CPU 飙高、内存泄漏 / 选 synchronized 还是 Lock / 用不用虚拟线程 / 分布式事务与一致性方案选型 / 幂等与分布式 ID 设计。
  前端侧：碰到渲染卡顿 / 异步顺序混乱 / 缓存不更新 / 跨域报错 / 打包体积过大 / 需要理解原理做决策。
---

# Fundamentals · 程序员内功维度

> 这里是「内功」，但一律写成**规约 + 工程决策**视角——回答「该怎么选 / 该怎么设 / 出问题怎么办」，而非原理八股。
> 与 `lang/java/` 和 `framework/` 的「用法」互补：那边讲怎么写，这边讲为什么这么选、出问题怎么定位。
> 性能/量级数字为业界参考，落地需自测。

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| jvm | 文件夹 | GC 选型 / 堆参数 / OOM 排查 / 类加载（4 子项） |
| concurrency-internals | 文件夹 | 锁选型原理 / volatile 边界 / CAS-LongAdder / happens-before（4 子项） |
| collection-internals | 文件夹 | HashMap 容量 / 并发 Map 选型 / 树化（3 子项） |
| virtual-threads | 文件夹 | 虚拟线程何时用 / pinning / 与线程池（3 子项） |
| troubleshooting | 文件夹 | CPU 高 / 内存泄漏 / Arthas / 决策树（4 子项） |
| distributed-theory | 文件夹 | CAP / 分布式事务选型 / 幂等 / 分布式 ID（4 子项） |
| frontend | 文件夹 | 浏览器渲染 / 事件循环 / HTTP 缓存 / 跨域 / 防抖节流 / 模块化 / 构建 / 状态管理思想（8 子项） |

## 下钻决策表

| 你在做什么 | 进哪个 |
|-----------|-------|
| 调 GC / 设堆参数 / 排查 OOM / 理解类加载 | jvm |
| 纠结 synchronized 还是 Lock、volatile 够不够、用啥计数 | concurrency-internals |
| HashMap 要不要预设容量、并发用哪个 Map | collection-internals |
| 评估要不要上虚拟线程（JDK21） | virtual-threads |
| 线上 CPU 高 / 内存泄漏 / 接口变慢，要定位 | troubleshooting |
| 做分布式事务 / 一致性 / 幂等 / 分布式 ID 方案选型 | distributed-theory |

## 链接

- 上层：[`../index.md`](../index.md)
- 用法侧（互补）：[`../lang/java/concurrency/index.md`](../lang/java/concurrency/index.md) · [`../lang/java/collections/index.md`](../lang/java/collections/index.md) · [`../framework/mysql/index.md`](../framework/mysql/index.md) · [`../framework/seata/index.md`](../framework/seata/index.md)
- 平行维度：[`../lang/index.md`](../lang/index.md) · [`../framework/index.md`](../framework/index.md) · [`../design-pattern/index.md`](../design-pattern/index.md) · [`../habit/index.md`](../habit/index.md) · [`../tech-selection/index.md`](../tech-selection/index.md) · [`../ai/index.md`](../ai/index.md)
