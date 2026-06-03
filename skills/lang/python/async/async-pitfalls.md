---
name: py-async-async-pitfalls
description: 忘记 await、未捕获 task 异常、fire-and-forget 丢引用三类异步常见 bug。Use when 协程没执行 / 协程 never awaited 警告 / 后台任务静默消失。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 忘记await
  - fire-and-forget
  - never awaited
  - create_task
  - 任务引用
  - background task
effort: medium
context: inline
version: '1.0'
---
# Python · 异步常见陷阱

## 规则

| 陷阱 | 症状 | 修法 |
|------|------|------|
| 忘记 `await` | `RuntimeWarning: coroutine was never awaited`，逻辑没跑 | 调协程必须 `await` |
| 后台任务异常被吞 | task 内异常无人 `await` → 静默丢失 | `await` 它，或加 `add_done_callback` 记录 |
| fire-and-forget 丢引用 | task 被 GC，可能中途消失 | 持有强引用，存进集合直到完成 |
| 在循环里串行 await | 该并发的却一个个等 | 用 `gather` / `TaskGroup` 并发 |

## 正例

```python
import asyncio

# 后台任务：保留强引用 + 完成回调，否则任务可能被 GC 或异常被吞
_background: set[asyncio.Task] = set()

def spawn(coro) -> asyncio.Task:
    task = asyncio.create_task(coro)
    _background.add(task)                      # 强引用，防 GC
    task.add_done_callback(_background.discard)
    task.add_done_callback(_log_if_failed)     # 暴露异常
    return task

def _log_if_failed(task: asyncio.Task) -> None:
    if not task.cancelled() and task.exception():
        logger.error("后台任务失败", exc_info=task.exception())
```

```python
# 优先用 TaskGroup：自动持有引用、自动暴露异常，无需手动管理集合
async def run_batch(items: list) -> None:
    async with asyncio.TaskGroup() as tg:
        for it in items:
            tg.create_task(process(it))
```

## 反例

```python
# ❌ 忘记 await —— send_email() 返回 coroutine 对象但从未执行，邮件没发
async def register(user):
    await save(user)
    send_email(user)          # 漏 await！RuntimeWarning，邮件丢失

# ✅
    await send_email(user)
```

```python
# ❌ fire-and-forget 不持引用 —— task 可能被 GC，且内部异常无人知晓
asyncio.create_task(sync_to_crm(user))   # 返回值被丢弃

# ✅ 保留引用并处理结果（见上方 spawn）
task = spawn(sync_to_crm(user))
```

```python
# ❌ 该并发却串行
for url in urls:
    await fetch(url)          # 一个等一个

# ✅ 并发
await asyncio.gather(*(fetch(u) for u in urls))
```

## 自检

- [ ] 每个协程调用都加了 `await`（或显式 `create_task`）？
- [ ] 后台任务持有强引用，直到完成才释放？
- [ ] 后台任务的异常通过 `await` 或 `add_done_callback` 暴露？
- [ ] 循环内无依赖的 await 改用 `gather` / `TaskGroup`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`taskgroup-timeout.md`](./taskgroup-timeout.md) · [`cancellation-handling.md`](./cancellation-handling.md) · [`sync-bridge.md`](./sync-bridge.md)
