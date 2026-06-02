---
name: framework-redisson-index
description: Redisson 客户端使用约定 — 分布式锁/锁对比手写 SETNX/限流/延迟队列四个独立决策点。Use when 用 RLock 加分布式锁 / 选 Redisson 还是手写 SETNX / 做 RRateLimiter 限流 / 用 RDelayedQueue 延迟队列时。
parent: ../index.md
children:
  - { name: redisson-distributed-lock, path: distributed-lock.md, tag: skill, note: "RLock：lock() 看门狗续期 / tryLock 等待+租期 / finally unlock" }
  - { name: redisson-lock-vs-setnx, path: lock-vs-setnx.md, tag: skill, note: "对比手写 SETNX：续期/可重入/原子释放 + RedLock 争议" }
  - { name: redisson-rate-limiter, path: rate-limiter.md, tag: skill, note: "RRateLimiter 分布式限流（令牌桶）" }
  - { name: redisson-delayed-queue, path: delayed-queue.md, tag: skill, note: "RDelayedQueue 延迟队列（延迟取消/重试）" }
when_to_descend: 写 / 改 Java 里用 Redisson 客户端的代码：加分布式锁、对比手写 SETNX 选型、做限流或延迟队列。
---

# Redisson · 客户端使用约定索引

四个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 用 `RLock` 加锁，配看门狗续期 / tryLock 等待与租期 / finally 释放 | [distributed-lock](distributed-lock.md) |
| 纠结 Redisson 还是手写 SETNX，想知道 Redisson 解决了什么 + RedLock 要不要用 | [lock-vs-setnx](lock-vs-setnx.md) |
| 用 `RRateLimiter` 做跨进程限流 | [rate-limiter](rate-limiter.md) |
| 用 `RDelayedQueue` 做延迟任务（延迟取消订单 / 延迟重试） | [delayed-queue](delayed-queue.md) |

> **与 Redis 模块的分工**：[`../redis/distributed-lock.md`](../redis/distributed-lock.md) 是 **Redis 视角**（SETNX/Lua/过期命令本身怎么用对），本模块是 **Redisson 客户端视角**（RLock API、看门狗、限流器、延迟队列）。选型对比集中在 [lock-vs-setnx](lock-vs-setnx.md)。

## 链接

- 上层：[`../index.md`](../index.md)
- 相关：[`../redis/index.md`](../redis/index.md)（Redis 序列化 / key 设计 / 缓存 / Redis 视角分布式锁）
- 相关：[`../scheduling/index.md`](../scheduling/index.md)（@Scheduled 集群重复执行需分布式锁兜底）
