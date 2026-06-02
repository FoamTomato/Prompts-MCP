---
name: spring-security-oauth2-resource-server
description: Spring Security OAuth2 资源服务器 — 用 starter 配 issuer/jwk-set 自动校验外部签发 JWT 的签名，不手写解析。Use when 接 OAuth2/OIDC / 校验第三方 JWT 签名 / 配资源服务器时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 资源服务器
  - JWT 签名校验
  - oauth2ResourceServer
  - JwtDecoder
  - jwk-set-uri
effort: medium
context: inline
version: '1.0'
---
# Spring Security · OAuth2 资源服务器

> 本条只管「token 由外部授权服务器（IdP）签发时，怎么让框架校验签名」（**验签侧**）。token 由谁**签发**见 [`oauth2-authorization-server.md`](./oauth2-authorization-server.md)——授权服务器签发、资源服务器验签，是两端。自己签发的 JWT 手写解析见 [`jwt-stateless.md`](./jwt-stateless.md)——二者别混用。

## 规则

| 维度 | 约定 |
|------|------|
| 依赖 | `spring-boot-starter-oauth2-resource-server`，**别手写 `OncePerRequestFilter` 解析外部 JWT** |
| 启用 | 链里 `http.oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))` |
| 签名校验 | 配 `issuer-uri`（自动拉取 JWKS）或直接 `jwk-set-uri`；框架按公钥验签，过期/篡改自动拒 |
| 权限映射 | JWT 的 `scope`/`roles` claim → `GrantedAuthority`，必要时配 `JwtAuthenticationConverter` |
| 密钥管理 | **公钥来自 IdP 的 JWKS 端点**，不硬编码密钥；对称密钥（HMAC）的 secret 走配置中心/环境变量 |

## 正例

```yaml
# application.yml —— 配 issuer，框架自动发现 JWKS 端点并验签
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://auth.example.com/realms/app
```

```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http
        .authorizeHttpRequests(a -> a.anyRequest().authenticated())
        // 启用资源服务器：框架按 JWKS 公钥校验签名，无需手写解析
        .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()));
    return http.build();
}
```

## 反例

```java
// ❌ 对外部 IdP 签发的 JWT 手写过滤器解析，还跳过签名校验 —— 任何人伪造 payload 即可冒充
String payload = new String(Base64.getDecoder().decode(token.split("\\.")[1]));
// 只 decode 不验签：等于不设防
```

❌ 把验签密钥（HMAC secret / 私钥）硬编码进代码或提交进仓库：密钥必须走配置中心/环境变量；非对称场景只持有 IdP 公钥（JWKS），服务端不该有私钥。

## 自检

- [ ] 用 `spring-boot-starter-oauth2-resource-server`，没手写解析外部 JWT？
- [ ] 配了 `issuer-uri` 或 `jwk-set-uri`，框架按公钥自动验签？
- [ ] 没有「只 decode 不验签」的代码？
- [ ] 密钥来自 JWKS / 配置中心 / 环境变量，没硬编码进仓库？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`oauth2-authorization-server.md`](./oauth2-authorization-server.md)（对端：授权服务器签发 token，本条拉 JWKS 公钥验签）
- 兄弟：[`oauth2-grant-types.md`](./oauth2-grant-types.md)（token 是用哪种授权模式签发的）
- 兄弟：[`jwt-stateless.md`](./jwt-stateless.md)（自签 JWT 手写解析；外部签发用本条，别混）
- 兄弟：[`filter-chain.md`](./filter-chain.md)（在链里挂资源服务器）
- 兄弟：[`authorization.md`](./authorization.md)（claim 映射成权限后做授权）
