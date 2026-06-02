---
name: spring-security-oauth2-grant-types
description: OAuth2 授权模式选型 — 授权码 + PKCE（用户登录，推荐）/客户端凭证（服务间）/刷新令牌（续期）/密码模式（已废弃）。Use when 选 OAuth2 grant type / 判断用授权码还是客户端凭证 / 续期 token 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 授权模式选型
  - 授权码模式
  - 客户端凭证模式
  - 密码模式
  - 刷新令牌
  - AuthorizationGrantType
effort: low
context: inline
version: '1.0'
---
# Spring Security · OAuth2 授权模式选型

> 本条只回答「该选哪种 grant type」。怎么在授权服务器上注册 client、配 PKCE 见 [`oauth2-authorization-server.md`](./oauth2-authorization-server.md)；资源服务器怎么验签见 [`oauth2-resource-server.md`](./oauth2-resource-server.md)。

## 规则

| 模式 | 适用场景 | 选用建议 |
|------|---------|---------|
| 授权码 Authorization Code + PKCE | 有用户登录的 Web / SPA / 移动端 | **首选**。SPA / App 等公共客户端**必须**带 PKCE；有后端能保密 secret 的也建议带 |
| 客户端凭证 Client Credentials | 服务间调用，**无用户**参与（定时任务、后端互调） | 服务到服务用它，代表「应用自己」而非某个用户；secret 走配置中心 |
| 刷新令牌 Refresh Token | access token 过期后**静默续期**，不让用户重新登录 | 配合授权码用；access token 短（分钟级）、refresh token 长，refresh 用一次轮换一次 |
| 密码模式 Resource Owner Password | —— | **已废弃**（OAuth 2.1 移除）。要求 client 直接拿用户明文密码，违背 OAuth 初衷，禁新用 |
| 隐式模式 Implicit | —— | **已废弃**。token 走 URL 片段易泄露，SPA 改用授权码 + PKCE |

## 正例

```java
// 服务间调用：客户端凭证模式，代表应用自身，无用户上下文
RegisteredClient backendClient = RegisteredClient.withId(id)
    .clientId("order-service")
    .clientSecret(encoder.encode(secret))                          // 保密客户端有 secret
    .clientAuthenticationMethod(ClientAuthenticationMethod.CLIENT_SECRET_BASIC)
    .authorizationGrantType(AuthorizationGrantType.CLIENT_CREDENTIALS)
    .scope("inventory.read")
    .build();

// 用户登录：授权码 + 刷新令牌（PKCE 在 client settings 里强制，见授权服务器条）
RegisteredClient userClient = RegisteredClient.withId(id2)
    .clientId("web-app")
    .authorizationGrantType(AuthorizationGrantType.AUTHORIZATION_CODE)
    .authorizationGrantType(AuthorizationGrantType.REFRESH_TOKEN)   // 配合授权码做静默续期
    .build();
```

## 反例

```java
// ❌ 新接入还用密码模式（OAuth 2.1 已移除）：client 直接经手用户明文密码
.authorizationGrantType(AuthorizationGrantType.PASSWORD)
```

❌ 给服务间互调用授权码模式：授权码模式是为「有用户授权」设计的，无人点同意页的后端互调应用客户端凭证模式。

## 自检

- [ ] 有用户登录的前端选了授权码 + PKCE，没用隐式/密码模式？
- [ ] 服务间无用户调用选了客户端凭证模式，不是授权码？
- [ ] access token 短时效 + 刷新令牌续期，refresh token 一次一轮换？
- [ ] 没有任何新代码使用已废弃的密码模式 / 隐式模式？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`oauth2-authorization-server.md`](./oauth2-authorization-server.md)（选定 grant type 后在授权服务器注册 client、配 PKCE）
- 兄弟：[`oauth2-resource-server.md`](./oauth2-resource-server.md)（拿到 token 的资源服务器侧验签）
