---
name: py-yield-from-delegation
description: yield from 把迭代委托给子生成器/可迭代对象，自动转发值、send 与返回值。Use when 嵌套生成器扁平化 / 拼接多个可迭代 / 转发子生成器。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 委托生成器
  - 子生成器
  - yield from
  - delegation
  - 扁平化
effort: medium
context: inline
version: '1.0'
---
# Python · yield from 委托

## 规则

| 你想 | 写法 |
|------|------|
| 把一个可迭代的所有元素逐个产出 | `yield from iterable` |
| 拼接多个生成器/序列 | 多行 `yield from a` / `yield from b` |
| 委托并拿子生成器的返回值 | `result = yield from subgen()` |
| 递归遍历嵌套结构 | 在递归函数里 `yield from recurse(child)` |

`yield from sub` 等价于「`for x in sub: yield x`」，但额外**透明转发** `send()` / `throw()` 给子生成器，并把子生成器 `return` 的值作为 `yield from` 表达式的结果——这是手写 `for` 转发做不到的。

## 正例

```python
from collections.abc import Iterator
from typing import Any

# 1. 扁平化嵌套列表（递归委托）
def flatten(items: list[Any]) -> Iterator[Any]:
    for it in items:
        if isinstance(it, list):
            yield from flatten(it)      # 委托给递归子生成器
        else:
            yield it

list(flatten([1, [2, [3, 4]], 5]))      # [1, 2, 3, 4, 5]

# 2. 拼接多个来源
def merged() -> Iterator[int]:
    yield from range(3)                 # 0, 1, 2
    yield from [10, 11]                 # 10, 11

# 3. 接住子生成器的 return 值
def producer() -> Iterator[int]:
    yield 1
    yield 2
    return "done"                       # 生成器的返回值

def driver() -> Iterator[int]:
    status = yield from producer()      # status == "done"
    print(f"子生成器结束: {status}")
```

## 反例

```python
# ❌ 手写 for 转发：啰嗦，且丢掉 send/throw 透传与 return 值
def merged() -> Iterator[int]:
    for x in range(3):
        yield x
    for x in [10, 11]:
        yield x

# ❌ 对单个非可迭代对象用 yield from
def gen():
    yield from 42        # TypeError: 'int' object is not iterable
    # 想产出单个值用 yield 42

# ❌ 想「展开」字符串却得到一堆字符
def chars():
    yield from "ab"      # 产出 'a', 'b'（字符串可迭代），通常不是你要的
```

理由：`yield from` 只接可迭代对象；对标量用普通 `yield`。注意字符串也是可迭代的，`yield from "ab"` 会拆成单字符，多数时候应 `yield "ab"`。

## 自检

- [ ] 转发整个子生成器/可迭代用 `yield from`，不手写 `for ... yield`？
- [ ] 需要子生成器的 `return` 值时用 `x = yield from sub()` 接住？
- [ ] 递归遍历嵌套结构用 `yield from recurse(...)`？
- [ ] 没有对标量或被误当可迭代的字符串用 `yield from`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`generator-lazy.md`](./generator-lazy.md) · [`iterator-protocol.md`](./iterator-protocol.md) · [`comprehension-style.md`](./comprehension-style.md)
