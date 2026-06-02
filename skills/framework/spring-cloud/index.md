---
name: framework-spring-cloud-index
description: Spring Cloud Alibaba 微服务栈 — 声明式调用 OpenFeign / 网关路由 / 配置中心 Nacos / 服务注册发现 / 熔断限流五个独立决策点。Use when 拆微服务 / 配网关与配置中心 / 做服务调用与容错时。
parent: ../index.md
children:
  - { name: spring-cloud-openfeign, path: openfeign.md, tag: skill, note: "声明式 @FeignClient 调用 + 超时 + fallback 降级" }
  - { name: spring-cloud-gateway-routing, path: gateway-routing.md, tag: skill, note: "网关 route/predicate/filter + 鉴权 + 限流 + CORS" }
  - { name: spring-cloud-config-center, path: config-center.md, tag: skill, note: "Nacos/Apollo 配置外置 + 动态刷新 + namespace 分环境" }
  - { name: spring-cloud-service-discovery, path: service-discovery.md, tag: skill, note: "Nacos 服务注册/健康检查/元数据/优雅上下线" }
  - { name: spring-cloud-circuit-breaker, path: circuit-breaker.md, tag: skill, note: "Sentinel/Resilience4j 熔断限流降级 + 整合 Feign" }
when_to_descend: 写 / 改 Spring Cloud 的服务调用、网关、配置中心、注册发现或熔断限流相关代码。
---

# Spring Cloud · 微服务栈索引

五个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 服务间调用，想用接口声明式 HTTP 客户端 | [openfeign](openfeign.md) |
| 配网关路由、统一鉴权、限流、跨域 | [gateway-routing](gateway-routing.md) |
| 配置外置、动态刷新、按环境隔离配置 | [config-center](config-center.md) |
| 服务注册到注册中心、按服务名调用、上下线 | [service-discovery](service-discovery.md) |
| 给调用加熔断、限流、降级，防雪崩 | [circuit-breaker](circuit-breaker.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../spring-boot/index.md`](../spring-boot/index.md)
- 相关：[`../../lang/java/error-handling/index.md`](../../lang/java/error-handling/index.md)
