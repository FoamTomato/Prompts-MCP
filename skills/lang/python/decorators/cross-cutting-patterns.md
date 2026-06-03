---
name: py-decorator-cross-cutting
description: 用装饰器实现重试 / 限流 / 计时 / 缓存等横切关注点的实战模板。Use when 给函数加重试 / 限流节流 / 耗时统计 / 结果缓存等横切逻辑。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 横切关注点
  - 重试
  - 限流
  - 计时
  - 缓存
  - retry
  - cross-cutting
effort: medium
context: inline
version: '1.0'
---
# Python · 装饰器横切关注点实战

## 规则

把**跨多个函数复用、与业务无关**的逻辑（重试 / 限流 / 计时 / 缓存）抽成装饰器，而非抄进每个函数体；各模板都遵循 [`decorator-basics`](./decorator-basics.md) 与 [`parametrized-decorator`](./parametrized-decorator.md) 的规则。

| 关注点 | 首选 | 何时自己写 |
|--------|------|-----------|
| 缓存 | 标准库 `functools.lru_cache` / `cache` | 需 TTL / 外部缓存才自写 |
| 计时 | 自写 `timer` | — |
| 重试 | `tenacity` 库 | 简单场景可自写 |
| 限流 | 自写 token/时间窗 | 分布式限流用 Redis |

## 正例：计时

```python
import functools, time, logging

logger = logging.getLogger(__name__)

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()        # 计时用 perf_counter，非 time.time
        try:
            return func(*args, **kwargs)
        finally:
            cost = (time.perf_counter() - start) * 1000
            logger.info("%s 耗时 %.1f ms", func.__name__, cost)
    return wrapper
```

## 正例：缓存（优先标准库）

```python
@functools.lru_cache(maxsize=256)          # 参数须可哈希；有副作用的函数勿缓存
def query_config(key: str) -> str: ...
```

## 正例：重试（带参，指数退避）

```python
def retry(times: int = 3, backoff: float = 0.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except (TimeoutError, ConnectionError) as e:   # 只重试可恢复异常
                    if attempt == times:
                        raise
                    logger.warning("%s 第 %d 次失败: %s", func.__name__, attempt, e)
                    time.sleep(backoff * 2 ** (attempt - 1))
        return wrapper
    return decorator
```

## 正例：限流（固定窗口，进程内单实例；分布式用 Redis 计数）

```python
def rate_limit(max_calls: int, period: float):
    calls: list[float] = []
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.monotonic()
            calls[:] = [t for t in calls if now - t < period]   # 淘汰过期
            if len(calls) >= max_calls:
                raise RuntimeError("rate limit exceeded")
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

## 反例

```python
except Exception:                  # ❌ 重试抓所有异常，连 ValueError / 业务错误也无脑重试

@functools.lru_cache               # ❌ 缓存有副作用的函数：第二次调用静默跳过写库 / 发请求
def create_order(uid): ...

# ❌ 自造缓存装饰器却没上限 —— 内存无限增长（标准库用 lru_cache(maxsize=...)）
```

## 自检

- [ ] 横切逻辑抽成了装饰器，没在每个函数里抄一遍？
- [ ] 缓存优先用 `functools.lru_cache` / `cache`，自写的有容量上限？
- [ ] 重试只捕获可恢复异常（超时 / 连接），不是 `except Exception`？
- [ ] 缓存只用于纯函数，没缓存带副作用的调用？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`decorator-basics.md`](./decorator-basics.md) · [`parametrized-decorator.md`](./parametrized-decorator.md)
- 缓存选型（权威）：[`../performance/caching-strategy.md`](../performance/caching-strategy.md)（本条给「缓存装饰器」写法，选 lru_cache 还是 Redis 分层看这条）
