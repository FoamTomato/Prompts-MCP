---
name: fastapi-router-di
description: Depends 依赖注入 — current_user / redis_pool / db
parent: ./index.md
paths:
  - "backend/routers/**/*.py"
  - "py/routers/**/*.py"
triggers:
  keywords: [Depends, 依赖注入, current_user]
effort: medium
context: inline
version: "1.0"
---

# FastAPI Router · Depends 依赖注入

## 规则

Router 用 `Depends` 注入依赖（current_user / redis_pool / db）。Service 通过参数接收。

## 标准依赖

```python
# core/deps.py
from fastapi import Depends, Header, HTTPException
from typing import Annotated

async def get_session_id(x_session_id: Annotated[str | None, Header()] = None) -> str:
    if not x_session_id:
        raise HTTPException(status_code=401, detail="missing X-Session-Id")
    return x_session_id

async def get_current_user(session_id: Annotated[str, Depends(get_session_id)]) -> dict:
    session = await SessionRepo.find(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="invalid session")
    return {"account_id": session.user_id, "session_id": session.id}

async def get_redis_pool():
    # 从应用 lifespan 注入的连接池获取
    ...

async def get_db():
    # Tortoise 连接管理通常无需手工取，但若用 raw conn 时:
    async with conn_pool.acquire() as conn:
        yield conn
```

## Router 注入

```python
@router.post("/create")
async def create(
    req: CreateReq,
    current_user: Annotated[dict, Depends(get_current_user)],
    redis_pool=Depends(get_redis_pool),
):
    result = await service_create(req, current_user["account_id"], redis_pool)
    return JsonData.success(result)
```

## 子依赖（依赖嵌套）

```python
async def get_current_admin(
    user: Annotated[dict, Depends(get_current_user)],
) -> dict:
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="admin only")
    return user

@router.post("/admin/foo")
async def admin_foo(admin: Annotated[dict, Depends(get_current_admin)]):
    ...
```

## 路由级 Depends（全路由 require auth）

```python
admin_router = APIRouter(
    prefix="/api/admin",
    tags=["Admin"],
    dependencies=[Depends(get_current_admin)],   # 路由级
)

# 所有 admin_router 下的 endpoint 自动 require admin
```

## 反例

```python
# ❌ Router 内手工读 header / 查 DB
@router.post("/create")
async def create(req: CreateReq, request: Request):
    session_id = request.headers.get("X-Session-Id")
    session = await SessionRepo.find(session_id)
    if not session:
        raise HTTPException(401)
    ...

# ✅ 抽到依赖
@router.post("/create")
async def create(req: CreateReq, user: Annotated[dict, Depends(get_current_user)]):
    ...
```

## 测试时 override

```python
# tests/conftest.py
app.dependency_overrides[get_current_user] = lambda: {"account_id": 1, "session_id": "test"}
```

## 自检

- [ ] 鉴权 / DB / Redis 用 Depends 注入？
- [ ] 公共依赖在 `core/deps.py`？
- [ ] 测试用 `dependency_overrides` mock？
- [ ] 路由级要求统一鉴权时用 `APIRouter(dependencies=[...])`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`zero-logic-principle.md`](./zero-logic-principle.md)

