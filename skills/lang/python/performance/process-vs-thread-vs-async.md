---
name: py-perf-process-vs-thread-vs-async
description: Python 并发模型选型 — CPU 密集走多进程、I/O 密集走 async、阻塞库走线程，及 free-threading 影响。Use when 选并发模型 / 绕开 GIL / CPU 与 IO 任务提速。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 并发选型
  - GIL
  - 多进程
  - multiprocessing
  - ProcessPoolExecutor
  - asyncio
effort: high
context: inline
version: '1.0'
---
# Python · 并发模型选型

这里只回答「选哪个模型」。具体 asyncio 写法见 [`../async/asyncio-pattern.md`](../async/asyncio-pattern.md)。

核心约束：CPython 默认有 GIL，**多线程跑不满多核**做 CPU 密集任务。先判断任务是 CPU 密集还是 I/O 密集。

## 规则

| 任务类型 | 选什么 | 为什么 |
|---------|-------|-------|
| CPU 密集（计算/编码/压缩） | `multiprocessing` / `ProcessPoolExecutor` | 每进程独立解释器，绕开 GIL，吃满多核 |
| I/O 密集（网络/磁盘/DB，库支持 async） | `asyncio` | 单线程协程，万级并发连接、内存开销最小 |
| I/O 密集，但只有同步阻塞库 | `ThreadPoolExecutor` / `asyncio.to_thread` | 阻塞时 GIL 释放，线程可重叠 I/O 等待 |
| 已在 async 里却要跑 CPU 重活 | `run_in_executor(ProcessPool)` | 别在事件循环里算，会卡死所有协程 |

## 正例

```python
from concurrent.futures import ProcessPoolExecutor

# CPU 密集：多进程吃满多核
def crunch(chunk: bytes) -> int:
    return sum(expensive_transform(b) for b in chunk)

with ProcessPoolExecutor() as pool:
    totals = list(pool.map(crunch, split_into_chunks(data)))
```

```python
import asyncio

# I/O 密集 + 支持 async 的客户端：协程并发
async def fetch_all(urls: list[str]) -> list[bytes]:
    async with httpx.AsyncClient() as client:
        return await asyncio.gather(*(client.get(u) for u in urls))
```

```python
# 在 async 上下文里调阻塞库：丢给线程，别阻塞事件循环
def blocking_pdf_render(doc: bytes) -> bytes: ...

async def handler(doc: bytes) -> bytes:
    return await asyncio.to_thread(blocking_pdf_render, doc)
```

## 反例

```python
# ❌ 用线程池做 CPU 密集 —— GIL 让它们串行执行，4 线程 ≈ 1 核
with ThreadPoolExecutor(max_workers=4) as pool:
    pool.map(crunch, chunks)        # 加速比接近 1，白忙

# ❌ 在事件循环里直接跑重计算 —— 阻塞期间所有协程全部停摆
async def handler(data):
    return heavy_cpu_work(data)     # 应 run_in_executor(ProcessPool)
```

理由：GIL 同一时刻只让一个线程执行 Python 字节码，CPU 密集任务用线程无加速，必须用进程。free-threading 构建（3.13 实验 / 3.14 PEP 779 官方支持）可移除 GIL 让线程真并行，但单线程性能有约 5-10% 损耗，且依赖需全部兼容 no-GIL，迁移前务必实测。

## 自检

- [ ] 先判断了 CPU 密集还是 I/O 密集，再选模型？
- [ ] CPU 密集用进程（不是线程）绕开 GIL？
- [ ] async 上下文里的阻塞调用都丢进 executor，没卡事件循环？
- [ ] 评估 free-threading 时实测过单线程损耗与依赖兼容性？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`profiling.md`](./profiling.md) · [`subinterpreters-jit.md`](./subinterpreters-jit.md)（GIL 的另一条绕行路）
- async 写法：[`../async/asyncio-pattern.md`](../async/asyncio-pattern.md)
- GIL 原理（权威）：[`../data-model/gil-and-free-threading.md`](../data-model/gil-and-free-threading.md)（为什么 CPU 密集多线程不加速、no-GIL 的影响——本条据此做选型）
