---
name: python-strict-annotations
description: 函数签名 100% 类型注解 — 含返回类型
parent: ./index.md
paths:
  - "backend/**/*.py"
  - "py/**/*.py"
triggers:
  keywords: [type hint, mypy, annotation, 类型注解]
effort: medium
context: inline
version: "1.0"
---

# Python · 100% 类型注解

## 规则

**所有函数签名必须含完整类型注解**：参数 + 返回值 + raise（写在 docstring）。

```python
async def service_create_presentation(
    req: PresentationCreateReq,
    user_id: int,
    redis_pool: Redis,
) -> PresentationResponse:
    """创建课件 — Service 编排

    Args:
        req: 创建请求
        user_id: 当前用户 ID
        redis_pool: Redis 连接池

    Returns:
        创建后的课件响应

    Raises:
        ApiException: 配额不足 / 参数错误
    """
    ...
```

## 关键工具：Pyright / mypy strict

`pyproject.toml`：
```toml
[tool.pyright]
typeCheckingMode = "strict"
reportMissingTypeArgument = "error"
reportUnknownArgumentType = "error"
reportUnknownVariableType = "error"
```

CI:
```bash
uv run pyright
```

## 命名约定（与类型配合）

| 含义 | 类型 |
|------|------|
| 可选参数 | `value: int \| None = None` |
| 集合 | `users: list[User]` / `user_map: dict[int, User]` |
| 异步生成器 | `AsyncGenerator[str, None]` |
| Callback | `on_finish: Callable[[Result], None]` |
| 协程返回 | `async def f() -> Result` |

## 反例

```python
# ❌ 缺返回类型
async def list_users(uid):
    return await User.filter(owner=uid)

# ❌ 用 Any 兜底
def process(data: Any) -> Any:
    ...

# ❌ 旧式 typing
from typing import List, Dict
def f() -> List[Dict]: ...   # → list[dict]（Py 3.9+）
```

## 配套：Pydantic Field 必填 description

详见 [`pydantic-v2-field.md`](./pydantic-v2-field.md)。

## 自检

- [ ] 每个 `def` / `async def` 有返回类型？
- [ ] 没有 `Any`（必要时用 `Union` / 类型守卫）？
- [ ] 用现代语法 `list[X]` / `dict[K,V]` / `X | None` 而非 `List`/`Optional`？
- [ ] Pyright strict 跑过？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`pydantic-v2-field.md`](./pydantic-v2-field.md) · [`no-any.md`](./no-any.md)

