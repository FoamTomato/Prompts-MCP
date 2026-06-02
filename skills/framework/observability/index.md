---
name: framework-observability-index
description: 通用应用可观测性规约 — Micrometer 指标、SkyWalking 链路追踪、结构化日志、黄金指标四个独立决策点。Use when 埋点指标 / 接入链路追踪 / 规范 JSON 日志 / 定监控告警指标时。
parent: ../index.md
children:
  - { name: observability-micrometer-metrics, path: micrometer-metrics.md, tag: skill, note: "Micrometer 门面 @Timed/Counter/Gauge 对接 Prometheus" }
  - { name: observability-skywalking-tracing, path: skywalking-tracing.md, tag: skill, note: "SkyWalking javaagent 无侵入链路追踪，traceId 贯穿" }
  - { name: observability-structured-logging, path: structured-logging.md, tag: skill, note: "结构化 JSON 日志 + traceId(MDC)，ELK/EFK 收集" }
  - { name: observability-golden-signals, path: golden-signals.md, tag: skill, note: 黄金指标：延迟/流量/错误/饱和度，监控告警建在这四类 }
when_to_descend: 给 Java 应用做可观测：埋指标对接 Prometheus、接入 SkyWalking 链路追踪、规范结构化日志、或确定监控告警该盯哪些指标。
---

# 通用应用可观测性 · 子项索引

四个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 给方法埋耗时/计数/瞬时值，对接 Prometheus 采集 | [micrometer-metrics](micrometer-metrics.md) |
| 跨服务排查调用链、让 traceId 贯穿全链路 | [skywalking-tracing](skywalking-tracing.md) |
| 规范日志格式、让日志带 traceId 进 ELK/EFK | [structured-logging](structured-logging.md) |
| 不知道该监控/告警哪些指标 | [golden-signals](golden-signals.md) |

> 本模块是**通用应用可观测**。LLM 调用链的 prompt/token/成本可观测见 [`../../ai/llm-engineering/observability.md`](../../ai/llm-engineering/observability.md)，不在此重复。

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../spring-boot/index.md`](../spring-boot/index.md) · [`../connection-pool/index.md`](../connection-pool/index.md)
- 相关：[`../../ai/llm-engineering/observability.md`](../../ai/llm-engineering/observability.md)（LLM 维度可观测）
