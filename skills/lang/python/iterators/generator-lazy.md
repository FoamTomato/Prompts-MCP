---
name: py-generator-lazy
description: 生成器函数与生成器表达式的惰性求值，用流式处理替代一次性建大 list 来降内存。Use when 处理大文件 / 大查询结果 / 想边产边消省内存。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 生成器
  - 惰性求值
  - generator
  - yield
  - 流式处理
effort: medium
context: inline
version: '1.0'
---
# Python · 生成器惰性求值

## 规则

| 场景 | 用什么 | 为什么 |
|------|--------|--------|
| 函数要逐个产出值 | `yield`（生成器函数） | 不在内存里囤全部结果 |
| 一次性表达式映射/过滤 | `(x for x in it)` 生成器表达式 | 比 `[...]` 省内存，惰性 |
| 把结果传给只遍历一次的消费者 | 直接传生成器 | 边产边消，峰值内存 O(1) |
| 需要随机访问 / 多次遍历 / `len()` | 物化成 `list` | 生成器只能走一遍 |

核心：生成器是**惰性**的——调用生成器函数只返回一个迭代器，函数体一行都不执行，直到 `next()` / `for` 拉取才推进到下一个 `yield`。

## 正例

```python
from collections.abc import Iterator
from pathlib import Path

def read_large_lines(path: Path) -> Iterator[str]:
    """逐行产出，整个文件从不一次性进内存。"""
    with path.open(encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")

# 流式管道：过滤 + 转换 + 聚合，全程不建中间大 list
def count_errors(path: Path) -> int:
    lines = read_large_lines(path)
    errors = (ln for ln in lines if ln.startswith("ERROR"))
    return sum(1 for _ in errors)
```

生成器表达式比列表推导省内存——只在被遍历时逐个算：

```python
total = sum(row.amount for row in fetch_orders())   # 不建临时 list
```

## 反例

```python
# ❌ 把整个文件读进 list，10GB 文件直接 OOM
def read_all(path: Path) -> list[str]:
    return path.read_text().splitlines()   # 全量进内存

# ❌ 生成器只能遍历一次，第二次遍历是空的
gen = (x * 2 for x in range(3))
list(gen)   # [0, 2, 4]
list(gen)   # []  ← 已耗尽，静默返回空，常见 bug

# ❌ 对生成器取 len() 直接 TypeError
len(x for x in range(3))   # TypeError: object of type 'generator' has no len()
```

理由：生成器是**一次性、无长度**的迭代器。需要重复遍历或随机访问时，要么物化成 `list`，要么每次重新调用生成器函数拿新迭代器。

## 自检

- [ ] 大文件 / 大结果集用 `yield` 流式产出，没有一次性建大 list？
- [ ] 只遍历一次的聚合（sum/any/max）用生成器表达式而非 `[...]`？
- [ ] 没有对同一个生成器对象遍历两次（误以为还有数据）？
- [ ] 需要 `len()` / 索引 / 多次遍历时才物化成 `list`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`iterator-protocol.md`](./iterator-protocol.md) · [`yield-from-delegation.md`](./yield-from-delegation.md) · [`comprehension-style.md`](./comprehension-style.md)
