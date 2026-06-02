---
name: spring-security-jwt-stateless
description: Spring Security 无状态 JWT 鉴权 — STATELESS 禁 session，OncePerRequestFilter 解析 token 写入 SecurityContext。Use when 接 JWT 鉴权 / 禁 session / 写 token 解析过滤器时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 无状态鉴权
  - JWT 解析
  - OncePerRequestFilter
  - SecurityContextHolder
  - SessionCreationPolicy
  - token 过滤器
effort: medium
context: inline
version: '1.0'
---
# Spring Security · 无状态 JWT 鉴权

> 本条只管「自己签发的 JWT 怎么在无状态模式下解析并写认证」。链骨架见 [`filter-chain.md`](./filter-chain.md)；接外部 OAuth2/OIDC 让框架校验签名见 [`oauth2-resource-server.md`](./oauth2-resource-server.md)。

## 规则

| 维度 | 约定 |
|------|------|
| 会话策略 | `SessionCreationPolicy.STATELESS`：不创建也不用 `HttpSession`，每个请求靠 token 自证 |
| token 解析 | 自定义 `OncePerRequestFilter`（保证一次请求只过一次），从 `Authorization: Bearer xxx` 取 token |
| 写认证 | 解析成功后 `SecurityContextHolder.getContext().setAuthentication(...)`；不抛异常，交后续链判 401 |
| 过滤器位置 | `addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class)` |
| 关无状态无关项 | 关 CSRF、关表单登录；前端跨域用 token，不依赖 Cookie |

## 正例

```java
@Component
@RequiredArgsConstructor
public class JwtAuthFilter extends OncePerRequestFilter {
    private final JwtParser jwtParser;

    @Override
    protected void doFilterInternal(HttpServletRequest req, HttpServletResponse resp,
                                    FilterChain chain) throws ServletException, IOException {
        // 取 Bearer token，缺失则放行交后续链判 401
        final String header = req.getHeader("Authorization");
        if (header == null || !header.startsWith("Bearer ")) {
            chain.doFilter(req, resp);
            return;
        }
        // 解析 token 并写入 SecurityContext
        final Authentication auth = jwtParser.parse(header.substring(7));
        SecurityContextHolder.getContext().setAuthentication(auth);
        chain.doFilter(req, resp);
    }
}
```

链中启用无状态并挂上过滤器：

```java
http.sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
    .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class);
```

## 反例

```java
// ❌ 没设 STATELESS：Spring 仍创建 HttpSession 存 SecurityContext，
//    无状态架构失去意义，且多实例下 session 不共享导致鉴权漂移
http.authorizeHttpRequests(a -> a.anyRequest().authenticated());
// 默认 SessionCreationPolicy.IF_REQUIRED
```

❌ token 解析失败时在过滤器里直接 `throw`，绕过统一异常出口：应不写 `Authentication` 后放行，让后续链返回标准 401。

## 自检

- [ ] 配了 `SessionCreationPolicy.STATELESS`，不依赖 `HttpSession`？
- [ ] 解析过滤器继承 `OncePerRequestFilter`，从 `Bearer` 头取 token？
- [ ] 成功后写 `SecurityContextHolder`，失败不抛异常只放行交后续判 401？
- [ ] 过滤器用 `addFilterBefore(..., UsernamePasswordAuthenticationFilter.class)` 挂载？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`filter-chain.md`](./filter-chain.md)（链骨架，在哪挂过滤器）
- 兄弟：[`oauth2-resource-server.md`](./oauth2-resource-server.md)（外部签发的 JWT 用资源服务器校验，别手写解析）
- 兄弟：[`authorization.md`](./authorization.md)（认证写入后才轮到授权判定）
