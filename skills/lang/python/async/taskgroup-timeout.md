---
name: py-async-taskgroup-timeout
description: asyncio.TaskGroup 结构化并发 + asyncio.timeout 取代裸 gather。Use when 并发跑多任务 / 需要一败全停 / 给一组任务设统一超时。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 结构化并发
  - TaskGroup
  - asyncio.timeout
  - gather
  - ExceptionGroup
  - 超时
effort: medium
context: inline
version: '1.0'
---
# Python · TaskGroup 结构化并发与超时

## 规则

| 场景 | 用 | 理由 |
|------|----|------|
| 多任务并发、一败全停 | `async with asyncio.TaskGroup()`（3.11+） | 任一子任务异常 → 自动取消其余 + 等待清理 |
| 给一段代码设超时 | `async with asyncio.timeout(秒)`（3.11+） | 比 `wait_for` 更易包裹多个 await |
| 收集多任务的所有错误 | TaskGroup 抛出的 `ExceptionGroup` | 失败聚合，不丢任何一个异常 |
| 需要部分失败继续 | `gather(..., return_exceptions=True)` | 这是 TaskGroup 不适用的场景 |

`gather` 默认不取消兄弟任务、错误只暴露第一个，泄漏其余任务。结构化并发优先用 TaskGroup。

## 正例

```python
import asyncio

async def assemble(uid: int) -> tuple[list, list, list]:
    async with asyncio.TaskGroup() as tg:
        t_pres = tg.create_task(list_presentations(uid))
        t_theme = tg.create_task(list_themes(uid))
        t_font = tg.create_task(list_fonts(uid))
    # 退出 with 时所有任务已完成；任一失败则整组取消并抛 ExceptionGroup
    return t_pres.result(), t_theme.result(), t_font.result()
```

```python
# 统一超时：到点自动取消组内所有 await，抛 TimeoutError
async def fetch_all(urls: list[str]) -> list[bytes]:
    results: list[bytes] = []
    async with asyncio.timeout(10):
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(fetch(u)) for u in urls]
    return [t.result() for t in tasks]
```

```python
# 聚合多个失败：用 except* 解构 ExceptionGroup（见 error-handling/exception-group）
try:
    async with asyncio.TaskGroup() as tg:
        for item in batch:
            tg.create_task(process(item))
except* ValueError as eg:
    logger.warning("部分条目校验失败: %d 个", len(eg.exceptions))
```

## 反例

```python
# ❌ 裸 gather：call_b 抛错时 call_a / call_c 不会被取消，泄漏为孤儿任务
a, b, c = await asyncio.gather(call_a(), call_b(), call_c())
# 且只有第一个异常被抛出，其余异常被静默丢弃

# ✅ TaskGroup 自动取消兄弟任务，并用 ExceptionGroup 暴露全部错误
async with asyncio.TaskGroup() as tg:
    ta, tb, tc = tg.create_task(call_a()), tg.create_task(call_b()), tg.create_task(call_c())
a, b, c = ta.result(), tb.result(), tc.result()
```

```python
# ❌ 想要一败全停，却用 return_exceptions=True 把异常变成返回值，错误被吞
results = await asyncio.gather(*coros, return_exceptions=True)
# 调用方很容易忘记逐个检查 isinstance(r, Exception)
```

## 自检

- [ ] 一败全停的并发用 `TaskGroup` 而非裸 `gather`？
- [ ] 一组任务的超时用 `async with asyncio.timeout(...)` 包裹？
- [ ] 多任务的多个异常用 `except*` 解构 `ExceptionGroup`？
- [ ] 仅在"部分失败仍要全部结果"时才用 `gather(return_exceptions=True)`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`cancellation-handling.md`](./cancellation-handling.md) · [`async-pitfalls.md`](./async-pitfalls.md) · [`asyncio-pattern.md`](./asyncio-pattern.md)
- 配套：[`../error-handling/index.md`](../error-handling/index.md)（ExceptionGroup / except*）
