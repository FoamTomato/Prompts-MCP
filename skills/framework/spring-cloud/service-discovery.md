---
name: spring-cloud-service-discovery
description: 服务注册发现 Nacos — 服务注册、健康检查、实例元数据、按服务名调用、优雅上下线。Use when 把服务注册到 Nacos / 按服务名做负载调用 / 配健康检查与优雅停机时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 服务注册发现
  - Nacos 注册
  - 健康检查
  - 服务元数据
  - 优雅上下线
  - service discovery
effort: medium
context: inline
version: '1.0'
---
# Spring Cloud · 服务注册发现（Nacos）

> 本条只管「服务怎么注册、怎么按服务名找到对方、怎么优雅上下线」。声明式调用见 [`openfeign.md`](./openfeign.md)；Nacos 作配置中心见 [`config-center.md`](./config-center.md)。

## 规则

| 项 | 规则 |
|----|------|
| 注册 | 引 `spring-cloud-starter-alibaba-nacos-discovery`，`spring.application.name` 即注册的服务名 |
| 调用 | 一律**按服务名**调用（Feign 的 `name` / `lb://服务名`），由负载均衡选实例，禁写死 IP |
| 健康检查 | 暴露 `/actuator/health`，Nacos 临时实例靠心跳，心跳停即剔除 |
| 元数据 | 灰度/版本/区域等用 `metadata` 打标，配合负载均衡做路由 |
| 优雅上下线 | 先从注册中心**下线**（停止接新流量）→ 等存量请求处理完 → 再停进程 |

## 正例

```yaml
spring:
  application:
    name: order-service                # ✅ 这就是注册中心里的服务名
  cloud:
    nacos:
      discovery:
        server-addr: ${NACOS_ADDR}
        namespace: ${ENV_NAMESPACE}
        metadata:
          version: v2                   # ✅ 元数据打标，供灰度路由
# 优雅停机：先注销再处理完存量
server:
  shutdown: graceful
spring.lifecycle.timeout-per-shutdown-phase: 30s
```

```java
// ✅ 按服务名调用，地址由负载均衡解析
@LoadBalanced
@Bean
RestTemplate restTemplate() { return new RestTemplate(); }

// 调用方写服务名，不写 IP
restTemplate.getForObject("http://order-service/orders/1", OrderVO.class);
```

## 反例

```java
// ❌ 写死实例 IP：扩容、漂移、下线全部失效，绕过了注册中心的意义
restTemplate.getForObject("http://10.0.0.7:8080/orders/1", OrderVO.class);
```

```text
❌ 直接 kill -9 进程：注册中心还没剔除，流量继续打过来 → 报错。
   应先调下线接口 / graceful shutdown，等心跳过期再停。
```

## 自检

- [ ] `spring.application.name` 设了、就是要注册的服务名？
- [ ] 调用一律按服务名 + 负载均衡，没写死任何实例 IP？
- [ ] 暴露了 `/actuator/health` 供健康检查？
- [ ] 灰度/版本用 `metadata` 打标，没硬编码分支判断？
- [ ] 停机走优雅下线（先注销再停），没直接 `kill -9`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`openfeign.md`](./openfeign.md)（按服务名做声明式调用）
- 兄弟：[`config-center.md`](./config-center.md)（同一 Nacos 兼作配置中心）
