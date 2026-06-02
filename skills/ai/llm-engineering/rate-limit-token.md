---
name: ai-llm-rate-limit
description: LLM 网关层做 TPM+RPM 双限流（TPM 是成本主控维度），并按 input/output/cached token 单价实时核算每次调用成本。Use when 设计 LLM 网关限流 / 防超额烧钱 / 评审调用成本核算时。
parent: ./index.md
paths:
- '*.java'
- '*.py'
- '*.md'
triggers:
  keywords:
  - 双限流
  - TPM
  - RPM
  - token 成本
  - 限流网关
  - cost accounting
effort: medium
context: inline
version: '1.0'
---
# LLM · 限流与 token 成本核算

> 本条只管「限流 + 算成本」。超阈值后的熔断见 [`retry-degradation.md`](./retry-degradation.md)；缓存省 token 见 [`caching.md`](./caching.md)。

## 规则

| 维度 | 要求 |
|------|------|
| 双限流 | 网关层同时限 **TPM**（tokens/分钟）和 **RPM**（requests/分钟）；缺一不可 |
| TPM 是主控 | 成本与限额几乎都按 token 计，**TPM 是成本主控维度**；只限 RPM 挡不住大上下文请求烧穿预算 |
| 集中在网关 | 限流放统一网关/队列，不散落各业务方；超限请求排队或快速拒绝，不直接打穿上游 |
| 实时算成本 | 每次调用按 **input / output / cached** token 各自单价分别计价求和（cached token 单价低，分开算才准） |
| 按维度归集 | 成本按租户/接口/prompt 版本归集，喂给监控与成本熔断 |

## 正例：分类计价（伪代码）

```java
// ✅ input/output/cached 三类 token 各乘各自单价，cached 不能按 input 价算
final long inTok = usage.inputTokens();
final long outTok = usage.outputTokens();
final long cachedTok = usage.cachedTokens();
final BigDecimal cost = price.in().multiply(BigDecimal.valueOf(inTok))
    .add(price.out().multiply(BigDecimal.valueOf(outTok)))
    .add(price.cached().multiply(BigDecimal.valueOf(cachedTok)));
costMeter.record(tenantId, promptVersion, cost);
```

## 反例：只限 RPM / 成本一口价

```java
// ❌ 只按请求数限流：一个 100K 上下文的请求就能烧穿 TPM 预算
rateLimiter.acquire();   // 仅 RPM
// ❌ 成本按总 token 一口价：cached token 单价不同，账算不准
cost = totalTokens * UNIT_PRICE;
```

## 自检

- [ ] 网关同时限了 TPM 和 RPM，不是只限其一？
- [ ] 限流集中在网关/队列，业务方不各自实现？
- [ ] 成本按 input/output/cached 分类单价分别计算？
- [ ] 成本按租户/接口/prompt 版本归集，可供熔断与监控用？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`retry-degradation.md`](./retry-degradation.md)（成本速率超阈值要熔断）
- 兄弟：[`observability.md`](./observability.md)（成本数据进监控）
