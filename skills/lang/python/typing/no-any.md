---
name: python-no-any
description: 禁 Any — 必要时用 Union / TypeVar / 类型守卫。Use when 写 Python 后端代码 / 评审涉及 `no-any`
  的 PR。
parent: ./index.md
paths:
- backend/**/*.py
- py/**/*.py
triggers:
  keywords:
  - Any
  - Union
  - TypeVar
  - 类型守卫
effort: medium
context: inline
version: '1.0'
---
# Python · 禁 Any

## 规则

**禁用 `typing.Any`**。必要时用 `Union[A, B]` / `TypeVar` / 类型守卫缩窄。

## 为什么

`Any` 是类型系统的逃逸口——一旦出现，pyright/mypy 沿着这条链路完全失效。后续 Refactor 改了上游类型，下游用 `Any` 的地方静默坏掉。

## 替代方案

### 1. Union（多种已知类型）

```python
# ❌
def parse(data: Any) -> Any: ...

# ✅
def parse(data: str | bytes | dict) -> ParsedResult: ...
```

### 2. TypeVar（泛型）

```python
from typing import TypeVar

T = TypeVar("T", bound=BaseModel)

async def fetch_one(model: type[T], id: int) -> T | None:
    return await model.filter(id=id).first()
```

### 3. 类型守卫（窄化 unknown）

```python
from typing import TypeGuard

def is_str_list(v: object) -> TypeGuard[list[str]]:
    return isinstance(v, list) and all(isinstance(x, str) for x in v)

def process(data: object):
    if is_str_list(data):
        # 这里 data 已经被守卫缩窄成 list[str]
        return ",".join(data)
```

### 4. JSON 任意结构

```python
# 与外部 JSON 交互不可避免（如 task.result 字段）
JsonValue = str | int | float | bool | None | list["JsonValue"] | dict[str, "JsonValue"]

# 比 Any 强：保留了 JSON 的递归结构
```

## 例外（极少数）

| 场景 | 处理 |
|------|------|
| 第三方 SDK 返回未声明类型 | 立即 cast / 守卫 narrow，不再向下游传 Any |
| 测试 mock | tests/ 下允许 |
| 元编程（`__getattr__` 等） | 加 `# type: ignore[no-any-return]` 注释说明 |

## 检测

```bash
# Pyright strict 自动报
uv run pyright

# 或 grep
grep -RIn "import Any\|: Any" --include="*.py" backend/ py/
```

## 自检

- [ ] 业务代码无 `Any`？
- [ ] 测试代码的 `Any` 已加注释？
- [ ] 第三方未声明类型立即守卫 narrow，不向下传？

## 相关

- 父：[`./index.md`](./index.md)
- 配套：[`strict-annotations.md`](./strict-annotations.md)

