---
name: py-decorator-parametrized
description: 带参装饰器的三层嵌套写法、类实现装饰器、以及多个装饰器叠加顺序。Use when 写 @retry(times=3) 这类带参装饰器 / 用类实现装饰器 / 多个装饰器叠加。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 带参装饰器
  - 三层嵌套
  - 类装饰器
  - 叠加顺序
  - decorator factory
  - __call__
effort: medium
context: inline
version: '1.0'
---
# Python · 带参装饰器与叠加顺序

## 规则

| 场景 | 结构 |
|------|------|
| 装饰器带参数 `@retry(times=3)` | **三层**：参数层 → 接收 func 层 → `wrapper` 层 |
| 用类实现装饰器 | `__init__` 存配置，`__call__` 接收 func 返回 `wrapper` |
| 多个装饰器叠加 | **自下而上**包裹、**自上而下**执行（最靠近 def 的最先包裹） |

带参装饰器 = 装饰器工厂：`@retry(times=3)` 先**调用** `retry(times=3)` 得到真正的
装饰器，再用它装饰函数。每层 wrapper 都要 `functools.wraps`。

## 正例：三层嵌套

```python
import functools
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

def retry(times: int = 3) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == times:
                        raise
        return wrapper
    return decorator

@retry(times=3)                  # 等价 fetch = retry(times=3)(fetch)
def fetch(url: str) -> bytes: ...
```

## 正例：类装饰器

```python
class CountCalls:
    def __init__(self, func: Callable) -> None:
        functools.update_wrapper(self, func)   # 类形态用 update_wrapper
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)

@CountCalls
def ping() -> str: ...
```

## 正例：叠加顺序

```python
@timer        # 后包裹 → 最外层 → 最先进入
@retry(3)     # 先包裹 → 内层
def task(): ...

# 等价：task = timer(retry(3)(task))
# 执行进入顺序：timer → retry → task；返回时反向
```

把横切关注点按“最外层最先生效”排列：日志/计时通常在最外，缓存/重试在内。

## 反例

```python
# ❌ 1. 带参装饰器漏掉一层，直接把参数当 func
def retry(func):                 # 这样 @retry(times=3) 会把 3 当 func 传入
    ...

# ❌ 2. 误以为执行顺序是自下而上（实际最外层最先进入）
@cache
@timer                           # 想计时含 cache 命中？错：timer 在 cache 内层
def f(): ...                     # cache 命中时根本不进入 timer

# ❌ 3. 类装饰器忘了 update_wrapper —— 实例没有 __name__ / __doc__
class CountCalls:
    def __init__(self, func): self.func = func
```

## 自检

- [ ] 带参装饰器是三层（工厂 → decorator → wrapper），不是两层？
- [ ] 每层 `wrapper` 都有 `functools.wraps` / 类用 `update_wrapper`？
- [ ] 多个装饰器的叠加顺序符合“最外层最先进入”预期？
- [ ] 类装饰器的 `__call__` 透传 `*args, **kwargs` 与返回值？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`decorator-basics.md`](./decorator-basics.md) · [`cross-cutting-patterns.md`](./cross-cutting-patterns.md)
