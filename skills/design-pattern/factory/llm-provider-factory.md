---
name: factory-llm-provider
description: LLM provider 工厂 — provider_name → ProviderInstance
parent: ./index.md
paths:
  - "backend/services/llm_*.py"
  - "py/services/llm_*.py"
  - "backend/agents/**/*"
  - "py/agents/**/*"
triggers:
  keywords: [factory, provider, LLM]
effort: medium
context: inline
version: "1.0"
---

# Factory · LLM Provider 工厂

## 何时用 Factory

| 信号 | 用 Factory |
|------|-----------|
| 多个实现接口相同，需运行时选 | ✅ |
| 实现需要参数化构造（环境变量等） | ✅ |
| 单一实现 | ❌（直接 new 即可） |
| 需依赖注入 | ✅ |

## Quill LLM Provider Factory

```python
# backend/services/llm_factory.py
from abc import ABC, abstractmethod
from typing import AsyncGenerator
from langchain_community.chat_models import ChatTongyi, ChatOpenAI
from core.config import llm_settings

class LLMProvider(ABC):
    @abstractmethod
    async def astream(self, prompt: str) -> AsyncGenerator[str, None]: ...

class QwenProvider(LLMProvider):
    def __init__(self, model: str = "qwen-plus"):
        self.llm = ChatTongyi(
            model=model,
            dashscope_api_key=llm_settings.dashscope_api_key,
            streaming=True,
        )

    async def astream(self, prompt: str):
        async for chunk in self.llm.astream(prompt):
            yield chunk.content

class OpenAIProvider(LLMProvider):
    def __init__(self, model: str = "gpt-4o-mini"):
        self.llm = ChatOpenAI(
            model=model,
            api_key=llm_settings.openai_api_key,
            base_url=llm_settings.openai_base_url,
            streaming=True,
        )

    async def astream(self, prompt: str):
        async for chunk in self.llm.astream(prompt):
            yield chunk.content


# Factory
PROVIDERS: dict[str, type[LLMProvider]] = {
    "qwen": QwenProvider,
    "openai": OpenAIProvider,
}

def get_llm(provider: str = "qwen", **kwargs) -> LLMProvider:
    if provider not in PROVIDERS:
        raise ValueError(f"unknown provider: {provider}")
    return PROVIDERS[provider](**kwargs)
```

## 使用

```python
llm = get_llm("qwen")
async for chunk in llm.astream(prompt):
    print(chunk)

# 降级到备用
llm = get_llm("openai")
```

## 注册新 Provider

```python
class ClaudeProvider(LLMProvider):
    ...

PROVIDERS["claude"] = ClaudeProvider
```

调用方代码不变（开放 / 封闭原则）。

## 与依赖注入协同

FastAPI 风格：

```python
# core/deps.py
def get_default_llm() -> LLMProvider:
    return get_llm("qwen")

@router.post("/stream")
async def stream(
    req: ...,
    llm: Annotated[LLMProvider, Depends(get_default_llm)],
):
    ...
```

## 反例

```python
# ❌ 在 Service 内 if/else 选 provider
async def generate(prompt: str, provider: str):
    if provider == "qwen":
        llm = ChatTongyi(...)
    elif provider == "openai":
        llm = ChatOpenAI(...)
    # 新增 claude 要改这里所有 service

# ✅ 用工厂
llm = get_llm(provider)
```

## 自检

- [ ] 多个实现继承公共抽象 LLMProvider？
- [ ] 工厂函数 get_llm() 集中创建？
- [ ] 注册表 PROVIDERS 可扩展？
- [ ] 调用方不知道具体类（只用接口）？

## 相关

- 父：[`./index.md`](./index.md)
- 配套：[`../../framework/fastapi/llm/provider-selection.md`](../../framework/fastapi/llm/provider-selection.md)

