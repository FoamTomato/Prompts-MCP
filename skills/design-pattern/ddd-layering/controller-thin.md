---
name: ddd-controller-thin
description: Controller 薄壳 — Router/Service 边界
parent: ./index.md
paths:
  - "backend/routers/**/*.py"
  - "py/routers/**/*.py"
  - "frontend/src/pages/**/*.tsx"
triggers:
  keywords: [Controller, Router, 薄壳]
effort: medium
context: inline
version: "1.0"
---

# DDD · Controller 薄

## 规则

Controller / Router 是**入站门面**，只做：参数绑定 → 调用应用层 → 返回响应。

```
Controller 责任清单:
  1. HTTP/SSE 协议处理（method、headers、status code）
  2. 参数反序列化 + 校验
  3. 调用 Application/Service 一次
  4. 响应序列化
```

## 反例 → 正例

```python
# ❌ Controller 下沉业务
@router.post("/orders")
async def create_order(req: CreateOrderReq, current_user=Depends(get_current_user)):
    user = await User.filter(id=current_user["account_id"]).first()
    if user.balance < req.amount:
        raise ApiException("余额不足")
    order = await Order.create(user_id=user.id, amount=req.amount)
    user.balance -= req.amount
    await user.save()
    return JsonData.success(order.dict())

# ✅ Controller 只调用 Service
@router.post("/orders", response_model=JsonData[OrderResp])
async def create_order(req: CreateOrderReq, current_user=Depends(get_current_user)):
    result = await order_service.create(req, current_user["account_id"])
    return JsonData.success(result)
```

## 各语言落点

| 语言/框架 | "Controller" 对应文件 |
|---------|-----------------|
| Python FastAPI | `routers/*.py` |
| Node Express | `routes/*.js` |
| Java Spring | `*Controller.java` |
| 前端 React | `pages/*.tsx`（页面级，编排不写逻辑） |

## 与领域纯净对齐

详见：
- Service 编排 → [`service-orchestration.md`](./service-orchestration.md)
- Domain 纯净 → [`domain-pure.md`](./domain-pure.md)
- Repository 薄 → [`repository-thin.md`](./repository-thin.md)

## 自检

- [ ] Controller 函数 ≤ 5 行？
- [ ] 不直接 import Repository / Model？
- [ ] 不写 if 业务判断？
- [ ] 只调用 Service 一次？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`service-orchestration.md`](./service-orchestration.md) · [`domain-pure.md`](./domain-pure.md) · [`repository-thin.md`](./repository-thin.md)
- 配套：[`../../framework/fastapi/router/zero-logic-principle.md`](../../framework/fastapi/router/zero-logic-principle.md)

