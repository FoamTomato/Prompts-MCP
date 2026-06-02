---
name: webflux-webclient
description: WebClient 替代 RestTemplate — 响应式非阻塞 HTTP 调用，配超时(responseTimeout)、重试(retryWhen 带退避)、错误状态映射。Use when 发响应式 HTTP 请求 / 从 RestTemplate 迁移 / 配 HTTP 超时与重试时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - WebClient
  - 响应式 HTTP 调用
  - RestTemplate 替代
  - retryWhen
  - 超时重试
  - bodyToMono
effort: medium
context: inline
version: '1.0'
---
# Spring WebFlux · WebClient 替代 RestTemplate

> 本条只管「响应式发 HTTP 请求 + 超时/重试」。为什么不能用 RestTemplate 见 [`blocking-trap.md`](./blocking-trap.md)；Mono/Flux 基础见 [`mono-flux.md`](./mono-flux.md)。

## 规则

| 维度 | 约定 |
|------|------|
| 客户端 | 用 `WebClient`（非阻塞），WebFlux 里**禁用** `RestTemplate`（阻塞） |
| 复用 | `WebClient.Builder` 注入后建**共享实例**，别每次请求 new |
| 取值 | `.retrieve().bodyToMono(T.class)` / `.bodyToFlux(T.class)`，**不要 `.block()`** |
| 超时 | 连接超时 + `responseTimeout`，必配，避免线程/连接被悬挂 |
| 重试 | `retryWhen(Retry.backoff(n, duration))` 指数退避，只对可重试错误重试 |
| 错误 | `.onStatus(...)` 把 4xx/5xx 映射成业务异常，别让原始状态漏出 |

## 正例

```java
// ✅ 共享实例 + 超时 + 退避重试 + 状态映射
@Bean
WebClient extClient(WebClient.Builder builder) {
    HttpClient http = HttpClient.create()
        .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, 2000)
        .responseTimeout(Duration.ofSeconds(3));
    return builder.baseUrl("https://ext.api")
        .clientConnector(new ReactorClientHttpConnector(http)).build();
}

public Mono<UserVO> fetch(Long id) {
    return extClient.get().uri("/users/{id}", id)
        .retrieve()
        .onStatus(HttpStatusCode::is5xxServerError,
                  r -> Mono.error(new ExtServiceException()))
        .bodyToMono(UserVO.class)
        .retryWhen(Retry.backoff(3, Duration.ofMillis(200))   // 退避重试
            .filter(ex -> ex instanceof ExtServiceException));
}
```

## 反例

```java
// ❌ WebFlux 里用 RestTemplate —— 阻塞事件循环线程（见 blocking-trap）
restTemplate.getForObject(url, UserVO.class);

// ❌ 拿到 Mono 立刻 block 取值 —— 抵消非阻塞，仍卡线程
UserVO u = extClient.get().uri(url).retrieve().bodyToMono(UserVO.class).block();

// ❌ 不配超时 + 无脑重试任何异常 —— 故障时连接耗尽、雪崩放大
extClient.get().uri(url).retrieve().bodyToMono(X.class).retry(3);
```

## 自检

- [ ] 用 `WebClient` 而非 `RestTemplate`，且是共享实例？
- [ ] 配了连接超时 + `responseTimeout`，没有无限等待？
- [ ] 重试用 `Retry.backoff` 退避，且只 filter 可重试错误（非全部）？
- [ ] 用 `bodyToMono/Flux` 把流 return 出去，没在中途 `.block()`？
- [ ] 4xx/5xx 用 `onStatus` 映射成业务异常？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`blocking-trap.md`](./blocking-trap.md)（为何禁 RestTemplate，全链非阻塞）
- 兄弟：[`mono-flux.md`](./mono-flux.md)（bodyToMono/Flux 返回的流怎么用）
