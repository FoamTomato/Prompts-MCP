---
name: framework-grpc-index
description: gRPC 使用规范 4 项 — Protobuf 定义与兼容 / 四种调用方式 / 错误与 deadline / 与 REST·Dubbo 选型。Use when 写 .proto 或 gRPC 服务 / 选调用方式 / 处理超时错误 / 做 RPC 选型时。
parent: ../index.md
children:
  - { name: grpc-proto-definition, path: proto-definition.md, tag: skill, note: "Protobuf 定义：message/service、字段编号不复用、reserved、向后兼容" }
  - { name: grpc-four-call-types, path: four-call-types.md, tag: skill, note: "四种调用：一元/服务端流/客户端流/双向流及适用场景" }
  - { name: grpc-error-and-deadline, path: error-and-deadline.md, tag: skill, note: "错误处理 Status code + deadline 超时传播，必设 deadline" }
  - { name: grpc-vs-rest-dubbo, path: grpc-vs-rest-dubbo.md, tag: skill, note: "选型：gRPC vs REST vs Dubbo，跨语言/HTTP2/Protobuf vs 生态" }
when_to_descend: 写 / 评审 .proto 或 gRPC 服务、选调用方式、处理错误超时、做 RPC 通信选型
---

# gRPC · 子项索引

gRPC 使用拆成 4 个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 写/改 .proto：定义 message/service、改字段又要保证向后兼容 | [proto-definition](proto-definition.md) |
| 定义 rpc 方法：选一元还是服务端流/客户端流/双向流 | [four-call-types](four-call-types.md) |
| 处理错误（Status code）、设超时与 deadline 传播 | [error-and-deadline](error-and-deadline.md) |
| 在 gRPC / REST / Dubbo 之间做通信选型 | [grpc-vs-rest-dubbo](grpc-vs-rest-dubbo.md) |
