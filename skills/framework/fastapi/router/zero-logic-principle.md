---
name: fastapi-router-zero-logic
description: Router 零逻辑 — 只做接收/注入/调用/返回，3 行内
parent: ./index.md
paths:
- backend/routers/**/*.py
- py/routers/**/*.py
triggers:
  keywords:
  - '@router'
  - APIRouter
  - FastAPI
  - 零逻辑
  - 只做接收
  - 注入
effort: medium
context: inline
version: '1.0'
---
# FastAPI Router · 零逻辑

## 规则

Router 只做 4 件事：**接收 → 注入 → 调用 → 返回**。三行以内。

## 标准模板

```python
# backend/routers/textbooks.py
from fastapi import APIRouter, Depends
from schemas.textbook import TextbookListReq, TextbookListResp
from services.textbook import service_list_textbooks
from core.response import JsonData
from core.deps import get_current_user, get_redis_pool

router = APIRouter(prefix="/api/textbooks", tags=["Textbook"])

@router.post("/list", response_model=JsonData[TextbookListResp])
async def list_textbooks(
    req: TextbookListReq,
    current_user=Depends(get_current_user),
    redis_pool=Depends(get_redis_pool),
):
    result = await service_list_textbooks(
        req=req,
        user_id=current_user["account_id"],
        redis_pool=redis_pool,
    )
    return JsonData.success(result)
```

## 反例

```python
# ❌ Router 写业务逻辑
@router.post("/list")
async def list_textbooks(req: TextbookListReq):
    if req.subject == "math":
        items = await Textbook.filter(subject="math").all()  # 直接查 DB
    else:
        items = await Textbook.all()

    for item in items:                                       # 业务规则
        if item.is_premium and not current_user.is_paid:
            item.locked = True

    return [t.dict() for t in items]                          # 手工序列化
```

## 正确分工

| 层 | 职责 |
|----|------|
| Router | 接收 / 注入 / 调用 / 返回 |
| Service | 业务编排（校验、查询、Agent 调用、组装） |
| Adapter | ORM → Pydantic 规整 |
| Model | Tortoise ORM 表定义 |

## response_model 必填

```python
# ✅
@router.post("/create", response_model=JsonData[PresentationResp])
async def create(...): ...

# ❌ 不写 response_model 等于失去类型检查
@router.post("/create")
async def create(...) -> Any: ...
```

## SSE 流式响应

详见 [`sse-streaming.md`](./sse-streaming.md)。

## 自检

- [ ] Router 函数体 ≤ 5 行？
- [ ] 不直接查 DB（不 import Tortoise Model）？
- [ ] 不写 if/for 业务判断？
- [ ] response_model 必填？
- [ ] 用 `Depends` 注入依赖？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`sse-streaming.md`](./sse-streaming.md) · [`dependency-injection.md`](./dependency-injection.md)
- 配套：[`../../../design-pattern/ddd-layering/controller-thin.md`](../../../design-pattern/ddd-layering/controller-thin.md)

