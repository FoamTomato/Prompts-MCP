---
name: fastapi-router-sse
description: SSE 流式响应模板 — StreamingResponse + text/event-stream
parent: ./index.md
paths:
  - "backend/routers/**/*.py"
  - "py/routers/**/*.py"
triggers:
  keywords: [StreamingResponse, SSE, event-stream]
effort: medium
context: inline
version: "1.0"
---

# FastAPI Router · SSE 流式

## 规则

LLM 生成、长任务进度推送等流式场景**必须用 SSE**（Server-Sent Events），不要用 WebSocket（除非真的需要双向）。

## Router 模板

```python
# backend/routers/outlines.py
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from schemas.outline import OutlineGenReq
from services.outline_generator import generate_outline_stream

router = APIRouter(prefix="/api/outlines", tags=["Outline"])

@router.post("/stream")
async def stream_outline(req: OutlineGenReq):
    return StreamingResponse(
        generate_outline_stream(req),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",   # nginx 不缓冲
            "Connection": "keep-alive",
        },
    )
```

## Service 层（生成器）

```python
# backend/services/outline_generator.py
from typing import AsyncGenerator
from core.response import JsonData

async def generate_outline_stream(req: OutlineGenReq) -> AsyncGenerator[str, None]:
    chain = build_outline_prompt(req) | get_llm_model() | StrOutputParser()

    try:
        async for chunk in chain.astream(req.dict()):
            if not chunk: continue
            payload = JsonData.stream_data(chunk.encode("utf-8")).model_dump_json()
            yield f"data: {payload}\n\n"

        # 必发 done 信号
        done = JsonData.stream_data(b"", msg="done").model_dump_json()
        yield f"data: {done}\n\n"

    except Exception as e:
        logger.exception(f"outline stream failed: {e}")
        err = JsonData.stream_data(b"", msg="error", error=str(e)).model_dump_json()
        yield f"data: {err}\n\n"
```

## SSE 帧格式

```
data: {"chunk":"第一段","msg":""}\n\n
data: {"chunk":"第二段","msg":""}\n\n
data: {"chunk":"","msg":"done"}\n\n
```

**双换行**结束每一帧。

## 前端配合

参见 `frontend/src/hooks/useSSE.ts`。

## nginx 配置（如部署在 nginx 后）

```nginx
location /api/outlines/stream {
    proxy_pass http://backend;
    proxy_http_version 1.1;
    proxy_set_header Connection "";
    proxy_buffering off;          # SSE 必须关缓冲
    proxy_cache off;
    proxy_read_timeout 600s;
}
```

## 反例

```python
# ❌ 缺 done 信号
async for chunk in chain.astream(params):
    yield f"data: {chunk}\n\n"
# 前端永远等不到结束

# ❌ 单换行
yield f"data: {data}\n"   # 必须双换行

# ❌ 直接 raise（无效）
raise ApiException(...)    # 客户端只收到不完整 chunk

# ✅ 通过 SSE error 帧通知
yield f"data: {error_frame}\n\n"
```

## 自检

- [ ] media_type 是 `text/event-stream`？
- [ ] 每帧 `data: ...\n\n`？
- [ ] 完成发 done / 失败发 error 帧？
- [ ] 异常被 catch 后通过 SSE 通知，不 raise？
- [ ] 加 `X-Accel-Buffering: no`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`zero-logic-principle.md`](./zero-logic-principle.md)
- 配套：[`../llm/sse-protocol.md`](../llm/sse-protocol.md) · [`../../../lang/python/async/sse-streaming.md`](../../../lang/python/async/sse-streaming.md)

