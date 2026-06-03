---
name: py-stdlib-dataclasses-usage
description: dataclasses 数据载体 — @dataclass / field / frozen / slots / __post_init__。Use when 定义纯数据类 / 不可变值对象 / 默认工厂 / 省内存 / 初始化后校验。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 数据类
  - 数据载体
  - dataclass
  - frozen
  - slots
  - field
effort: medium
context: inline
version: '1.0'
---
# Python · dataclasses 数据载体

## 规则

| 选项 | 作用 | 何时用 |
|------|------|--------|
| `@dataclass` | 自动生成 `__init__`/`__repr__`/`__eq__` | 任何纯数据聚合 |
| `field(default_factory=list)` | 可变默认值的安全工厂 | 默认值是 list/dict/set |
| `frozen=True` | 不可变、可哈希（可入 set/dict 键） | 值对象、配置 |
| `slots=True`（3.10+） | 省内存、禁动态属性 | 大量实例 |
| `__post_init__` | 初始化后派生/校验 | 计算派生字段、断言约束 |

可变默认值**必须**用 `field(default_factory=...)`，直接写 `= []` 会被所有实例共享。

## 正例

```python
from dataclasses import dataclass, field

@dataclass(slots=True)
class Order:
    order_id: str
    items: list[str] = field(default_factory=list)   # 每实例独立列表
    discount: float = 0.0
    total: float = field(init=False, default=0.0)     # 派生，不进 __init__

    def __post_init__(self) -> None:
        if self.discount < 0:
            raise ValueError("discount 不能为负")
        self.total = sum_prices(self.items) * (1 - self.discount)

@dataclass(frozen=True)               # 不可变 + 可哈希
class Point:
    x: int
    y: int

p = Point(1, 2)
seen: set[Point] = {p}                # frozen 才能进 set
```

## 反例

```python
from dataclasses import dataclass

# ❌ 可变默认值直接写字面量 -> 所有实例共享同一个 list
@dataclass
class Cart:
    items: list = []                  # 抛 ValueError（dataclass 会检测）
                                      # 即便不抛，共享可变默认也是经典陷阱

# ❌ 需要不可变/可哈希却没加 frozen
@dataclass
class Coord:
    x: int
    y: int
c = Coord(1, 2)
{c}                                   # TypeError: unhashable（默认不可哈希）

# ❌ 手写满是样板的 __init__/__repr__/__eq__
class Order:                          # dataclass 一行装饰器即可全自动
    def __init__(self, order_id, items=None):
        self.order_id = order_id
        self.items = items or []
```

理由：`@dataclass` 消除 `__init__`/`__repr__`/`__eq__` 样板；`default_factory` 杜绝可变默认共享；`frozen` 提供不可变与可哈希；`slots` 省内存。建模优先用 dataclass，需要校验时再考虑 pydantic。

## 自检

- [ ] 纯数据类用 `@dataclass` 而非手写样板？
- [ ] 可变默认值都用 `field(default_factory=...)`？
- [ ] 值对象/需入 set 或字典键的类加了 `frozen=True`？
- [ ] 大量实例的类考虑了 `slots=True`？
- [ ] 派生字段/初始化校验放在 `__post_init__`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`enum-usage.md`](./enum-usage.md) · [`collections-toolkit.md`](./collections-toolkit.md)
