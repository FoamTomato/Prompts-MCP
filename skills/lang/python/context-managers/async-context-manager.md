---
name: py-ctx-async-context-manager
description: 异步上下文管理器 async with、__aenter__/__aexit__ 与 AsyncExitStack 动态异步资源。Use when 异步资源用 async with / 自定义异步上下文管理器 / 动态管理多个异步连接。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 异步上下文管理器
  - async with
  - __aenter__
  - __aexit__
  - AsyncExitStack
effort: medium
context: inline
version: '1.0'
---
# Python · async with 与 AsyncExitStack

## 规则

| 要点 | 做法 |
|------|------|
| 异步资源 | 用 `async with`，对象实现 `__aenter__` / `__aexit__`（均为 `async def`） |
| 生成器写法 | `@contextlib.asynccontextmanager`，函数内用 `await`，`yield` 前后分别是进入/退出 |
| 何时用 | 进入/退出本身需要 `await`（建连、握手、归还连接池）时 |
| 动态多资源 | `AsyncExitStack` + `await stack.enter_async_context(cm)`，逆序异步关闭 |
| 兼容同步 cm | `AsyncExitStack` 还能 `enter_context()` 混入普通同步上下文管理器 |
| 取消安全 | `__aexit__` 内的清理也要 `await`；不要在其中吞掉 `CancelledError` |

## 正例

```python
import contextlib
from contextlib import AsyncExitStack

# 写法一：生成器，归还连接到池
@contextlib.asynccontextmanager
async def acquire(pool):
    conn = await pool.acquire()         # 进入需要 await
    try:
        yield conn
    finally:
        await pool.release(conn)        # 退出也需要 await，放 finally

async def fetch_one(pool, uid: int):
    async with acquire(pool) as conn:
        return await conn.fetchrow("SELECT * FROM users WHERE id=$1", uid)

# 写法二：AsyncExitStack 动态管理多个异步连接
async def gather_from(pools: list) -> list:
    async with AsyncExitStack() as stack:
        conns = [await stack.enter_async_context(acquire(p)) for p in pools]
        return [await c.fetchval("SELECT 1") for c in conns]
```

## 反例

```python
# ❌ 1. 异步资源用同步 with —— __aenter__ 不会被 await，拿到协程对象
with acquire(pool) as conn:             # 应为 async with
    ...

# ❌ 2. __aexit__ / finally 里漏 await —— 协程从未执行，连接泄漏
@contextlib.asynccontextmanager
async def acquire(pool):
    conn = await pool.acquire()
    try:
        yield conn
    finally:
        pool.release(conn)              # 缺 await，release 协程没跑

# ❌ 3. 多个异步资源写死嵌套 async with —— 数量可变时用 AsyncExitStack
async with acquire(p1) as c1, acquire(p2) as c2:  # 只能固定个数
    ...

# ❌ 4. 在 __aexit__ 吞掉 CancelledError —— 破坏任务取消语义
async def __aexit__(self, *exc):
    await self.close()
    return True                          # 连取消都吞了，应 return False/None
```

## 自检

- [ ] 进入/退出需要 `await` 的资源用 `async with`，不是同步 `with`？
- [ ] `__aexit__` / `finally` 内的清理都 `await` 了？
- [ ] 异步资源个数运行时才定 → 用 `AsyncExitStack`？
- [ ] 没有在 `__aexit__` 里 `return True` 吞掉异常（尤其 `CancelledError`）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`contextmanager-protocol.md`](./contextmanager-protocol.md) · [`exitstack-suppress.md`](./exitstack-suppress.md)
