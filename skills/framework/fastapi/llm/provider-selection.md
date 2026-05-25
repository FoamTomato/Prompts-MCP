---
name: fastapi-llm-provider-selection
description: LLM 主备选型 — 通义千问主 / OpenAI 备 / 通义万相生图
parent: ./index.md
paths:
  - "backend/services/llm_*.py"
  - "py/services/llm_*.py"
  - "backend/agents/**/*"
  - "py/agents/**/*"
triggers:
  keywords: [LLM, 通义, OpenAI, provider]
effort: medium
context: inline
version: "1.0"
---

# LLM · Provider 主备选型

## 主备方案

| 角色 | Provider | 模型 | 用途 |
|------|---------|------|------|
| **主** | 通义千问（DashScope） | `qwen-plus` / `qwen-max` | 大纲生成、文本编辑、备注生成 |
| **备** | OpenAI 兼容代理 | `gpt-4o-mini` | 通义不可用时降级 |
| **生图** | 通义万相 / DALL·E 3 | `wanx-v1` / `dall-e-3` | M7 AI 生图、M14 配图建议 |

## 选择依据

- **通义千问主**：国内访问稳定、对中文/教育场景友好、价格低（qwen-plus ¥0.004/1K token），无需走代理
- **OpenAI 备**：作为容灾；公司若已有 API key 可直接复用
- **生图独立**：图片生成对延迟和合规要求不同，单独走通义万相

## 不选用

| Provider | 原因 |
|---------|------|
| Claude API | 国内访问需代理，rate limit 易超 |
| 本地模型（Llama / Qwen 本地版） | MVP 阶段算力不划算，等用户量起来后再评估 |
| Azure OpenAI | 需企业账户，流程复杂；MVP 不用 |

## 决策矩阵

|  | 中文质量 | 价格 | 国内稳定性 | 中文 SSE 支持 |
|--|---------|------|----------|------------|
| qwen-plus | ✅ | ✅ | ✅ | ✅ |
| qwen-max | ✅✅ | ⚠️ | ✅ | ✅ |
| gpt-4o-mini | ✅ | ✅ | ⚠️（需代理） | ✅ |
| claude-3-haiku | ✅ | ✅ | ❌（国内不稳） | ✅ |

## 切换 / 降级

降级策略详见 [`error-fallback.md`](./error-fallback.md)。

## 自检

- [ ] 主用通义千问？
- [ ] 备用 OpenAI 兼容代理？
- [ ] 没引入 Claude / 本地模型？
- [ ] 生图独立用通义万相？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`config-env.md`](./config-env.md) · [`error-fallback.md`](./error-fallback.md) · [`sse-protocol.md`](./sse-protocol.md)
- 配套：[`../../../design-pattern/factory/llm-provider-factory.md`](../../../design-pattern/factory/llm-provider-factory.md)

