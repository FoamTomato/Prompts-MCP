---
name: py-typing-deferred-annotations
description: PEP 649/749 注解延迟求值（3.14 默认），影响 pydantic/FastAPI/dataclasses 运行时反射。Use when 处理前向引用 / 运行时读 __annotations__ / 排查类型在运行时取不到的报错。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 延迟注解
  - PEP 649
  - 前向引用
  - get_type_hints
  - annotations
effort: medium
context: inline
version: '1.0'
---
# Python · 注解延迟求值

## 规则

- **前向引用**（引用尚未定义的名字、自引用）直接写名字即可，不必加引号或手动 `from __future__ import annotations`。PEP 649/749 让注解**惰性求值**——定义时不执行，按需才计算。
- **运行时读注解**用 `typing.get_type_hints(obj)` 或 `inspect.get_annotations(obj, eval_str=True)`，**不要**直接读 `__annotations__`：延迟模式下原始 `__annotations__` 可能是未求值的字符串/对象。
- pydantic / FastAPI / dataclasses 依赖运行时反射读注解；3.14 默认延迟后，**所有被引用的类型必须在求值时可见**（在模块作用域内，或显式传 `localns`）。

## 正例

```python
from dataclasses import dataclass
from typing import get_type_hints

@dataclass
class Node:
    value: int
    next: Node | None = None   # 自引用：无需引号，惰性求值

# 运行时取已求值的真实类型
hints = get_type_hints(Node)   # {'value': int, 'next': Node | None}

# pydantic 模型互相引用——保证两个类在同一模块可见即可
from pydantic import BaseModel

class Author(BaseModel):
    name: str
    books: list[Book]   # Book 在下方定义，惰性求值时已存在

class Book(BaseModel):
    title: str
    author: Author
```

## 反例

```python
# ❌ 运行时直接读 __annotations__，延迟模式下拿到的可能不是真实类型对象
def field_types(cls):
    return cls.__annotations__   # → get_type_hints(cls)

# ❌ 把类型引用放在函数局部作用域，求值时该名字不在 globalns/localns
def make_model():
    class Inner: ...
    class M(BaseModel):
        x: Inner   # get_type_hints 默认查不到局部 Inner → 需显式传 localns

# ❌ 仍假设 from __future__ import annotations 会让 pydantic 自动解析任意字符串
# 字符串注解引用的名字若不在作用域，运行时反射照样 NameError
```

延迟注解把"前向引用"变简单，但把"运行时拿类型"的责任交给 `get_type_hints`——它需要能解析每个名字。局部定义的类型要么提到模块级，要么调用时传 `localns`。

## 自检

- [ ] 前向引用/自引用直接写名字，未滥用引号？
- [ ] 运行时取类型用 `get_type_hints` / `inspect.get_annotations(eval_str=True)`，不裸读 `__annotations__`？
- [ ] 被注解引用的类型在求值作用域内可见（模块级或显式 `localns`）？
- [ ] 升级 3.14 前验证过 pydantic/FastAPI 模型的反射仍正常？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`pep695-generics.md`](./pep695-generics.md) · [`typeddict-literal.md`](./typeddict-literal.md)
