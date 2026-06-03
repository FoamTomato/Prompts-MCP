---
name: py-async-cancellation-handling
description: CancelledError 正确传播、asyncio.shield 保护、cleanup。Use when 写取消逻辑 / except 误吞 CancelledError / 关键收尾需防被取消。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 取消传播
  - CancelledError
  - shield
  - cleanup
  - task.cancel
  - 收尾清理
effort: medium
context: inline
version: '1.0'
---
# Python · 取消传播与清理

## 规则

| 约束 | 做法 |
|------|------|
| `CancelledError` 必须重抛 | 在 `except` 里清理后用 `raise` 把它传播出去 |
| 不能被宽 except 吞掉 | 3.8+ 它继承 `BaseException`，但 `except Exception` 加 `CancelledError` 仍要警惕 |
| 收尾代码放 `finally` | `finally` 在取消时仍执行，是清理资源的唯一可靠位置 |
| 不可中断的关键段 | 用 `asyncio.shield(coro)` 保护，使其不被外层取消打断 |
| 清理里再 await | 可能再次抛 `CancelledError`；保持清理简短、幂等 |

## 正例

```python
import asyncio

async def worker(conn):
    try:
        await long_running_io(conn)
    except asyncio.CancelledError:
        logger.info("worker 被取消，回滚中")
        await conn.rollback()      # 清理
        raise                      # 关键：必须重抛，让取消继续传播
    finally:
        await conn.close()         # 取消/正常都会执行
```

```python
# shield：保护"已扣费必须落账"这类关键收尾不被取消打断
async def charge_and_commit(uid: int):
    await deduct_credits(uid, 1)
    # 即使外层超时/取消，commit 也要跑完，避免扣了费却没落账
    await asyncio.shield(commit_charge(uid))
```

```python
# 主动取消子任务后，await 它以触发清理并吞掉预期的 CancelledError
task = asyncio.create_task(stream())
task.cancel()
try:
    await task
except asyncio.CancelledError:
    pass  # 这是我们主动取消、预期内的，可吞
```

## 反例

```python
# ❌ 把 CancelledError 当普通异常吞掉 —— 任务"取消不掉"，TaskGroup/timeout 失效
async def worker():
    try:
        await long_io()
    except asyncio.CancelledError:
        logger.error("出错了")
        return  # 没 raise，取消被吃掉，协程继续，破坏结构化并发

# ❌ except Exception 顺带吞了取消（3.8+ CancelledError 不再是 Exception，
#    但混用宽捕获仍易出错）—— 清理后务必单独处理并重抛
try:
    await coro()
except Exception:
    handle()        # 这里捕不到 CancelledError，但下面这种会出事
except BaseException:
    pass            # ❌ 把取消也吞了
```

## 自检

- [ ] 每个 `except asyncio.CancelledError` 清理后都 `raise`？
- [ ] 资源关闭放在 `finally`，而非仅在正常路径？
- [ ] 必须跑完的关键收尾用 `asyncio.shield` 保护？
- [ ] 清理里的 `await` 简短、幂等，不会卡死取消？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`taskgroup-timeout.md`](./taskgroup-timeout.md) · [`async-pitfalls.md`](./async-pitfalls.md) · [`asyncio-pattern.md`](./asyncio-pattern.md)
