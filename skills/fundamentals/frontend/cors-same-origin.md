---
name: frontend-cors-same-origin
description: "同源策略与 CORS 的前端决策 — 同源=协议+域名+端口全同，跨域是响应被浏览器拦而非请求没发。Use when 接口报 CORS 错 / 预检 OPTIONS 失败 / 带 cookie 跨域不通 / 纠结该 devServer proxy 还是后端配响应头。"
parent: ./index.md
paths:
- frontend/src/**/*.ts
- frontend/src/**/*.tsx
- frontend/src/**/*.vue
triggers:
  keywords:
  - 同源策略
  - 跨域
  - CORS 预检
  - OPTIONS 预检
  - Access-Control-Allow-Origin
  - withCredentials
  - devServer proxy
  - same-origin policy
  - preflight
effort: medium
context: inline
version: '1.0'
---
# Frontend · 同源策略与跨域(决策视角)

## 规则

第一决策点:**报 CORS 错 ≠ 请求没发出去**。请求其实已到后端、后端也回了响应,是**浏览器**因缺少 `Access-Control-Allow-Origin` 把响应拦在 JS 之外。所以前端永远不能"自己解决 CORS"——放行头是**后端响应头**,前端只能选绕过(proxy)或推动后端配置。

| 决策点 | 选什么 | 理由 |
|--------|--------|------|
| 是否同源 | **协议 + 域名 + 端口** 三者全同才同源 | 任一不同即跨域;`https` vs `http`、`a.com` vs `api.a.com`、`:80` vs `:8080` 都算跨域 |
| 请求是否触发预检 | 简单请求直接带 `Origin` 发;**非简单请求先发 `OPTIONS` 预检** | 自定义头 / `PUT`·`DELETE` / `Content-Type: application/json` 任一命中即预检 |
| 开发环境绕过 | **devServer `proxy`**(Vite/Webpack)让浏览器以为同源 | 请求先打到本地 dev server 再转发,浏览器视角同源,无需后端配 |
| 生产环境放行 | 后端配 **`Access-Control-Allow-Origin`**(具体 origin) | 前端无法替代;`*` 不能与凭证共存 |
| 带 cookie 跨域 | 前端 `withCredentials`/`credentials:"include"` **+** 后端 `Allow-Credentials: true` 且 `Allow-Origin` 写**具体 origin** | 缺任一项 cookie 不带或响应被拦 |

> 性能/行为为业界参考,落地以浏览器 Network 面板实测为准。

### 反例 — 误判与误用

```ts
// ❌ 把 CORS 错当成"请求失败/接口挂了"去 retry —— 请求早发出去了,是响应被拦
fetch("https://api.other.com/data").catch(() => retry()); // retry 也一样被拦

// ❌ 想带 cookie 又把 Allow-Origin 配成 *(后端),浏览器直接拒收
fetch(url, { credentials: "include" }); // 后端 Allow-Origin:* + credentials → 失败
```

### 正例 — 开发用 proxy 绕过 + 生产带凭证

开发期靠 devServer proxy,业务代码只写同源相对路径,浏览器无从触发跨域:

```ts
// vite.config.ts —— 开发环境把 /api 转发到后端,前端请求维持同源
import { defineConfig } from "vite";

export default defineConfig({
  server: {
    proxy: {
      // 同源相对路径 → dev server 转发到真实后端,浏览器视角始终同源
      "/api": { target: "http://backend.internal:8080", changeOrigin: true },
    },
  },
});
```

请求与凭证的封装下沉到 utils,组件体不出现裸 fetch 配置:

```ts
// src/utils/http.ts
const BASE = import.meta.env.VITE_API_BASE ?? "/api";

export async function requestJson<T>(path: string, body: unknown): Promise<T> {
  // 拼同源相对路径:开发走 proxy、生产走同域网关,均不触发跨域
  const url = `${BASE}${path}`;
  // 非简单请求:application/json + 凭证 → 浏览器会先发 OPTIONS 预检
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    // 带 cookie 跨域必须显式开启,且后端须回 Allow-Credentials:true
    credentials: "include",
    body: JSON.stringify(body),
  });
  // 校验早返回:非 2xx 直接抛,交上层统一处理
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json() as Promise<T>;
}
```

> 排错路径:Network 面板看是否有一条 `OPTIONS` 在真实请求前。预检失败最常见是后端没配 **`Access-Control-Allow-Headers`**(漏了你发的自定义头/`Content-Type`),其次是 `Allow-Methods` 没含 `PUT`/`DELETE`。这些都改后端,前端无能为力。

## 自检

- [ ] 把 CORS 报错当"响应被拦"而非"请求没发/接口挂",没有盲目 retry?
- [ ] 判断同源时核对了协议 + 域名 + 端口三项全同?
- [ ] 自定义头 / `PUT`·`DELETE` / `application/json` 已预期会触发 `OPTIONS` 预检?
- [ ] 开发环境用 devServer `proxy` 绕过,而不是试图在前端代码里"关掉" CORS?
- [ ] 带 cookie 跨域:前端 `withCredentials`/`credentials:"include"` + 后端 `Allow-Credentials:true` + `Allow-Origin` 为具体 origin(非 `*`)?
- [ ] 预检失败先查后端 `Access-Control-Allow-Headers`/`Allow-Methods`,而非改前端?

## 相关

- 父:[`./index.md`](./index.md)
- 兄弟:[`http-caching.md`](./http-caching.md)(同为 HTTP 层前端决策,缓存 vs 跨域)
- 跨引:[`../../framework/react/security/token-storage-redirect.md`](../../framework/react/security/token-storage-redirect.md)(跨域带凭证时 token/cookie 怎么存与传)
