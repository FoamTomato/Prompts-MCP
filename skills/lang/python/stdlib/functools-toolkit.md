---
name: py-stdlib-functools-toolkit
description: functools 高阶工具 — lru_cache / cache / partial / wraps / singledispatch / cached_property。Use when 缓存纯函数 / 固定参数 / 写装饰器 / 按类型分派 / 惰性属性。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 函数缓存
  - 单分派
  - lru_cache
  - partial
  - wraps
  - cached_property
effort: medium
context: inline
version: '1.0'
---
# Python · functools 高阶工具

## 规则

| 工具 | 用途 | 注意 |
|------|------|------|
| `@cache` / `@lru_cache(maxsize=N)` | 缓存纯函数结果 | 参数须可哈希；勿用于有副作用/会变的数据 |
| `partial(fn, *a, **kw)` | 预绑定部分参数 | 比 lambda 更易内省、可 pickle |
| `@wraps(fn)` | 装饰器内保留原函数元数据 | 不加则 `__name__`/`__doc__` 丢失 |
| `@singledispatch` | 按首参类型分派实现 | 替代 isinstance 长链 |
| `@cached_property` | 实例级惰性缓存属性 | 实例须可写 `__dict__`（非 slots） |

## 正例

```python
from functools import cache, lru_cache, partial, wraps, singledispatch, cached_property

@lru_cache(maxsize=256)
def fib(n: int) -> int:               # 纯函数，幂等，适合缓存
    return n if n < 2 else fib(n - 1) + fib(n - 2)

# partial 预绑定：固定 base 参数
to_hex = partial(int, base=16)
assert to_hex("ff") == 255

# 自定义装饰器必须 @wraps
def timed(fn):
    @wraps(fn)                        # 保留 fn.__name__ / __doc__
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            log.info("%s took %.3fs", fn.__name__, time.perf_counter() - start)
    return wrapper

# 按类型分派
@singledispatch
def render(value) -> str:
    return str(value)

@render.register
def _(value: list) -> str:
    return ", ".join(render(v) for v in value)

# 惰性属性：首次访问才算，之后缓存
class Dataset:
    @cached_property
    def stats(self) -> dict:
        return expensive_scan(self.rows)
```

## 反例

```python
# ❌ 缓存接收可变参数 / 有副作用的函数
@cache
def load_user(ids: list[int]):        # list 不可哈希 -> TypeError
    ...

# ❌ 缓存随时间变化的结果，返回陈旧数据
@cache
def now_price(sku): return db_price(sku)   # 价格会变，缓存即 bug

# ❌ 自定义装饰器忘记 @wraps，元数据丢失
def timed(fn):
    def wrapper(*a, **kw): return fn(*a, **kw)
    return wrapper                    # wrapper.__name__ == "wrapper"
```

理由：`lru_cache` 只适合**纯函数 + 可哈希参数**；`@wraps` 是装饰器正确性的硬约束；`singledispatch` 让类型分支可扩展，胜过 isinstance 长链。

## 自检

- [ ] `lru_cache`/`cache` 只用在纯函数、参数可哈希、结果不随时间变？
- [ ] 自定义装饰器都加了 `@wraps`？
- [ ] 固定参数用 `partial` 而非裸 lambda？
- [ ] 类型分支用 `singledispatch` 而非 isinstance 长链？
- [ ] 惰性属性用 `cached_property`（且类未用 slots 禁掉 `__dict__`）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`itertools-pipeline.md`](./itertools-pipeline.md) · [`dataclasses-usage.md`](./dataclasses-usage.md)
- 缓存选型（权威）：[`../performance/caching-strategy.md`](../performance/caching-strategy.md)（lru_cache 进程内 vs Redis 跨进程的分层决策）
- wraps 怎么用（权威）：[`../decorators/decorator-basics.md`](../decorators/decorator-basics.md)（写装饰器时 functools.wraps 的必要性）
