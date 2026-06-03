---
name: py-typing-type-narrowing
description: TypeGuard/TypeIs 自定义窄化、Self 返回自身、assert_never 穷尽、Never/NoReturn。Use when 写类型守卫函数 / 链式方法返回 Self / 校验分支穷尽。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 类型窄化
  - TypeGuard
  - TypeIs
  - Self
  - assert_never
effort: medium
context: inline
version: '1.0'
---
# Python · 类型窄化

## 规则

| 工具 | 用途 |
|------|------|
| `TypeIs[T]` | 自定义守卫（3.13+），两个分支都窄化（True→T，False→排除 T），优先选它 |
| `TypeGuard[T]` | 自定义守卫，仅 True 分支窄化；返回类型与入参无子类关系时用 |
| `Self` | 方法返回自身实例类型，链式调用/工厂正确推导子类 |
| `assert_never(x)` | 穷尽检查：漏处理某分支时静态报错 |
| `Never` / `NoReturn` | 永不返回（抛异常/死循环）的函数返回类型 |

## 正例

```python
from typing import TypeIs, Self, assert_never, Never, Literal

# TypeIs：True/False 两侧都窄化
def is_str(v: object) -> TypeIs[str]:
    return isinstance(v, str)

def show(v: int | str) -> str:
    if is_str(v):
        return v.upper()    # 这里 v: str
    return hex(v)           # 这里 v: int（已排除 str）

# Self：子类链式调用返回子类型，不被钉死成父类
class Query:
    def where(self, cond: str) -> Self:
        ...
        return self

# assert_never：新增 Literal 分支忘了处理时静态报错
Mode = Literal["r", "w", "a"]

def handle(mode: Mode) -> str:
    if mode == "r": return "read"
    if mode == "w": return "write"
    if mode == "a": return "append"
    assert_never(mode)   # 加了 "x" 但漏分支 → 类型检查失败

# NoReturn：明确"必然抛出"
def fail(msg: str) -> Never:
    raise RuntimeError(msg)
```

## 反例

```python
# ❌ 守卫函数返回裸 bool——调用处不会窄化
def is_str(v: object) -> bool:   # → TypeIs[str]
    return isinstance(v, str)

# ❌ 链式方法硬编码父类，子类调用后类型丢失
class Query:
    def where(self, c: str) -> "Query": ...   # 子类返回也被当 Query → Self

# ❌ 手写 else raise 兜底，新增分支不报错
def handle(mode: Mode) -> str:
    if mode == "r": return "read"
    else: raise ValueError   # 漏 "w"/"a" 静默通过 → assert_never
```

`TypeIs` 与 `TypeGuard` 区别：`TypeIs` 要求返回类型是入参的子类型，能让 False 分支也窄化（更接近 `isinstance`）；跨类型转换的守卫仍用 `TypeGuard`。

## 自检

- [ ] 守卫函数返回 `TypeIs[T]` / `TypeGuard[T]` 而非裸 `bool`？
- [ ] 同子类窄化优先 `TypeIs`，仅 True 分支才需 `TypeGuard`？
- [ ] 链式/工厂方法返回 `Self`？
- [ ] `Literal`/枚举分发结尾 `assert_never` 保证穷尽？
- [ ] 必抛函数标 `Never` / `NoReturn`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`protocol-structural.md`](./protocol-structural.md) · [`typeddict-literal.md`](./typeddict-literal.md)
