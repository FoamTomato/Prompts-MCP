---
name: react-token-storage-redirect
description: 登录 token 存哪里 + 跳转/回调 url 防 open redirect 的前端约定。Use when 决定登录态存 localStorage/cookie / 读 redirect 参数跳转 / 做 OAuth 回调 / 评审 location.href=用户传入 url。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - token 存储
  - httpOnly cookie
  - localStorage token
  - open redirect
  - redirect 参数白名单
  - allow-list
  - returnUrl
  - SameSite
effort: high
context: inline
version: '1.0'
---
# React · token 存储与跳转安全

## 规则

两个独立决策点，都关乎被 XSS / 钓鱼利用：

| 决策点 | 选型 | 理由 |
|--------|------|------|
| 登录 token 存哪里 | 首选后端下发 **httpOnly cookie**(+`SameSite=Lax/Strict`+`Secure`) | JS 读不到 → 免疫 XSS 窃取；前端代码里根本不出现 token |
| | 退而求其次：**内存(变量/store)** | 刷新即失，但页面存活期仍被 XSS 读到 |
| | 高危：**localStorage / sessionStorage** | 任何注入脚本 `localStorage.getItem` 即可拖走，禁用于长效 token |
| 必须前端持有时 | **短有效期 access token + refresh 续期** | 缩小被盗窗口；access 过期靠 refresh(放 httpOnly cookie)换新 |
| 跳转/回调 url | **allow-list 校验** 或 **后端 ID→真实 URL 映射** | 绝不直接 `location.href = 用户传入 url`，否则 open redirect 把用户导去钓鱼站 |

allow-list 比较**整个 origin/路径前缀**，不能只 `includes('mysite.com')`（`mysite.com.evil.com` 会过）。

### 反例 — 直接跳 query 里的 redirect 参数

```tsx
// ❌ open redirect：?redirect=https://evil.com 直接把用户送去钓鱼站
function LoginRedirect() {
  const redirect = new URLSearchParams(location.search).get("redirect") ?? "/";
  useEffect(() => {
    location.href = redirect; // 完全不校验来源
  }, [redirect]);
  return null;
}
// ❌ 顺带:登录态 token 落 localStorage,任何 XSS 脚本可读
localStorage.setItem("access_token", token);
```

### 正例 — allow-list 早返回 + token 交给 httpOnly cookie

跳转目标校验下沉到 validator 纯函数（>3 行逻辑不写进组件体）：

```ts
// src/utils/safe-redirect.ts
const ALLOWED_HOSTS = ["app.mysite.com", "console.mysite.com"];

export function resolveSafeRedirect(raw: string | null): string {
  // 缺省回首页:无参数时不跳外链
  if (!raw) return "/";
  // 站内相对路径放行:必须以单个 / 开头,排除 //evil.com 的协议相对 url
  if (raw.startsWith("/") && !raw.startsWith("//")) return raw;
  // 绝对 url 必须解析成功且 host 命中白名单,否则降级回首页
  try {
    const url = new URL(raw);
    return ALLOWED_HOSTS.includes(url.host) ? url.toString() : "/";
  } catch {
    return "/";
  }
}
```

```tsx
import { useEffect } from "react";

function LoginRedirect() {
  // 读取回调参数:可能被攻击者构造
  const raw = new URLSearchParams(location.search).get("redirect");
  // 校验早返回:非白名单一律降级为 "/",杜绝 open redirect
  const target = resolveSafeRedirect(raw);

  useEffect(() => {
    // 跳已校验过的安全目标;token 不在此处,登录接口由后端 Set-Cookie 下发 httpOnly
    location.replace(target);
  }, [target]);

  return null;
}
```

> token 走 httpOnly cookie 后，前端 fetch 带 `credentials: "include"` 即可，业务代码里完全看不到 token，自然无从被 XSS 偷。

## 自检

- [ ] 登录 token 优先 httpOnly cookie(+`SameSite`+`Secure`)，没有 `localStorage.setItem("token", ...)`？
- [ ] 必须前端持有时是否短有效期 access + refresh 续期，而非长效令牌？
- [ ] 跳转前用 allow-list / 后端 ID 映射校验目标，没有裸 `location.href = 用户传入 url`？
- [ ] allow-list 比较整个 host/路径前缀，不是 `includes` 子串？相对路径排除了 `//` 协议相对 url？
- [ ] OAuth 回调的 `returnUrl`/`state` 同样过校验？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`xss-sanitization.md`](./xss-sanitization.md)（XSS 是 token 被偷的前提，两者配套）
- 跨引：[`../state/client-state-zustand.md`](../state/client-state-zustand.md)（内存态存放登录信息）
