---
name: spring-cloud-openfeign
description: OpenFeign 声明式调用 — @FeignClient 接口、超时配置、fallback/fallbackFactory 降级、日志级别、契约接口共享。Use when 写服务间 HTTP 调用 / 配 Feign 超时降级 / 排查 Feign 报错时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 声明式调用
  - '@FeignClient'
  - OpenFeign
  - fallbackFactory
  - 服务调用降级
  - feign 超时
effort: medium
context: inline
version: '1.0'
---
# Spring Cloud · OpenFeign 声明式调用

> 本条只管「服务间怎么用接口发 HTTP 调用 + 降级」。熔断限流规则本身见 [`circuit-breaker.md`](./circuit-breaker.md)；按服务名解析地址见 [`service-discovery.md`](./service-discovery.md)。

## 规则

| 项 | 规则 |
|----|------|
| 客户端定义 | 用 `@FeignClient(name="服务名")` 标接口，`name` 用注册中心的服务名，不写死 IP |
| 契约对齐 | 服务方接口（含 DTO）抽到独立 `api` 模块，提供方实现、消费方引依赖，**不手抄第二份** |
| 超时 | 必配 `connectTimeout` + `readTimeout`，别用默认（默认很容易拖垮调用方）|
| 降级 | 用 `fallbackFactory`（能拿到异常）优于 `fallback`；降级类要 `@Component` 注册 |
| 日志 | 排查时把对应包日志设 `DEBUG` + 配 `Logger.Level.FULL`，生产用 `BASIC` |

## 正例

```java
// 契约接口放 order-api 模块，提供方与消费方共享同一份
@FeignClient(name = "order-service", fallbackFactory = OrderClientFallback.class)
public interface OrderClient {
    @GetMapping("/orders/{id}")
    OrderVO getById(@PathVariable("id") Long id);
}

// ✅ fallbackFactory 能拿到触发降级的原始异常，便于记录
@Component
public class OrderClientFallback implements FallbackFactory<OrderClient> {
    @Override
    public OrderClient create(Throwable cause) {
        return id -> {
            log.warn("order-service 降级, id={}", id, cause);
            return OrderVO.empty();
        };
    }
}
```

```yaml
# ✅ 超时与日志按客户端粒度配置
feign:
  client:
    config:
      order-service:
        connectTimeout: 2000
        readTimeout: 5000
        loggerLevel: basic
```

## 反例

```java
// ❌ 写死地址，绕过注册中心，换机器/扩容即失效
@FeignClient(name = "order", url = "http://10.0.0.5:8080")
public interface OrderClient { /* ... */ }

// ❌ 用 fallback 而非 fallbackFactory，丢掉异常原因，降级了都不知道为什么
@FeignClient(name = "order-service", fallback = OrderClientFallback.class)
public interface OrderClient { /* ... */ }
```

## 自检

- [ ] `@FeignClient` 用服务名而非写死 `url`？
- [ ] 配了 `connectTimeout` + `readTimeout`，没吃默认值？
- [ ] 降级优先 `fallbackFactory`（保留异常），降级类已 `@Component`？
- [ ] 接口与 DTO 抽到共享 api 模块，没有两边手抄？
- [ ] 生产日志级别是 `BASIC`，没把 `FULL` 带上生产？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`circuit-breaker.md`](./circuit-breaker.md)（Feign 降级背后的熔断限流规则）
- 兄弟：[`service-discovery.md`](./service-discovery.md)（`name` 服务名如何解析为实例地址）
