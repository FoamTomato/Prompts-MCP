---
name: typescript-error-boundary
description: Next.js App Router 路由级 ErrorBoundary — app/error.tsx + "use client" + ApiError.code 分流 fallback。Use when 写 app/error.tsx / 嵌套专属错误页 / 评审 ErrorBoundary。
parent: ./index.md
paths:
  - "frontend/**/error.tsx"
  - "frontend/app/**/*.tsx"
triggers:
  keywords:
    - ErrorBoundary
    - error.tsx
    - 错误兜底
    - 路由级错误
    - Next.js error
    - unstable_retry
    - use client
effort: medium
version: "1.0"
---

# Next.js · 路由级 ErrorBoundary

## 规则

1. **文件位置约定** — App Router 用 `app/error.tsx`，子目录可放专属 `error.tsx`，**子目录的优先生效**。
2. **首行必须** `"use client";` — ErrorBoundary 内会用 antd 等客户端组件。
3. **参数名** 用 `unstable_retry`（**不是** 早期 Next 的 `reset`）。写前查 `node_modules/next/dist/docs/01-app/03-api-reference/03-file-conventions/error.md`。
4. **按 `ApiError.code` 前缀分流 fallback 文案** — `code.charAt(0)` 映射到业务标题（A=会话 / B=课件 / D=大纲 / E=AI / X=服务器）。
5. **fallback UI 必含「重试」按钮**调 `unstable_retry()`。
6. **`useEffect` 上报** 错误到 console（后期接 Sentry），但 **不要在 ErrorBoundary 内做副作用** 如 fetch / mutation。

## ErrorBoundary 捕不到的场景（要别的兜底）

| 场景 | 用什么处理 |
|------|---------|
| 事件回调内异常（onClick） | `try/catch` + toast |
| 异步异常未 await（floating promise） | ESLint `no-floating-promises` + 显式 `.catch` |
| 表单提交校验失败 | 局部 try/catch + setError（见 [`form-error-handling.md`](./form-error-handling.md)） |
| SSR / 服务端组件异常 | 同文件的服务端 error.tsx |

## 自检

- [ ] 文件首行 `"use client";`？
- [ ] 参数名 `unstable_retry`（非 `reset`）？
- [ ] `error instanceof ApiError` 守卫后利用 `code` 分流？
- [ ] fallback UI 包含「重试」按钮调 `unstable_retry()`？
- [ ] 嵌套路由按需放 sub `error.tsx`？
- [ ] `useEffect` 里只 console / 上报，**没有** fetch / mutation？

## 详细参考

- 完整 `app/error.tsx` 实现 + 嵌套布局 + 反例集：[`./error-boundary.examples.md`](./error-boundary.examples.md)
- Next.js 官方文档：`frontend/node_modules/next/dist/docs/01-app/03-api-reference/03-file-conventions/error.md`

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`api-error-class.md`](./api-error-class.md) · [`form-error-handling.md`](./form-error-handling.md)
- 实战代码：`frontend/app/error.tsx`
