---
name: spring-cloud-circuit-breaker
description: 熔断限流 Sentinel/Resilience4j — 熔断规则、限流规则、降级策略、与 OpenFeign 整合。Use when 给服务调用加熔断防雪崩 / 配限流 / 设计降级 / 整合 Feign 容错时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 熔断
  - 限流
  - Sentinel
  - Resilience4j
  - 服务降级
  - circuit breaker
effort: medium
context: inline
version: '1.0'
---
# Spring Cloud · 熔断限流（Sentinel/Resilience4j）

> 本条只管「熔断/限流/降级规则怎么定」。降级后接口怎么写（fallbackFactory）见 [`openfeign.md`](./openfeign.md)；网关入口限流见 [`gateway-routing.md`](./gateway-routing.md)。

## 概念区分（别混）

| 机制 | 解决什么 | 触发 |
|------|---------|------|
| 限流（Flow） | 入口流量超过承载能力 | QPS / 并发线程数超阈值 → 拒绝多余请求 |
| 熔断（Circuit Break） | 下游持续异常，再调只是雪上加霜 | 异常比例 / 慢调用比例超阈值 → 直接快速失败一段时间 |
| 降级（Fallback） | 上面两者触发后，给调用方一个兜底返回 | 返回默认值 / 缓存 / 友好提示，**不让异常裸抛** |

## 规则

| 项 | 规则 |
|----|------|
| 熔断阈值 | 按异常比例 + 慢调用比例配，半开态放少量探测请求恢复 |
| 限流维度 | 按资源（接口/方法）配 QPS 或并发，核心接口单独配 |
| 降级必配 | 凡熔断/限流的资源都要有 fallback，**禁裸抛 5xx 给上游** |
| Feign 整合 | Sentinel 开 `feign.sentinel.enabled=true`，降级走 Feign 的 `fallbackFactory` |
| 规则外置 | 规则放配置中心/控制台动态调，别硬编码进代码 |

## 正例

```java
// ✅ Sentinel：限流/熔断触发都走 blockHandler 兜底
@SentinelResource(value = "getOrder",
        fallback = "getOrderFallback",        // 业务异常降级
        blockHandler = "getOrderBlock")        // 限流/熔断降级
public OrderVO getOrder(Long id) {
    return orderClient.getById(id);
}
public OrderVO getOrderBlock(Long id, BlockException ex) {
    log.warn("getOrder 被限流/熔断, id={}", id);
    return OrderVO.empty();                     // ✅ 兜底，不裸抛
}
```

```yaml
# ✅ Feign 整合 Sentinel，降级走 Feign 的 fallbackFactory
feign:
  sentinel:
    enabled: true
```

```yaml
# Resilience4j 熔断阈值示例（异常率+慢调用）
resilience4j.circuitbreaker:
  instances:
    orderService:
      failureRateThreshold: 50
      slowCallRateThreshold: 80
      waitDurationInOpenState: 10s
```

## 反例

```java
// ❌ 加了 @SentinelResource 却没 fallback/blockHandler，
//    限流时直接抛 BlockException 给上游 → 雪崩没挡住
@SentinelResource("getOrder")
public OrderVO getOrder(Long id) {
    return orderClient.getById(id);
}
```

## 自检

- [ ] 分清了限流（入口）/熔断（下游异常）/降级（兜底）三件事？
- [ ] 每个熔断/限流资源都配了 fallback，没把异常裸抛给上游？
- [ ] 熔断阈值按异常比例 + 慢调用比例，含半开恢复？
- [ ] Feign 整合开了 `feign.sentinel.enabled`，降级走 `fallbackFactory`？
- [ ] 规则在控制台/配置中心动态调，没硬编码进代码？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`openfeign.md`](./openfeign.md)（降级接口 fallbackFactory 的写法）
- 兄弟：[`gateway-routing.md`](./gateway-routing.md)（网关入口处的限流）
