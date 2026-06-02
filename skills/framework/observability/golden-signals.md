---
name: observability-golden-signals
description: 黄金指标 — 延迟/流量/错误/饱和度四类信号决定该监控告警哪些指标，延迟看分位数而非平均，告警建在这四类上。Use when 不知道该监控哪些指标 / 配告警 / 评审看板覆盖度时。
parent: ./index.md
paths:
- '*.java'
- '*.yml'
triggers:
  keywords:
  - 黄金指标
  - 监控告警
  - 延迟分位
  - 饱和度
  - 错误率
  - golden signals
effort: medium
context: inline
version: '1.0'
---
# 可观测 · 黄金指标

> 本条只管「该监控/告警**哪些**指标」。指标怎么埋见 [`micrometer-metrics.md`](./micrometer-metrics.md)；调用链排查见 [`skywalking-tracing.md`](./skywalking-tracing.md)。

来自 Google SRE：监控**先覆盖这四类**，再谈业务指标。看板与告警都建在这四类上。

## 四类信号

| 信号 | 是什么 | 怎么测（Micrometer） | 告警怎么定 |
|------|--------|---------------------|-----------|
| 延迟 Latency | 处理请求耗时 | Timer **分位数** p95/p99 | 盯 p99，**别用平均**（被长尾掩盖）；成功与失败延迟分开统计 |
| 流量 Traffic | 系统负载/吞吐 | Counter → QPS、并发数 | 看趋势与突增突降 |
| 错误 Errors | 失败请求占比 | 错误 Counter / 总请求 | 错误率超阈值（如 >1%）告警；区分 5xx 与业务失败 |
| 饱和度 Saturation | 资源用满程度 | Gauge：线程池/连接池/队列/堆/CPU | 最接近瓶颈的资源；常配 80% 预警线 |

## 正例

```java
// ✅ 错误率：成功失败分别计数，可算 errors/total
public OrderVO place(OrderDTO dto) {
    try {
        OrderVO vo = doPlace(dto);
        registry.counter("order.req", "result", "success").increment();
        return vo;
    } catch (Exception e) {
        registry.counter("order.req", "result", "error").increment();
        throw e;
    }
}

// ✅ 饱和度：把线程池活跃数注册成 Gauge
Gauge.builder("executor.active", executor, ThreadPoolExecutor::getActiveCount)
     .register(registry);
```

```promql
# 延迟看 p99 分位，不看平均
histogram_quantile(0.99, rate(order_place_seconds_bucket[5m]))
```

## 反例

```text
❌ 只配「平均延迟」告警 —— 平均被海量快请求拉低，p99 已爆但均值正常，告警不响。
❌ 只监控 CPU 一项就以为够了 —— 漏了错误率与饱和度，错误激增时无人知晓。
❌ 把成功与失败请求的延迟混在一起统计 —— 失败常很快返回，会拉低整体延迟假象。
```

## 自检

- [ ] 延迟、流量、错误、饱和度四类都有覆盖？
- [ ] 延迟看 p95/p99 分位，不是只看平均？
- [ ] 错误率告警区分了 5xx 与业务失败？
- [ ] 饱和度盯的是最接近瓶颈的资源（线程池/连接池/队列）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`micrometer-metrics.md`](./micrometer-metrics.md)（这四类指标怎么埋）
- 兄弟：[`skywalking-tracing.md`](./skywalking-tracing.md)（指标异常后下钻调用链）
