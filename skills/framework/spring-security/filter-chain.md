---
name: spring-security-filter-chain
description: Spring Security 安全配置 — 用 SecurityFilterChain Bean + HttpSecurity 链式配置，替代已废弃的 WebSecurityConfigurerAdapter。Use when 写安全配置类 / 迁移废弃的适配器 / 定过滤器链时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 安全过滤器链
  - SecurityFilterChain
  - WebSecurityConfigurerAdapter
  - HttpSecurity
  - 组件化配置
effort: medium
context: inline
version: '1.0'
---
# Spring Security · 过滤器链配置

> 本条只管「安全配置类怎么搭骨架」。session 与 JWT 解析见 [`jwt-stateless.md`](./jwt-stateless.md)，授权规则见 [`authorization.md`](./authorization.md)。

## 规则

| 维度 | 约定 |
|------|------|
| 配置入口 | 暴露 `SecurityFilterChain` Bean（Spring Security 5.7+），**不再继承 `WebSecurityConfigurerAdapter`**（6.x 已删除） |
| 类标注 | `@Configuration` + `@EnableWebSecurity`；方法级授权再加 `@EnableMethodSecurity` |
| 配置方式 | `HttpSecurity` 链式 lambda DSL：`http.authorizeHttpRequests(...)` 而非旧 `and()` 拼接 |
| 多条链 | 不同 URL 段需不同策略时配多个 `SecurityFilterChain`，用 `@Order` + `securityMatcher` 区分 |
| 静态资源放行 | 用 `WebSecurityCustomizer` 的 `web.ignoring()`，别塞进鉴权链增加开销 |

## 正例

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity        // 开启 @PreAuthorize 方法级授权
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        // 链式 lambda DSL：授权规则 + 关 CSRF（无状态接口）+ 异常处理
        http
            .csrf(AbstractHttpConfigurer::disable)
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/auth/**").permitAll()
                .anyRequest().authenticated())
            .httpBasic(Customizer.withDefaults());
        return http.build();
    }
}
```

## 反例

```java
// ❌ 继承 WebSecurityConfigurerAdapter —— 5.7 起 @Deprecated，6.x 直接删除，编译不过
@Configuration
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.authorizeRequests().anyRequest().authenticated();  // 旧 API
    }
}
```

❌ 把放行的静态资源写进 `authorizeHttpRequests(...permitAll())`：每个静态请求仍走整条安全链，应改用 `WebSecurityCustomizer` 的 `web.ignoring()` 完全跳过。

## 自检

- [ ] 用 `SecurityFilterChain` Bean，没继承 `WebSecurityConfigurerAdapter`？
- [ ] 配置类标了 `@Configuration` + `@EnableWebSecurity`？
- [ ] 用 `authorizeHttpRequests` 的 lambda DSL，没用废弃的 `authorizeRequests`？
- [ ] 静态资源用 `web.ignoring()` 放行，没塞进鉴权链？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`jwt-stateless.md`](./jwt-stateless.md)（在链里禁 session、加 token 过滤器）
- 兄弟：[`authorization.md`](./authorization.md)（`requestMatchers` URL 级授权规则）
- 兄弟：[`oauth2-resource-server.md`](./oauth2-resource-server.md)（在链里挂 OAuth2 资源服务器）
