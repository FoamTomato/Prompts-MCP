---
name: py-stdlib-itertools-pipeline
description: itertools 惰性迭代管道 — chain / groupby / islice / accumulate。Use when 拼接多个序列 / 连续分组 / 切片大流 / 滚动累计 / 避免中间列表。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 惰性迭代
  - 迭代管道
  - chain
  - groupby
  - islice
  - accumulate
effort: medium
context: inline
version: '1.0'
---
# Python · itertools 惰性管道

## 规则

| 函数 | 用途 | 关键点 |
|------|------|--------|
| `chain(a, b)` | 顺序拼接多个可迭代 | 不建中间列表 |
| `chain.from_iterable(lists)` | 扁平化嵌套序列 | 一层展开 |
| `groupby(seq, key)` | 按相邻相同键分组 | **必须先按 key 排序** |
| `islice(it, start, stop)` | 惰性切片 | 不支持负索引，但能切无穷流 |
| `accumulate(seq, func)` | 滚动累计（前缀和等） | 默认累加 |

`groupby` 只对**相邻**元素分组：未排序会得到碎片化分组，几乎总是 bug。

## 正例

```python
from itertools import chain, groupby, islice, accumulate
from operator import attrgetter

# 拼接多源、扁平化，全程惰性
combined = chain(active_users, pending_users)
flat = chain.from_iterable([[1, 2], [3, 4]])    # 1 2 3 4

# 分组：先排序再 groupby
orders.sort(key=attrgetter("customer_id"))
for cust_id, group in groupby(orders, key=attrgetter("customer_id")):
    total = sum(o.amount for o in group)        # group 是一次性迭代器

# 切大流的前 10 条，不物化整个序列
first_10 = list(islice(huge_log_stream(), 10))

# 滚动累计：余额变动 -> 余额序列
balances = list(accumulate([100, -30, 50]))     # [100, 70, 120]
```

## 反例

```python
# ❌ 拼接前先各自物化成 list，浪费内存
combined = list(active_users) + list(pending_users)   # 用 chain(...) 即可

# ❌ groupby 前未排序：相同 key 被拆成多个碎片组
for cust_id, group in groupby(orders, key=attrgetter("customer_id")):
    ...        # orders 未排序 -> 同一客户出现多次

# ❌ 复用 groupby 的 group：它是迭代器，第二次遍历为空
for cust_id, group in groupby(orders, key=keyfn):
    items = list(group)      # 想复用必须先转 list，别二次迭代原 group
```

理由：itertools 返回**惰性迭代器**，省内存且可链式组合；`groupby` 与 SQL 的 `GROUP BY` 不同，只看相邻元素，必须预排序。

## 自检

- [ ] 拼接序列用 `chain` 而非 `list(a) + list(b)`？
- [ ] `groupby` 前已按相同 key 排序？
- [ ] 大流/无穷流取前 N 用 `islice` 而非全部物化？
- [ ] 前缀和/滚动统计用 `accumulate`？
- [ ] 没有二次遍历 `groupby` 产出的同一个 group 迭代器？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`collections-toolkit.md`](./collections-toolkit.md) · [`functools-toolkit.md`](./functools-toolkit.md)
