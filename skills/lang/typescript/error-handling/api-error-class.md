---
name: typescript-api-error-class
description: ApiError extends Error 子类设计 + fetcher 集成 + 与后端 ApiException 对齐
parent: ./index.md
paths:
  - "frontend/app/lib/assertion.ts"
  - "frontend/app/lib/api.ts"
  - "frontend/app/**/*.ts"
  - "frontend/app/**/*.tsx"
triggers:
  keywords: [ApiError, Error subclass, fetcher, ApiEnvelope, ApiException]
effort: low
context: inline
version: "1.0"
---

# ApiError 类设计

## 标准实现

```typescript
// frontend/app/lib/assertion.ts
export class ApiError extends Error {
  readonly code: string;
  readonly httpStatus: number;
  readonly data: unknown;

  constructor(opts: {
    code: string;
    message: string;
    httpStatus?: number;
    data?: unknown;
  }) {
    super(opts.message);
    this.name = "ApiError";
    this.code = opts.code;
    this.httpStatus = opts.httpStatus ?? 400;
    this.data = opts.data;
  }
}
```

## 与后端 ApiException 字段对齐

| 后端 ApiException | 前端 ApiError | HTTP 序列化 |
|------------------|--------------|----------|
| `code: str` (业务码 A001) | `code: string` | `detail.code` |
| `message: str` | `message: string` | `detail.message` |
| `http_status: int` | `httpStatus: number` | `status_code` |
| `data: Any` | `data: unknown` | `detail.data` |

## fetcher 集成

```typescript
async function fetcher<T>(url: string): Promise<T> {
  const res = await fetch(url, { credentials: "include" });
  const text = await res.text();

  let body: ApiEnvelope<T> | null = null;
  try {
    body = text ? (JSON.parse(text) as ApiEnvelope<T>) : null;
  } catch {
    // 非 JSON 响应（代理 502 HTML 等）
  }

  // 1. HTTP 失败
  if (!res.ok) {
    const detail = body as { code: string; message: string; data: unknown } | null;
    throw new ApiError({
      code: detail?.code ?? `HTTP_${res.status}`,
      message: detail?.message ?? `HTTP ${res.status}: ${text || res.statusText}`,
      httpStatus: res.status,
      data: detail?.data,
    });
  }

  // 2. 业务失败（HTTP 200 + code !== 0）
  if (body && body.code !== 0) {
    throw new ApiError({
      code: String(body.code),
      message: body.message,
      httpStatus: res.status,
      data: body.data,
    });
  }

  return body.data as T;
}
```

## 调用方使用 `instanceof`

```typescript
import { ApiError } from "@/app/lib/assertion";

try {
  const data = await fetcher("/api/...");
} catch (e) {
  if (e instanceof ApiError) {
    // 已知业务错误：拿到 code/httpStatus/data
    if (e.code === "A001") redirectToBootstrap();
    if (e.code.startsWith("E")) toast.error(e.message);
    return;
  }
  // 未知错误：透传或上报
  throw e;
}
```

## 反例

```typescript
// ❌ 用泛型 Error
throw new Error(`code=${code} msg=${msg}`);  // 调用方拿不到 code，只能 parse message

// ❌ 在 catch 里用字符串匹配
catch (e: any) {
  if (e.message.includes("session")) {  // 脆弱
    ...
  }
}

// ❌ 把 code 当 number（与后端不一致）
throw new ApiError({ code: 401, ... });  // 应该 "A001" 等字符串

// ❌ 在 fetcher 外抛 new Error()
const res = await fetch(...);
if (!res.ok) throw new Error(...);  // 已经改为 ApiError 了
```

## 自检

- [ ] `class ApiError extends Error`，含 code/httpStatus/data 字段？
- [ ] code 是字符串（"A001"）不是 number？
- [ ] fetcher 失败 100% 抛 ApiError，不抛 new Error？
- [ ] 调用方用 `instanceof ApiError` 守卫？
- [ ] 与后端 detail = {code, message, data} 序列化对齐？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`assert-helpers.md`](./assert-helpers.md) · [`error-boundary.md`](./error-boundary.md) · [`form-error-handling.md`](./form-error-handling.md)
- 后端对应：[`../../python/error-handling/api-exception.md`](../../python/error-handling/api-exception.md)
- 实战代码：`frontend/app/lib/assertion.ts` / `frontend/app/lib/api.ts`
