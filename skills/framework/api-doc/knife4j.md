---
name: api-doc-knife4j
description: Knife4j 是国内常用的 OpenAPI 3 增强文档 UI，在 springdoc 之上提供调试、接口分组、全局认证参数。Use when 想要比默认 Swagger UI 更好用的文档界面 / 配接口分组与全局 token 调试时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 增强文档界面
  - Knife4j
  - 接口调试 UI
  - Swagger UI 替代
  - 接口分组
  - 全局认证参数
effort: medium
context: inline
version: '1.0'
---
# API 文档 · Knife4j 增强 UI

> 本条只管「换一个更好用的文档 UI 并配分组/认证」。注解怎么写见 [`springdoc-openapi.md`](./springdoc-openapi.md)；生产是否暴露见 [`doc-as-contract.md`](./doc-as-contract.md)。

## 规则

| 维度 | 约定 |
|------|------|
| 定位 | Knife4j 只是 UI 层，**底层仍是 springdoc/OpenAPI 3**，注解照常用 `@Operation` 等 |
| Boot 3 依赖 | 用 `knife4j-openapi3-jakarta-spring-boot-starter`（jakarta 版，匹配 Boot 3） |
| 访问入口 | 默认 `/doc.html`（区别于原生 `/swagger-ui.html`），比默认 UI 更适合调试 |
| 接口分组 | 多模块/多业务用 `GroupedOpenApi` 按包路径分组，避免一页几百个接口 |
| 全局认证 | 鉴权接口在 `OpenAPI` 里配 securitySchemes，UI 上一次性填 token 全局带上 |

## 正例

```java
@Configuration
public class OpenApiConfig {

    // 全局信息 + 全局认证：UI 顶部填一次 JWT，调试时自动带 Authorization 头
    @Bean
    public OpenAPI openAPI() {
        return new OpenAPI()
            .info(new Info().title("订单服务 API").version("v1"))
            .addSecurityItem(new SecurityRequirement().addList("JWT"))
            .components(new Components().addSecuritySchemes("JWT",
                new SecurityScheme().type(SecurityScheme.Type.HTTP)
                    .scheme("bearer").bearerFormat("JWT")));
    }

    // 按包分组，文档左侧分模块
    @Bean
    public GroupedOpenApi orderApi() {
        return GroupedOpenApi.builder()
            .group("订单")
            .packagesToScan("com.example.order.controller")
            .build();
    }
}
```

依赖（Maven，Boot 3）：

```xml
<dependency>
    <groupId>com.github.xiaoymin</groupId>
    <artifactId>knife4j-openapi3-jakarta-spring-boot-starter</artifactId>
    <version>4.x</version>  <!-- 以官网最新 4.x 为准 -->
</dependency>
```

## 反例

```java
// ❌ Boot 3 引了 knife4j 的 spring/2.x 老版本（非 jakarta）：启动即类找不到
// com.github.xiaoymin:knife4j-spring-boot-starter  —— Boot 2 时代产物

// ❌ 不分组：单体里几百个接口全堆一页，左侧列表无法浏览
```

## 自检

- [ ] Boot 3 用的是 `knife4j-openapi3-jakarta-spring-boot-starter`（jakarta 版）？
- [ ] 接口注解仍写 springdoc 的 `@Operation`/`@Schema`，没因为换 UI 改注解？
- [ ] 接口多时用 `GroupedOpenApi` 分组，没全堆一页？
- [ ] 鉴权服务配了全局 securityScheme，调试不用每个接口手填 token？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`springdoc-openapi.md`](./springdoc-openapi.md)（底层注解，UI 的数据来源）
- 兄弟：[`doc-as-contract.md`](./doc-as-contract.md)（生产环境是否暴露 `/doc.html`）
