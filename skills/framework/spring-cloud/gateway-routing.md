---
name: spring-cloud-gateway-routing
description: Spring Cloud Gateway 网关 — route/predicate/filter 路由、全局过滤器鉴权、限流、CORS 跨域，禁在网关写业务逻辑。Use when 配网关路由 / 加统一鉴权或限流 / 处理跨域时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 网关路由
  - Gateway
  - 全局过滤器
  - GlobalFilter
  - 网关鉴权
  - CORS 跨域
effort: medium
context: inline
version: '1.0'
---
# Spring Cloud · Gateway 网关路由

> 本条只管「网关层怎么路由 + 统一切面（鉴权/限流/跨域）」。具体业务调用见 [`openfeign.md`](./openfeign.md)；限流规则的精细配置见 [`circuit-breaker.md`](./circuit-breaker.md)。

## 规则

| 概念 | 作用 | 要点 |
|------|------|------|
| route | 一条路由 = id + uri + predicates + filters | `uri: lb://服务名` 走负载均衡，不写死 IP |
| predicate | 匹配条件（Path/Method/Header） | 用 `Path=/api/order/**` 按前缀分发 |
| filter | 单路由级处理（改路径/加头） | `StripPrefix` 去前缀最常用 |
| GlobalFilter | 全局过滤器，所有请求都过 | 鉴权、日志、链路 ID 注入放这里 |
| 限流 | `RequestRateLimiter` + Redis 令牌桶 | 按 IP / 用户 / 接口维度限流 |
| CORS | 全局统一配 `globalcors` | 跨域**只在网关配一处**，别每个服务各配 |

**铁律：网关只做转发与横切（鉴权/限流/路由/跨域），禁写任何业务逻辑。** 业务下沉到各微服务。

## 正例

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: order-route
          uri: lb://order-service          # ✅ lb:// 走注册中心负载均衡
          predicates:
            - Path=/api/order/**
          filters:
            - StripPrefix=2                 # 去掉 /api/order 前缀
      globalcors:                            # ✅ 跨域统一在网关配一次
        cors-configurations:
          '[/**]':
            allowedOriginPatterns: "https://*.example.com"
            allowedMethods: "*"
```

```java
// ✅ 全局过滤器做统一鉴权，未通过直接短路返回 401
@Component
public class AuthFilter implements GlobalFilter, Ordered {
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        String token = exchange.getRequest().getHeaders().getFirst("Authorization");
        if (!valid(token)) {
            exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);
            return exchange.getResponse().setComplete();
        }
        return chain.filter(exchange);
    }
    @Override public int getOrder() { return -100; }  // 越小越先执行
}
```

## 反例

```java
// ❌ 在网关里查库、拼业务结果 —— 业务逻辑越界，网关应只转发
@Component
public class OrderFilter implements GlobalFilter {
    public Mono<Void> filter(ServerWebExchange ex, GatewayFilterChain chain) {
        Order o = orderMapper.selectById(...);   // 业务该在 order-service
        // ...
    }
}
```

## 自检

- [ ] 路由 `uri` 用 `lb://服务名`，没写死实例 IP？
- [ ] 鉴权/限流/链路用 `GlobalFilter` 统一做，没散落到各路由？
- [ ] CORS 只在网关配一处，没有各服务重复配？
- [ ] 网关里没有任何查库 / 拼业务结果的逻辑？
- [ ] 阻塞调用没写进 WebFlux 过滤器（Gateway 基于 Reactor）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`openfeign.md`](./openfeign.md)（网关转发后服务间的内部调用）
- 兄弟：[`circuit-breaker.md`](./circuit-breaker.md)（网关限流背后的 Sentinel 规则）
