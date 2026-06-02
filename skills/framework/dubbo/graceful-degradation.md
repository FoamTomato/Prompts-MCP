---
name: dubbo-graceful-degradation
description: Dubbo 优雅降级与容错 — mock 降级、配合 Sentinel 熔断、优雅停机、provider 异常不直接抛给 consumer。Use when 给 Dubbo 调用加降级 / 配熔断 / 处理优雅停机 / 隔离 provider 异常时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 优雅降级
  - 熔断
  - 优雅停机
  - mock
  - Sentinel
  - graceful shutdown
effort: medium
context: inline
version: '1.0'
---
# Apache Dubbo · 优雅降级与容错

> 本条只管「调用失败/停机时怎么兜底」。重试与容错策略选型见 [`reference-config.md`](./reference-config.md)；异常类型设计见 lang/java error-handling。

## 规则

| 项 | 约定 |
|----|------|
| mock 降级 | 非核心依赖在 `@DubboReference(mock = "...")` 指定降级类，失败返回兜底值 |
| 熔断 | 高频/易雪崩调用接入 Sentinel，按 QPS/异常比例熔断，避免拖垮 consumer |
| 优雅停机 | provider 下线先注销注册中心、停收新请求、等存量请求处理完再退出 |
| 异常隔离 | provider 内部异常（如 SQLException）**禁止裸抛给 consumer**，转成 api jar 里定义的业务异常 |

## 正例

```java
// consumer：非核心依赖配 mock 降级类
@DubboReference(timeout = 2000, mock = "com.x.order.OrderQueryMock")
private OrderQueryService orderQueryService;

// 降级类实现同一接口，失败时返回兜底
public class OrderQueryMock implements OrderQueryService {
    @Override
    public OrderDTO getById(Long id) {
        return OrderDTO.unknown(id);   // 返回占位，不阻塞主流程
    }
}
```

```java
// provider：把内部异常转成 api 里定义的业务异常再抛
@Override
public OrderDTO getById(Long id) {
    try {
        return orderRepository.find(id);
    } catch (DataAccessException e) {
        // OrderServiceException 定义在 api jar，consumer 能识别
        throw new OrderServiceException("order query failed: " + id, e);
    }
}
```

## 反例

❌ provider 直接把 `SQLException` / `NullPointerException` 抛回 consumer：consumer 拿不到 provider 私有异常类，反序列化失败，且泄漏内部实现。

❌ 核心链路全靠重试硬扛，无熔断：下游故障时请求堆积，consumer 线程池被打满雪崩。

❌ 直接 `kill -9` provider：在途请求被强行中断，注册中心仍指向已死节点，consumer 持续报错。

## 自检

- [ ] 非核心依赖配了 `mock` 降级，失败返回兜底而非抛错？
- [ ] 易雪崩调用接入了 Sentinel 熔断？
- [ ] 停机走优雅流程（先注销、停新请求、等存量），未 `kill -9`？
- [ ] provider 异常已转成 api jar 里的业务异常，未裸抛内部异常？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`reference-config.md`](./reference-config.md)（重试/容错策略选型）
- 兄弟：[`service-export.md`](./service-export.md)（provider 暴露）
- 兄弟：[`api-module-design.md`](./api-module-design.md)（业务异常定义在 api jar）
