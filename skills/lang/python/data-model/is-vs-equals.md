---
name: py-is-vs-equals
description: is 比对象身份（同一个对象）/ == 比值相等；None、True、False 等单例用 is。Use when 不确定写 is 还是 == / 判 None / 被小整数或字符串驻留缓存坑到。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 身份比较
  - is vs ==
  - 单例判断
  - identity comparison
  - 'is None'
effort: low
context: inline
version: '1.0'
---
# Python · is 与 == 的区别

## 规则

| 比较 | 含义 | 何时用 |
|------|------|--------|
| `a is b` | 身份：两个名字指向**同一个对象**（`id(a) == id(b)`） | 比单例：`None` / `True` / `False` / 枚举成员 / 哨兵对象 |
| `a == b` | 相等：值相等（调用 `__eq__`） | 比内容：数字、字符串、容器、值对象 |

铁律：**和单例比一律用 `is` / `is not`；和普通值比一律用 `==`。** 永远不要写 `x == None`。

## 正例

```python
def fetch(uid: int, cache: dict | None = None) -> User:
    if cache is None:               # ✅ 单例用 is
        cache = {}
    if user_name == "":             # ✅ 值用 ==
        ...
    if status is OrderStatus.PAID:  # ✅ Enum 成员是单例，is 更快更准
        ...
```

```python
# 自定义哨兵：当 None 是合法值、需区分“没传”时
_MISSING = object()

def get(key: str, default=_MISSING):
    val = store.get(key, _MISSING)
    if val is _MISSING:             # 身份比较，绝不与真实值冲突
        return default
    return val
```

## 反例

```python
# ❌ 与 None 用 ==：可被 __eq__ 重载误导，linter (ruff E711) 直接报
if x == None: ...

# ❌ 用 is 比值：依赖 CPython 的小整数/字符串驻留，是实现细节，不可靠
a = 1000
b = 1000
print(a is b)        # 可能 False（小整数 -5..256 缓存命中才 True）
print("ab" == "ab")  # ✅ 比值就该用 ==

# ❌ 把 is 当 == 比较容器
[1, 2] is [1, 2]     # False：两个不同对象
[1, 2] == [1, 2]     # ✅ True
```

理由：`is` 比的是内存身份，`1000 is 1000` 的结果取决于解释器是否驻留该对象，**靠 `is` 比数值/字符串是 undefined behavior**。

## 自检

- [ ] 判 None 写的是 `is None` / `is not None`，没有 `== None`？
- [ ] 比数字、字符串、容器内容用的是 `==`？
- [ ] 比 Enum 成员 / 自定义哨兵用的是 `is`？
- [ ] 没有靠 `is` 比较整数 / 字符串字面量来判相等？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`mutable-default-arg.md`](./mutable-default-arg.md)（`is None` 哨兵的典型用例） · [`dunder-protocol.md`](./dunder-protocol.md)（`==` 背后的 `__eq__`）
