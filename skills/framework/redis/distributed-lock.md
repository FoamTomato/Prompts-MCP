---
name: redis-distributed-lock
description: Redis 分布式锁 — 推荐 Redisson（看门狗自动续期），手写 SETNX 须带过期+唯一值+Lua 释放，禁用 setIfAbsent 不带过期。Use when 实现分布式锁 / 选 Redisson 还是手写 / 排查锁误删与死锁时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 分布式锁
  - 看门狗续期
  - Redisson
  - SETNX
  - Lua 释放锁
effort: high
context: inline
version: '1.0'
---
# Redis · 分布式锁

> 本条只管「跨进程互斥锁怎么做对」。缓存击穿的单 JVM 重建互斥见 [`cache-patterns.md`](./cache-patterns.md)；key 命名见 [`key-design.md`](./key-design.md)。

## 规则

| 项 | 约定 |
|----|------|
| 首选 | **Redisson** `RLock`，自带看门狗续期，避免业务没跑完锁先过期 |
| 加锁 | 必须 `SET key val NX PX ttl` 一条原子命令，禁先 set 再 expire |
| 唯一值 | value 存当前线程唯一标识（UUID），防止释放别人的锁 |
| 释放 | 用 Lua 脚本「比对 value 再 del」，保证判断+删除原子 |
| 禁用 | `setIfAbsent(k, v)` 不带过期 → 持有者宕机即死锁 |

## 正例：Redisson（推荐）

```java
RLock lock = redisson.getLock("lock:order:" + orderId);
try {
    if (lock.tryLock(3, 30, TimeUnit.SECONDS)) {   // 看门狗自动续期
        doBusiness();
    }
} finally {
    if (lock.isHeldByCurrentThread()) lock.unlock(); // 只释放自己持有的
}
```

## 正例：手写 SETNX + Lua 释放

```java
String token = UUID.randomUUID().toString();
Boolean ok = stringRedisTemplate.opsForValue()
        .setIfAbsent(key, token, Duration.ofSeconds(30)); // NX + 过期一条命令

// 释放：Lua 保证「比对 token 再删」原子
String lua = "if redis.call('get',KEYS[1])==ARGV[1] "
           + "then return redis.call('del',KEYS[1]) else return 0 end";
stringRedisTemplate.execute(new DefaultRedisScript<>(lua, Long.class),
        List.of(key), token);
```

## 反例

```java
// ❌ 不带过期：持锁线程崩了 → 锁永不释放，死锁
stringRedisTemplate.opsForValue().setIfAbsent(key, "1");

// ❌ 不比对直接 del：可能删掉已超时后别人重新加的锁
stringRedisTemplate.delete(key);
```

## 自检

- [ ] 优先用 Redisson `RLock`（看门狗续期），不是裸 SETNX？
- [ ] 加锁用带过期的原子命令（`setIfAbsent(k,v,ttl)` / `SET NX PX`）？
- [ ] value 存唯一标识，释放前比对，不误删别人的锁？
- [ ] 释放用 Lua 脚本保证「比对+删除」原子？
- [ ] 没有 `setIfAbsent(k,v)` 不带过期的写法？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`cache-patterns.md`](./cache-patterns.md)（缓存击穿的重建互斥）
- 兄弟：[`key-design.md`](./key-design.md)（锁 key 的命名与 TTL）
- 生产推荐：[`../redisson/distributed-lock.md`](../redisson/distributed-lock.md)（Redisson 看门狗续期/可重入，省掉手写 SETNX 的坑）
