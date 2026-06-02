---
name: redis-cache-annotation
description: Spring Cache 注解 — @Cacheable/@CacheEvict/@CachePut、key 写 SpEL、condition/unless 控缓存、CacheManager 配 TTL。Use when 用注解做声明式缓存 / 写缓存 key 表达式 / 配缓存过期时间时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 声明式缓存
  - SpEL key
  - '@Cacheable'
  - '@CacheEvict'
  - CacheManager TTL
effort: medium
context: inline
version: '1.0'
---
# Redis · Spring Cache 注解

> 本条只管「注解式声明缓存」。手动 RedisTemplate 序列化见 [`redistemplate-usage.md`](./redistemplate-usage.md)；穿透/击穿/一致性见 [`cache-patterns.md`](./cache-patterns.md)。

## 规则

| 注解 | 作用 | 用在 |
|------|------|------|
| `@Cacheable` | 有缓存读缓存，无则执行并写入 | 查询方法 |
| `@CacheEvict` | 执行后删缓存（`allEntries=true` 清整 cache） | 更新 / 删除方法 |
| `@CachePut` | 总执行方法并把返回值写入缓存 | 需刷新缓存的更新 |

| 属性 | 含义 |
|------|------|
| `key` | SpEL，如 `#id` / `#user.id` / `'p:' + #id` |
| `condition` | 满足才走缓存（调用前判断），如 `#id > 0` |
| `unless` | 满足则**不**缓存（执行后判断），如 `#result == null` |

## 正例：注解用法

```java
@Cacheable(cacheNames = "order", key = "#id", unless = "#result == null")
public Order findById(Long id) { return db.find(id); }

@CacheEvict(cacheNames = "order", key = "#order.id")
public void update(Order order) { db.update(order); }
```

## 正例：CacheManager 配 TTL

```java
@Bean
public RedisCacheManager cacheManager(RedisConnectionFactory factory) {
    RedisCacheConfiguration cfg = RedisCacheConfiguration.defaultCacheConfig()
            .entryTtl(Duration.ofMinutes(30))                 // 默认 TTL，防永久驻留
            .serializeValuesWith(SerializationPair.fromSerializer(
                    new GenericJackson2JsonRedisSerializer())); // 可读 JSON
    return RedisCacheManager.builder(factory).cacheDefaults(cfg).build();
}
```

## 反例

```java
// ❌ 不配 CacheManager TTL：注解缓存默认永不过期，内存只增
@Cacheable(cacheNames = "order", key = "#id")
public Order findById(Long id) { return db.find(id); }

// ❌ key 用 #result（调用前还没结果），SpEL 解析报错
@Cacheable(cacheNames = "order", key = "#result.id")
public Order findById(Long id) { return db.find(id); }
```

## 自检

- [ ] 查询用 `@Cacheable`、改删用 `@CacheEvict`、刷新用 `@CachePut`？
- [ ] `key` 用 SpEL 引用入参（`#id`），不在调用前引用 `#result`？
- [ ] 用 `unless = "#result == null"` 避免缓存空结果？
- [ ] CacheManager 配了默认 TTL，注解缓存不会永久驻留？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`redistemplate-usage.md`](./redistemplate-usage.md)（手动操作的序列化）
- 兄弟：[`cache-patterns.md`](./cache-patterns.md)（注解外的穿透/击穿/一致性）
