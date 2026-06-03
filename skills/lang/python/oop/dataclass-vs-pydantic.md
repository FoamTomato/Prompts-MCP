---
name: py-oop-dataclass-vs-pydantic
description: 数据载体建模选型——纯内部结构用 dataclass、外部输入需校验用 pydantic v2、第三方零依赖值对象用 attrs。Use when 新建数据类不知道选哪个 / 纠结是否需要运行时校验 / 评审建模方案。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 建模选型
  - dataclass
  - pydantic
  - attrs
  - 数据载体
effort: medium
context: inline
version: '1.0'
---
# Python · 数据建模选型

## 规则

| 方案 | 校验 | 何时选 |
|------|------|--------|
| `@dataclass` | 无（仅类型注解，不运行时校验） | 内部结构、可信数据、配置聚合；标准库零依赖 |
| Pydantic v2 `BaseModel` | 有（构造即校验 + 解析） | API 请求/响应、配置加载、任何外部不可信输入 |
| `attrs` | 可选（`@define` + validators） | 不想引入 pydantic 又要校验/不可变；库作者偏好 |

选型判据：**数据从哪来**。来自外部（HTTP/文件/环境变量）必须校验 → pydantic；纯内部传递、自己造的数据 → dataclass。不要用 pydantic 包装内部结构（白付校验开销），也不要用 dataclass 接外部输入（无校验埋雷）。

边界：本条只讲**选哪种**；pydantic 的 `Field` 约束写法见 typing/pydantic-v2-field，不在此重复。

## 正例

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)          # ✅ 内部值对象：不可变 + 省内存
class Point:
    x: int
    y: int
```

```python
from pydantic import BaseModel

class CreateUserReq(BaseModel):              # ✅ 外部输入：构造即校验类型/约束
    name: str
    age: int

CreateUserReq(name="ann", age="not-int")     # 立即 ValidationError，挡在边界
```

```python
from attrs import define, field
from attrs.validators import ge

@define(frozen=True)                          # ✅ 要校验又不想依赖 pydantic
class Port:
    number: int = field(validator=ge(1))
```

## 反例

```python
# ❌ 用 dataclass 接 API 输入 → 类型/范围全不校验，脏数据进系统
@dataclass
class CreateUserReq:
    name: str
    age: int
CreateUserReq(name="ann", age="oops")        # 不报错，age 是字符串也照收

# ❌ 内部纯数据强行套 pydantic → 每次构造都跑校验，无谓开销
class InternalCounter(BaseModel):            # 自己造的可信数据，dataclass 足矣
    value: int

# ❌ 可变值对象当 dict key → 见 data-model/dunder-protocol
@dataclass                                    # 缺 frozen=True，不可哈希
class Key:
    k: str
```

理由：pydantic 的价值在**信任边界**做解析+校验，把它用在内部数据上只换来运行时开销；dataclass 不校验，拿它接外部输入等于把脏数据放进系统。选型对了，校验该有的地方有、不该有的地方零成本。

## 自检

- [ ] 外部不可信输入（HTTP / 文件 / env）用 pydantic，不是裸 dataclass？
- [ ] 纯内部、可信的数据用 dataclass，没用 pydantic 白付校验开销？
- [ ] 值对象 dataclass 加了 `frozen=True`（+ `slots=True` 省内存）？
- [ ] 选定方案有一致理由（数据来源 + 是否需校验），不是随手挑？

## 相关

- 父：[`./index.md`](./index.md)
- 配套：[`../typing/pydantic-v2-field.md`](../typing/pydantic-v2-field.md)（选定 pydantic 后，Field 约束怎么写）
- 兄弟：[`../data-model/dunder-protocol.md`](../data-model/dunder-protocol.md)（dataclass 的 `__eq__`/`__hash__` 由 `frozen` 控制）
