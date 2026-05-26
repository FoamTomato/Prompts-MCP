---
name: pipeline-validator-converter
description: Validator/Converter 独立 — Service 方法只调用，不内嵌。Use when 写 Python 后端代码 / 评审涉及
  `validator-converter-split` 的 PR。
parent: ./index.md
paths:
- backend/services/**/*.py
- py/services/**/*.py
- backend/adapters/**/*.py
- py/adapters/**/*.py
triggers:
  keywords:
  - Validator
  - Converter
  - Adapter
  - 方法只调用
  - 不内嵌
effort: medium
context: inline
version: '1.0'
---
# Pipeline · Validator/Converter 独立

## 规则

参数校验抽到 `*Validator`，字段映射抽到 `*Converter` / `*Adapter`。Service 方法只调用一行。

## Validator

```python
# py/validators/order.py
class OrderValidator:
    @staticmethod
    def validate_submit(req: SubmitOrderReq) -> None:
        if not req.cart_id:
            raise ApiException(msg="cart_id 必填")
        if req.amount <= 0:
            raise ApiException(msg="金额必须 > 0")
        if req.coupon and len(req.coupon) > 16:
            raise ApiException(msg="优惠券码无效")

    @staticmethod
    def assert_exists(obj, name: str) -> None:
        if obj is None:
            raise ApiException(msg=f"{name} 不存在", code=404)

    @staticmethod
    def assert_owned(obj, user_id: int) -> None:
        if obj.owner_id != user_id:
            raise ApiException(msg="无权限", code=403)
```

Service 内一行调用：

```python
async def submit_order(self, req, user_id):
    OrderValidator.validate_submit(req)
    order = await self.repo.find_by_id(req.order_id)
    OrderValidator.assert_exists(order, "订单")
    OrderValidator.assert_owned(order, user_id)
    ...
```

## Converter / Adapter

```python
# py/adapters/order.py
class OrderAdapter:
    @staticmethod
    def to_resp(order: Order) -> OrderResp:
        return OrderResp(
            id=str(order.id),
            title=order.title,
            amount=order.amount,
            status=order.status.value,
            created_at=order.created_at.isoformat(),
        )

    @staticmethod
    def to_list_resp(orders: list[Order]) -> list[OrderResp]:
        return [OrderAdapter.to_resp(o) for o in orders]

    @staticmethod
    def to_detail_resp(order: Order, items: list[OrderItem]) -> OrderDetailResp:
        base = OrderAdapter.to_resp(order)
        return OrderDetailResp(
            **base.model_dump(),
            items=[ItemAdapter.to_resp(i) for i in items],
        )
```

Service 内一行调用：

```python
async def get_order_detail(order_id):
    order = await self.repo.find_by_id(order_id)
    items = await self.item_repo.find_by_order(order_id)
    return OrderAdapter.to_detail_resp(order, items)
```

## 何时抽

| 信号 | 抽 |
|------|------|
| 同样的校验在 ≥ 2 个方法重复 | ✅ Validator |
| 校验逻辑 ≥ 5 行 | ✅ Validator |
| 同样的字段映射在 ≥ 2 个方法重复 | ✅ Adapter |
| 字段映射 ≥ 5 个字段 | ✅ Adapter |

## 反例

```python
# ❌ 散落 if 校验在每个 service 方法
async def create(req, user_id):
    if not req.title: raise ApiException(...)
    if len(req.title) > 200: raise ApiException(...)
    ...

async def update(req, user_id):
    if not req.title: raise ApiException(...)   # 重复
    if len(req.title) > 200: raise ApiException(...)
    ...

# ✅
OrderValidator.validate_title(req.title)
```

```python
# ❌ Service 内手工映射
return OrderResp(
    id=str(order.id),
    title=order.title,
    amount=order.amount,
    # ... 20 字段
)

# ✅
return OrderAdapter.to_resp(order)
```

## 自检

- [ ] 重复 ≥ 2 次的校验抽到 Validator？
- [ ] 重复 ≥ 2 次的字段映射抽到 Adapter？
- [ ] Service 主方法看不到散落 if 校验？
- [ ] Service 主方法看不到散落 `OrderResp(id=..., title=..., ...)` 散装构造？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`method-as-flow.md`](./method-as-flow.md)

