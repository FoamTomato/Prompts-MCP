---
name: spring-security-authorization
description: Spring Security 授权 — 方法级 @PreAuthorize 表达式 + URL 级 requestMatchers，按角色/权限控制访问。Use when 加接口访问控制 / 按角色限权 / 写方法级授权表达式时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 授权控制
  - 角色权限
  - '@PreAuthorize'
  - requestMatchers
  - hasRole
  - 方法级安全
effort: medium
context: inline
version: '1.0'
---
# Spring Security · 授权

> 本条只管「认证之后，谁能访问什么」。怎么认证（解析 token）见 [`jwt-stateless.md`](./jwt-stateless.md)。

## 规则

| 层级 | 用法 | 适合 |
|------|------|------|
| URL 级 | `authorizeHttpRequests` 里 `requestMatchers("/admin/**").hasRole("ADMIN")` | 粗粒度按路径段放行/限权 |
| 方法级 | 方法上 `@PreAuthorize("hasRole('ADMIN')")`，需 `@EnableMethodSecurity` | 细粒度、按业务参数判定 |
| 表达式 | `hasRole` / `hasAuthority` / `#id == authentication.principal.id` 数据级隔离 | 复杂条件 |
| ROLE 前缀 | `hasRole("ADMIN")` 自动匹配权限 `ROLE_ADMIN`；`hasAuthority` 要写全名 | 别两处混用 |
| 顺序 | `requestMatchers` 从具体到宽泛，最后 `anyRequest().authenticated()` 兜底 | 防越权放行 |

## 正例

```java
// URL 级：在过滤器链里按路径段限权
http.authorizeHttpRequests(auth -> auth
    .requestMatchers("/api/public/**").permitAll()
    .requestMatchers("/api/admin/**").hasRole("ADMIN")
    .anyRequest().authenticated());
```

```java
// 方法级：细粒度 + 数据级隔离（只能改自己的资源）
@Service
public class OrderService {

    @PreAuthorize("hasRole('ADMIN')")
    public void deleteAny(Long id) { /* ... */ }

    @PreAuthorize("#userId == authentication.principal.id")
    public OrderVO myOrders(Long userId) { /* 越权访问他人 id 直接 403 */ }
}
```

## 反例

```java
// ❌ 规则顺序反了：anyRequest 先匹配，后面 admin 规则永远到不了
http.authorizeHttpRequests(auth -> auth
    .anyRequest().authenticated()
    .requestMatchers("/api/admin/**").hasRole("ADMIN"));  // 不生效
```

❌ 在 Controller 里手写 `if (!user.isAdmin()) throw ...` 散落各处做授权：授权逻辑应集中在 `@PreAuthorize` / `requestMatchers`，散写易漏判、难审计。

## 自检

- [ ] URL 级 `requestMatchers` 从具体到宽泛排序，末尾 `anyRequest()` 兜底？
- [ ] 方法级用 `@PreAuthorize` 且开了 `@EnableMethodSecurity`？
- [ ] `hasRole` 与 `hasAuthority` 的 `ROLE_` 前缀语义没混用？
- [ ] 没在业务代码里散写 `if` 手判权限？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`jwt-stateless.md`](./jwt-stateless.md)（先认证写入 `SecurityContext`，才轮到授权）
- 兄弟：[`filter-chain.md`](./filter-chain.md)（`@EnableMethodSecurity` 在配置类开启）
