---
name: framework-spring-boot-index
description: Spring Boot 框架使用约定 — 控制器/全局异常/参数校验/配置绑定/依赖注入/事务六个独立决策点。Use when 写 Spring Boot Controller / 配异常与校验 / 注入 Bean / 加 @Transactional 时。
parent: ../index.md
children:
  - { name: spring-boot-controller-design, path: controller-design.md, tag: skill, note: "@RestController + RESTful + 统一返回体 Result<T>" }
  - { name: spring-boot-global-exception-handler, path: global-exception-handler.md, tag: skill, note: "@RestControllerAdvice 全局兜异常转 Result" }
  - { name: spring-boot-param-validation, path: param-validation.md, tag: skill, note: "@Valid + JSR-303 + 分组校验 + 自定义校验器" }
  - { name: spring-boot-config-properties, path: config-properties.md, tag: skill, note: "@ConfigurationProperties 类型安全绑定优于 @Value" }
  - { name: spring-boot-bean-injection, path: bean-injection.md, tag: skill, note: 构造器注入优于字段注入与循环依赖处理 }
  - { name: spring-boot-transaction, path: transaction.md, tag: skill, note: "@Transactional 失效场景与传播行为" }
when_to_descend: 写 / 改 Spring Boot 的 Controller、异常处理、参数校验、配置类、Bean 注入或事务相关代码。
---

# Spring Boot · 框架使用约定索引

六个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 写 REST 接口、定统一返回体 | [controller-design](controller-design.md) |
| 想把异常统一转成接口返回体 | [global-exception-handler](global-exception-handler.md) |
| 校验请求入参（必填/格式/分组） | [param-validation](param-validation.md) |
| 读配置项、做类型安全的配置绑定 | [config-properties](config-properties.md) |
| 注入依赖、纠结字段还是构造器 / 循环依赖 | [bean-injection](bean-injection.md) |
| 加 @Transactional 却不回滚 / 不生效 | [transaction](transaction.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../fastapi/index.md`](../fastapi/index.md)
- 相关：[`../../lang/java/error-handling/index.md`](../../lang/java/error-handling/index.md)
