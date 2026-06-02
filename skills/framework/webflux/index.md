---
name: framework-webflux-index
description: Spring WebFlux 响应式编程约定 — Mono/Flux 基础、何时用响应式、阻塞陷阱、背压、WebClient 五个独立决策点。Use when 写 WebFlux 响应式代码 / 评估上不上响应式 / 排查阻塞与背压 / 发响应式 HTTP 时。
parent: ../index.md
children:
  - { name: webflux-mono-flux, path: mono-flux.md, tag: skill, note: "Mono(0-1)/Flux(0-N) + map/flatMap/zip + 订阅才执行" }
  - { name: webflux-when-reactive, path: when-reactive.md, tag: skill, note: "何时用响应式 + 与虚拟线程取舍" }
  - { name: webflux-blocking-trap, path: blocking-trap.md, tag: skill, note: "禁 block/JDBC，用 R2DBC/WebClient，BlockHound 检测" }
  - { name: webflux-backpressure, path: backpressure.md, tag: skill, note: "背压 Buffer/Drop/Latest，生产快于消费" }
  - { name: webflux-webclient, path: webclient.md, tag: skill, note: "WebClient 替代 RestTemplate + 超时重试" }
when_to_descend: 写 / 改 Spring WebFlux 响应式代码，或评估要不要上响应式、排查阻塞与背压、发响应式 HTTP 调用。
---

# Spring WebFlux · 响应式编程约定索引

五个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 写响应式代码、选 Mono/Flux、用 map/flatMap/zip | [mono-flux](mono-flux.md) |
| 纠结该不该上响应式 / 响应式还是虚拟线程 | [when-reactive](when-reactive.md) |
| 排查 WebFlux 卡顿、链里有 block()/JDBC | [blocking-trap](blocking-trap.md) |
| 生产快于消费、Flux 内存涨/OOM | [backpressure](backpressure.md) |
| 发响应式 HTTP、从 RestTemplate 迁移 | [webclient](webclient.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../spring-boot/index.md`](../spring-boot/index.md)
- 相关：[`../../fundamentals/virtual-threads/index.md`](../../fundamentals/virtual-threads/index.md)（响应式 vs 虚拟线程的取舍）
