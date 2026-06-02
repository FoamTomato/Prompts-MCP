---
name: grpc-vs-rest-dubbo
description: RPC/接口选型 — gRPC vs REST vs Dubbo，对比跨语言、HTTP/2、Protobuf 性能与生态。Use when 选 gRPC 还是 REST 还是 Dubbo / 评审跨语言或对外接口选型时。
parent: ./index.md
paths:
- '*.java'
- '*.proto'
triggers:
  keywords:
  - 选型
  - 跨语言
  - HTTP2
  - gRPC
  - REST
  - Dubbo
effort: medium
context: inline
version: '1.0'
---
# gRPC · vs REST vs Dubbo 选型

> 本条只管「该选哪种通信方式」。gRPC 自身怎么用见兄弟叶子；Dubbo 用法见 [`../dubbo/index.md`](../dubbo/index.md)。

## 规则

| 维度 | gRPC | REST/JSON | Dubbo |
|------|------|-----------|-------|
| 传输/编码 | HTTP/2 + Protobuf（二进制，体积小、序列化快） | HTTP/1.1 + JSON（文本，可读、体积大） | 默认 Triple(HTTP/2) 或私有 dubbo 协议 |
| 跨语言 | 强：官方多语言代码生成，异构系统首选 | 强：任何语言/工具都能调 | 弱：以 Java 生态为主，其他语言支持有限 |
| 流式 | 原生四种（含双向流） | 需 SSE/WebSocket 另搞 | Triple 支持流式，传统调用以一元为主 |
| 浏览器直连 | 不能直连（需 grpc-web 代理） | 原生支持，最适合对外/前端 | 不适合对外 |
| 契约 | .proto 强契约、强类型 | OpenAPI/约定式，弱类型 | Java 接口即契约 |
| 服务治理 | 需自配（xDS/服务网格/Nacos 等） | 需自配 | 内建：注册发现、负载均衡、容错、降级 |

## 选型口诀

- **对外 / 给浏览器 / 给第三方** → REST/JSON（通用、可读、易调试）。
- **内部高频、跨语言、要流式、追求低延迟** → gRPC。
- **纯 Java 微服务、要开箱即用的服务治理（注册/容错/降级）** → Dubbo（见 [`../dubbo/index.md`](../dubbo/index.md)）。

## 正例

```text
场景：Java 订单服务 ←→ Go 风控服务，内部高频、要低延迟、要流式推送
选择：gRPC —— Protobuf 跨语言、HTTP/2 多路复用、原生服务端流推送
```

```text
场景：纯 Java 内部微服务集群，要现成的注册发现 + 容错 + 灰度
选择：Dubbo —— 服务治理开箱即用，无需自搭一套
```

## 反例

❌ 对外开放 API 用 gRPC 裸协议：浏览器无法直连、第三方接入成本高 → 对外用 REST。

❌ 只为「显得高级」在单语言、低频、无流式需求的场景上 gRPC：徒增 proto 编译与调试成本，REST 更省事。

❌ 异构多语言系统硬用 Dubbo：非 Java 端支持薄弱，不如 gRPC 跨语言。

## 自检

- [ ] 对外/浏览器场景选了 REST，没有裸用 gRPC？
- [ ] 跨语言 + 高频 + 流式才选 gRPC？
- [ ] 纯 Java 且要现成服务治理才选 Dubbo？
- [ ] 选型是按真实需求，而非「技术新潮」？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`proto-definition.md`](./proto-definition.md)（选了 gRPC 后怎么定义 proto）
- 兄弟：[`four-call-types.md`](./four-call-types.md)（gRPC 四种调用）
- 跨模块：[`../dubbo/index.md`](../dubbo/index.md)（选了 Dubbo 看这里）
