---
name: py-ctx-contextmanager-protocol
description: with 协议 __enter__/__exit__ 与 @contextmanager 生成器写法，含异常传播规则。Use when 自己写上下文管理器 / 控制 with 块的清理与异常 / 评审资源释放代码。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 上下文管理器
  - with 语句
  - contextmanager
  - __enter__
  - __exit__
effort: medium
context: inline
version: '1.0'
---
# Python · with 协议与 @contextmanager

## 规则

| 要点 | 做法 |
|------|------|
| `__enter__` | 进入 `with` 时调用，返回值绑定到 `as` 后的变量 |
| `__exit__(exc_type, exc, tb)` | 退出时调用，**无论是否异常都执行**，写清理逻辑 |
| 异常传播 | `__exit__` 返回 `True` → 吞掉异常；返回 `False`/`None` → 异常继续抛出 |
| 生成器写法 | `@contextlib.contextmanager`：`yield` 前是 enter，`yield` 后是 exit |
| 清理位置 | 生成器写法的清理必须放 `finally`，否则块内异常会跳过清理 |

默认让异常透传（`__exit__` 返回 `None`）。只有明确要消费某类异常时才返回 `True`。

## 正例

```python
import contextlib

# 写法一：类实现，完整控制异常
class managed_conn:
    def __init__(self, dsn: str) -> None:
        self.dsn = dsn

    def __enter__(self) -> "Connection":
        self.conn = connect(self.dsn)
        return self.conn                 # 绑定到 as 后的变量

    def __exit__(self, exc_type, exc, tb) -> bool:
        self.conn.close()                # 异常与否都关闭
        return False                     # 不吞异常，让它继续抛出

# 写法二：生成器，更简洁（首选）
@contextlib.contextmanager
def managed_conn(dsn: str):
    conn = connect(dsn)
    try:
        yield conn                       # yield 的值即 as 的值
    finally:
        conn.close()                     # 放 finally，异常时也清理

with managed_conn("...") as conn:
    conn.execute("SELECT 1")
```

## 反例

```python
# ❌ 1. 清理放在 yield 后但没用 try/finally —— 块内异常时连接不关
@contextlib.contextmanager
def bad_conn(dsn):
    conn = connect(dsn)
    yield conn
    conn.close()                         # with 块抛异常就永远到不了这里

# ❌ 2. __exit__ 无脑 return True —— 静默吞掉所有异常，调用方以为成功
def __exit__(self, exc_type, exc, tb):
    self.conn.close()
    return True                          # KeyError、超时全被吞，极难排查

# ❌ 3. 手动 try/finally 管理资源 —— 应交给 with
conn = connect(dsn)
try:
    conn.execute(...)
finally:
    conn.close()                         # 改用 with managed_conn(dsn)
```

## 自检

- [ ] 生成器写法的清理放在 `finally` 里？
- [ ] `__exit__` 默认 `return False`/`None` 让异常透传，没有误吞？
- [ ] 真正要清理的资源用 `with`，而不是裸 `try/finally`？
- [ ] `__enter__` / `yield` 返回了调用方需要的对象？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`exitstack-suppress.md`](./exitstack-suppress.md) · [`async-context-manager.md`](./async-context-manager.md)
