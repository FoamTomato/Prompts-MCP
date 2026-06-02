---
name: dubbo-reference-config
description: Dubbo consumer 用 @DubboReference 引用服务，含 retries（仅幂等重试）、loadbalance、cluster 容错。Use when 写 Dubbo consumer / 配重试与负载均衡 / 选 failover 还是 failfast 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 服务引用
  - 重试
  - 集群容错
  - '@DubboReference'
  - retries
  - loadbalance
  - failover
effort: medium
context: inline
version: '1.0'
---
# Apache Dubbo · 服务引用（consumer）

> 本条只管「consumer 怎么引用与配重试/容错」。provider 怎么暴露见 [`service-export.md`](./service-export.md)；降级 mock 见 [`graceful-degradation.md`](./graceful-degradation.md)。

## 规则

| 项 | 约定 |
|----|------|
| 引用注解 | 字段标 `@DubboReference`（3.x 注解，替代旧 `@Reference`） |
| version/group | 与目标 provider 的 `version`/`group` 对齐，否则引用不到 |
| retries | **仅幂等方法**可重试（查询/幂等写）；非幂等（下单/扣款）必设 `retries = 0` |
| loadbalance | 默认 `random`；要平滑用 `roundrobin`，长连接慢节点用 `leastactive` |
| cluster | 默认 `failover`（失败重试他节点）；非幂等用 `failfast`（快速失败不重试） |

## 正例

```java
// 幂等查询：可重试 + failover
@DubboReference(version = "1.0.0", group = "order",
        timeout = 3000, retries = 2,
        loadbalance = "roundrobin", cluster = "failover")
private OrderQueryService orderQueryService;
```

```java
// 非幂等写：禁重试 + failfast，避免重复下单
@DubboReference(version = "1.0.0", group = "order",
        timeout = 3000, retries = 0, cluster = "failfast")
private OrderCommandService orderCommandService;
```

## 反例

```java
// ❌ 非幂等的下单接口配了 retries=2 + failover：
// 一次超时会被重发到其他节点，造成重复下单
@DubboReference(timeout = 1000, retries = 2)
private OrderCommandService orderCommandService;
```

❌ consumer 的 `version`/`group` 与 provider 不一致，启动报 `No provider available`。

❌ 用重试当容量补救：节点本就过载，重试只会放大雪崩。

## 自检

- [ ] 字段用 `@DubboReference`，`version`/`group` 与 provider 对齐？
- [ ] 非幂等方法 `retries = 0` 且 `cluster = "failfast"`？
- [ ] `retries` 只用在确实幂等的方法上？
- [ ] `loadbalance` 按场景选（random/roundrobin/leastactive）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`service-export.md`](./service-export.md)（provider 怎么暴露）
- 兄弟：[`graceful-degradation.md`](./graceful-degradation.md)（失败时怎么 mock 降级）
- 兄弟：[`api-module-design.md`](./api-module-design.md)（引用的接口从哪来）
