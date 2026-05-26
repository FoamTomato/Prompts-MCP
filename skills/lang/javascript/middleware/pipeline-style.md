---
name: javascript-pipeline-style
description: Pipeline 风格编排 — 同 FlowStyle。Use when 写 JavaScript 代码 / 评审涉及 `pipeline-style`
  的 PR。
parent: ./index.md
paths:
- '*.js'
triggers:
  keywords:
  - pipeline
  - middleware
  - 风格编排
effort: medium
context: inline
version: '1.0'
---
# JS · Express 中间件 Pipeline

## 规则

Express handler 写成"流水线"风格——参数校验 → 加载资源 → 业务编排 → 响应，每步一行 + 注释。

## 模板

```js
import { wrap } from "../utils/wrap.js";
import { validateCreateOrder } from "../validators/order.js";
import { OrderService } from "../services/order.js";

router.post("/orders", wrap(async (req, res) => {
  // 参数校验
  const input = validateCreateOrder(req.body);

  // 加载上下文
  const user = req.user;

  // 业务编排
  const order = await OrderService.create({ ...input, userId: user.id });

  // 响应
  res.json({ data: order });
}));
```

## 中间件链

```js
import express from "express";
import auth from "./middleware/auth.js";
import rateLimit from "./middleware/rate-limit.js";
import requestId from "./middleware/request-id.js";

const app = express();

app.use(express.json({ limit: "1mb" }));
app.use(requestId);
app.use(auth);                          // 401 if no token
app.use("/api/admin", rateLimit(60));   // 60 req/min admin

// 业务路由
app.use("/api/orders", ordersRouter);
app.use("/api/users", usersRouter);

// 错误中间件
app.use(errorMiddleware);
```

## 与 FlowStyle 对齐

JS 的 Express handler ≈ Python FastAPI router + service。结构上仍遵循 DDD：

- handler 薄壳（参数 + 调用 + 响应）
- service 编排（业务逻辑）
- repository 持久化

详见 [`../../../design-pattern/ddd-layering/index.md`](../../../design-pattern/ddd-layering/index.md)。

## 自检

- [ ] handler 内只调 service，不直接查库？
- [ ] 中间件按"通用 → 安全 → 限流 → 业务"顺序？
- [ ] 错误中间件最末位？
- [ ] async handler 都被 wrap 包装？

## 相关

- 父：[`./index.md`](./index.md)
- 配套：[`error-middleware.md`](./error-middleware.md) · [`../../../design-pattern/pipeline/method-as-flow.md`](../../../design-pattern/pipeline/method-as-flow.md)

