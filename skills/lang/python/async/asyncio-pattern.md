---
name: python-asyncio-pattern
description: asyncio 并发模式 — gather / wait / 锁 / 取消 / 超时
parent: ./index.md
paths:
  - "backend/**/*.py"
  - "py/**/*.py"
triggers:
  keywords: [asyncio, gather, wait_for, Lock, Semaphore]
effort: medium
context: inline
version: "1.0"
---

# Python · asyncio 并发模式

## 规则

| 模式 | 用法 | 何时用 |
|------|------|--------|
| `asyncio.gather(*coros)` | 并发等待多个 coroutine | 多个无依赖请求并发（如同时拉课本 + 主题 + 字体） |
| `asyncio.wait_for(coro, timeout=5)` | 单任务超时控制 | 调用外部 API / LLM 必须设超时 |
| `asyncio.Lock()` | 异步互斥锁 | 防并发写同一资源（积分扣减） |
| `asyncio.Semaphore(N)` | 并发上限 | 批量调 LLM 限流 |
| `asyncio.TaskGroup`（Py 3.11+） | 结构化并发 | 多个任务一旦有失败全取消 |

## 模板：并发拉取

```python
import asyncio

async def assemble_dashboard(uid: int) -> DashboardData:
    presentations, themes, fonts = await asyncio.gather(
        list_user_presentations(uid),
        list_user_themes(uid),
        list_user_fonts(uid),
    )
    return DashboardData(presentations=presentations, themes=themes, fonts=fonts)
```

## 模板：带超时

```python
try:
    result = await asyncio.wait_for(
        llm_call(prompt),
        timeout=30.0,
    )
except asyncio.TimeoutError:
    logger.warning(f"LLM 超时 - prompt={prompt[:50]}")
    raise ApiException(msg="生成超时，请稍后重试")
```

## 模板：批量限流

```python
sem = asyncio.Semaphore(5)  # 最多并发 5

async def generate_one(slide_idx: int):
    async with sem:
        return await llm_generate_slide(slide_idx)

results = await asyncio.gather(*(generate_one(i) for i in range(20)))
```

## 模板：分布式锁（积分扣减）

```python
locked = await redis_pool.set(f"lock:credits:{uid}", "1", ex=10, nx=True)
if not locked:
    raise ApiException(msg="操作太频繁，请稍后重试")
try:
    await deduct_credits(uid, amount)
finally:
    await redis_pool.delete(f"lock:credits:{uid}")
```

## 反例

```python
# ❌ 串行（应改 gather）
a = await call_a()
b = await call_b()  # a 和 b 无依赖
c = await call_c()

# ✅ 并发
a, b, c = await asyncio.gather(call_a(), call_b(), call_c())
```

```python
# ❌ 无超时调外部
result = await httpx.AsyncClient().get(url)  # 可能挂死整个请求

# ✅ 必带 timeout
async with httpx.AsyncClient(timeout=10) as client:
    result = await client.get(url)
```

## 自检

- [ ] 多个无依赖 await 用 `gather` 并发？
- [ ] 调外部 API / LLM 都设了超时？
- [ ] 批量请求做了 Semaphore 限流？
- [ ] 跨进程互斥用 Redis 锁，单进程用 `asyncio.Lock`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`no-blocking-call.md`](./no-blocking-call.md) · [`sse-streaming.md`](./sse-streaming.md)

