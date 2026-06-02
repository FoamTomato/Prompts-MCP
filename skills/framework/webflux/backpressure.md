---
name: webflux-backpressure
description: WebFlux 背压(backpressure) — 生产者快于消费者时用 onBackpressureBuffer/Drop/Latest 三种策略协调，避免内存堆积或 OOM。Use when 生产快于消费 / Flux 内存涨/OOM / 选背压策略 / 处理快速数据源时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 背压
  - backpressure
  - onBackpressureBuffer
  - onBackpressureDrop
  - 生产快于消费
  - 限速 limitRate
effort: medium
context: inline
version: '1.0'
---
# Spring WebFlux · 背压 Backpressure

> 本条只管「生产者快于消费者时怎么协调」。基础流操作见 [`mono-flux.md`](./mono-flux.md)；阻塞调用见 [`blocking-trap.md`](./blocking-trap.md)。

## 问题本质

背压 = 消费者向上游**申请它能处理的量**（`request(n)`），上游按需推送。当生产者（如高频传感器、Kafka 流）**快于**消费者，又**无法被请求量约束**（hot/外部源）时，元素会堆积——必须显式选一种策略，否则内存无限涨直到 OOM。

## 规则

| 策略 | 行为 | 适用 |
|------|------|------|
| `onBackpressureBuffer(n)` | 缓冲到上限，超了按策略报错/丢 | 不能丢数据，且峰值可控 |
| `onBackpressureDrop()` | 消费不过来就**丢最新到来的** | 可丢、要最早的（如监控采样）|
| `onBackpressureLatest()` | 只**保留最新一个**，旧的丢 | 只关心最新值（如实时仪表盘）|
| `limitRate(n)` | 下游主动**分批请求**，从源头限速 | 数据源支持按需拉取时优先用 |

判据：**能限速从源头 `limitRate`；不能丢用 `Buffer`（设上限）；可丢看要旧值还是新值选 `Drop`/`Latest`。**

## 正例

```java
// ✅ 高频源 + 慢消费：缓冲 1000，溢出丢最旧并告警
fastSource()
    .onBackpressureBuffer(1000,
        dropped -> log.warn("背压丢弃: {}", dropped),
        BufferOverflowStrategy.DROP_OLDEST)
    .flatMap(this::slowPersist);

// ✅ 实时仪表盘只要最新值
sensorFlux().onBackpressureLatest().subscribe(dashboard::render);

// ✅ 数据源可拉取：从源头限速，最稳
Flux.fromIterable(huge).limitRate(256).flatMap(this::handle);
```

## 反例

```java
// ❌ 高频 hot 源直接慢消费，不设任何背压策略 —— 元素无限堆积直至 OOM
hotSensorFlux().flatMap(this::slowPersist);   // 缺 onBackpressure*/limitRate

// ❌ onBackpressureBuffer() 不设上限当"万能解" —— 只是把 OOM 推迟
flux.onBackpressureBuffer();   // 无界缓冲，峰值一样炸
```

## 自检

- [ ] 生产可能快于消费的链路，显式选了背压策略而非放任堆积？
- [ ] 数据源支持按需拉取时优先用 `limitRate` 从源头限速？
- [ ] `onBackpressureBuffer` 设了**有限**上限 + 溢出处理，没用无界缓冲？
- [ ] 选 `Drop`/`Latest` 前确认这条流**允许丢数据**？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`mono-flux.md`](./mono-flux.md)（Flux 基础与操作符）
- 兄弟：[`when-reactive.md`](./when-reactive.md)（流式/背压是选 WebFlux 的理由之一）
