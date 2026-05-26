---
name: fastapi-schema-response-model
description: '@router 必带 response_model — 类型即文档。Use when 写 Python 后端代码 / 评审涉及 `response-model-required`
  的 PR。'
parent: ./index.md
paths:
- backend/routers/**/*.py
- py/routers/**/*.py
triggers:
  keywords:
  - response_model
  - '@router.post'
  - '@router.get'
  - 类型即文档
effort: medium
context: inline
version: '1.0'
---
# FastAPI Schema · response_model 必填

## 规则

每个 `@router.<method>` 装饰器**必须**带 `response_model=...`。这是 FastAPI 文档生成、类型检查、序列化的统一入口。

## 标准

```python
@router.post("/create", response_model=JsonData[PresentationResp])
async def create(req: PresentationCreateReq, user=Depends(get_current_user)):
    result = await service_create(req, user["account_id"])
    return JsonData.success(result)
```

## JsonData 统一包装

```python
# backend/core/response.py
from typing import Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")

class JsonData(BaseModel, Generic[T]):
    success: bool = Field(True, description="是否成功")
    data: T | None = Field(None, description="业务数据")
    msg: str | None = Field(None, description="提示信息")
    code: int | None = Field(None, description="业务错误码")

    @classmethod
    def success(cls, data: T, msg: str | None = None):
        return cls(success=True, data=data, msg=msg)

    @classmethod
    def error(cls, msg: str, code: int = 400):
        return cls(success=False, msg=msg, code=code)
```

## OpenAPI 文档自动生成

response_model 让 FastAPI 自动生成 OpenAPI schema，前端能根据 `/docs` 看到准确类型：

```
GET  /docs        → Swagger UI
GET  /redoc       → ReDoc UI
GET  /openapi.json → 原始 schema
```

## SSE 流式 response_model

SSE 不能用 response_model（流式不固定 schema），改用注释 + 文档：

```python
@router.post(
    "/stream",
    response_class=StreamingResponse,
    responses={200: {"content": {"text/event-stream": {}}}},
)
async def stream_outline(req: OutlineGenReq) -> StreamingResponse:
    return StreamingResponse(generate_outline_stream(req), media_type="text/event-stream")
```

## 反例

```python
# ❌ 无 response_model
@router.post("/create")
async def create(req: ...) -> Any:
    return {"id": ..., "title": ...}

# 后果：
# 1. OpenAPI 文档缺类型
# 2. 返回字段未被 Pydantic 过滤（可能泄露内部字段）
# 3. 类型检查无法捕捉错误
```

## 自检

- [ ] 每个 endpoint 都有 response_model？
- [ ] 用 `JsonData[T]` 统一包装？
- [ ] SSE 用 response_class + responses 注释？
- [ ] /docs 能看到完整 schema？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`pydantic-v2-base.md`](./pydantic-v2-base.md)

