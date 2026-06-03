---
name: py-err-exception-group
description: ExceptionGroup / except* 聚合并发错误 + add_note() 附加诊断信息（Py 3.11+）。Use when 处理 TaskGroup 多任务失败 / 一次抛多个异常 / 给异常加上下文备注。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 异常组
  - ExceptionGroup
  - except*
  - add_note
  - TaskGroup
  - 并发错误
effort: medium
context: inline
version: '1.0'
---
# Python · ExceptionGroup 与 except*

## 规则

| 场景 | 用什么 |
|------|--------|
| 一组并发任务可能各自失败 | `asyncio.TaskGroup` 自动把子异常打包成 `ExceptionGroup` |
| 手动同时上报多个错误 | `raise ExceptionGroup("msg", [exc1, exc2])` |
| 按类型从异常组里挑出来处理 | `except* SomeError:`（注意星号） |
| 给现有异常追加诊断说明 | `exc.add_note("...")`（Py 3.11+，不改 type/args） |

`except*` 与普通 `except` **不能混用**在同一个 try 上。每个 `except*` 块拿到的是“该类型子异常组成的子组”，未匹配的子组继续向上传播。

## 正例

```python
import asyncio

async def fetch_all(urls: list[str]) -> list[bytes]:
    async with asyncio.TaskGroup() as tg:          # 任一子任务失败 → 其余取消
        tasks = [tg.create_task(fetch(u)) for u in urls]
    return [t.result() for t in tasks]

async def main(urls: list[str]) -> None:
    try:
        await fetch_all(urls)
    except* TimeoutError as eg:                    # 只接超时类子组
        for exc in eg.exceptions:
            logger.warning("超时: %s", exc)
    except* (ConnectionError, OSError) as eg:      # 网络类子组
        logger.error("网络失败 %d 个", len(eg.exceptions), exc_info=eg)
```

`add_note` 在不丢原始异常的前提下补充定位信息：

```python
try:
    parse_config(path)
except ValueError as e:
    e.add_note(f"配置文件: {path}")               # traceback 末尾会打印这条 note
    raise                                          # 保留原异常，不重新包装
```

## 反例

```python
# ❌ 用普通 except 接 TaskGroup —— 只能拿到“第一个”，其余子异常被忽视
try:
    async with asyncio.TaskGroup() as tg:
        tg.create_task(a()); tg.create_task(b())
except Exception as e:        # e 是 ExceptionGroup，直接当单异常处理会丢信息
    handle(e)

# ❌ 把多个错误拼成字符串再抛 —— 丢类型、丢 traceback、无法分类捕获
errors = [run(x) for x in items]
if errors:
    raise RuntimeError("; ".join(str(e) for e in errors))
# ✅ 用异常组保留每个原始异常
if errors:
    raise ExceptionGroup("批处理失败", errors)
```

理由：`ExceptionGroup` 保留每个子异常的类型与 traceback，`except*` 能按类型分流；拼字符串后类型信息永久丢失，调用方无法分类处理。

## 自检

- [ ] 用 `TaskGroup` 的地方，捕获端用了 `except*` 而非普通 `except`？
- [ ] 同一个 try 没有混用 `except` 和 `except*`？
- [ ] 需要同时上报多个错误时用 `raise ExceptionGroup(...)` 而非拼字符串？
- [ ] 给异常补充上下文用 `add_note()` 而非重新包装成新异常？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`raise-from-chaining.md`](./raise-from-chaining.md) · [`eafp-vs-lbyl.md`](./eafp-vs-lbyl.md) · [`no-bare-except.md`](./no-bare-except.md)
- 配套：[`../async/asyncio-pattern.md`](../async/asyncio-pattern.md)（TaskGroup 写法）
