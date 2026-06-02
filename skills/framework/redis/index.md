---
name: framework-redis-index
description: Redis（Java/Spring 视角）使用约定 — 序列化/key 设计/缓存三大问题/分布式锁/缓存注解五个独立决策点。Use when 配 RedisTemplate / 设计 key / 处理缓存穿透击穿雪崩 / 加分布式锁 / 用缓存注解时。
parent: ../index.md
children:
  - { name: redis-redistemplate-usage, path: redistemplate-usage.md, tag: skill, note: RedisTemplate 序列化器显式配 String+JSON }
  - { name: redis-key-design, path: key-design.md, tag: skill, note: 冒号分层命名+必设 TTL+value 类型选型 }
  - { name: redis-cache-patterns, path: cache-patterns.md, tag: skill, note: 穿透击穿雪崩+先更 DB 再删缓存 }
  - { name: redis-distributed-lock, path: distributed-lock.md, tag: skill, note: Redisson 看门狗+手写 SETNX Lua 释放的坑 }
  - { name: redis-cache-annotation, path: cache-annotation.md, tag: skill, note: "@Cacheable/@CacheEvict + SpEL key + TTL" }
when_to_descend: 写 / 改 Java 里操作 Redis 的代码：配 template、设计 key、做缓存、加分布式锁或用 Spring Cache 注解。
---

# Redis · 框架使用约定索引

五个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 配 RedisTemplate、选序列化器、排查乱码 key | [redistemplate-usage](redistemplate-usage.md) |
| 起 key 名、设 TTL、选 String/Hash/Set/ZSet | [key-design](key-design.md) |
| 防缓存穿透/击穿/雪崩、处理缓存与 DB 一致性 | [cache-patterns](cache-patterns.md) |
| 跨进程加分布式锁（Redisson / 手写 SETNX） | [distributed-lock](distributed-lock.md) |
| 用 @Cacheable / @CacheEvict 做声明式缓存 | [cache-annotation](cache-annotation.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../spring-boot/index.md`](../spring-boot/index.md)
- 相关：[`../../lang/java/error-handling/index.md`](../../lang/java/error-handling/index.md)
