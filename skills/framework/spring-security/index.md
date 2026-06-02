---
name: framework-spring-security-index
description: Spring Security 安全约定 — 过滤器链/无状态 JWT/授权/密码加密/OAuth2 资源服务器·授权服务器·授权模式选型七个独立决策点。Use when 配链 / 接 JWT / 加授权 / 选密码加密 / 验签或签发 token 时。
parent: ../index.md
children:
  - { name: spring-security-filter-chain, path: filter-chain.md, tag: skill, note: "SecurityFilterChain Bean 替代已废弃的 WebSecurityConfigurerAdapter" }
  - { name: spring-security-jwt-stateless, path: jwt-stateless.md, tag: skill, note: "无状态：禁 session + OncePerRequestFilter 解析 token 写 SecurityContext" }
  - { name: spring-security-authorization, path: authorization.md, tag: skill, note: "授权：@PreAuthorize 方法级 + requestMatchers URL 级" }
  - { name: spring-security-password-encoding, path: password-encoding.md, tag: skill, note: "BCryptPasswordEncoder 加盐哈希，禁明文/MD5" }
  - { name: spring-security-oauth2-resource-server, path: oauth2-resource-server.md, tag: skill, note: "OAuth2 Resource Server 校验 JWT 签名，不自己解析" }
  - { name: spring-security-oauth2-authorization-server, path: oauth2-authorization-server.md, tag: skill, note: "Spring Authorization Server 签发侧：注册 client + 授权码 PKCE + 签发 token" }
  - { name: spring-security-oauth2-grant-types, path: oauth2-grant-types.md, tag: skill, note: "授权模式选型：授权码 PKCE / 客户端凭证 / 刷新令牌 / 密码模式已废弃" }
when_to_descend: 写 / 改 Spring Security 的过滤器链、JWT 鉴权、授权规则、密码加密，或 OAuth2 资源服务器（验签）/ 授权服务器（签发）/ 授权模式选型相关代码。
---

# Spring Security · 安全约定索引

七个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 写安全配置类、定过滤器链（旧 WebSecurityConfigurerAdapter 报废了） | [filter-chain](filter-chain.md) |
| 做无状态 JWT 鉴权、禁 session、自己解析 token | [jwt-stateless](jwt-stateless.md) |
| 控制谁能访问哪个接口（方法级 / URL 级） | [authorization](authorization.md) |
| 存用户密码、选密码编码器 | [password-encoding](password-encoding.md) |
| 接 OAuth2 / OIDC，让框架校验外部签发的 JWT 签名（验签侧） | [oauth2-resource-server](oauth2-resource-server.md) |
| 搭授权服务器：注册 client、走授权码 + PKCE、签发 token（签发侧） | [oauth2-authorization-server](oauth2-authorization-server.md) |
| 选授权模式：授权码 PKCE / 客户端凭证 / 刷新令牌 / 密码模式 | [oauth2-grant-types](oauth2-grant-types.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../spring-boot/index.md`](../spring-boot/index.md) · [`../spring-cloud/index.md`](../spring-cloud/index.md)
- 相关：[`../redis/index.md`](../redis/index.md)（token 黑名单 / 会话缓存）
