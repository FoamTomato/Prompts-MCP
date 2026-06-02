---
name: spring-security-oauth2-authorization-server
description: Spring Authorization Server 授权服务器 — 注册 client、走授权码 + PKCE、签发 token，与资源服务器分工（签发 vs 验签）。Use when 搭授权服务器 / 配 RegisteredClient / 签发 token / 接授权码 PKCE 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 授权服务器
  - 授权码模式
  - PKCE
  - RegisteredClient
  - AuthorizationServerSettings
  - token 签发
effort: medium
context: inline
version: '1.0'
---
# Spring Security · OAuth2 授权服务器

> 本条只管「授权服务器侧怎么注册 client、签发 token」。token 发出去后由资源服务器**验签**见 [`oauth2-resource-server.md`](./oauth2-resource-server.md)——授权服务器**签发**、资源服务器**验签**，是两端，别混在一个应用里写。选哪种授权模式见 [`oauth2-grant-types.md`](./oauth2-grant-types.md)。

## 规则

| 维度 | 约定 |
|------|------|
| 依赖 | `spring-boot-starter-oauth2-authorization-server`（独立于资源服务器 starter，由 Spring Authorization Server 提供） |
| 默认配置 | 用 `OAuth2AuthorizationServerConfiguration.applyDefaultSecurity(http)` 暴露 `/oauth2/authorize`、`/oauth2/token`、`/oauth2/jwks` 等标准端点 |
| client 注册 | `RegisteredClient` + `RegisteredClientRepository`（生产用 `JdbcRegisteredClientRepository` 落库，别只用内存版） |
| 授权码 + PKCE | 公共客户端（SPA / App 无法保密 secret）必须 `requireProofKey(true)` 强制 PKCE，挡授权码拦截攻击 |
| 签名密钥 | 暴露 `JWKSource`（RSA/EC 密钥对），私钥签 token、公钥发布在 `/oauth2/jwks` 供资源服务器拉取验签 |
| issuer | `AuthorizationServerSettings.builder().issuer(...)`，须与资源服务器配的 `issuer-uri` 一致 |

## 正例

```java
@Bean
public RegisteredClientRepository registeredClientRepository() {
    // 授权码 + PKCE 的公共客户端：不发 client secret，强制 PKCE
    RegisteredClient spaClient = RegisteredClient.withId(UUID.randomUUID().toString())
        .clientId("spa-app")
        .clientAuthenticationMethod(ClientAuthenticationMethod.NONE)   // 公共客户端无 secret
        .authorizationGrantType(AuthorizationGrantType.AUTHORIZATION_CODE)
        .authorizationGrantType(AuthorizationGrantType.REFRESH_TOKEN)
        .redirectUri("https://app.example.com/callback")
        .scope("read")
        .clientSettings(ClientSettings.builder().requireProofKey(true).build()) // 强制 PKCE
        .build();
    return new InMemoryRegisteredClientRepository(spaClient);
}

@Bean
public AuthorizationServerSettings authorizationServerSettings() {
    // issuer 必须与资源服务器的 issuer-uri 完全一致，否则验签时 iss 校验失败
    return AuthorizationServerSettings.builder().issuer("https://auth.example.com").build();
}
```

## 反例

```java
// ❌ 公共客户端（SPA/App）却不强制 PKCE：授权码可被中间人拦截后直接换 token
RegisteredClient.withId(id).clientId("spa-app")
    .clientAuthenticationMethod(ClientAuthenticationMethod.NONE)
    .authorizationGrantType(AuthorizationGrantType.AUTHORIZATION_CODE)
    .redirectUri("https://app.example.com/callback")
    .build();   // 缺 requireProofKey(true)
```

❌ 在同一个应用里既配授权服务器签发又配资源服务器自校验、还把签名私钥同时给两端：签发与验签是两端职责，私钥只留在授权服务器，资源服务器只拿 JWKS 公钥。

## 自检

- [ ] 用 `spring-boot-starter-oauth2-authorization-server` 而非资源服务器 starter？
- [ ] `RegisteredClient` 落库（`JdbcRegisteredClientRepository`），不是只用内存版上生产？
- [ ] 公共客户端（SPA/App）`requireProofKey(true)` 强制了 PKCE？
- [ ] `issuer` 与资源服务器的 `issuer-uri` 一致，私钥只在授权服务器、公钥经 JWKS 发布？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`oauth2-resource-server.md`](./oauth2-resource-server.md)（对端：授权服务器签发 token，资源服务器拉 JWKS 公钥验签）
- 兄弟：[`oauth2-grant-types.md`](./oauth2-grant-types.md)（注册 client 时给它配哪种 grant type）
- 兄弟：[`filter-chain.md`](./filter-chain.md)（授权服务器端点的安全链配置）
