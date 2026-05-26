---
name: typescript-error-handling-index
description: TypeScript 错误处理 — ApiError 子类 + Asserts 工具 + 路由级 ErrorBoundary
parent: ../index.md
children:
  - { name: api-error-class, path: api-error-class.md, tag: skill, note: ApiError extends Error + fetcher 集成 }
  - { name: assert-helpers, path: assert-helpers.md, tag: skill, note: Asserts 工具 + asserts value is T 谓词 }
  - { name: error-boundary, path: error-boundary.md, tag: skill, note: Next.js app/error.tsx 按 code 前缀分流 }
  - { name: form-error-handling, path: form-error-handling.md, tag: skill, note: 表单局部 catch + 字段映射 }
when_to_descend: |
  写 fetcher / 表单 / ErrorBoundary / 任何抛 / 捕获前端错误时。
---

# TypeScript · Error Handling

## 一句话

**前端镜像后端 ApiException 模型**：`ApiError extends Error`（含 code + httpStatus + data），`Asserts.<方法>` 失败抛 ApiError，路由级 ErrorBoundary 按 code 前缀分流。

## 推荐落点

| 文件 | 内容 |
|------|------|
| `frontend/app/lib/assertion.ts` | ApiError + Asserts 方法集合 |
| `frontend/app/lib/api.ts` | fetcher 抛 ApiError（替换原 `new Error(...)`）|
| `frontend/app/error.tsx` | 路由级 ErrorBoundary，按 code 前缀路由 fallback 标题 |

## 何时下钻

| 任务 | 选哪个子项 |
|------|---------|
| 写 fetcher / 调 API | api-error-class |
| 写表单 / 客户端校验 | assert-helpers + form-error-handling |
| 设计页面级错误兜底 | error-boundary |
| 表单字段绑定错误 | form-error-handling |

## 与后端的对齐

```
后端 ApiException(code, message, http_status, data)
        ↓ FastAPI JSON 序列化 detail = {code, message, data}
        ↓ HTTP 响应（status_code = http_status）
        ↓
前端 fetcher 抛 ApiError({code, message, httpStatus, data})
        ↓ ErrorBoundary 按 code.charAt(0) 路由
```

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../naming/`](../naming/) · [`../typing/`](../typing/) · [`../async/`](../async/)
- 后端对应：[`../../python/error-handling/api-exception.md`](../../python/error-handling/api-exception.md)
- 配套：[`../../../design-pattern/assertion/`](../../../design-pattern/assertion/index.md)
