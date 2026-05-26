---
name: python-redis-key-format
description: Redis Key 格式：[module]:[entity]:[id] + 必带 ex TTL
parent: ./index.md
paths:
- backend/**/*.py
- py/**/*.py
triggers:
  keywords:
  - Redis
  - redis_pool
  - cache_key
  - TTL
  - ex=
  - 格式
effort: medium
context: inline
version: '1.0'
---
# Python · Redis Key 格式

## 规则

| 规则 | 示例 |
|------|------|
| Key 格式 `[module]:[entity]:[id]` | `session:info:anon_abc123` |
| 必带 TTL `ex=N` | `await redis.set(k, v, ex=3600)` |
| TTL 用秒 + 命名常量 | `TTL_SESSION = 30 * 24 * 3600` |
| 值是 JSON 字符串（结构化） | `json.dumps(data, ensure_ascii=False, default=str)` |
| 用 Pipeline 批量操作 | 同一请求多个 set/get → pipeline |

## 模板：缓存查询

```python
async def get_textbook_cached(textbook_id: str, redis_pool) -> dict | None:
    cache_key = f"textbook:info:{textbook_id}"

    cached = await redis_pool.get(cache_key)
    if cached:
        return json.loads(cached)

    record = await Textbook.filter(id=textbook_id).first()
    if not record:
        return None

    data = await TextbookAdapter.to_dict(record)
    await redis_pool.set(
        cache_key,
        json.dumps(data, ensure_ascii=False, default=str),
        ex=TTL_TEXTBOOK,  # 24h
    )
    return data
```

## 模板：进度追踪

```python
TTL_PROGRESS = 10 * 60  # 10 分钟

await redis_pool.set(
    f"progress:{task_id}",
    json.dumps({"step": current_step, "total": total_steps, "msg": "渲染中"}),
    ex=TTL_PROGRESS,
)
```

## 模板：分布式锁

```python
TTL_LOCK = 5 * 60  # 5 分钟

locked = await redis_pool.set(
    f"lock:credits:{user_id}",
    "1",
    ex=TTL_LOCK,
    nx=True,
)
if not locked:
    raise ApiException(msg="操作太频繁")
try:
    ...
finally:
    await redis_pool.delete(f"lock:credits:{user_id}")
```

## 反例

```python
# ❌ 不带 TTL — 内存泄漏
await redis.set(k, v)

# ❌ 拼接 Key 不规范
await redis.set(f"user_{uid}_data", v)  # → user:data:{uid}

# ❌ 直接存 Python 对象（pickle）
await redis.set(k, pickle.dumps(obj))   # 跨语言 / 跨版本灾难

# ❌ TTL 用魔法数字
await redis.set(k, v, ex=3600)   # 3600 是什么？→ TTL_SESSION_HOUR
```

## TTL 推荐表

| 场景 | TTL |
|------|-----|
| Session 长期 | 30 天 |
| 用户信息缓存 | 1 小时 |
| 课本元数据 | 24 小时 |
| 任务进度 | 10 分钟 |
| 分布式锁 | ≤ 5 分钟 |
| 验证码 / SMS | 5 分钟 |
| Rate Limit window | ≤ 1 小时 |

## 自检

- [ ] 所有 `set` 带 `ex=`？
- [ ] Key 格式 `[module]:[entity]:[id]`？
- [ ] TTL 用命名常量？
- [ ] 值是 JSON 字符串而非 pickle？

## 相关

- 父：[`./index.md`](./index.md)

