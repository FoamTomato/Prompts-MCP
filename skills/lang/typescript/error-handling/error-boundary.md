---
name: typescript-error-boundary
description: Next.js App Router error.tsx 路由级 ErrorBoundary — 按 code 前缀分流 fallback
parent: ./index.md
paths:
  - "frontend/app/error.tsx"
  - "frontend/app/**/error.tsx"
triggers:
  keywords: [ErrorBoundary, error.tsx, GlobalError, fallback, ApiError, "use client"]
effort: medium
context: inline
version: "1.0"
---

# Next.js · 路由级 ErrorBoundary

## Next.js 约定

`app/error.tsx` 是 App Router 的 ErrorBoundary 约定文件。这个项目用的 Next.js 版本中，签名是：

```typescript
export default function Error({
  error,
  unstable_retry,
}: {
  error: Error & { digest?: string };
  unstable_retry: () => void;
}) { ... }
```

**注意**：参数名 `unstable_retry`（不是早期 Next 的 `reset`）。写代码前查 `node_modules/next/dist/docs/01-app/03-api-reference/03-file-conventions/error.md`。

## ErrorBoundary 必须是 Client Component

文件首行必须 `"use client";`。

## 按 code 前缀路由 fallback

```typescript
// frontend/app/error.tsx
"use client";

import { Button, Result } from "antd";
import { useEffect } from "react";

import { ApiError } from "@/app/lib/assertion";

export default function GlobalError({
  error,
  unstable_retry,
}: {
  error: Error & { digest?: string };
  unstable_retry: () => void;
}) {
  useEffect(() => {
    console.error("[ErrorBoundary]", error);
  }, [error]);

  if (error instanceof ApiError) {
    const status = error.httpStatus >= 500 ? "error" : "warning";
    return (
      <Result
        status={status}
        title={errorTitleByCode(error.code)}
        subTitle={`${error.code} · ${error.message}`}
        extra={<Button type="primary" onClick={unstable_retry}>重试</Button>}
      />
    );
  }

  return (
    <Result
      status="500"
      title="出错了"
      subTitle={error.message || "未知错误"}
      extra={<Button type="primary" onClick={unstable_retry}>重试</Button>}
    />
  );
}

function errorTitleByCode(code: string): string {
  switch (code.charAt(0)) {
    case "A": return "会话失效";
    case "B": return "课件操作失败";
    case "D": return "大纲操作失败";
    case "E": return "AI 服务异常";
    case "G": return "课本数据异常";
    case "I": return "试卷操作失败";
    case "J": return "知识库操作失败";
    case "R": return "邀请操作失败";
    case "S": return "会话/积分异常";
    case "X": return "服务器异常";
    default:  return "请求失败";
  }
}
```

## 嵌套 ErrorBoundary

可以在子路由放更专门的 `error.tsx`：

```
app/
├── error.tsx                # 全局兜底
├── outline/
│   └── error.tsx            # 大纲页专属（处理 D 系列错误特殊场景）
└── dashboard/
    └── error.tsx            # 控制台专属
```

子目录的 error.tsx 优先生效。

## ErrorBoundary 捕不到的场景

| 场景 | 用什么处理 |
|------|---------|
| 事件回调内的异常（onClick） | `try/catch` + toast |
| 异步异常未被 await（floating promise） | ESLint `no-floating-promises` + 显式 `.catch` |
| 表单提交校验失败 | 局部 try/catch + setError（见 form-error-handling） |
| SSR / 服务器组件异常 | 服务端 error.tsx（同文件） |

## 上报到日志

```typescript
useEffect(() => {
  // W3.5 阶段：console；后期接 Sentry
  console.error("[ErrorBoundary]", error);

  // 含业务 code 的可单独上报
  if (error instanceof ApiError && error.code.startsWith("X")) {
    // 后端错误上报
  }
}, [error]);
```

## 反例

```tsx
// ❌ 没标 "use client"
import { ... } from "antd";  // antd 是客户端组件
export default function Error(...) { ... }
// → Next.js 报错

// ❌ 用错参数名（旧版 Next.js 的 reset）
export default function Error({ error, reset }) {
  return <button onClick={reset}>重试</button>;  // 这个版本叫 unstable_retry
}

// ❌ 通用 Error 不分类型
return <div>{error.message}</div>;  // 没利用 ApiError 的 code

// ❌ 在 ErrorBoundary 内调用 fetch / mutation
useEffect(() => {
  fetch("/api/cleanup");  // ErrorBoundary 不该做副作用
}, [error]);
```

## 自检

- [ ] 文件首行 `"use client";`？
- [ ] 用对参数名（`unstable_retry` not `reset`）？
- [ ] `error instanceof ApiError` 守卫后利用 code 分流？
- [ ] fallback UI 包含「重试」按钮调 `unstable_retry()`？
- [ ] 嵌套路由按需放 sub `error.tsx`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`api-error-class.md`](./api-error-class.md) · [`form-error-handling.md`](./form-error-handling.md)
- Next.js 文档：`frontend/node_modules/next/dist/docs/01-app/03-api-reference/03-file-conventions/error.md`
- 实战代码：`frontend/app/error.tsx`
