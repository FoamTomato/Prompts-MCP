---
name: py-oop-mro-super
description: 用 MRO（C3 线性化）理解多继承调用顺序，正确写 super() 协作链，优先组合而非深继承。Use when 多继承调用顺序不符预期 / super() 不知怎么传参 / 决定继承还是组合。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 多继承
  - MRO
  - super
  - C3 线性化
  - 组合优于继承
effort: medium
context: inline
version: '1.0'
---
# Python · MRO 与 super

## 规则

| 概念 | 要点 |
|------|------|
| MRO | 每个类有确定的方法解析顺序，由 C3 线性化算出；查 `Cls.__mro__` 或 `Cls.mro()` |
| `super()` | 沿**当前实例的 MRO** 走到下一个类，不是“父类”——多继承下可能是兄弟类 |
| 协作式继承 | 链上每个方法都 `super().method(...)` 才不会漏调；`__init__` 用 `**kwargs` 透传 |
| 组合优于继承 | 只为复用行为而继承 → 改用持有对象（has-a）；继承仅用于真正的 is-a + 多态 |

铁律：多继承下 `super()` 不等于父类，**永远按 MRO 推理**；任何会被 mixin 叠加的方法都必须 `super()` 接力，否则链断。

## 正例

```python
class Base:
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)          # ✅ 顶到 object 前一直透传

class Loggable:
    def __init__(self, *, tag: str, **kwargs) -> None:
        self.tag = tag
        super().__init__(**kwargs)          # ✅ 不吞 kwargs，接力给下一个

class Service(Loggable, Base):
    def __init__(self, *, name: str, **kwargs) -> None:
        self.name = name
        super().__init__(**kwargs)

s = Service(name="api", tag="prod")
print([c.__name__ for c in Service.__mro__])
# ['Service', 'Loggable', 'Base', 'object']  ← super() 就沿这条链走
```

组合优于继承——只想复用功能而非建立 is-a：

```python
class ReportBuilder:
    def __init__(self, formatter: "Formatter") -> None:
        self._formatter = formatter          # ✅ has-a：持有而非继承
    def build(self, data: dict) -> str:
        return self._formatter.render(data)
```

## 反例

```python
# ❌ 多继承却写死父类名 → 绕过 MRO，兄弟类的 __init__ 被跳过
class Service(Loggable, Base):
    def __init__(self, name, tag):
        Loggable.__init__(self, tag=tag)     # 漏掉 Base，且不可协作
        self.name = name

# ❌ 链中某个 __init__ 不调 super() → 后续类初始化全被吞
class Loggable:
    def __init__(self, tag):
        self.tag = tag                       # 没 super().__init__()，链断

# ❌ 为复用一个方法而继承庞大基类 → 强耦合、MRO 复杂
class CsvReport(PandasDataFrame):            # 只想用一个导出方法却背上整张表
    ...
```

理由：`super()` 的语义是“MRO 里的下一个”，多继承时直接调父类名会跳过协作链上的兄弟类，导致状态初始化不全；深继承把无关基类的全部表面积塞进子类，组合则只暴露你真正需要的接口。

## 自检

- [ ] 多继承时按 `__mro__` 推理调用顺序，没把 `super()` 当“父类”？
- [ ] 会被叠加的方法（含 `__init__`）每个都 `super().xxx(**kwargs)` 接力？
- [ ] 协作链的 `__init__` 用关键字参数 + `**kwargs` 透传，不靠位置参数？
- [ ] 仅为复用行为时用组合（持有对象），没用继承制造强耦合？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`init-subclass-metaclass.md`](./init-subclass-metaclass.md)（ABC / 子类钩子也参与 MRO） · [`method-types-property.md`](./method-types-property.md)（classmethod 在子类的多态）
