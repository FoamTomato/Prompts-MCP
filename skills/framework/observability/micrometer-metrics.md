---
name: observability-micrometer-metrics
description: Micrometer 指标门面 — @Timed/Counter/Gauge 三类仪表对接 Prometheus，Actuator 暴露 /actuator/prometheus 供拉取。Use when 给方法埋耗时/计数/瞬时值 / 对接 Prometheus / 暴露指标端点时。
parent: ./index.md
paths:
- '*.java'
- '*.yml'
triggers:
  keywords:
  - 指标埋点
  - 监控门面
  - Micrometer
  - '@Timed'
  - Prometheus
  - actuator/prometheus
effort: medium
context: inline
version: '1.0'
---
# 可观测 · Micrometer 指标

> 本条只管「指标怎么埋、怎么暴露给 Prometheus」。该埋哪些指标见 [`golden-signals.md`](./golden-signals.md)；链路追踪见 [`skywalking-tracing.md`](./skywalking-tracing.md)。

Micrometer 是指标**门面**（类比 SLF4J），代码不绑 Prometheus，换后端不改埋点。

## 规则

| 仪表类型 | 用途 | 怎么埋 |
|---------|------|--------|
| Timer | 耗时分布（含 count/max/分位） | 方法标 `@Timed`，或 `Timer.record()` |
| Counter | 只增计数（请求数、错误数） | `Counter.increment()` |
| Gauge | 瞬时值（队列长度、连接数） | `Gauge.builder()` 绑一个被观测对象 |
| 标签 tag | 同名指标按维度（接口/状态码）下钻 | `tags("uri", uri, "status", code)`，**禁用高基数值**（如用户 id） |
| 暴露 | Prometheus 拉取端点 | Actuator 暴露 `/actuator/prometheus` |

## 正例

```java
@Service
@RequiredArgsConstructor
public class OrderService {
    private final MeterRegistry registry;

    @Timed(value = "order.place", description = "下单耗时")  // 自动产出 Timer
    public void place(OrderDTO dto) { /* ... */ }

    public void onPaid(String channel) {
        // ✅ 低基数标签：渠道是有限枚举
        registry.counter("order.paid", "channel", channel).increment();
    }
}
```

```yaml
# application.yml —— 暴露 prometheus 端点 + 给所有指标打公共标签
management:
  endpoints.web.exposure.include: health,info,prometheus
  metrics.tags.application: order-service   # 公共标签便于多服务区分
```

`@Timed` 需注册 `TimedAspect` Bean（引 `micrometer-registry-prometheus` + AOP）。

## 反例

```java
// ❌ 标签用高基数值：每个 userId 生成一条时间序列，撑爆 Prometheus 内存
registry.counter("order.paid", "userId", userId).increment();

// ❌ 自己 new AtomicLong 打日志统计，不进指标系统，无法聚合/告警
log.info("current qps = {}", count.incrementAndGet());
```

## 自检

- [ ] 用 Micrometer 门面而非直接依赖 Prometheus 客户端？
- [ ] 标签只用**低基数**枚举值，没把 userId/订单号当 tag？
- [ ] 耗时用 Timer（含分位），不是自己算平均？
- [ ] Actuator 已暴露 `/actuator/prometheus`，公共标签区分了服务？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`golden-signals.md`](./golden-signals.md)（该埋哪些指标）
- 兄弟：[`skywalking-tracing.md`](./skywalking-tracing.md)（链路追踪互补）
