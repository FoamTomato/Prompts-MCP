---
name: py-stdlib-enum-usage
description: enum 命名常量 — Enum / IntEnum / StrEnum / Flag + auto()。Use when 定义一组状态码 / 类型常量 / 可比较整数枚举 / 字符串枚举 / 位标志组合。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 枚举
  - 命名常量
  - 位标志
  - Enum
  - StrEnum
  - Flag
effort: low
context: inline
version: '1.0'
---
# Python · enum 命名常量

## 规则

| 类型 | 用途 | 关键点 |
|------|------|--------|
| `Enum` | 一组互斥命名常量 | 成员不等于其值，比较用成员本身 |
| `IntEnum` | 需当整数用/比较的枚举 | 可与 int 直接比较 |
| `StrEnum`（3.11+） | 需当字符串用的枚举 | 可直接拼接/序列化为字符串 |
| `Flag` / `IntFlag` | 位标志，可 `|` 组合 | 权限位、特性开关 |
| `auto()` | 自动赋值，免手写魔数 | 配合任意枚举类型 |

## 正例

```python
from enum import Enum, IntEnum, StrEnum, Flag, auto

class Color(Enum):
    RED = auto()                  # 值自动分配，无需关心具体数字
    GREEN = auto()
    BLUE = auto()

class Priority(IntEnum):          # 可比较大小、可当 int
    LOW = 1
    HIGH = 3

assert Priority.HIGH > Priority.LOW

class Status(StrEnum):            # 直接当字符串用，JSON 友好
    ACTIVE = "active"
    CLOSED = "closed"

payload = {"status": Status.ACTIVE}    # 序列化即 "active"

class Perm(Flag):                 # 位标志，| 组合
    READ = auto()
    WRITE = auto()
    EXEC = auto()

rights = Perm.READ | Perm.WRITE
assert Perm.READ in rights        # 成员包含判断
```

## 反例

```python
# ❌ 用裸字符串/魔数当常量：无类型约束、易拼错、不可枚举
STATUS_ACTIVE = "active"
STATUS_CLOSED = "closed"
if order.status == "activ":       # 拼错不报错，静默失效

# ❌ 普通 Enum 却拿来和原始值比较
class Status(Enum):
    ACTIVE = "active"
if order.status == "active":      # False！成员 != 其 value，用 StrEnum 或比成员

# ❌ 多个布尔标志参数，组合爆炸、调用处可读性差
def open_file(read: bool, write: bool, execute: bool): ...
open_file(True, False, True)      # 哪个是哪个？用 Flag 组合更清晰
```

理由：枚举提供**类型安全的命名常量集合**，可迭代、可校验、IDE 可补全；`IntEnum`/`StrEnum` 在需要与原始 int/str 互操作时避免「成员 != 值」陷阱；`Flag` 让位标志组合显式且可读。

## 自检

- [ ] 一组相关常量用 Enum 而非散落的字符串/魔数？
- [ ] 需要和 int 比较/排序用 `IntEnum`，需要当字符串用 `StrEnum`？
- [ ] 用普通 `Enum` 时比较的是成员本身，而非其 `.value`？
- [ ] 可组合的标志位用 `Flag` / `IntFlag` + `|`？
- [ ] 值无业务含义时用 `auto()` 而非手写魔数？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`dataclasses-usage.md`](./dataclasses-usage.md) · [`collections-toolkit.md`](./collections-toolkit.md)
