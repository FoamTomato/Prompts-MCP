---
name: py-async-sync-bridge
description: asyncio.to_thread / run_in_executor 把同步阻塞代码桥接进事件循环。Use when async 内要调同步库 / CPU 密集计算 / 没有 async 版本的第三方 SDK。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 同步桥接
  - to_thread
  - run_in_executor
  - ProcessPoolExecutor
  - 线程池
  - blocking
effort: medium
context: inline
version: '1.0'
---
# Python · 同步代码桥接到异步

## 规则

| 阻塞类型 | 用 | 说明 |
|---------|----|------|
| 同步 I/O / 无 async 版的 SDK | `await asyncio.to_thread(fn, *args)`（3.9+） | 丢到默认线程池，释放事件循环 |
| 需要自定义线程池 | `loop.run_in_executor(pool, fn, *args)` | 控制并发数；只接受位置参数 |
| CPU 密集（GIL 限制） | `run_in_executor(ProcessPoolExecutor(), fn)` | 线程救不了 CPU 密集，必须用进程池 |
| 反向：同步代码里跑协程 | `asyncio.run(coro)` / `asyncio.run_coroutine_threadsafe` | 入口或跨线程提交 |

线程池只解决"阻塞 I/O 不卡 loop"；CPU 密集受 GIL 限制要用进程池或交给后台 worker。

## 正例

```python
import asyncio

# 同步阻塞库（如老式 SDK），无 async 版本
async def render_pdf(html: str) -> bytes:
    return await asyncio.to_thread(blocking_pdf_render, html)
```

```python
# 自定义线程池控制并发；run_in_executor 只收位置参数，关键字参数用 partial
from functools import partial
from concurrent.futures import ThreadPoolExecutor

pool = ThreadPoolExecutor(max_workers=4)

async def query_legacy(sql: str, *, timeout: int) -> list:
    loop = asyncio.get_running_loop()
    fn = partial(legacy_db.execute, sql, timeout=timeout)
    return await loop.run_in_executor(pool, fn)
```

```python
# CPU 密集：线程被 GIL 锁死，必须用进程池
from concurrent.futures import ProcessPoolExecutor

async def crunch(data: bytes) -> int:
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as pool:
        return await loop.run_in_executor(pool, heavy_compute, data)
```

## 反例

```python
# ❌ async 内直接调同步阻塞库 —— 整个 event loop 卡住，所有并发任务停摆
async def render(html: str) -> bytes:
    return blocking_pdf_render(html)  # 阻塞！应 await asyncio.to_thread(...)

# ❌ CPU 密集丢线程池 —— GIL 让多线程串行，毫无加速
async def crunch(data: bytes) -> int:
    return await asyncio.to_thread(heavy_compute, data)  # 应用 ProcessPoolExecutor

# ❌ run_in_executor 直接传关键字参数 —— TypeError，要用 functools.partial 包
await loop.run_in_executor(pool, legacy_db.execute, sql, timeout=5)
```

## 自检

- [ ] async 内的同步阻塞调用都包了 `to_thread` / `run_in_executor`？
- [ ] CPU 密集任务用了 `ProcessPoolExecutor` 而非线程池？
- [ ] `run_in_executor` 的关键字参数用 `functools.partial` 处理？
- [ ] 长任务考虑交给后台 worker，而非占用请求线程？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`no-blocking-call.md`](./no-blocking-call.md) · [`async-pitfalls.md`](./async-pitfalls.md) · [`taskgroup-timeout.md`](./taskgroup-timeout.md)
