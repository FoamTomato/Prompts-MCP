---
name: py-typing-protocol-structural
description: Protocol 结构化子类型 + runtime_checkable，按行为而非继承约定接口。Use when 定义鸭子类型接口 / 解耦实现与协议 / 替代 ABC 强制继承。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 结构化子类型
  - Protocol
  - runtime_checkable
  - duck typing
  - 接口
effort: medium
context: inline
version: '1.0'
---
# Python · Protocol 结构化子类型

## 规则

用 `typing.Protocol` 按**结构（有哪些方法/属性）**定义接口，而非靠继承（名义子类型）。任何对象只要形状匹配就被认作该类型——无需显式 `class Impl(MyProto)`。需要 `isinstance` 检查时加 `@runtime_checkable`。

| 维度 | ABC（名义） | Protocol（结构） |
|------|------|------|
| 匹配方式 | 必须显式继承 | 形状匹配即可 |
| 第三方类型 | 改不了源码就无法适配 | 自动适配 |
| `isinstance` | 始终支持 | 需 `@runtime_checkable` |

## 正例

```python
from typing import Protocol, runtime_checkable

class SupportsClose(Protocol):
    def close(self) -> None: ...

# 任何有 close() 的对象都满足——文件、连接、客户端
def cleanup(resource: SupportsClose) -> None:
    resource.close()

# 带泛型的 Protocol（PEP 695 语法）
class Repository[T](Protocol):
    async def get(self, id: int) -> T | None: ...
    async def save(self, item: T) -> None: ...

# 运行时可检查：仅检查方法是否存在
@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> str: ...

def render(obj: object) -> str:
    if isinstance(obj, Drawable):
        return obj.draw()
    return repr(obj)
```

## 反例

```python
# ❌ 为了类型约束强制业务类继承框架基类，造成耦合
class MyService(SomeFrameworkBase):  # 只为满足 isinstance
    ...

# ❌ runtime_checkable 误以为会校验签名——它只看方法名是否存在
@runtime_checkable
class HasRun(Protocol):
    def run(self, x: int) -> int: ...

isinstance(obj, HasRun)   # obj.run 参数/返回不匹配也返回 True，别依赖它做强校验

# ❌ 该用结构接口却写了一个空 ABC + 到处显式继承
import abc
class Closer(abc.ABC):
    @abc.abstractmethod
    def close(self) -> None: ...   # 第三方类无法适配，改用 Protocol
```

## 自检

- [ ] 接口按行为定义，没有为类型而强制继承？
- [ ] 需要 `isinstance` 才加 `@runtime_checkable`，且只依赖它判断方法存在（不校验签名）？
- [ ] 第三方/无法改源码的类型用 Protocol 适配？
- [ ] 泛型 Protocol 用 `class P[T](Protocol)`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`pep695-generics.md`](./pep695-generics.md) · [`type-narrowing.md`](./type-narrowing.md)
