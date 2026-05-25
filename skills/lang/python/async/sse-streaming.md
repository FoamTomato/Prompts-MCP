---
name: python-sse-streaming
description: SSE 生成器模板 — yield + done 终止信号
parent: ./index.md
paths:
  - "backend/routers/*.py"
  - "py/routers/*.py"
  - "backend/services/*.py"
  - "py/services/*.py"
triggers:
  keywords: [SSE, StreamingResponse, yield, AsyncGenerator, event-stream]
effort: medium
context: inline
version: "1.0"
---

# Python · SSE 流式生成器

## 规则

| 约束 | 说明 |
|------|------|
| 媒体类型 | `text/event-stream` |
| 帧格式 | `data: <json>\n\n`（双换行结尾） |
| 必发 done 信号 | 完成时显式 `yield "data: {...,"msg":"done"}\n\n"` |
| 异步生成器 | `AsyncGenerator[str, None]` |
| 心跳（可选） | 长时间无数据每 15s 发 `:ping\n\n`（注释帧） |

## Service 层模板

```python
# services/outline_generator.py
from typing import AsyncGenerator
from core.response import JsonData

async def generate_outline(req: OutlineReq) -> AsyncGenerator[str, None]:
    chain = build_outline_prompt(req) | get_llm_model() | StrOutputParser()

    try:
        async for chunk in chain.astream(req.dict()):
            if not chunk: continue
            json_str = JsonData.stream_data(chunk.encode("utf-8")).model_dump_json()
            yield f"data: {json_str}\n\n"

        # 必发 done
        end_json = JsonData.stream_data(b"", msg="done").model_dump_json()
        yield f"data: {end_json}\n\n"

    except Exception as e:
        logger.error(f"SSE 失败: {e}", exc_info=True)
        err_json = JsonData.stream_data(b"", msg="error", error=str(e)).model_dump_json()
        yield f"data: {err_json}\n\n"
```

## Router 层模板

```python
# routers/outlines.py
from fastapi.responses import StreamingResponse

@router.post("/outlines/stream")
async def stream_outline(req: OutlineReq):
    return StreamingResponse(
        generate_outline(req),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # nginx 不缓冲
        },
    )
```

## 反例

```python
# ❌ 不发 done 信号 — 前端永远等不到结束
async for chunk in chain.astream(params):
    yield f"data: {chunk}\n\n"
# 缺：done 帧

# ❌ 单换行（无效的 SSE 帧）
yield f"data: {data}\n"      # 必须 \n\n

# ❌ 把异常抛出 — FastAPI 默认不会包成 SSE 错误帧
raise ApiException(msg="...")  # 在 generator 内会让客户端看到不完整 chunk
```

## 前端配合

参见 [`../../../framework/react/state/server-state-tanstack.md`](../../../framework/react/state/server-state-tanstack.md) 和 `frontend/src/hooks/useSSE.ts`。

## 自检

- [ ] 媒体类型 `text/event-stream`？
- [ ] 每帧 `data: ...\n\n`？
- [ ] 完成发 done / 失败发 error 帧？
- [ ] 异常被 catch 后通过 SSE 通知前端，而不是 raise？
- [ ] 加 `X-Accel-Buffering: no` 防 nginx 缓冲？

## 相关

- 父：[`./index.md`](./index.md)
- 配套：[`../../../framework/fastapi/router/sse-streaming.md`](../../../framework/fastapi/router/sse-streaming.md)

