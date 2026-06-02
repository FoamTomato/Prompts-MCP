---
name: webflux-mono-flux
description: Spring WebFlux 响应式基础 — Mono(0-1) vs Flux(0-N)、操作符 map/flatMap/zip、订阅才执行(lazy)。Use when 写第一段响应式代码 / 选 Mono 还是 Flux / 用 map 还是 flatMap / 链不执行时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 响应式流
  - Mono
  - Flux
  - flatMap
  - 订阅才执行
  - reactive stream
effort: medium
context: inline
version: '1.0'
---
# Spring WebFlux · Mono / Flux 基础

> 本条只管「Mono/Flux 怎么选、操作符怎么用、为什么不执行」。何时该用响应式见 [`when-reactive.md`](./when-reactive.md)；链里禁止阻塞调用见 [`blocking-trap.md`](./blocking-trap.md)。

## 规则

| 维度 | 约定 |
|------|------|
| `Mono<T>` | 异步序列 **0 或 1** 个元素：查单条、保存返回、`void` 用 `Mono<Void>` |
| `Flux<T>` | 异步序列 **0 到 N** 个元素：列表、流式、SSE |
| `map` | 同步 1:1 转换，函数返回**普通值** `T -> R` |
| `flatMap` | 转换返回**另一个 Publisher** `T -> Mono/Flux`，用于嵌套异步调用，自动展平 |
| `zip` | 并行合并多条流，全部到齐后组装：`Mono.zip(a, b)` |
| **lazy** | 流是声明式蓝图，**不订阅(subscribe)就不执行**；framework 调接口时自动订阅，自己别手动 block |

判据一句话：**返回普通值用 `map`，返回又一个 Mono/Flux 用 `flatMap`（否则会嵌套成 `Mono<Mono<T>>`）。**

## 正例

```java
// ✅ Mono：查单条 + 链式异步
public Mono<OrderVO> detail(Long id) {
    return orderRepo.findById(id)              // Mono<Order>
        .flatMap(order -> userRepo.findById(order.userId())  // 返回 Mono → flatMap
            .map(user -> toVO(order, user)));  // 返回普通值 → map
}

// ✅ Flux：0-N 流
public Flux<UserVO> list() {
    return userRepo.findAll().map(this::toVO);
}

// ✅ zip：两个独立调用并行后合并
public Mono<DashboardVO> dashboard(Long uid) {
    return Mono.zip(orderRepo.countByUser(uid), pointRepo.sumByUser(uid))
        .map(t -> new DashboardVO(t.getT1(), t.getT2()));
}
```

## 反例

```java
// ❌ 该用 flatMap 却用 map：得到 Mono<Mono<User>>，外层永远拿不到值
orderRepo.findById(id).map(o -> userRepo.findById(o.userId()));

// ❌ 声明了流却不返回/不订阅：什么都不会发生（lazy）
public void save(Order o) {
    orderRepo.save(o);   // 没 return、没 subscribe → 根本没执行
}
```

## 自检

- [ ] 0-1 用 `Mono`、0-N 用 `Flux`，`void` 语义用 `Mono<Void>`？
- [ ] 转换返回普通值用 `map`、返回 Publisher 用 `flatMap`（无 `Mono<Mono>`）？
- [ ] 方法把流 `return` 出去交给 framework 订阅，没在中途吞掉/不订阅？
- [ ] 多个独立异步调用用 `zip` 并行而非串行 `flatMap`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`when-reactive.md`](./when-reactive.md)（先确认该不该用响应式）
- 兄弟：[`blocking-trap.md`](./blocking-trap.md)（链里禁止 block()/JDBC）
- 兄弟：[`webclient.md`](./webclient.md)（用 WebClient 发响应式 HTTP）
