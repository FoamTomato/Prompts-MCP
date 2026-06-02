---
name: framework-dubbo-index
description: Apache Dubbo 3.x RPC 使用规范 4 项 — 服务暴露 / 服务引用 / API 模块设计 / 优雅降级容错。Use when 写 Dubbo provider 或 consumer / 设计 RPC 接口与 DTO / 评审 Dubbo 调用与容错 PR 时。
parent: ../index.md
children:
  - { name: dubbo-service-export, path: service-export.md, tag: skill, note: "服务暴露：@DubboService、version/group 多版本、timeout、接口实现分离" }
  - { name: dubbo-reference-config, path: reference-config.md, tag: skill, note: "服务引用：@DubboReference、retries、loadbalance、cluster 容错" }
  - { name: dubbo-api-module-design, path: api-module-design.md, tag: skill, note: "API 模块：接口与 DTO 独立 jar、DTO 必须 Serializable、版本兼容" }
  - { name: dubbo-graceful-degradation, path: graceful-degradation.md, tag: skill, note: "优雅降级：mock 降级、熔断 Sentinel、优雅停机、异常隔离" }
when_to_descend: 写 / 评审 Dubbo provider 暴露、consumer 引用、API 模块设计或降级容错
---

# Apache Dubbo · 子项索引

Dubbo 3.x RPC 使用拆成 4 个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| provider 端暴露服务（注解、多版本、超时、接口实现分离） | [service-export](service-export.md) |
| consumer 端引用服务（注解、重试、负载均衡、集群容错） | [reference-config](reference-config.md) |
| 设计 provider/consumer 共享的 API 模块（接口 + DTO jar、序列化、版本兼容） | [api-module-design](api-module-design.md) |
| 做降级、熔断、优雅停机、防止 provider 异常直接打到 consumer | [graceful-degradation](graceful-degradation.md) |
