---
name: py-oop-init-subclass-metaclass
description: 在子类定义时做注册或校验优先用 __init_subclass__，定义接口契约用 ABC/abstractmethod，元类仅留给极少数框架级场景。Use when 想在子类定义时自动注册或校验 / 强制子类实现某方法 / 评估是否要写元类。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 子类钩子
  - __init_subclass__
  - 元类
  - metaclass
  - 抽象基类
  - abstractmethod
effort: high
context: inline
version: '1.0'
---
# Python · 子类钩子、ABC 与元类

## 规则

| 需求 | 用什么 | 不要用 |
|------|--------|--------|
| 子类定义时自动注册 / 校验配置 | `__init_subclass__(cls, **kwargs)` | 元类 |
| 强制子类实现某方法 / 定义接口 | `ABC` + `@abstractmethod` | 元类 |
| 真正改写类创建机制（如 ORM 字段收集、Enum） | `metaclass` | —— 仅框架作者 |

铁律：优先级 **`__init_subclass__` > ABC > 元类**。能用前两者解决就别写元类——元类污染整条继承链、与其他元类冲突、可读性差。`__init_subclass__` 定义在父类、`@classmethod`（隐式），每个子类创建时自动触发。

## 正例

```python
class Plugin:
    registry: dict[str, type["Plugin"]] = {}

    def __init_subclass__(cls, *, key: str, **kwargs) -> None:
        super().__init_subclass__(**kwargs)  # ✅ 必须接力，别断 MRO 链
        cls.registry[key] = cls               # 子类一定义即自动注册

class JsonPlugin(Plugin, key="json"):         # 触发钩子，登记到 registry
    ...

assert Plugin.registry["json"] is JsonPlugin
```

强制子类实现接口用 ABC：

```python
from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def save(self, data: bytes) -> None: ...

class S3Storage(Storage):                     # 不实现 save 则实例化时 TypeError
    def save(self, data: bytes) -> None:
        ...
```

## 反例

```python
# ❌ 为“子类自动注册”动用元类 → 杀鸡用牛刀，污染继承链
class PluginMeta(type):
    def __new__(mcs, name, bases, ns):
        cls = super().__new__(mcs, name, bases, ns)
        registry[name] = cls                  # __init_subclass__ 三行就够
        return cls

# ❌ __init_subclass__ 忘了 super() → 多层继承时上游钩子被吞
class Plugin:
    def __init_subclass__(cls, **kwargs):
        registry[cls.__name__] = cls          # 漏 super().__init_subclass__(**kwargs)

# ❌ 用普通基类 + 运行时 if 假装“抽象” → 子类漏实现要到调用才炸
class Storage:
    def save(self, data):
        raise NotImplementedError             # 改用 ABC，实例化即拦截
```

理由：`__init_subclass__`（PEP 487）就是为“子类钩子”而生，比元类轻得多且不冲突；ABC 让“未实现抽象方法”在**实例化时**就报错而非运行到才崩。元类会改变类的类型，叠加多个会冲突，绝大多数库级以下代码都不需要。

## 自检

- [ ] 子类注册 / 定义期校验用 `__init_subclass__`，没动用元类？
- [ ] `__init_subclass__` 里调了 `super().__init_subclass__(**kwargs)`？
- [ ] 接口契约用 `ABC` + `@abstractmethod`，没靠运行时 `NotImplementedError` 假装抽象？
- [ ] 确实需要改写类创建机制（框架级）才用元类，否则不写？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`mro-super.md`](./mro-super.md)（`__init_subclass__` / ABC 都依赖 `super()` 与 MRO 接力）
