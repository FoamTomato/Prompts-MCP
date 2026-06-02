---
name: spring-boot-config-properties
description: Spring Boot 配置绑定 — @ConfigurationProperties 类型安全绑定优于散落 @Value，配 @Validated 校验与 profile 分环境。Use when 读多个配置项 / 配置需校验 / 按环境切换配置时。
parent: ./index.md
paths:
- '*.java'
- 'application*.yml'
triggers:
  keywords:
  - 配置绑定
  - 类型安全配置
  - '@ConfigurationProperties'
  - '@Value'
  - profile 分环境
  - 配置校验
effort: medium
context: inline
version: '1.0'
---
# Spring Boot · 配置绑定

> 本条只管「外部配置怎么读进代码」。配置类怎么被注入见 [`bean-injection.md`](./bean-injection.md)。

## 规则

| 维度 | 约定 |
|------|------|
| 一组相关配置 | 用 `@ConfigurationProperties(prefix)` 绑到类型安全的 POJO，**别散落一堆 `@Value`** |
| 配置校验 | 配置类加 `@Validated` + JSR-303 注解，启动期就拦截非法配置 |
| 分环境 | `application-{profile}.yml` 分文件，`spring.profiles.active` 切换 |
| 单个零散值 | 才用 `@Value("${a.b}")`；但同一前缀有多个值时优先聚合成类 |
| 复杂结构 | `@ConfigurationProperties` 原生支持 List / Map / 嵌套对象绑定 |

## 正例

```java
@Data
@Validated
@Component
@ConfigurationProperties(prefix = "app.storage")
public class StorageProperties {
    @NotBlank
    private String bucket;

    @Min(1)
    private int maxSizeMb = 10;     // 默认值

    private List<String> allowedTypes;  // app.storage.allowed-types
}
```

```yaml
# application.yml
app:
  storage:
    bucket: user-uploads
    max-size-mb: 20
    allowed-types: [jpg, png, pdf]
---
# application-prod.yml（spring.profiles.active=prod 时覆盖）
app:
  storage:
    bucket: prod-uploads
```

注入时直接 `private final StorageProperties props;`（构造器注入见相关链接）。

## 反例

```java
// ❌ 同一组配置拆成一堆 @Value：无类型校验、无默认值聚合、改前缀要全局搜
@Component
public class StorageConfig {
    @Value("${app.storage.bucket}")
    private String bucket;
    @Value("${app.storage.max-size-mb}")
    private int maxSizeMb;
    @Value("${app.storage.allowed-types}")
    private String allowedTypes; // 还得自己 split
}
```

❌ 不加 `@Validated` —— 配错值（如空 bucket）要等运行时才炸，而不是启动期。

## 自检

- [ ] 同前缀的多个配置聚合成 `@ConfigurationProperties` 类，没散一堆 `@Value`？
- [ ] 配置类加 `@Validated` + 约束注解，启动期校验？
- [ ] 环境差异放 `application-{profile}.yml`，靠 active profile 切换？
- [ ] List / Map / 嵌套配置用类型安全绑定，没手动 split 字符串？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`bean-injection.md`](./bean-injection.md)（配置类如何注入）
- 兄弟：[`param-validation.md`](./param-validation.md)（同一套 JSR-303 注解）
