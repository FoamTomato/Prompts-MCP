---
name: fastapi-llm-config-env
description: LLM 环境变量配置 — DASHSCOPE_API_KEY / OPENAI_API_KEY
parent: ./index.md
paths:
  - "backend/core/config.py"
  - "py/core/config.py"
  - ".env*"
triggers:
  keywords: [DASHSCOPE_API_KEY, OPENAI_API_KEY, 环境变量]
effort: medium
context: inline
version: "1.0"
---

# LLM · 环境变量配置

## 完整 .env 模板

```bash
# .env.example

# ===== 通义千问（主） =====
DASHSCOPE_API_KEY=sk-xxx
DASHSCOPE_MODEL=qwen-plus
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# ===== OpenAI 兼容代理（备） =====
OPENAI_API_KEY=sk-xxx
OPENAI_MODEL=gpt-4o-mini
OPENAI_BASE_URL=https://api.openai.com/v1   # 或代理 URL

# ===== 通义万相（生图） =====
WANX_API_KEY=sk-xxx
WANX_MODEL=wanx-v1

# ===== LLM 通用 =====
LLM_TIMEOUT_SEC=60
LLM_MAX_RETRIES=2
LLM_FALLBACK_ENABLED=true

# ===== 限流 =====
LLM_RPM_PER_USER=10            # 单用户每分钟最多 10 次
LLM_TPM_PER_USER=20000         # 单用户每分钟最多 20K token
```

## pydantic-settings 加载

```python
# backend/core/config.py
from pydantic_settings import BaseSettings
from pydantic import Field

class LLMSettings(BaseSettings):
    dashscope_api_key: str = Field(..., env="DASHSCOPE_API_KEY")
    dashscope_model: str = Field("qwen-plus", env="DASHSCOPE_MODEL")
    dashscope_base_url: str = Field(
        "https://dashscope.aliyuncs.com/compatible-mode/v1",
        env="DASHSCOPE_BASE_URL",
    )

    openai_api_key: str | None = Field(None, env="OPENAI_API_KEY")
    openai_model: str = Field("gpt-4o-mini", env="OPENAI_MODEL")
    openai_base_url: str = Field("https://api.openai.com/v1", env="OPENAI_BASE_URL")

    timeout_sec: int = Field(60, env="LLM_TIMEOUT_SEC")
    max_retries: int = Field(2, env="LLM_MAX_RETRIES")
    fallback_enabled: bool = Field(True, env="LLM_FALLBACK_ENABLED")

    rpm_per_user: int = Field(10, env="LLM_RPM_PER_USER")
    tpm_per_user: int = Field(20000, env="LLM_TPM_PER_USER")

    class Config:
        env_file = ".env"

llm_settings = LLMSettings()
```

## 不同环境覆盖

```
.env                   # 本地默认（不提交）
.env.example           # 模板（提交）
.env.production        # 生产（CI/CD 注入，不提交）
```

`.gitignore` 必须包含 `.env*`（除 `.env.example`）。

## 自检

- [ ] `.env.example` 列出所有 key 字段？
- [ ] `.env` 在 `.gitignore`？
- [ ] 用 pydantic-settings 加载？
- [ ] 没在代码里硬编码 API Key？
- [ ] 生产环境通过 CI/CD secret 注入？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`provider-selection.md`](./provider-selection.md) · [`sse-protocol.md`](./sse-protocol.md) · [`error-fallback.md`](./error-fallback.md)

