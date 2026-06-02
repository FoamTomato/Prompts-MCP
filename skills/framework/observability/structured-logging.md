---
name: observability-structured-logging
description: 结构化 JSON 日志 — 输出机器可解析的 JSON 字段并携带 traceId(MDC)，供 ELK/EFK 采集检索，禁日志中打印敏感信息。Use when 规范日志格式 / 让日志带 traceId / 接入 ELK/EFK 时。
parent: ./index.md
paths:
- '*.java'
- '*.yml'
triggers:
  keywords:
  - 结构化日志
  - JSON 日志
  - MDC
  - traceId
  - ELK
  - EFK
effort: medium
context: inline
version: '1.0'
---
# 可观测 · 结构化日志

> 本条只管「日志格式与采集」。traceId 怎么来见 [`skywalking-tracing.md`](./skywalking-tracing.md)；数值型监控用指标见 [`micrometer-metrics.md`](./micrometer-metrics.md)。

日志要给**机器解析**，不是给人 grep。输出 JSON、带 traceId，进 ELK/EFK 后可按字段检索聚合。

## 规则

| 维度 | 约定 |
|------|------|
| 格式 | 生产输出 **JSON**（`logstash-logback-encoder`），别用人肉拼接的纯文本 |
| 关联字段 | 每条日志带 `traceId`/`spanId`，从 MDC 取，串起同一请求 |
| MDC 注入 | 入口（Filter/拦截器）`MDC.put`，**finally 必须 `MDC.clear()`**（线程池复用会串号） |
| 参数化 | 用 `log.info("user={}", id)` 占位符，不用字符串拼接 |
| 级别 | ERROR 记可定位异常（带堆栈），INFO 记关键链路，DEBUG 默认关 |
| 脱敏 | **禁打印**密码/token/身份证/手机号等敏感信息 |
| 采集 | 容器日志写 stdout，由 Filebeat/Fluentd 收集进 ES，Kibana 检索 |

## 正例

```java
// ✅ 入口拦截器注入 traceId，finally 清理防线程复用串号
public class TraceIdFilter extends OncePerRequestFilter {
    protected void doFilterInternal(HttpServletRequest req,
            HttpServletResponse resp, FilterChain chain) throws IOException, ServletException {
        MDC.put("traceId", resolveTraceId(req));   // 或取自 SkyWalking
        try {
            chain.doFilter(req, resp);
        } finally {
            MDC.clear();                            // 必须清理
        }
    }
}
```

```xml
<!-- logback-spring.xml：JSON 编码器，traceId 随每条日志输出 -->
<encoder class="net.logstash.logback.encoder.LogstashEncoder">
    <includeMdcKeyName>traceId</includeMdcKeyName>
</encoder>
```

## 反例

```java
// ❌ 字符串拼接 + 打印敏感信息 + 无 traceId，ELK 无法按字段检索、且泄密
log.info("login user=" + username + " pwd=" + password);

// ❌ MDC.put 后不 clear：线程池复用时下一个请求看到上一个的 traceId
MDC.put("traceId", id);   // 没有 finally clear
```

## 自检

- [ ] 生产日志输出 JSON，可被 ELK/EFK 按字段解析？
- [ ] 每条日志带 traceId（MDC），能串起整条请求？
- [ ] MDC 在 finally 里 `clear()`，没线程复用串号？
- [ ] 用占位符参数化，没字符串拼接？
- [ ] 没打印密码/token 等敏感信息？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`skywalking-tracing.md`](./skywalking-tracing.md)（traceId 来源）
- 兄弟：[`micrometer-metrics.md`](./micrometer-metrics.md)（数值监控走指标不走日志）
