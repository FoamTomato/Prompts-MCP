---
name: ai-llm-engineering-index
description: LLM 调用工程规范七件事 — prompt 版本化 / 流式 SSE / TPM+RPM 限流 / 重试熔断 / 结构化输出 / 缓存 / 可观测性。Use when 设计 LLM 网关 / 上线大模型调用链 / 评审调用韧性与成本时。
parent: ../index.md
children:
  - { name: prompt-management, path: prompt-management.md, tag: skill, note: "prompt 版本化 + 模板外置 + 格式/范围/长度约束" }
  - { name: streaming-sse, path: streaming-sse.md, tag: skill, note: "流式默认 SSE，token 边到边 flush" }
  - { name: rate-limit-token, path: rate-limit-token.md, tag: skill, note: "网关 TPM+RPM 双限流 + 按 token 实时算成本" }
  - { name: retry-degradation, path: retry-degradation.md, tag: skill, note: "指数退避 full jitter + 区分瞬时/结构性 + 熔断" }
  - { name: structured-output, path: structured-output.md, tag: skill, note: "强制 JSON schema/function calling + 每次响应 schema 校验" }
  - { name: caching, path: caching.md, tag: skill, note: "普通缓存 + 语义缓存 + 供应商 prompt caching" }
  - { name: observability, path: observability.md, tag: skill, note: "追踪 prompt/response/token/延迟 + 按调用归集成本" }
when_to_descend: 在设计 LLM 调用网关、做调用韧性/成本治理或评审大模型调用链
---

# LLM Engineering · 子项索引

LLM 调用工程拆成七个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 管理 prompt（版本化、模板外置、写约束） | [prompt-management](prompt-management.md) |
| 把模型输出流式推给前端 | [streaming-sse](streaming-sse.md) |
| 在网关层做限流并算成本 | [rate-limit-token](rate-limit-token.md) |
| 处理调用失败的重试、降级与熔断 | [retry-degradation](retry-degradation.md) |
| 要求模型返回可解析的结构化结果 | [structured-output](structured-output.md) |
| 用缓存省 token / 降延迟 | [caching](caching.md) |
| 给整条调用链做埋点、追踪与成本归集 | [observability](observability.md) |

> 韧性栈顺序：请求队列(TPM/RPM 双限) → 熔断(错误率+成本+延迟) → 网关(指数退避+full jitter 重试) → LLM。
> 文中省钱比例为第三方观察的**量级参考**，需用自有调用数据复测后定参。
