---
name: framework-api-doc-index
description: Spring Boot 3 API 文档规范 3 项 — springdoc-openapi 注解 / Knife4j 增强 UI / 文档即契约与生产安全。Use when 给接口加 OpenAPI 注解 / 接 Knife4j 文档 UI / 防文档漂移与关生产文档端点时。
parent: ../index.md
children:
  - { name: api-doc-springdoc-openapi, path: springdoc-openapi.md, tag: skill, note: "springdoc-openapi 替代 springfox：@Operation / @Schema / @Parameter 注解" }
  - { name: api-doc-knife4j, path: knife4j.md, tag: skill, note: "Knife4j 增强 UI，国内常用，基于 OpenAPI 3" }
  - { name: api-doc-doc-as-contract, path: doc-as-contract.md, tag: skill, note: "文档即契约：注解与代码同源防漂移、生产关文档端点" }
when_to_descend: 写 / 评审 Spring Boot 3 的 OpenAPI 注解、Knife4j 接入或文档安全相关配置
---

# API 文档 · 子项索引

Spring Boot 3 的 API 文档拆成 3 个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 给 Controller / DTO 加 OpenAPI 注解（选 starter、@Operation/@Schema/@Parameter 写法） | [springdoc-openapi](springdoc-openapi.md) |
| 接增强版文档 UI（国内常用的 Knife4j，调试/分组/认证） | [knife4j](knife4j.md) |
| 防注解与代码漂移、生产环境关闭文档端点保安全 | [doc-as-contract](doc-as-contract.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 相关：[`../spring-boot/controller-design.md`](../spring-boot/controller-design.md)（接口与 Result 返回体）
