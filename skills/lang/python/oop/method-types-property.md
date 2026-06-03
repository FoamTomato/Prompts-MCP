---
name: py-oop-method-types-property
description: 区分实例方法 / @classmethod / @staticmethod，并用 @property 把计算字段暴露成只读属性。Use when 不确定方法第一参数该写 self/cls/无 / 想加备用构造器 / 把方法暴露成属性。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 实例方法
  - classmethod
  - staticmethod
  - property
  - 备用构造器
effort: medium
context: inline
version: '1.0'
---
# Python · 方法类型与 property

## 规则

| 类型 | 第一参数 | 何时用 |
|------|---------|--------|
| 实例方法 | `self` | 需要读写实例状态 |
| `@classmethod` | `cls` | 备用构造器 / 操作类本身；子类调用拿到子类 |
| `@staticmethod` | 无 | 逻辑归属本类但不碰 `self`/`cls`，纯工具函数 |
| `@property` | `self` | 把无副作用的计算暴露成只读属性，不让调用方写 `()` |

铁律：备用构造器用 `@classmethod`（返回 `cls(...)` 才能被子类继承）；`@property` 只包**无副作用、廉价**的计算，重计算或有 I/O 的留成方法。

## 正例

```python
class Temperature:
    def __init__(self, celsius: float) -> None:
        self._celsius = celsius

    @classmethod
    def from_fahrenheit(cls, f: float) -> "Temperature":
        return cls((f - 32) / 1.8)          # ✅ 用 cls，子类调用得到子类实例

    @staticmethod
    def is_freezing(celsius: float) -> bool:
        return celsius <= 0                  # ✅ 不依赖实例，归类于此

    @property
    def fahrenheit(self) -> float:           # ✅ 调用方写 t.fahrenheit 而非 t.fahrenheit()
        return self._celsius * 1.8 + 32

t = Temperature.from_fahrenheit(212)
print(t.fahrenheit)                          # 212.0
```

只读属性配只设值校验时用 setter：

```python
    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        self._celsius = (value - 32) / 1.8
```

## 反例

```python
# ❌ 备用构造器硬编码类名 → 子类调用仍返回父类实例
class Temperature:
    @classmethod
    def from_fahrenheit(cls, f):
        return Temperature((f - 32) / 1.8)   # 应为 cls(...)

# ❌ 不碰 self 却用实例方法 → 误导“依赖实例”，且无法不建实例调用
class Temperature:
    def is_freezing(self, c):                # 应为 @staticmethod
        return c <= 0

# ❌ property 里塞重计算 / I/O → 调用方以为是廉价取值，反复触发慢操作
    @property
    def report(self):
        return requests.get(url).json()      # property 不该有网络请求，改成方法
```

理由：`@classmethod` 用 `cls` 才支持继承多态；`@staticmethod` 让“不依赖实例”可被静态检查与调用方一眼看出；`@property` 的契约是“像取字段一样廉价无副作用”，违背它会让调用方踩性能坑。

## 自检

- [ ] 备用构造器是 `@classmethod` 且 `return cls(...)`，没硬编码类名？
- [ ] 不读写 `self`/`cls` 的函数标了 `@staticmethod`？
- [ ] `@property` 只包无副作用、廉价的计算，没塞 I/O 或重计算？
- [ ] 需要赋值校验时才加 `@x.setter`，否则保持只读？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`descriptor-protocol.md`](./descriptor-protocol.md)（property 多个字段复用时的底层机制） · [`mro-super.md`](./mro-super.md)（继承时方法解析顺序）
