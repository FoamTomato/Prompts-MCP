---
name: py-typing-typeddict-literal
description: TypedDict/NotRequired/Required、Literal、Final、NewType、overload 精确建模字典与常量。Use when 给 JSON/kwargs 字典加类型 / 限定枚举值 / 重载函数签名。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 字典类型
  - TypedDict
  - Literal
  - overload
  - NewType
effort: medium
context: inline
version: '1.0'
---
# Python · TypedDict / Literal / overload

## 规则

| 工具 | 用途 |
|------|------|
| `TypedDict` | 给固定键的字典（JSON、配置、kwargs）逐键标类型 |
| `NotRequired` / `Required` | 标记可选/必需键（3.11+），优于 `total=False` 全表 |
| `Literal["a", "b"]` | 限定取值集合（模式、状态、枚举字符串） |
| `Final` | 常量不可重新赋值 |
| `NewType` | 给同底层类型造**区分性**别名，防止 UserId/OrderId 混用 |
| `@overload` | 同名函数随入参不同返回不同类型 |

## 正例

```python
from typing import TypedDict, NotRequired, Literal, Final, NewType, overload

class UserPayload(TypedDict):
    id: int
    name: str
    email: NotRequired[str]   # 该键可缺省

Status = Literal["pending", "active", "closed"]

def transition(s: Status) -> Status:   # 传 "open" 会被静态拒绝
    ...

MAX_RETRIES: Final = 3   # 重新赋值即报错

UserId = NewType("UserId", int)
OrderId = NewType("OrderId", int)

def load(uid: UserId) -> UserPayload: ...
load(OrderId(5))   # 类型错误：OrderId 不是 UserId

# overload：标量返回标量，列表返回列表
@overload
def double(x: int) -> int: ...
@overload
def double(x: list[int]) -> list[int]: ...
def double(x: int | list[int]) -> int | list[int]:
    return [i * 2 for i in x] if isinstance(x, list) else x * 2
```

## 反例

```python
# ❌ 字典用 dict[str, Any]——丢掉每个键的类型
def handle(payload: dict[str, Any]) -> None: ...   # → TypedDict

# ❌ 用裸 str 表示有限状态
def transition(status: str): ...   # 拼错 "actve" 无人发现 → Literal

# ❌ 不同语义的 ID 都用 int，参数顺序写反静默 bug
def link(user: int, order: int): ...   # → NewType 区分

# ❌ overload 只写实现签名，调用方看到的是宽 Union
def double(x): ...   # 无 @overload，返回类型推不准
```

## 自检

- [ ] 固定键字典用 `TypedDict`，可选键用 `NotRequired`？
- [ ] 有限取值用 `Literal` 而非裸 `str`/`int`？
- [ ] 模块常量标 `Final`？
- [ ] 易混的同底层 ID 用 `NewType` 区分？
- [ ] 随入参变返回类型的函数写 `@overload`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`type-narrowing.md`](./type-narrowing.md) · [`pydantic-v2-field.md`](./pydantic-v2-field.md)
