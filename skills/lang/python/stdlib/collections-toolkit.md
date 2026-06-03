---
name: py-stdlib-collections-toolkit
description: collections 容器选型 — defaultdict / Counter / deque / namedtuple / ChainMap。Use when 分组聚合 / 计数 / 双端队列 / 轻量记录 / 多层默认值。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 计数
  - 分组聚合
  - defaultdict
  - Counter
  - deque
  - namedtuple
effort: medium
context: inline
version: '1.0'
---
# Python · collections 容器选型

## 规则

| 容器 | 用途 | 取代 |
|------|------|------|
| `defaultdict(list)` | 分组聚合，键缺省自动建值 | `dict` + `setdefault` |
| `Counter(iterable)` | 计数、取 Top-N | 手写 `d[k] = d.get(k,0)+1` |
| `deque(maxlen=N)` | 两端 O(1) 增删、滑动窗口 | `list.pop(0)`（O(n)） |
| `namedtuple` | 不可变轻量记录、字段命名 | 裸 tuple 靠下标取值 |
| `ChainMap` | 多层映射叠加查找（默认+覆盖） | 反复 `{**base, **override}` |

`deque` 头部操作是 O(1)，`list.pop(0)` 是 O(n)；队列/滑窗一律用 `deque`。

## 正例

```python
from collections import defaultdict, Counter, deque, namedtuple, ChainMap

# 分组聚合：按部门归并员工
groups: defaultdict[str, list[str]] = defaultdict(list)
for name, dept in employees:
    groups[dept].append(name)

# 计数 + Top-3 高频词
counts = Counter(words)
top3 = counts.most_common(3)

# 滑动窗口：只保留最近 100 条
recent: deque[float] = deque(maxlen=100)
recent.append(latency)            # 超出自动丢弃最旧

# 轻量记录：字段可读、可解包
Point = namedtuple("Point", ["x", "y"])
p = Point(1, 2)
x, y = p

# 多层配置：CLI 覆盖环境变量覆盖默认值
config = ChainMap(cli_args, env_vars, defaults)
```

## 反例

```python
# ❌ 手动初始化分组列表，每次都判空
groups = {}
for name, dept in employees:
    if dept not in groups:        # 噪声，defaultdict 自动处理
        groups[dept] = []
    groups[dept].append(name)

# ❌ 用 list 当队列，头部弹出是 O(n)，大数据量退化
queue = []
queue.append(item)
first = queue.pop(0)              # 每次搬移整个底层数组

# ❌ 裸 tuple 靠下标，可读性差且易错位
p = (1, 2)
distance = (p[0] ** 2 + p[1] ** 2) ** 0.5   # p[0] 是什么？
```

理由：`defaultdict` 把「缺省建值」内聚进容器；`deque` 保证两端 O(1)；`namedtuple` 让字段自解释。手写等价物更长且更易出错。

## 自检

- [ ] 分组聚合用了 `defaultdict` 而非手动判空？
- [ ] 计数/Top-N 用了 `Counter.most_common`？
- [ ] 队列/滑动窗口用 `deque`（带 `maxlen`）而非 `list.pop(0)`？
- [ ] 多字段记录用 `namedtuple` 或 dataclass，而非裸 tuple 下标？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`itertools-pipeline.md`](./itertools-pipeline.md) · [`dataclasses-usage.md`](./dataclasses-usage.md)
