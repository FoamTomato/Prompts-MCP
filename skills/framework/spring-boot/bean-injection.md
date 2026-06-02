---
name: spring-boot-bean-injection
description: Spring Boot 依赖注入 — 构造器注入优于字段注入，配 @RequiredArgsConstructor、@Qualifier 选型、循环依赖处理。Use when 注入 Bean / 纠结字段还是构造器注入 / 排查循环依赖时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 依赖注入
  - 构造器注入
  - 循环依赖
  - '@Autowired'
  - '@RequiredArgsConstructor'
  - '@Qualifier'
effort: medium
context: inline
version: '1.0'
---
# Spring Boot · 依赖注入

> 本条只管「Bean 怎么注入进来」。配置类的绑定见 [`config-properties.md`](./config-properties.md)。

## 规则

| 维度 | 约定 |
|------|------|
| 默认方式 | **构造器注入**：依赖 `final`、可测试、启动期暴露缺失依赖 |
| 字段注入 | 反模式，`@Autowired` 写字段上隐藏依赖、`final` 用不了、单测难 mock |
| 省样板 | Lombok `@RequiredArgsConstructor` 自动为 `final` 字段生成构造器 |
| 多实现选一个 | `@Qualifier("beanName")` 指定，或在某个实现上标 `@Primary` |
| 循环依赖 | 是**设计信号**：优先拆职责 / 引入第三方协作类，别靠 `@Lazy` 硬绕 |

## 正例

```java
// ✅ 构造器注入 + Lombok，依赖 final、无 @Autowired 噪声
@Service
@RequiredArgsConstructor
public class OrderService {
    private final UserService userService;
    private final PaymentGateway paymentGateway;
}

// ✅ 多实现按名选取
@Service
@RequiredArgsConstructor
public class NotifyService {
    @Qualifier("smsSender")
    private final MessageSender sender;
}
```

单 Spring 4.3+，类只有一个构造器时连 `@Autowired` 都不用写。

## 反例

```java
// ❌ 字段注入：依赖不能 final、被隐藏、单测必须起 Spring 容器才能注入
@Service
public class OrderService {
    @Autowired
    private UserService userService;
    @Autowired
    private PaymentGateway paymentGateway;
}
```

❌ A 构造器注入 B、B 又构造器注入 A —— 启动直接 `BeanCurrentlyInCreationException`。用 `@Lazy` 只是掩盖，正解是抽出共用逻辑到第三个类，打破环。

## 自检

- [ ] 用构造器注入，依赖字段都是 `final`？
- [ ] 没有 `@Autowired` 标在字段上的写法？
- [ ] 多个候选 Bean 时用 `@Qualifier` 或 `@Primary` 明确选取？
- [ ] 出现循环依赖时拆职责打破环，而不是 `@Lazy` 硬绕？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`config-properties.md`](./config-properties.md)（配置类的注入）
- 兄弟：[`transaction.md`](./transaction.md)（自调用绕过代理与注入相关）
