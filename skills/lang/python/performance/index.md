---
name: lang-python-performance-index
description: Python 性能与并发优化（profiling / 缓存分层 / 并发模型选型 / 子解释器与 JIT 前沿）。Use when 优化热点 / 选并发模型 / 加缓存 / 评估 free-threading。
parent: ../index.md
children:
  - { name: profiling, path: profiling.md, tag: skill, note: 先测后优 cProfile/py-spy/timeit/memray }
  - { name: caching-strategy, path: caching-strategy.md, tag: skill, note: lru_cache 进程内 + Redis 分层 }
  - { name: process-vs-thread-vs-async, path: process-vs-thread-vs-async.md, tag: skill, note: CPU/IO 选进程/线程/async }
  - { name: subinterpreters-jit, path: subinterpreters-jit.md, tag: skill, note: "子解释器 PEP 734 / JIT PEP 744 前沿" }
when_to_descend: 优化慢代码 / 选并发模型 / 加缓存 / 评估 3.13+ 新运行时特性
---

# Python · 性能与并发优化

> 进阶维度：先量化、再选型、最后才上前沿特性。不要凭直觉优化。

## 下钻决策表

| 你在做什么 | 进哪个 |
|-----------|-------|
| 代码慢但不知慢在哪 | profiling |
| 重复计算 / 重复查库想加缓存 | caching-strategy |
| CPU 密集 vs I/O 密集选并发模型 | process-vs-thread-vs-async |
| 评估 3.13/3.14 子解释器、JIT、free-threading | subinterpreters-jit |

## 链接

- 上层：[`../index.md`](../index.md)
- 关联：[`../async/asyncio-pattern.md`](../async/asyncio-pattern.md)（async 写法，本模块讲选型）
