---
name: behavioral-chain-of-responsibility
description: 责任链模式 — 请求沿一串处理者依次流转，每个节点处理或放行，链可增删重排（过滤器/拦截器链同源）。Use when 一个请求要过多道处理 / 想可插拔增删处理节点 / 实现过滤拦截链时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 责任链
  - Chain of Responsibility
  - 过滤器链
  - 拦截器链
  - 处理节点
  - Filter
effort: medium
context: inline
version: '1.0'
---
# Behavioral · 责任链

## 何时用

| 信号 | 用责任链 |
|------|---------|
| 一个请求要依次过多道处理（鉴权→限流→校验→业务） | ✅ |
| 处理节点要可插拔增删、可重排顺序 | ✅ |
| 节点能决定「拦截终止」或「放行给下一个」 | ✅ |
| 只有固定两三步、永不变 | ❌ 直接顺序调用 |

## 正例：可增删的处理链

```java
public interface Handler {
    // 返回 true 放行给下一个；false 终止链
    boolean handle(Request req, Chain chain);
}

public class Chain {
    private final List<Handler> handlers;
    private int idx = 0;
    public Chain(List<Handler> handlers) { this.handlers = handlers; }
    public boolean proceed(Request req) {
        if (idx >= handlers.size()) return true;       // 链末尾
        return handlers.get(idx++).handle(req, this);  // 交下一个节点
    }
}

public class AuthHandler implements Handler {
    public boolean handle(Request req, Chain chain) {
        if (!req.authed()) return false;               // 拦截
        return chain.proceed(req);                     // 放行
    }
}
// 增删节点 = 改 handlers 列表，节点之间互不知道彼此
```

## 实际中的责任链

Servlet `Filter` / Spring `HandlerInterceptor` / OkHttp `Interceptor` / Netty `ChannelPipeline` / Spring Security 过滤器链——都是责任链。自己实现前先确认框架是否已提供。

## 反例：写死的 if 串

```java
// ❌ 节点写死、加一道处理就改这个方法，且顺序与开关耦合
public boolean process(Request req) {
    if (!req.authed()) return false;
    if (overLimit(req)) return false;
    if (!valid(req)) return false;
    // 想插一道、想跳过一道都得改这里
    return true;
}
```

## 自检

- [ ] 每个处理节点只关心自己那段，不知道前后是谁？
- [ ] 节点能「放行 / 终止」，由链统一驱动 proceed？
- [ ] 增删/重排节点只改配置/列表，不改节点内部？
- [ ] 框架已提供拦截链（Filter/Interceptor）时，没有重复造轮子？

## 相关

- 父：[`./index.md`](./index.md)
- 流程编排对比：[`../pipeline/index.md`](../pipeline/index.md)（固定多步 vs 可插拔链）
