---
name: react-error-boundary
description: 路由级 ErrorBoundary 包裹 — 不让一个组件崩塌整棵树
parent: ./index.md
paths:
  - "frontend/src/pages/**/*.tsx"
  - "frontend/src/App.tsx"
  - "frontend/src/router.tsx"
triggers:
  keywords: [ErrorBoundary, componentDidCatch, fallback]
effort: medium
context: inline
version: "1.0"
---

# React · ErrorBoundary

## 规则

**每个 page 都用 `<ErrorBoundary>` 包裹**，避免单组件崩溃影响全局。

## 实现

```tsx
// src/components/ErrorBoundary.tsx
import { Component, type ReactNode, type ErrorInfo } from "react";
import { ErrorState } from "@/components/ErrorState";

interface Props {
  children: ReactNode;
  fallback?: ReactNode | ((error: Error, reset: () => void) => ReactNode);
}

interface State {
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { error: null };

  static getDerivedStateFromError(error: Error): State {
    return { error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    // 上报到 sentry / 自家日志
    console.error("[ErrorBoundary]", error, info);
  }

  reset = () => this.setState({ error: null });

  render() {
    if (this.state.error) {
      if (typeof this.props.fallback === "function") {
        return this.props.fallback(this.state.error, this.reset);
      }
      return this.props.fallback ?? (
        <ErrorState
          title="出错了"
          description={this.state.error.message}
          action={<button onClick={this.reset}>重试</button>}
        />
      );
    }
    return this.props.children;
  }
}
```

## 路由级使用

```tsx
// src/router.tsx
import { createBrowserRouter } from "react-router-dom";
import { ErrorBoundary } from "@/components/ErrorBoundary";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <ErrorBoundary><HomePage /></ErrorBoundary>,
  },
  {
    path: "/editor/:id",
    element: <ErrorBoundary><EditorPage /></ErrorBoundary>,
  },
  {
    path: "/dashboard",
    element: <ErrorBoundary><DashboardLayout /></ErrorBoundary>,
  },
]);
```

## ErrorBoundary 不会捕获什么

| 不捕获 | 用什么处理 |
|--------|---------|
| 事件回调内的异常 | try/catch + toast |
| 异步异常（setTimeout / Promise） | try/catch + toast |
| 服务端渲染异常 | renderToString 的 try/catch |
| ErrorBoundary 自身的异常 | 嵌套外层 boundary |

## TanStack Query 错误

useQuery 抛错可以**主动让 boundary 接管**：

```tsx
const { data } = useQuery({
  queryKey: ["x"],
  queryFn: ...,
  throwOnError: true,    // 让 ErrorBoundary 接管
});
```

## 自检

- [ ] 每个 page 都被 ErrorBoundary 包裹？
- [ ] fallback 有"重试"按钮？
- [ ] 异步异常用 try/catch 兜底？
- [ ] 上报到日志系统？

## 相关

- 父：[`./index.md`](./index.md)
- 配套：[`../state/server-state-tanstack.md`](../state/server-state-tanstack.md)

