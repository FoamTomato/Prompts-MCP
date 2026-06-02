---
name: redis-cache-patterns
description: Redis 缓存三大问题 — 穿透（布隆/缓存空值）、击穿（互斥锁/逻辑过期）、雪崩（TTL 加随机/多级缓存），及缓存与 DB 一致性（先更 DB 再删缓存）。Use when 设计缓存读写 / 排查缓存击穿雪崩 / 处理缓存与库不一致时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 缓存穿透
  - 缓存击穿
  - 缓存雪崩
  - 缓存一致性
  - 布隆过滤器
  - Cache-Aside
effort: high
context: inline
version: '1.0'
---
# Redis · 缓存三大问题与一致性

> 本条只管「读多写少缓存的穿透/击穿/雪崩与一致性」。单 key 并发写互斥见 [`distributed-lock.md`](./distributed-lock.md)；TTL 命名见 [`key-design.md`](./key-design.md)。

## 规则

| 问题 | 现象 | 解法 |
|------|------|------|
| 穿透 | 查不存在的 key，每次都打 DB | 布隆过滤器拦截 / 缓存空值（短 TTL） |
| 击穿 | 单个热 key 过期瞬间大量请求压 DB | 互斥锁重建 / 逻辑过期（不真过期） |
| 雪崩 | 大批 key 同时过期，DB 被打垮 | TTL 加随机偏移 / 多级缓存 / 服务降级 |
| 一致性 | 改了 DB 缓存还是旧值 | **先更 DB 再删缓存**（Cache-Aside） |

## 正例：缓存空值防穿透

```java
String v = redisTemplate.opsForValue().get(key);
if (v != null) return "".equals(v) ? null : parse(v);   // 命中空值标记

Order o = db.find(id);
if (o == null) {
    redisTemplate.opsForValue().set(key, "", Duration.ofMinutes(2)); // 空值短 TTL
    return null;
}
redisTemplate.opsForValue().set(key, toJson(o), randomTtl());        // 加随机防雪崩
return o;
```

## 正例：TTL 加随机 + 先更 DB 再删缓存

```java
// 防雪崩：基础 30min + 0~5min 随机
Duration randomTtl() {
    return Duration.ofMinutes(30).plusSeconds(ThreadLocalRandom.current().nextInt(300));
}

// Cache-Aside 写：先落库，再删缓存（不是更新缓存）
@Transactional
public void update(Order o) {
    db.update(o);
    redisTemplate.delete("order:detail:" + o.getId());
}
```

## 反例

```java
// ❌ 先删缓存再更 DB：删后更前的读会把旧值重新写回缓存
redisTemplate.delete(key);
db.update(o);

// ❌ 所有 key 同一固定 TTL：到点集体过期 → 雪崩
redisTemplate.opsForValue().set(key, v, Duration.ofMinutes(30));
```

## 自检

- [ ] 不存在的 key 做了布隆 / 缓存空值，避免穿透？
- [ ] 热 key 重建用互斥锁或逻辑过期，避免击穿？
- [ ] TTL 加了随机偏移，避免集体过期雪崩？
- [ ] 写路径是「先更 DB 再删缓存」，不是先删缓存或更新缓存？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`distributed-lock.md`](./distributed-lock.md)（重建时的互斥锁实现）
- 兄弟：[`key-design.md`](./key-design.md)（TTL 与 value 类型）
