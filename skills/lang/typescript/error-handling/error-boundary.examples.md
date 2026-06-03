# Next.js 路由级 ErrorBoundary — 完整代码示例

> 这是 [`error-boundary.md`](./error-boundary.md) 的配套代码集。主 skill 已经讲清楚规则与自检；这里只放可直接复制的实现。

## 完整 ApiError 路由 fallback 实现

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

## 嵌套 ErrorBoundary 目录布局

```
app/
├── error.tsx                # 全局兜底
├── outline/
│   └── error.tsx            # 大纲页专属（处理 D 系列错误特殊场景）
└── dashboard/
    └── error.tsx            # 控制台专属
```

子目录的 error.tsx 优先生效，未匹配回退到父级。

## 上报片段

```typescript
useEffect(() => {
  // 先用 console；后期接 Sentry
  console.error("[ErrorBoundary]", error);

  // 含业务 code 的可单独上报
  if (error instanceof ApiError && error.code.startsWith("X")) {
    // 后端错误上报
  }
}, [error]);
```

## 反例集

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
