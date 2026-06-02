---
name: observability-skywalking-tracing
description: SkyWalking 链路追踪 — javaagent 字节码增强无侵入埋点，traceId 跨服务贯穿，跨线程/MQ 需手动透传上下文。Use when 接入分布式链路追踪 / 排查跨服务调用链 / 让 traceId 贯穿时。
parent: ./index.md
paths:
- '*.java'
- '*.yml'
triggers:
  keywords:
  - 链路追踪
  - 无侵入埋点
  - SkyWalking
  - javaagent
  - traceId
  - 分布式追踪
effort: medium
context: inline
version: '1.0'
---
# 可观测 · SkyWalking 链路追踪

> 本条只管「跨服务调用链怎么追踪、traceId 怎么贯穿」。指标埋点见 [`micrometer-metrics.md`](./micrometer-metrics.md)；traceId 进日志见 [`structured-logging.md`](./structured-logging.md)。

SkyWalking 靠 **javaagent 字节码增强**，对 HTTP/RPC/DB/MQ 等主流框架**零代码侵入**自动埋点。

## 规则

| 维度 | 约定 |
|------|------|
| 接入方式 | 启动加 `-javaagent:/path/skywalking-agent.jar`，**不改业务代码** |
| 服务标识 | 配 `SW_AGENT_NAME=order-service`、`SW_AGENT_COLLECTOR_BACKEND_SERVICES` 指向 OAP |
| traceId 贯穿 | agent 自动在跨服务调用头里透传 trace 上下文，全链路同一 traceId |
| 取 traceId | 代码里用 `TraceContext.traceId()`（依赖 `apm-toolkit`）写进日志 MDC |
| 自定义埋点 | 需追踪的本地方法标 `@Trace`，`@Tags`/`@Tag` 加业务标签 |
| 跨线程/异步 | 线程池/手动建线程**会丢上下文**，用 SkyWalking 增强的线程池或 `RunnableWrapper` 透传 |

## 正例

```java
// ✅ 把 agent 维护的 traceId 注入日志 MDC，日志与链路可关联
import org.apache.skywalking.apm.toolkit.trace.TraceContext;

@Trace                          // 本地方法也纳入链路
@Tags({@Tag(key = "orderId", value = "arg[0]")})
public void settle(Long orderId) {
    MDC.put("traceId", TraceContext.traceId());
    try {
        // 业务逻辑：调下游服务时 agent 自动透传 trace 上下文
    } finally {
        MDC.remove("traceId");
    }
}
```

```yaml
# 启动参数（k8s/JVM）
# JAVA_TOOL_OPTIONS: "-javaagent:/sw/skywalking-agent.jar"
# SW_AGENT_NAME: order-service
# SW_AGENT_COLLECTOR_BACKEND_SERVICES: oap-svc:11800
```

## 反例

```java
// ❌ 自己往业务里塞 OpenTracing API 全量手动埋点：维护成本高，agent 已自动做
Span span = tracer.buildSpan("call").start();   // 重复造轮子

// ❌ 异步任务直接丢进裸线程池：trace 上下文丢失，链路在此断裂
executor.submit(() -> downstream.call());        // 需用增强线程池透传
```

## 自检

- [ ] 用 javaagent 无侵入接入，没在业务里写大量手动 Span？
- [ ] 配了 `SW_AGENT_NAME` 与 OAP 后端地址？
- [ ] 跨线程/异步场景透传了 trace 上下文（增强线程池 / Wrapper）？
- [ ] traceId 写进日志 MDC，链路与日志能互相关联？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`structured-logging.md`](./structured-logging.md)（traceId 进日志 MDC）
- 兄弟：[`micrometer-metrics.md`](./micrometer-metrics.md)（指标与追踪互补）
