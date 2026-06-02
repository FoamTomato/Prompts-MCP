---
name: redisson-lock-vs-setnx
description: Redisson 锁 vs 手写 SETNX 选型 — Redisson 解决续期/可重入/原子释放三大痛点，生产推荐；RedLock 多节点方案争议大，单点 Redisson 多数场景够用。Use when 纠结用 Redisson 还是手写 SETNX / 要不要上 RedLock 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 锁选型
  - 手写 SETNX
  - Redisson
  - RedLock
  - 可重入锁
effort: medium
context: inline
version: '1.0'
---
# Redisson · 锁选型（vs 手写 SETNX / RedLock）

> 本条只管「该用 Redisson 还是手写 SETNX，要不要 RedLock」这个决策。RLock 的 API 怎么写见 [`distributed-lock.md`](./distributed-lock.md)；SETNX/Lua 命令本身怎么写对见 [`../redis/distributed-lock.md`](../redis/distributed-lock.md)。

## 规则

| 痛点 | 手写 SETNX | Redisson `RLock` |
|------|-----------|------------------|
| 续期 | 锁过期但业务没跑完 → 锁提前丢，需自己起线程续 | **看门狗自动续期**，开箱即用 |
| 可重入 | 同线程二次加锁会死锁，要自己计数 | **天然可重入**（Hash 记 threadId+次数） |
| 原子释放 | 必须手写「比对 value 再 del」的 Lua，写错就误删 | `unlock()` 内部已是原子 Lua，封装好 |
| 阻塞等待/唤醒 | 只能 sleep 轮询，浪费且不及时 | 基于 pub/sub 的等待唤醒，效率高 |
| 结论 | 仅学习/极简场景 | **生产推荐**：成熟、踩坑少 |

## RedLock（多节点）—— 默认不用

| 项 | 说明 |
|----|------|
| 是什么 | 在 N 个**独立** Redis 主节点上各加锁，多数成功才算持锁，提升单点故障下的安全性 |
| 争议 | Martin Kleppmann 质疑其在 GC 停顿/时钟漂移下的安全性，业界长期争论，无定论 |
| 取舍 | **多数业务单点 / 主从 Redisson 已足够**；锁只是「优化」而非「正确性唯一保障」时不必上 RedLock |
| 真要强一致 | 别赌 Redis 锁，用 DB 唯一键 / 乐观锁 / Fencing Token 等手段兜底 |

> 性能/数字为业界量级参考，落地需自测。

## 正例：直接用 Redisson，不重复造轮子

```java
// ✅ 续期、可重入、原子释放都由 Redisson 兜底，业务只关心加锁/解锁
RLock lock = redisson.getLock("lock:stock:" + skuId);
lock.lock();
try {
    deductStock(skuId);
} finally {
    lock.unlock();
}
```

## 反例

```java
// ❌ 手写 SETNX 没续期：业务 40s，锁 30s 过期 → 临界区被两个线程同时进
String token = UUID.randomUUID().toString();
redis.opsForValue().setIfAbsent(key, token, Duration.ofSeconds(30));
slowBusiness();      // 跑了 40s，第 30s 锁已自动过期

// ❌ 默认就上 RedLock：增加 N 个节点的运维与延迟，多数场景收益为负
```

## 自检

- [ ] 生产代码用 Redisson `RLock`，而不是自己手写 SETNX + 续期线程？
- [ ] 没有为了「更安全」盲目上 RedLock（已确认单点/主从 Redisson 满足需求）？
- [ ] 对正确性要求强一致的场景，另有 DB 唯一键 / 乐观锁兜底，没把 Redis 锁当唯一保障？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`distributed-lock.md`](./distributed-lock.md)（选定 Redisson 后 RLock 怎么写）
- 相关：[`../redis/distributed-lock.md`](../redis/distributed-lock.md)（真要手写 SETNX 时的 Lua 释放写法）
