---
name: fastapi-llm-sse-protocol
description: LLM SSE 协议 — 流式 chunk + done 终止。Use when 写 Python 后端代码 / 评审涉及 `sse-protocol`
  的 PR。
parent: ./index.md
paths:
- backend/services/**/*.py
- py/services/**/*.py
- backend/agents/**/*
- py/agents/**/*
triggers:
  keywords:
  - SSE
  - stream
  - chunk
  - done
  - 流式
effort: medium
context: inline
version: '1.0'
---
# LLM · SSE 协议

## 协议约定

每个 LLM 流式调用通过 SSE 推送 chunk。前端通过 `useSSE` hook 接收。

## 帧格式

```
data: {"chunk":"第一段","msg":""}\n\n
data: {"chunk":"第二段","msg":""}\n\n
data: {"chunk":"","msg":"done","total_tokens":1234}\n\n
```

| 字段 | 说明 |
|------|------|
| `chunk` | LLM 当前 token / 文本片段 |
| `msg` | "" 正常 / "done" 完成 / "error" 失败 |
| `total_tokens` | 完成时附带（用于配额扣减） |
| `error` | 失败时附带错误信息 |

## Service 层模板

```python
# backend/services/outline_generator.py
from typing import AsyncGenerator
from langchain_core.output_parsers import StrOutputParser

from core.response import JsonData
from services.llm_client import get_llm

async def generate_outline_stream(req: OutlineGenReq) -> AsyncGenerator[str, None]:
    llm = get_llm(req.provider or "qwen")
    prompt = build_outline_prompt(req)
    chain = prompt | llm | StrOutputParser()

    total_tokens = 0
    try:
        async for chunk in chain.astream(req.dict()):
            if not chunk: continue
            total_tokens += estimate_tokens(chunk)
            payload = JsonData.stream_data(chunk.encode("utf-8")).model_dump_json()
            yield f"data: {payload}\n\n"

        # 完成 — 附带 token 数
        done = JsonData.stream_data(b"", msg="done", total_tokens=total_tokens).model_dump_json()
        yield f"data: {done}\n\n"

        # 扣积分
        await deduct_credits(req.user_id, total_tokens // 1000)

    except Exception as e:
        logger.exception(f"outline stream failed: {e}")
        err = JsonData.stream_data(b"", msg="error", error=str(e)).model_dump_json()
        yield f"data: {err}\n\n"
```

## 前端解析

```ts
// src/hooks/useSSE.ts
const blocks = buffer.split("\n\n");
for (const block of blocks) {
  const event = parseSseBlock(block);
  if (event.msg === "done") { ... }
  else if (event.msg === "error") { ... }
  else { /* 累积 chunk */ }
}
```

## 心跳（可选）

长时间无 chunk 时每 15s 发心跳避免 nginx 超时：

```python
yield ":keepalive\n\n"   # 注释帧（前端忽略）
```

## 自检

- [ ] 每帧 `data: ...\n\n` 双换行？
- [ ] 完成发 done 帧带 total_tokens？
- [ ] 失败发 error 帧不 raise？
- [ ] 长生成加心跳？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`provider-selection.md`](./provider-selection.md) · [`error-fallback.md`](./error-fallback.md)
- 配套：[`../router/sse-streaming.md`](../router/sse-streaming.md) · [`../../../lang/python/async/sse-streaming.md`](../../../lang/python/async/sse-streaming.md)

