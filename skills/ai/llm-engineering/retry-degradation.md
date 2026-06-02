---
name: ai-llm-retry-degradation
description: LLM 调用失败用指数退避+full jitter 重试，先区分瞬时错误（可重试）与结构性错误（不盲目重试），并按错误率+成本速率+延迟三类触发器熔断降级。Use when 处理 LLM 超时/限流/失败 / 设计调用降级 / 评审重试与熔断时。
parent: ./index.md
paths:
- '*.java'
- '*.py'
- '*.md'
triggers:
  keywords:
  - 指数退避
  - full jitter
  - 重试
  - 熔断
  - 成本熔断
  - 瞬时错误
  - circuit breaker
effort: high
context: inline
version: '1.0'
---
# LLM · 重试、降级与熔断

> 本条只管「失败后的韧性」。限流与成本计量见 [`rate-limit-token.md`](./rate-limit-token.md)；流式失败收尾见 [`streaming-sse.md`](./streaming-sse.md)。

## 规则

| 维度 | 要求 |
|------|------|
| 先分类再重试 | **瞬时错误**（429/503/超时）才重试；**结构性错误**（400 参数错、鉴权失败、内容被拒）**不盲目重试**，重试只是浪费配额 |
| 退避算法 | 指数退避 **+ full jitter**（`sleep = random(0, base·2^n)`），打散并发重试避免惊群 |
| 重试上限 | 设最大重试次数 + 总超时；超限即走降级，不无限重试 |
| 降级路径 | 主模型不可用时降级到备用模型/缓存/兜底文案，而非直接报错给用户 |
| 三类熔断 | 熔断触发器 = **错误率 + 成本速率(cost-velocity) + 延迟**；多数团队漏做成本熔断，导致异常重试把账单打爆 |

## 正例：full jitter + 错误分类

```java
// ✅ 仅瞬时错误重试；退避用 full jitter
for (int n = 0; n < MAX_RETRY; n++) {
    try {
        return llm.call(req);
    } catch (LlmException e) {
        if (!e.isTransient()) throw e;          // 结构性错误立即上抛，不重试
        final long base = 200L;                  // ms
        final long sleep = ThreadLocalRandom.current().nextLong(base << n);
        Thread.sleep(sleep);                     // full jitter: random(0, base·2^n)
    }
}
return fallback.degrade(req);                     // 超限走降级
```

## 反例：固定间隔 + 无脑重试 + 无成本熔断

```java
// ❌ 400 参数错也重试 3 次（必然再失败）；固定 sleep 惊群；只看错误率没看成本速率
for (int i = 0; i < 3; i++) {
    try { return llm.call(req); }
    catch (Exception e) { Thread.sleep(1000); }   // 异常风暴时成本飙升却不熔断
}
```

## 自检

- [ ] 重试前区分了瞬时 vs 结构性错误，结构性错误不重试？
- [ ] 退避是指数 + full jitter，不是固定间隔？
- [ ] 有最大重试次数和总超时，超限走降级而非无限重试？
- [ ] 熔断触发器包含错误率**和成本速率和延迟**三类，没漏成本熔断？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`rate-limit-token.md`](./rate-limit-token.md)（成本速率从这里来）
- 兄弟：[`caching.md`](./caching.md)（缓存可作降级兜底）
