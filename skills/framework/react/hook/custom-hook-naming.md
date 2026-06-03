---
name: react-custom-hook-naming
description: 自定义 hook 必须 useXxx 命名 + 文件 useXxx.ts。Use when 写 TS 业务代码 / 评审涉及 `custom-hook-naming`
  的 PR。
parent: ./index.md
paths:
- frontend/src/hooks/**/*.ts
- frontend/src/features/**/use*.ts
triggers:
  keywords:
  - hook 命名
  - use 前缀
  - useXxx 文件名
  - 一文件一 hook
  - hook naming
effort: medium
context: inline
version: '1.0'
---
# React · 自定义 Hook 命名

## 规则

| 规则 | 示例 |
|------|------|
| 必 `use` 前缀（小写） | `useSSE` / `useArticleHistory` / `useTaskPolling` |
| 文件名 = hook 名 + `.ts` | `useSSE.ts` / `useArticleHistory.ts` |
| 一文件一 hook | 必要时同文件 export 小工具函数 |
| 路径：`src/hooks/<name>.ts` 通用 / `src/features/<page>/use<X>.ts` 业务专属 | — |

## 模板

```ts
// src/hooks/useSSE.ts
import { useEffect, useReducer, useRef } from "react";

type State<T> =
  | { status: "idle" }
  | { status: "streaming"; events: T[] }
  | { status: "done"; events: T[] }
  | { status: "error"; error: string; events: T[] };

interface Options<T> {
  url: string;
  body?: unknown;
  enabled?: boolean;
  onEvent?: (eventType: string, data: T) => void;
}

export function useSSE<T>({ url, body, enabled = true, onEvent }: Options<T>): State<T> {
  const [state, dispatch] = useReducer(reducer<T>, { status: "idle" });

  useEffect(() => {
    if (!enabled) return;
    const ctrl = new AbortController();
    // ... 实现略
    return () => ctrl.abort();
  }, [url, JSON.stringify(body), enabled]);

  return state;
}
```

## 示例 hooks

| 名 | 用途 | 路径 |
|----|------|------|
| `useSSE` | SSE 流式响应 | `src/hooks/useSSE.ts` |
| `useTaskPolling` | 异步任务轮询 | `src/hooks/useTaskPolling.ts` |
| `useArticleHistory` | 用户内容历史 | `src/hooks/useArticleHistory.ts` |
| `useUndoStack` | 撤销栈 | `src/hooks/useUndoStack.ts` |
| `usePresentKeyboard` | 演示模式快捷键 | `src/hooks/usePresentKeyboard.ts` |

## 反例

```ts
// ❌ 不带 use 前缀（不会被 ESLint 当 hook）
function sse() { useState(...) }

// ❌ Pascal 命名
function UseSSE() {}

// ❌ 一文件多 hook
// useEverything.ts
export function useA() {}
export function useB() {}   // 拆开
```

## 返回值约定

| Hook 类型 | 返回 |
|----------|------|
| 状态机 hook | 单 state 对象（含 status discriminator） |
| 多状态 hook | 对象 `{state, actions}` |
| 简单订阅 | 单值 |
| 操作型 | `[value, setter]` 类似 useState |

## 自检

- [ ] 名以 `use` 开头（小写 u）？
- [ ] 文件名 = hook 名 + `.ts`？
- [ ] 一文件一主 hook？
- [ ] 返回值类型有 export？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`order-and-rules.md`](./order-and-rules.md)
