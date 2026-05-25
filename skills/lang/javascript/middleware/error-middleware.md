---
name: javascript-error-middleware
description: Express 错误中间件模板
parent: ./index.md
paths:
  - "*.js"
triggers:
  keywords: [error middleware, next(err)]
effort: medium
context: inline
version: "1.0"
---

# JS · Express 错误中间件

## 规则

Express 错误中间件签名是 4 参数 `(err, req, res, next)`，必须放在所有路由之后。

```js
import express from "express";

const app = express();

// 路由
app.get("/api/users", async (req, res, next) => {
  try { ... }
  catch (err) { next(err); }
});

// 错误中间件 — 放最后
app.use((err, req, res, next) => {
  const code = err.code || 500;
  const msg = err.message || "internal error";

  console.error(`[err] ${req.method} ${req.url}`, err);

  res.status(code).json({ success: false, msg, code });
});
```

## 业务异常 vs 系统异常

```js
class ApiError extends Error {
  constructor(msg, code = 400) {
    super(msg);
    this.code = code;
  }
}

// 业务异常
throw new ApiError("配额不足", 403);

// 中间件按类型分别处理
app.use((err, req, res, next) => {
  if (err instanceof ApiError) {
    return res.status(err.code).json({ msg: err.message });
  }
  console.error(err);
  res.status(500).json({ msg: "服务繁忙" });
});
```

## async handler 包装器

```js
const wrap = fn => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next);

app.get("/api/users", wrap(async (req, res) => {
  const users = await listUsers();
  res.json(users);
}));
```

## 自检

- [ ] 错误中间件签名 `(err, req, res, next)` 4 参数？
- [ ] 位置在所有路由之后？
- [ ] 业务异常用 `ApiError` 子类？
- [ ] async handler 用 wrap 包装或 try/catch + next？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`pipeline-style.md`](./pipeline-style.md)

