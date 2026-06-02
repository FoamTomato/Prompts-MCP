---
name: tech-selection-cache-comparison
description: Caffeine（本地）/ Redis / Memcached 缓存对比 + 多级缓存（Caffeine L1 微秒级 + Redis L2 分布式一致）组合与失效广播。Use when 选缓存方案 / 对比本地与分布式缓存 / 设计多级缓存时。
parent: ./index.md
paths:
- '*.java'
- '*.yml'
- '*.xml'
triggers:
  keywords:
  - 缓存选型
  - 多级缓存
  - 本地缓存
  - Caffeine
  - Redis
  - Memcached
effort: medium
context: inline
version: '1.0'
---
# 缓存 · Caffeine vs Redis vs Memcached

> 本条管「缓存放哪、要不要多级」。Redis 当主存储而非缓存的边界见 [`../database/redis-as-store.md`](../database/redis-as-store.md)。
> 延迟为量级参考，落地前按真实负载压测。

## 对比

| 维度 | Caffeine（本地） | Memcached | Redis |
|---|---|---|---|
| 位置 | JVM 进程内，无网络 | 独立服务 | 独立服务 |
| 延迟 | 纳秒~微秒（最快） | 亚毫秒 | 亚毫秒 |
| 数据结构 | 任意 Java 对象 | 仅字符串 KV | 丰富（Hash/ZSet/Stream/Geo…） |
| 持久化 | 无 | 无 | 有（RDB+AOF） |
| 跨节点一致 | 无（需失效广播） | 共享一致 | 共享一致 + pub/sub |

## 怎么选

| 场景 | 选谁 |
|------|------|
| 单节点 / 可容忍节点间不一致 / 极致延迟 | 只用 Caffeine |
| 简单字符串 KV + 纯缓存 + 想多线程吃满核 | Memcached（新项目要结构化直接 Redis） |
| 需要分布式一致 + 丰富结构 | Redis |
| 既要扛热点又要分布式一致 | 多级缓存（见下） |

## 多级缓存（Caffeine L1 + Redis L2）

- **L1 Caffeine**：进程内微秒级，扛热点 key，挡住大部分请求。
- **L2 Redis**：分布式一致兜底，L1 未命中回源到它。
- **关键**：数据更新时需 **L2 → L1 失效广播**（Redis pub/sub），否则各节点 L1 脏读。
- Spring 生态常用 Caffeine + Redisson 组合。

## 反例

- ❌ 多节点服务只用 Caffeine 又要求强一致 —— 各节点本地副本不同步会脏读。
- ❌ 新项目要存结构化数据还选 Memcached —— 只有字符串 KV，应直接上 Redis。

## 自检

- [ ] 单节点还是多节点？多节点 + 需一致 → 至少 Redis，热点再叠 Caffeine。
- [ ] 上了多级缓存就配了 L1 失效广播（pub/sub）？
- [ ] 没为「只存字符串的纯缓存」过度选了重型方案？

## 相关

- 父：[`./index.md`](./index.md)
- 跨模块：[`../database/redis-as-store.md`](../database/redis-as-store.md)（Redis 当主存储 vs 缓存的边界）
