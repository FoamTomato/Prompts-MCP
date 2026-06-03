---
name: py-dunder-protocol
description: 自定义类的核心 dunder——__eq__ 与 __hash__ 必须成对、__repr__ 给开发者、__bool__/__len__ 定义真值。Use when 给类加相等性 / 放进 set 或 dict key / 让 print 有意义 / 控制 if obj 判断。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 魔术方法
  - dunder
  - __eq__ __hash__
  - __repr__
  - 真值协议
effort: medium
context: inline
version: '1.0'
---
# Python · 核心 dunder 协议

## 规则

| dunder | 作用 | 关键约束 |
|--------|------|---------|
| `__eq__` | 定义 `==` | 重写它会把 `__hash__` 置 None → 实例不可哈希 |
| `__hash__` | 进 set / 做 dict key | 必须与 `__eq__` 一致：`a == b` ⇒ `hash(a) == hash(b)` |
| `__repr__` | 开发者可读表示（调试 / 日志 / REPL） | 尽量能 eval 还原，永远要实现 |
| `__bool__` / `__len__` | `if obj:` 真值 | 无 `__bool__` 时回退 `__len__`，再回退恒 True |

铁律：**改了 `__eq__` 就要么显式定义 `__hash__`，要么让对象保持可变且不进 set。** 值对象优先用 `@dataclass`，自动正确生成。

## 正例

```python
from dataclasses import dataclass

@dataclass(frozen=True)          # frozen=True 自动生成一致的 __eq__ + __hash__
class Point:
    x: int
    y: int

p = {Point(1, 2), Point(1, 2)}   # ✅ 去重为 1 个，可做 dict key
```

```python
class Cart:
    def __init__(self, items: list[str]):
        self.items = items

    def __repr__(self) -> str:           # ✅ 调试友好，能看出内容
        return f"Cart(items={self.items!r})"

    def __len__(self) -> int:            # if cart: 等价于 len != 0
        return len(self.items)
```

## 反例

```python
# ❌ 只写 __eq__ 不管 __hash__ → 实例不能进 set / 当 key
class User:
    def __init__(self, uid): self.uid = uid
    def __eq__(self, other): return self.uid == other.uid

{User(1)}            # TypeError: unhashable type: 'User'

# ❌ __eq__ 与 __hash__ 不一致 → set 去重 / dict 查找出错
class Bad:
    def __eq__(self, o): return self.uid == o.uid
    def __hash__(self): return id(self)   # 相等的对象哈希却不同 → 字典里查不到

# ❌ 没有 __repr__ → 日志里只有 <User object at 0x10f...>
```

理由：哈希容器先比 `hash` 再比 `==`；两者不一致会让“相等的对象”落到不同桶，集合去重失败、字典查不到。可变对象当 key 后被改还会永久丢失。

## 自检

- [ ] 重写了 `__eq__` 的类，要么定义了一致的 `__hash__`，要么明确不进 set / dict？
- [ ] 值对象优先用 `@dataclass(frozen=True)` 自动生成，而非手写？
- [ ] 每个领域类都有 `__repr__`（含关键字段，用 `!r`）？
- [ ] 用 `__len__` / `__bool__` 显式控制真值，没依赖默认恒 True？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`is-vs-equals.md`](./is-vs-equals.md)（`==` 调 `__eq__`，`is` 不调） · [`copy-semantics.md`](./copy-semantics.md)（可变对象当 key 的隐患）
