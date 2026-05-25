---
name: fastapi-anonymous-session
description: 匿名会话中间件 — anon_xxx + 双积分池
parent: ./index.md
paths:
  - "backend/middleware/anonymous_session.py"
  - "py/middleware/anonymous_session.py"
triggers:
  keywords: [anonymous, session, anon_, middleware]
effort: medium
context: inline
version: "1.0"
---

# FastAPI Middleware · 匿名 Session

## 规则

Quill 是匿名 + 邀请的模式。每个请求必须带 `X-Session-Id`（`anon_<uuid>` 格式），中间件自动加载 session 上下文。

## 中间件实现

```python
# backend/middleware/anonymous_session.py
from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)

EXEMPT_PATHS = {"/health", "/docs", "/openapi.json", "/redoc"}

class AnonymousSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if any(request.url.path.startswith(p) for p in EXEMPT_PATHS):
            return await call_next(request)

        session_id = request.headers.get("X-Session-Id")
        if not session_id or not session_id.startswith("anon_"):
            return JSONResponse(
                status_code=401,
                content={"success": False, "msg": "missing or invalid X-Session-Id", "code": 401},
            )

        # 加载 / 创建 session
        session = await SessionRepo.get_or_create(session_id)
        if session.is_blocked:
            return JSONResponse(
                status_code=403,
                content={"success": False, "msg": "session blocked", "code": 403},
            )

        # 注入到 request.state，供后续依赖读取
        request.state.session = session

        response = await call_next(request)
        return response
```

## 注册

```python
# backend/main.py
app.add_middleware(AnonymousSessionMiddleware)
```

## 依赖读取

```python
# core/deps.py
from fastapi import Request

async def get_current_session(request: Request):
    if not hasattr(request.state, "session"):
        raise HTTPException(status_code=401, detail="no session")
    return request.state.session
```

## 双积分池约定

详见 `project-index/modules/anonymous_session.md`（S1-S6）。中间件层只负责加载 session，**不扣减积分**——扣减逻辑在 Service 层。

```python
class Session(Model):
    session_id = fields.CharField(max_length=64, pk=True)  # anon_<uuid>
    base_credits = fields.IntField(default=10)
    bonus_credits = fields.IntField(default=0)
    base_credits_lifetime = fields.IntField(default=10)
    bonus_credits_lifetime = fields.IntField(default=0)
    invite_code = fields.CharField(max_length=16, null=True)
    invited_by_code = fields.CharField(max_length=16, null=True)
    is_blocked = fields.BooleanField(default=False)
    risk_score = fields.IntField(default=0)
    ...
```

## 与反爬虫协同

`AntiCrawlerMiddleware`（anti_crawler 模块 AC1）在 `AnonymousSessionMiddleware` **之前**运行——先评分再加载。详见 `project-index/modules/anti_crawler.md`。

## 自检

- [ ] 中间件加载顺序：AntiCrawler → AnonymousSession → Auth → Logging？
- [ ] 排除路径不需要 session（/health / /docs）？
- [ ] is_blocked session 直接 403？
- [ ] session 挂在 request.state.session？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`error-handler.md`](./error-handler.md)
- 配套：`project-index/modules/anonymous_session.md` · `project-index/modules/anti_crawler.md`

