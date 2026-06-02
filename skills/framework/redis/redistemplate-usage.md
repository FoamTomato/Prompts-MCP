---
name: redis-redistemplate-usage
description: RedisTemplate 序列化配置 — 默认 Jdk 序列化不可读且体积大，须显式配 String + Jackson JSON 序列化器。Use when 配 RedisTemplate / 选序列化器 / 排查 Redis 乱码 key 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 序列化器
  - RedisTemplate
  - StringRedisTemplate
  - Jackson2JsonRedisSerializer
  - JdkSerialization 乱码
effort: medium
context: inline
version: '1.0'
---
# Redis · RedisTemplate 序列化配置

> 本条只管「RedisTemplate 怎么配序列化」。Key 怎么命名见 [`key-design.md`](./key-design.md)；缓存注解见 [`cache-annotation.md`](./cache-annotation.md)。

## 规则

| 项 | 配什么 | 为什么 |
|----|--------|--------|
| key / hashKey | `StringRedisSerializer` | key 在 redis-cli 里可读，不带 `\xac\xed` 前缀 |
| value / hashValue | `Jackson2JsonRedisSerializer` | JSON 可读、跨语言、体积比 JDK 小 |
| 纯字符串场景 | 直接用 `StringRedisTemplate` | 已内置 String 序列化，无需自配 |
| 默认（不配） | ❌ `JdkSerializationRedisSerializer` | 二进制不可读、体积大、改类即反序列化失败 |

## 正例：显式配置 RedisTemplate

```java
@Bean
public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory factory) {
    RedisTemplate<String, Object> t = new RedisTemplate<>();
    t.setConnectionFactory(factory);

    StringRedisSerializer keySer = new StringRedisSerializer();
    Jackson2JsonRedisSerializer<Object> valSer =
            new Jackson2JsonRedisSerializer<>(Object.class);

    t.setKeySerializer(keySer);
    t.setHashKeySerializer(keySer);
    t.setValueSerializer(valSer);
    t.setHashValueSerializer(valSer);
    t.afterPropertiesSet();
    return t;
}
```

## 正例：纯字符串用 StringRedisTemplate

```java
@Autowired StringRedisTemplate stringRedisTemplate;

// 存取都是 String，无序列化困扰
stringRedisTemplate.opsForValue().set("token:" + uid, jwt, Duration.ofHours(2));
String jwt = stringRedisTemplate.opsForValue().get("token:" + uid);
```

## 反例：用默认序列化器

```java
// ❌ 不配序列化器，key/value 全走 JDK 序列化
RedisTemplate<String, Object> t = new RedisTemplate<>();
t.setConnectionFactory(factory);
// redis-cli 里看到 "\xac\xed\x00\x05t\x00..."，无法肉眼排查
```

## 自检

- [ ] key / hashKey 用了 `StringRedisSerializer`？
- [ ] value / hashValue 用了 `Jackson2JsonRedisSerializer`（或等价 JSON）？
- [ ] 没有依赖默认的 `JdkSerializationRedisSerializer`？
- [ ] 纯字符串场景直接用 `StringRedisTemplate` 而非自配 template？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`key-design.md`](./key-design.md)（key 怎么命名 / 选 value 类型）
- 兄弟：[`cache-annotation.md`](./cache-annotation.md)（Spring Cache 注解的序列化）
