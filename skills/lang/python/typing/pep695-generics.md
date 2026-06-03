---
name: py-typing-pep695-generics
description: PEP 695 新泛型语法 def f[T] / class C[T] / type Alias，取代 TypeVar/Generic 样板。Use when 写泛型函数或容器类 / 定义类型别名 / 评审 TypeVar 旧写法。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 泛型
  - PEP 695
  - type parameter
  - TypeVar
  - bound
effort: medium
context: inline
version: '1.0'
---
# Python · PEP 695 新泛型语法

## 规则

Python 3.12+ 写泛型用**内联类型参数** `def f[T]` / `class C[T]` / `type X = ...`，不再手写 `TypeVar` + `Generic` 样板。类型参数作用域自动绑定到该函数/类，无需模块级声明。

| 旧写法（3.11-） | 新写法（3.12+） |
|------|------|
| `T = TypeVar("T")` + `def f(x: T) -> T` | `def f[T](x: T) -> T` |
| `class Box(Generic[T])` | `class Box[T]` |
| `T = TypeVar("T", bound=Base)` | `def f[T: Base]()` |
| `T = TypeVar("T", int, str)` | `def f[T: (int, str)]()` |
| `MyAlias = list[int]` | `type MyAlias = list[int]` |

## 正例

```python
# 泛型函数：返回类型跟随入参
def first[T](items: list[T]) -> T:
    return items[0]

# 上界约束：T 必须是 BaseModel 子类
def parse[T: BaseModel](model: type[T], raw: dict) -> T:
    return model.model_validate(raw)

# 泛型类：无需继承 Generic
class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

# 类型别名：type 语句惰性求值，可前向引用
type Vector = list[float]
type Tree[T] = T | list["Tree[T]"]
```

## 反例

```python
# ❌ 3.12+ 还手写 TypeVar 样板
from typing import TypeVar, Generic
T = TypeVar("T")
class Box(Generic[T]):  # → class Box[T]
    ...

# ❌ 用旧 TypeAlias 注解而非 type 语句
from typing import TypeAlias
Vector: TypeAlias = list[float]   # → type Vector = list[float]

# ❌ 把 type 参数泄漏成模块级名字
T = TypeVar("T")          # 多余的全局污染
def first(items: list[T]) -> T: ...   # → def first[T](...)
```

PEP 695 的 `T` 是函数/类的**局部**参数，不在模块命名空间，避免多个无关泛型共用一个 `TypeVar` 的隐式耦合。

## 自检

- [ ] 目标运行时 ≥3.12？用内联 `def f[T]` / `class C[T]`？
- [ ] 类型别名用 `type X = ...` 而非裸赋值或 `TypeAlias`？
- [ ] 上界写 `[T: Base]`、约束集写 `[T: (int, str)]`？
- [ ] 没有残留的模块级 `TypeVar(...)` 样板？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`protocol-structural.md`](./protocol-structural.md) · [`deferred-annotations.md`](./deferred-annotations.md)
