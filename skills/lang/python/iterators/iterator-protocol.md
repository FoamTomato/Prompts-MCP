---
name: py-iterator-protocol
description: 迭代器协议 __iter__ / __next__ / StopIteration，以及可迭代对象与迭代器的区别。Use when 让自定义类支持 for / 实现 __iter__ / 调试 StopIteration。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 迭代器协议
  - 可迭代对象
  - iterator
  - StopIteration
  - __iter__
effort: medium
context: inline
version: '1.0'
---
# Python · 迭代器协议

## 规则

| 概念 | 需实现 | 说明 |
|------|--------|------|
| 可迭代对象 Iterable | `__iter__()` 返回一个迭代器 | 能被 `for` / `iter()` 使用，可多次取新迭代器 |
| 迭代器 Iterator | `__iter__()` 返回 `self` + `__next__()` | 持有遍历状态，耗尽后每次 `__next__` 抛 `StopIteration` |
| 终止 | `raise StopIteration` | `for` 捕获它来结束循环；**不要**让它泄漏到生成器外 |

要点：**可迭代 ≠ 迭代器**。`list` 是可迭代对象但不是迭代器（无 `__next__`）；`iter(list)` 才得到迭代器。把状态放在迭代器里，让可迭代对象每次 `__iter__` 返回**新**迭代器，才能支持多次独立遍历。

## 正例

```python
from collections.abc import Iterator

class Countdown:
    """可迭代对象：每次 __iter__ 返回新迭代器，支持多次遍历。"""

    def __init__(self, start: int) -> None:
        self.start = start

    def __iter__(self) -> Iterator[int]:
        return _CountdownIter(self.start)


class _CountdownIter:
    def __init__(self, n: int) -> None:
        self.n = n

    def __iter__(self) -> "_CountdownIter":
        return self                      # 迭代器返回自身

    def __next__(self) -> int:
        if self.n <= 0:
            raise StopIteration          # 终止信号
        self.n -= 1
        return self.n + 1

for x in Countdown(3):                   # 3, 2, 1
    print(x)
```

绝大多数情况下，用生成器实现 `__iter__` 更省事——`yield` 自动满足迭代器协议：

```python
class Countdown:
    def __init__(self, start: int) -> None:
        self.start = start

    def __iter__(self) -> Iterator[int]:
        n = self.start
        while n > 0:
            yield n
            n -= 1
```

## 反例

```python
# ❌ 把状态放在可迭代对象自身 + __iter__ 返回 self，只能遍历一次
class Bad:
    def __init__(self, n): self.n = n
    def __iter__(self): return self          # 同一对象当迭代器
    def __next__(self):
        if self.n <= 0: raise StopIteration
        self.n -= 1; return self.n
b = Bad(3)
list(b)   # [2, 1, 0]
list(b)   # []  ← 状态被第一次遍历耗尽

# ❌ 在生成器函数里手动 raise StopIteration（PEP 479 起会变成 RuntimeError）
def gen():
    yield 1
    raise StopIteration   # ❌ 用 return 结束生成器，不要 raise
```

理由：状态属于迭代器而非可迭代对象，否则多次 `for` 互相污染；生成器内用 `return` 终止，手动 `raise StopIteration` 会被转成 `RuntimeError`。

## 自检

- [ ] 可迭代对象的 `__iter__` 每次返回**新**迭代器（支持多次遍历）？
- [ ] 迭代器的 `__iter__` 返回 `self`，`__next__` 耗尽时 `raise StopIteration`？
- [ ] 生成器函数用 `return` 结束，没有手动 `raise StopIteration`？
- [ ] 能用生成器实现 `__iter__` 时优先用 `yield`，不手写 `__next__`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`generator-lazy.md`](./generator-lazy.md) · [`yield-from-delegation.md`](./yield-from-delegation.md) · [`comprehension-style.md`](./comprehension-style.md)
