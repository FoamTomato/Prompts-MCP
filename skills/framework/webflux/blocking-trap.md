---
name: webflux-blocking-trap
description: WebFlux 阻塞陷阱 — 事件循环线程里禁 block()/JDBC，改用 R2DBC/WebClient，用 BlockHound 检测。Use when 排查 WebFlux 卡顿 / 链里要调阻塞 API / 引入 R2DBC / 检测阻塞调用时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 阻塞陷阱
  - block 阻塞调用
  - R2DBC
  - BlockHound
  - boundedElastic
  - 事件循环线程
effort: high
context: inline
version: '1.0'
---
# Spring WebFlux · 阻塞陷阱

> 本条只管「响应式线程里绝不能阻塞，以及阻塞了怎么办」。何时该用响应式见 [`when-reactive.md`](./when-reactive.md)；发 HTTP 用 WebClient 见 [`webclient.md`](./webclient.md)。

## 核心铁律

WebFlux 用**极少数事件循环线程**（默认约等于核数）承载所有请求。在这些线程上**任何阻塞调用都会卡死整组线程**，并发能力瞬间崩塌——这是响应式最致命的坑。

## 规则

| 禁用（阻塞） | 改用（非阻塞） |
|------|------|
| `Mono.block()` / `Flux.blockFirst()` | 一路 `return` 流，交 framework 订阅，**永不手动 block** |
| JDBC / MyBatis / JPA | **R2DBC**（响应式驱动）|
| `RestTemplate` / 同步 HTTP 客户端 | **WebClient** |
| `Thread.sleep` / 同步文件 IO / 同步锁 | `Mono.delay` / 异步 IO / 非阻塞协调 |
| 实在无替代的阻塞 SDK | 隔离到 `Schedulers.boundedElastic()`，别在事件循环线程跑 |

检测：测试时挂 **BlockHound** —— 它在响应式线程上侦测到阻塞调用会直接抛错，把坑暴露在 CI 而非线上。

## 正例

```java
// ✅ 全链非阻塞：R2DBC + WebClient
public Mono<UserVO> profile(Long id) {
    return r2dbcUserRepo.findById(id)                 // R2DBC，非阻塞
        .flatMap(u -> webClient.get().uri("/ext/{id}", id)
            .retrieve().bodyToMono(Ext.class)         // WebClient，非阻塞
            .map(ext -> toVO(u, ext)));
}

// ✅ 无法替代的阻塞 SDK：隔离到 boundedElastic，不占事件循环线程
Mono.fromCallable(() -> legacyBlockingSdk.call())
    .subscribeOn(Schedulers.boundedElastic());
```

测试启用 BlockHound：

```java
@BeforeAll
static void setup() { BlockHound.install(); }  // 检测到阻塞即抛 BlockingOperationError
```

## 反例

```java
// ❌ 在响应式接口里 block：卡死事件循环线程，整个实例并发崩塌
@GetMapping("/u/{id}")
public UserVO get(@PathVariable Long id) {
    return userRepo.findById(id).block();   // 致命：阻塞事件循环线程
}

// ❌ WebFlux 里仍用 JDBC / RestTemplate —— 每次调用阻塞事件循环线程
jdbcTemplate.queryForObject(sql, ...);      // 该换 R2DBC
```

## 自检

- [ ] 接口/链路里没有任何 `block()` / `blockFirst()`？
- [ ] 数据访问走 R2DBC，HTTP 走 WebClient，没残留 JDBC/RestTemplate？
- [ ] 无可替代的阻塞调用已 `subscribeOn(boundedElastic())` 隔离？
- [ ] 测试挂了 BlockHound，CI 能拦住阻塞调用？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`when-reactive.md`](./when-reactive.md)（"全栈非阻塞"才该上响应式）
- 兄弟：[`webclient.md`](./webclient.md)（替代 RestTemplate 的非阻塞客户端）
- 兄弟：[`mono-flux.md`](./mono-flux.md)（lazy：return 流而非 block 取值）
