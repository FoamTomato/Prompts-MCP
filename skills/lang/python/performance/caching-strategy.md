---
name: py-perf-caching-strategy
description: Python 缓存分层 — lru_cache/cache 进程内缓存 + cached_property + Redis 跨进程分层。Use when 重复计算想缓存 / 选进程内 vs 外部缓存 / 设过期失效。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 缓存分层
  - 缓存失效
  - lru_cache
  - cached_property
  - Redis
effort: medium
context: inline
version: '1.0'
---
# Python · 缓存分层策略

缓存解决的是「重复计算 / 重复查询」。先判断数据是否可缓存（结果对相同输入稳定），再选层级。

## 规则

| 场景 | 用什么 | 理由 |
|------|-------|------|
| 纯函数、相同入参反复调用 | `@functools.lru_cache(maxsize=N)` | 进程内、有界、自动淘汰最久未用 |
| 无参全局计算（单例配置） | `@functools.cache` | 等价 `lru_cache(maxsize=None)`，无界谨慎 |
| 实例上的惰性属性 | `@functools.cached_property` | 首次访问计算，存到实例 `__dict__` |
| 跨进程 / 跨实例共享 | Redis 等外部缓存 | 多 worker / 多机共享同一份，可设 TTL |
| 多层组合 | 进程内 L1 + Redis L2 | 热数据走内存，温数据走 Redis，降库压 |

## 正例

```python
from functools import lru_cache, cached_property

@lru_cache(maxsize=1024)             # 参数必须可哈希（不可用 list/dict 入参）
def exchange_rate(base: str, quote: str) -> float:
    return _fetch_rate(base, quote)

class Report:
    def __init__(self, rows: tuple[Row, ...]) -> None:
        self.rows = rows            # 用不可变 tuple，避免 cached_property 失真

    @cached_property
    def total(self) -> int:          # 首次访问算一次，之后命中实例缓存
        return sum(r.amount for r in self.rows)
```

```python
# 跨进程分层：先查 Redis，未命中再算并回填，带 TTL 防陈旧
async def get_user_profile(uid: int) -> dict:
    key = f"profile:{uid}"
    if cached := await redis.get(key):
        return json.loads(cached)
    profile = await build_profile(uid)
    await redis.set(key, json.dumps(profile), ex=300)   # 5 分钟过期
    return profile
```

## 反例

```python
# ❌ 给「随时间变化」的结果套 lru_cache —— 数据更新后永远拿到旧值，且无 TTL
@lru_cache
def current_inventory(sku: str) -> int:
    return db_count(sku)            # 库存会变，缓存却永不失效

# ❌ 给方法用 lru_cache：self 进了缓存键，导致实例无法被 GC（内存泄漏）
class Svc:
    @lru_cache                       # 应改 cached_property，或缓存在外部
    def heavy(self, x): ...
```

理由：`lru_cache` 适用于「相同输入 → 相同输出」的纯函数，会变的数据必须有失效机制（外部缓存 + TTL）。给实例方法套 `lru_cache` 会把 `self` 锁进缓存键，造成内存泄漏，惰性属性应用 `cached_property`。

## 自检

- [ ] 缓存的是纯函数 / 稳定结果，会变的数据有 TTL 或主动失效？
- [ ] `lru_cache` 设了 `maxsize`，没用无界的 `@cache` 缓存大量入参？
- [ ] 实例惰性属性用 `cached_property`，没给方法套 `lru_cache`？
- [ ] 跨进程 / 多机共享走 Redis，没误用进程内缓存期待全局一致？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`profiling.md`](./profiling.md)（先 profile 确认重复计算是热点再加缓存） · [`process-vs-thread-vs-async.md`](./process-vs-thread-vs-async.md)
