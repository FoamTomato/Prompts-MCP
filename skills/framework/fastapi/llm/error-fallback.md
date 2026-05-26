---
name: fastapi-llm-error-fallback
description: LLM 降级与重试 — 主 provider 失败切备用 + 指数退避。Use when 写 Python 后端代码 / 评审涉及 `error-fallback`
  的 PR。
parent: ./index.md
paths:
- backend/services/**/*.py
- py/services/**/*.py
triggers:
  keywords:
  - 降级
  - fallback
  - retry
  - backoff
effort: medium
context: inline
version: '1.0'
---
# LLM · 降级与重试

## 策略

```
主 (qwen-plus)
  ↓ 失败
重试 主（指数退避，最多 2 次）
  ↓ 仍失败
切备 (gpt-4o-mini)
  ↓ 失败
重试 备（最多 1 次）
  ↓ 仍失败
通知前端：暂时不可用
```

## 实现模板

```python
# backend/services/llm_client.py
import asyncio
from typing import AsyncGenerator
from core.config import llm_settings

async def call_with_fallback(
    prompt: str,
    *,
    max_retries: int = 2,
) -> AsyncGenerator[str, None]:
    """主 → 备的流式降级"""

    # 1. 尝试主
    try:
        async for chunk in _call_with_retry("qwen", prompt, max_retries):
            yield chunk
        return
    except Exception as e:
        logger.warning(f"主 provider 失败，切备用: {e}")

    if not llm_settings.fallback_enabled:
        raise ApiException(msg="LLM 主服务不可用", code=503)

    # 2. 切备
    try:
        async for chunk in _call_with_retry("openai", prompt, max_retries=1):
            yield chunk
    except Exception as e:
        logger.exception(f"备用 provider 也失败: {e}")
        raise ApiException(msg="生成服务暂时不可用，请稍后重试", code=503)


async def _call_with_retry(
    provider: str,
    prompt: str,
    max_retries: int,
) -> AsyncGenerator[str, None]:
    """单 provider 指数退避重试"""
    for attempt in range(max_retries + 1):
        try:
            llm = get_llm(provider)
            async for chunk in llm.astream(prompt):
                yield chunk
            return
        except (TimeoutError, ConnectionError, RateLimitError) as e:
            if attempt >= max_retries:
                raise
            wait = 2 ** attempt
            logger.warning(f"{provider} 重试 {attempt + 1}/{max_retries} 等 {wait}s: {e}")
            await asyncio.sleep(wait)
```

## 不重试的异常

| 异常 | 重试？ |
|------|-------|
| `TimeoutError` | ✅ |
| `ConnectionError` | ✅ |
| `RateLimitError` | ✅（按 retry-after 等待） |
| `APIError`（5xx） | ✅ |
| `AuthenticationError` | ❌（凭证错） |
| `InvalidRequestError`（4xx 非 429） | ❌（参数错） |
| `ContentFilterError` | ❌（违规） |

## 何时不降级

- 用户明确指定 provider（"用 OpenAI 生成"）→ 不切换
- 已扣过积分的二次重试 → 通知用户失败而非自动重生成
- 流式生成中途切换 → 实现复杂，不切换（让用户主动重试）

## 自检

- [ ] 主 / 备清晰？
- [ ] 重试用指数退避？
- [ ] 区分可重试和不可重试的异常？
- [ ] 降级前提示用户（前端用 warning toast）？
- [ ] 最终失败 SSE error 帧通知前端？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`provider-selection.md`](./provider-selection.md) · [`sse-protocol.md`](./sse-protocol.md)
- 配套：[`../../../design-pattern/factory/llm-provider-factory.md`](../../../design-pattern/factory/llm-provider-factory.md)

