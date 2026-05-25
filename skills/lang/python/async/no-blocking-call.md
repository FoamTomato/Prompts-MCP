---
name: python-no-blocking-call
description: async 函数内禁用同步阻塞 I/O — 一个阻塞调用拖死整个 event loop
parent: ./index.md
paths:
  - "backend/**/*.py"
  - "py/**/*.py"
triggers:
  keywords: [async, await, asyncio, blocking, sleep, requests]
effort: medium
context: inline
version: "1.0"
---

# Python · 禁同步阻塞调用

## 规则

`async def` 函数内**禁止任何同步阻塞 I/O**。否则一个调用就能阻塞整个 event loop，所有并发任务全卡。

## 必须替换的常见同步调用

| 同步（禁用） | 异步（必须替换为） |
|------------|---------------|
| `time.sleep(s)` | `await asyncio.sleep(s)` |
| `requests.get(url)` | `await httpx.AsyncClient().get(url)` 或 `aiohttp` |
| `redis.Redis().get(k)` | `await redis.asyncio.Redis().get(k)` |
| 同步 SQL 客户端 | Tortoise / SQLAlchemy async / asyncpg |
| `open(path).read()` 大文件 | `await aiofiles.open(path).read()` |
| `subprocess.run(cmd)` | `await asyncio.create_subprocess_exec(...)` |

## 检测方法

```bash
# 仓库内 grep 出可疑同步调用
grep -RIn --include="*.py" -E "^[^#]*\b(time\.sleep|requests\.(get|post|put|delete)|open\(.+\)\.read)\b" backend/ py/
```

CI 可以集成这一步，命中即 fail。

## 反例 → 正例

```python
# ❌ async 内调 requests（拉死 event loop）
async def fetch_textbook(tid: int):
    resp = requests.get(f"http://textbook/{tid}")  # blocking!
    return resp.json()

# ✅ 用 httpx async
async def fetch_textbook(tid: int):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"http://textbook/{tid}")
        return resp.json()
```

```python
# ❌ async 内 time.sleep
async def retry_with_backoff():
    for i in range(3):
        try:
            return await do_work()
        except Exception:
            time.sleep(2 ** i)   # blocking!

# ✅ asyncio.sleep
async def retry_with_backoff():
    for i in range(3):
        try:
            return await do_work()
        except Exception:
            await asyncio.sleep(2 ** i)
```

## 例外：CPU 密集型计算

CPU 密集型操作（图像处理、PDF 渲染、大数据处理）不算 I/O 阻塞，但仍会卡 loop。
用 `asyncio.to_thread` 或 `loop.run_in_executor` 丢到线程池：

```python
result = await asyncio.to_thread(pillow_resize, image_data, 800, 600)
```

或丢到 RQ worker（`workers/` 目录）异步处理，主路由立即返回 task_id。

## 自检

- [ ] async 函数内没有 `time.sleep` / `requests.*` / 同步 redis？
- [ ] 大文件 / CPU 密集型走 `to_thread` 或 RQ worker？
- [ ] 第三方库选了 async 版本？（httpx / redis.asyncio / aiofiles）

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`asyncio-pattern.md`](./asyncio-pattern.md) · [`sse-streaming.md`](./sse-streaming.md)
- 配套：[`../../../framework/fastapi/router/sse-streaming.md`](../../../framework/fastapi/router/sse-streaming.md)
