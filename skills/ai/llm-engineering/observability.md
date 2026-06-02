---
name: ai-llm-observability
description: LLM 调用每条 trace 记录 prompt(含版本)/response/token 用量/延迟，并按调用维度归集成本；prompt 版本化是可观测性的前提。Use when 给 LLM 调用链埋点 / 排查回归与延迟 / 评审成本与追踪时。
parent: ./index.md
paths:
- '*.java'
- '*.py'
- '*.md'
triggers:
  keywords:
  - 可观测性
  - LLM 追踪
  - token 用量
  - 成本归集
  - 调用埋点
  - LLM observability
effort: medium
context: inline
version: '1.0'
---
# LLM · 可观测性（追踪 + 成本归集）

> 本条只管「调用链怎么观测」。成本怎么算见 [`rate-limit-token.md`](./rate-limit-token.md)；prompt 版本怎么管见 [`prompt-management.md`](./prompt-management.md)。

## 规则

| 维度 | 要求 |
|------|------|
| 每调用一 trace | 记录输入 prompt（**含版本号**）、模型 response、token 用量、端到端延迟、模型/路由信息 |
| 流式额外指标 | 流式还要记**首 token 延迟(TTFT)**，它比总延迟更反映用户感知 |
| 质量信号 | 记录 schema 校验失败率、降级/熔断触发、缓存命中率，作回归先行指标 |
| 成本归集 | 把每次调用成本按**租户 / 接口 / prompt 版本 / 模型**归集，可下钻定位烧钱点 |
| 版本是前提 | prompt 不版本化就无法把回归归因到某次改动 —— **prompt 版本化是可观测性的前提** |
| 脱敏 | 落库前对 prompt/response 中的 PII 脱敏，遵守留存策略 |

## 正例：结构化埋点（伪代码）

```java
// ✅ 一条 trace 串起 prompt 版本、用量、延迟、成本，可按维度下钻
final LlmTrace t = LlmTrace.start(traceId)
    .promptVersion("order-summary@v3")     // 关联版本，回归可归因
    .model(model).input(prompt);
final var resp = llm.call(prompt);
t.response(resp).usage(resp.usage())
 .latency(elapsedMs).ttft(firstTokenMs)    // 流式记首 token 延迟
 .cost(cost).tags(tenantId);
tracer.emit(t);                            // 进可观测平台
```

## 反例：只打日志、无版本、无归集

```java
// ❌ 只 log 一行结果：没 prompt 版本、没 token、没成本，回归无法归因，账无法下钻
log.info("llm done: {}", resp.content());
```

## 自检

- [ ] 每条调用有 trace，含 prompt 版本 / response / token / 延迟？
- [ ] 流式记了首 token 延迟(TTFT)？
- [ ] 成本按租户/接口/prompt 版本/模型归集，可下钻？
- [ ] prompt 已版本化（否则回归无法归因）？
- [ ] prompt/response 落库前脱敏了 PII？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`rate-limit-token.md`](./rate-limit-token.md)（成本数据来源）
- 兄弟：[`prompt-management.md`](./prompt-management.md)（版本化是前提）
