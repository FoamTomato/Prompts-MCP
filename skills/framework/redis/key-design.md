---
name: redis-key-design
description: Redis Key 命名与 value 选型 — 业务:模块:id 冒号分层、必设 TTL 防内存泄漏、避免大 key/热 key，按场景选 String/Hash/Set/ZSet。Use when 设计 Redis key / 选 value 数据结构 / 排查内存暴涨时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 键命名规范
  - 大 key
  - 热 key
  - TTL 过期
  - Hash ZSet 选型
effort: medium
context: inline
version: '1.0'
---
# Redis · Key 命名与 value 选型

> 本条只管「key 怎么起名、value 选什么结构」。序列化怎么配见 [`redistemplate-usage.md`](./redistemplate-usage.md)；缓存一致性见 [`cache-patterns.md`](./cache-patterns.md)。

## 规则

| 项 | 约定 |
|----|------|
| 命名 | `业务:模块:id` 冒号分层，如 `order:detail:1001` |
| TTL | 缓存类 key **必设过期**，禁裸 `set` 不带 TTL（内存泄漏） |
| 大 key | 单 value > 10KB / 集合元素 > 5000 要拆分，否则阻塞 |
| 热 key | 高频单 key 加本地缓存或多副本分散，避免单分片打满 |
| 可读性 | 不用中文 / 空格 / 特殊字符，全小写 + 冒号 |

## value 类型选型

| 数据形态 | 选 | 例 |
|---------|-----|----|
| 单值 / 序列化对象 | String | token、JSON 缓存 |
| 对象多字段、需局部读写 | Hash | `user:1001` 的各属性 |
| 去重集合、无序 | Set | 用户标签、抽奖池 |
| 排行 / 带分数排序 | ZSet | 排行榜 `rank:score` |

## 正例

```java
// ✅ 冒号分层 + 必带 TTL
String key = "order:detail:" + orderId;
redisTemplate.opsForValue().set(key, dto, Duration.ofMinutes(30));

// ✅ 对象多字段用 Hash，局部更新不用整存整取
redisTemplate.opsForHash().put("user:" + uid, "nickname", "tom");

// ✅ 排行榜用 ZSet
redisTemplate.opsForZSet().add("rank:weekly", uid, score);
```

## 反例

```java
// ❌ 无 TTL，永久驻留 → 内存只增不减
redisTemplate.opsForValue().set("order:detail:" + id, dto);

// ❌ 一个 key 塞整张大 list（大 key），读写阻塞主线程
redisTemplate.opsForValue().set("all:orders", hugeListOf100k);
```

## 自检

- [ ] key 用 `业务:模块:id` 冒号分层、全小写无特殊字符？
- [ ] 缓存类 key 都设了 TTL？
- [ ] 没有单 value 过大 / 集合元素过多的大 key？
- [ ] value 类型按形态选（多字段用 Hash、排序用 ZSet），而非一律 String？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`redistemplate-usage.md`](./redistemplate-usage.md)（key 的序列化器）
- 兄弟：[`cache-patterns.md`](./cache-patterns.md)（TTL 加随机防雪崩）
