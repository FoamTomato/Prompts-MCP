---
name: ai-llm-streaming-sse
description: LLM 流式响应默认用 SSE（单向、标准 HTTP、EventSource 自动重连），token 边到边逐块 flush，仅双向交互才上 WebSocket。Use when 做大模型打字机效果 / 选 SSE 还是 WebSocket / 评审流式接口时。
parent: ./index.md
paths:
- '*.java'
- '*.py'
- '*.md'
triggers:
  keywords:
  - 流式响应
  - 打字机效果
  - SSE
  - Server-Sent Events
  - token flush
  - 自动重连
effort: medium
context: inline
version: '1.0'
---
# LLM · 流式响应（默认 SSE）

> 本条只管「流式怎么传」。限流/成本见 [`rate-limit-token.md`](./rate-limit-token.md)；失败重试见 [`retry-degradation.md`](./retry-degradation.md)。

## 规则

| 维度 | 要求 |
|------|------|
| 默认 SSE | LLM 输出是**单向服务端推**，用 SSE：基于标准 HTTP、轻量、`EventSource` 原生**自动重连**；不要默认上 WebSocket |
| 何时 WebSocket | 仅当需要**全双工**（客户端边说边收、实时打断/语音）才用 WebSocket，否则属过度设计 |
| 边到边 flush | 每收到模型一个 token / chunk 就立刻 flush 给前端，**禁止攒满再一次性返回**（攒满 = 失去流式意义） |
| 结束与错误事件 | 用约定事件标识结束（如 `event: done`）与错误，前端据此停渲染/重试 |
| 关闭即释放 | 客户端断开要级联取消上游 LLM 流，避免空转烧 token |

## 正例：SSE 边到边 flush（Spring WebFlux）

```java
// ✅ Flux<String> 每个 token 即时推；media type 为 text/event-stream
@GetMapping(value = "/chat", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public Flux<String> chat(@RequestParam String q) {
    // 逐 token 流式返回，框架自动按 chunk flush
    return chatClient.prompt().user(q).stream().content();
}
```

## 反例：攒满再返回 / 滥用 WebSocket

```java
// ❌ 收集完整结果再 return —— 前端等到全部生成完才见字，流式形同虚设
String full = chatClient.prompt().user(q).call().content();
return full;
```

## 自检

- [ ] 单向输出场景用的是 SSE（`text/event-stream`），不是 WebSocket？
- [ ] 每个 token/chunk 即时 flush，没有攒满再返回？
- [ ] 有结束事件与错误事件，前端能正确收尾？
- [ ] 客户端断开时取消了上游 LLM 流？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`rate-limit-token.md`](./rate-limit-token.md)（流式也要计 token 成本）
- 兄弟：[`observability.md`](./observability.md)（流式首 token 延迟埋点）
