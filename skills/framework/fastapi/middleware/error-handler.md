---
name: fastapi-error-handler
description: 全局异常处理中间件 — 捕获 ApiException + 兜底 500
parent: ./index.md
paths:
  - "backend/middleware/**/*.py"
  - "py/middleware/**/*.py"
triggers:
  keywords: [middleware, exception_handler, ApiException]
effort: medium
context: inline
version: "1.0"
---

# FastAPI Middleware · 全局错误处理

## 规则

通过 `@app.exception_handler` 注册全局异常映射，**不要在每个 router 内重复 try/catch HTTPException**。

## 实现

```python
# backend/middleware/error_handler.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

from core.exceptions import ApiException
from core.response import JsonData

logger = logging.getLogger(__name__)

def setup_error_handlers(app: FastAPI):

    @app.exception_handler(ApiException)
    async def api_exc_handler(req: Request, exc: ApiException):
        return JSONResponse(
            status_code=exc.code,
            content=JsonData.error(msg=exc.msg, code=exc.code).model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_handler(req: Request, exc: RequestValidationError):
        # Pydantic 校验失败
        errors = exc.errors()
        msg = "; ".join(f"{'.'.join(map(str, e['loc']))}: {e['msg']}" for e in errors)
        return JSONResponse(
            status_code=422,
            content=JsonData.error(msg=msg, code=422).model_dump(),
        )

    @app.exception_handler(Exception)
    async def fallback_handler(req: Request, exc: Exception):
        logger.exception(
            f"unhandled: path={req.url.path} method={req.method}",
        )
        return JSONResponse(
            status_code=500,
            content=JsonData.error(msg="服务繁忙，请稍后重试", code=500).model_dump(),
        )
```

## 在 main.py 注册

```python
# backend/main.py
from fastapi import FastAPI
from middleware.error_handler import setup_error_handlers

app = FastAPI()
setup_error_handlers(app)
```

## 业务异常类

```python
# backend/core/exceptions.py
class ApiException(Exception):
    def __init__(self, msg: str, code: int = 400, error_code: str | None = None):
        self.msg = msg
        self.code = code
        self.error_code = error_code
        super().__init__(msg)
```

## 业务使用

```python
# 任何 service 内
if not user.has_quota:
    raise ApiException(msg="积分不足", code=403, error_code="B402")
```

中间件统一返回：

```json
{
  "success": false,
  "msg": "积分不足",
  "code": 403,
  "data": null
}
```

## 反例

```python
# ❌ 每个 endpoint 重复 try/catch
@router.post("/foo")
async def foo():
    try:
        return await service_foo()
    except ApiException as e:
        return JSONResponse(status_code=e.code, content={...})
    except Exception:
        return JSONResponse(status_code=500, content={...})
```

## 自检

- [ ] 业务用 `raise ApiException(...)` 不用 HTTPException？
- [ ] 全局 handler 注册 3 种：ApiException / RequestValidationError / Exception？
- [ ] fallback handler 用 `logger.exception` 带 traceback？
- [ ] 不在 endpoint 内重复 try/catch？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`anonymous-session.md`](./anonymous-session.md)
- 配套：[`../../../lang/python/error-handling/api-exception.md`](../../../lang/python/error-handling/api-exception.md)

