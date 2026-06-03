---
name: py-mutable-default-arg
description: 可变默认参数陷阱——def f(x=[]) 的默认值只在定义时求值一次并被复用。Use when 写带默认参数的函数 / 排查多次调用结果互相串了 / 评审 list/dict 默认值。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 可变默认参数
  - mutable default argument
  - 默认值哨兵
  - None sentinel
  - 'def f(x=[])'
effort: medium
context: inline
version: '1.0'
---
# Python · 可变默认参数陷阱

## 规则

| 现象 | 原因 | 做法 |
|------|------|------|
| 默认值只求值一次 | 默认值在 `def` 执行（定义）时绑定，不是每次调用 | 默认值用不可变对象（`None`、`()`、数字、字符串） |
| 多次调用结果累积 | 同一个 list/dict/set 对象被所有调用共享 | 默认 `None`，函数体内 `if x is None: x = []` |
| 类属性同理 | `dataclass` 字段、类体里的 `attr = []` 也被实例共享 | dataclass 用 `field(default_factory=list)` |

核心：**默认参数是函数对象的属性，整个进程生命周期只有一份。**

## 正例

```python
def append_item(item: int, bucket: list[int] | None = None) -> list[int]:
    if bucket is None:
        bucket = []          # 每次调用都拿到全新 list
    bucket.append(item)
    return bucket

assert append_item(1) == [1]
assert append_item(2) == [2]   # 不会变成 [1, 2]
```

```python
from dataclasses import dataclass, field

@dataclass
class Order:
    # ❌ items: list[str] = []  —— dataclass 会直接报 ValueError
    items: list[str] = field(default_factory=list)   # 每个实例独立
```

## 反例

```python
# ❌ 默认 [] 在定义时创建一次，被所有调用共享
def append_item(item, bucket=[]):
    bucket.append(item)
    return bucket

append_item(1)        # [1]
append_item(2)        # [1, 2] —— 串了！
print(append_item.__defaults__)   # ([1, 2],) 默认值本身被改了
```

理由：`bucket=[]` 的 `[]` 在 `def` 执行时构造一次，存进 `append_item.__defaults__`；每次省略实参都复用这同一个 list，append 会累积。`{}`、`set()`、`datetime.now()`（求值时刻固定）同理。

## 自检

- [ ] 没有 `def f(x=[])` / `=` `{}` / `=set()` 这类可变默认值？
- [ ] 需要可变默认时，用了 `None` 哨兵 + 函数体内构造？
- [ ] 判哨兵用的是 `x is None` 而不是 `if not x`（避免误伤空 list/0）？
- [ ] dataclass 字段用 `field(default_factory=...)`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`is-vs-equals.md`](./is-vs-equals.md)（哨兵为何用 `is None`） · [`copy-semantics.md`](./copy-semantics.md)（共享可变对象的根因）
