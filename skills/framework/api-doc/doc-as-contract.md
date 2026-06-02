---
name: api-doc-doc-as-contract
description: 文档即契约 — 注解与代码同源避免文档漂移，生产环境关闭 OpenAPI/Swagger 端点保安全。Use when 担心文档与接口不一致 / 决定生产是否暴露文档端点 / 评审文档安全配置时。
parent: ./index.md
paths:
- '*.java'
- 'application*.yml'
triggers:
  keywords:
  - 文档即契约
  - 文档漂移
  - 注解同源
  - 生产关文档端点
  - springdoc disable
  - 文档安全
effort: medium
context: inline
version: '1.0'
---
# API 文档 · 文档即契约与生产安全

> 本条只管「文档怎么不与代码脱节 + 生产要不要暴露」。注解写法见 [`springdoc-openapi.md`](./springdoc-openapi.md)；UI 接入见 [`knife4j.md`](./knife4j.md)。

## 规则

| 维度 | 约定 |
|------|------|
| 同源 | 文档由 `@Operation`/`@Schema` 注解就地生成，**禁止**另维护一份手写 Markdown/Word 文档 |
| 防漂移 | 改接口必同步改注解（同一文件、同一 PR）；评审把注解当代码看 |
| 生产关闭 | 生产环境关 `springdoc.api-docs.enabled` 与 UI，靠 profile 区分，**默认不对外** |
| 兜安全 | 即使误开，也用 Spring Security 拦 `/v3/api-docs`、`/swagger-ui/**`、`/doc.html` |
| 不泄敏感 | `@Schema` 的 example 不写真实密钥/身份证等真值；文档泄露 = 攻击面清单 |

## 正例

```yaml
# application-prod.yml —— 生产关闭文档端点（开发/测试 profile 不设即默认开）
springdoc:
  api-docs:
    enabled: false
  swagger-ui:
    enabled: false
knife4j:
  enable: false
```

```java
// 即使配置误开，安全层再兜一道：仅非生产放行文档路径
http.authorizeHttpRequests(auth -> auth
    .requestMatchers("/v3/api-docs/**", "/swagger-ui/**", "/doc.html").denyAll()
    // ... 其余规则
);
```

## 反例

```text
❌ 接口改了入参，手写的接口文档没同步 —— 前端按旧文档对接，联调才发现漂移。
   根因：文档与代码不同源。改成注解就地生成即可消除。
```

```yaml
# ❌ 生产把文档端点对公网敞开：等于把全部接口、参数、内部模型送给攻击者
springdoc:
  api-docs:
    enabled: true   # prod 不该是 true
```

## 自检

- [ ] 文档全部来自代码注解，没有另一份手写文档需要人肉同步？
- [ ] 改接口的 PR 同时改了对应 `@Operation`/`@Schema`？
- [ ] 生产 profile 关了 `springdoc`/`knife4j` 端点？
- [ ] 安全层对 `/v3/api-docs`、`/swagger-ui/**`、`/doc.html` 有兜底拦截？
- [ ] `@Schema` 的 example 没写真实敏感值？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`springdoc-openapi.md`](./springdoc-openapi.md)（注解即文档来源）
- 兄弟：[`knife4j.md`](./knife4j.md)（生产是否暴露 `/doc.html`）
