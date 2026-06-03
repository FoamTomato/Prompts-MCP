---
name: py-decorator-basics
description: 装饰器闭包包裹原理 + 必须用 functools.wraps 保留元数据。Use when 第一次写装饰器 / 函数 __name__ 丢失 / 评审缺 @wraps 的装饰器。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 装饰器
  - functools.wraps
  - wrapper
  - 闭包
  - __name__
effort: medium
context: inline
version: '1.0'
---
# Python · 装饰器基础与 functools.wraps

## 规则

| 要点 | 做法 |
|------|------|
| 装饰器本质 | 一个接收函数、返回新函数（`wrapper`）的高阶函数 |
| 透传参数 | `wrapper` 用 `*args, **kwargs` 接收，原样转发 |
| 透传返回值 | `wrapper` 必须 `return func(...)`，否则原函数返回值丢失 |
| **保留元数据** | `wrapper` 上**必须**加 `@functools.wraps(func)` |

`@functools.wraps(func)` 把原函数的 `__name__` / `__doc__` / `__module__` /
`__qualname__` / `__wrapped__` / `__dict__` 复制到 `wrapper`。不加 → 被装饰函数对外
表现为 `wrapper`，破坏内省、文档工具、`inspect` 与依赖名字的框架（如 FastAPI、pytest）。

## 正例

```python
import functools
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

def log_call(func: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(func)             # 必加：保留 __name__ / __doc__ / 签名
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"调用 {func.__name__}")
        return func(*args, **kwargs)   # 必须 return，透传返回值
    return wrapper

@log_call
def add(a: int, b: int) -> int:
    """返回两数之和。"""
    return a + b

assert add(1, 2) == 3
assert add.__name__ == "add"           # 因为有 @wraps
assert add.__doc__ == "返回两数之和。"
add.__wrapped__                        # @wraps 额外暴露原函数，可拿回未装饰版本
```

`@log_call` 等价于 `add = log_call(add)`。

## 反例

```python
# ❌ 1. 漏 @functools.wraps —— 元数据被覆盖
def log_call(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper                     # add.__name__ 变成 'wrapper'，__doc__ 变 None

# ❌ 2. wrapper 不转发返回值 —— 调用方永远拿到 None
def log_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)          # 缺 return
    return wrapper

# ❌ 3. wrapper 写死位置参数 —— 一旦原函数用关键字传参就 TypeError
def log_call(func):
    @functools.wraps(func)
    def wrapper(a, b):                 # 应为 *args, **kwargs
        return func(a, b)
    return wrapper
```

## 自检

- [ ] `wrapper` 上加了 `@functools.wraps(func)`？
- [ ] `wrapper` 用 `*args, **kwargs` 接收并原样转发？
- [ ] `wrapper` 内 `return func(...)`，没有吞掉返回值？
- [ ] 装饰后 `f.__name__` 仍是原名（不是 `wrapper`）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`parametrized-decorator.md`](./parametrized-decorator.md) · [`cross-cutting-patterns.md`](./cross-cutting-patterns.md)
- 闭包基础与陷阱：[`../data-model/closure-late-binding.md`](../data-model/closure-late-binding.md)（装饰器靠闭包包裹，循环里建闭包注意延迟绑定）
