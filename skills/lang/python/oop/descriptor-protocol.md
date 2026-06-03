---
name: py-oop-descriptor-protocol
description: 用描述符协议（__get__/__set__/__set_name__）把字段的校验或惰性计算抽成可复用对象——property、ORM 字段背后的机制。Use when 多个字段要复用同一套取值/校验逻辑 / 想理解 property 原理。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 描述符
  - descriptor
  - __set_name__
  - __get__ __set__
  - 字段复用
effort: high
context: inline
version: '1.0'
---
# Python · 描述符协议

## 规则

| dunder | 触发时机 | 作用 |
|--------|---------|------|
| `__set_name__(self, owner, name)` | 类创建时自动调用 | 拿到自己被赋的属性名，免得手动传 |
| `__get__(self, obj, objtype)` | 读 `instance.attr` | 返回值；`obj` 为 None 时表示从类访问 |
| `__set__(self, obj, value)` | 写 `instance.attr = v` | 校验后存进实例（定义了它即“数据描述符”，优先级高于实例 `__dict__`） |

铁律：状态**存进 `obj.__dict__`**（每个实例独立），不要存在描述符实例上——描述符是类属性，所有实例共享一份，存上去会串数据。当一套校验逻辑要在多个字段重复时才上描述符；单个字段用 `@property` 更简单。

## 正例

```python
class Positive:
    """可复用：任何需要“正数”校验的字段都挂它。"""

    def __set_name__(self, owner, name: str) -> None:
        self._name = f"_{name}"              # ✅ 自动得到字段名

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self                       # 从类访问返回描述符自身
        return getattr(obj, self._name)

    def __set__(self, obj, value: float) -> None:
        if value <= 0:
            raise ValueError(f"{self._name[1:]} must be > 0, got {value}")
        setattr(obj, self._name, value)       # ✅ 存进实例 __dict__，互不干扰


class Order:
    price = Positive()                        # 一行复用校验
    quantity = Positive()

Order().price = -5                            # ValueError: price must be > 0
```

`@property` 本身就是数据描述符——单字段够用时不必自造：

```python
class Order:
    @property
    def total(self) -> float:                 # property == 描述符的便捷封装
        return self.price * self.quantity
```

## 反例

```python
# ❌ 状态存在描述符实例上 → 类级共享，所有实例互相覆盖
class Positive:
    def __set__(self, obj, value):
        self.value = value                    # 应 setattr(obj, self._name, value)
    def __get__(self, obj, objtype=None):
        return self.value                     # 两个 Order 实例会读到同一个值

# ❌ 手动硬编码字段名 → 改名要改两处，易错
class Positive:
    def __init__(self, name):
        self._name = "_" + name               # 用 __set_name__ 自动拿即可

# ❌ 只有单个字段也上描述符 → 过度设计，@property 三行解决
```

理由：描述符是定义在**类**上的对象，实例共享它；把数据存在 `self`（描述符）上必然串实例。`__set_name__` 让描述符自动知道字段名，避免重复书写。它的价值是“一套逻辑复用到多个字段”，单字段场景 property 更轻。

## 自检

- [ ] 状态用 `setattr(obj, ...)` 存进实例，没存在描述符自身？
- [ ] 用 `__set_name__` 自动获取字段名，没手动传字符串？
- [ ] `__get__` 处理了 `obj is None`（从类访问）的情况？
- [ ] 确实是多字段复用同一逻辑才用描述符，单字段已改用 `@property`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`method-types-property.md`](./method-types-property.md)（`@property` 是描述符的便捷封装，单字段首选）
