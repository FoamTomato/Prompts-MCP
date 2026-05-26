---
name: pipeline-method-as-flow
description: 方法即流程编排器 — 注释驱动的步骤大纲。Use when 写 Python 后端代码 / 评审涉及 `method-as-flow` 的
  PR。
parent: ./index.md
paths:
- backend/services/**/*.py
- py/services/**/*.py
triggers:
  keywords:
  - pipeline
  - 流水线
  - 注释驱动
effort: medium
context: inline
version: '1.0'
---
# Pipeline · 方法即流程编排器

## 核心思想

方法是流程编排器，**注释是步骤大纲，逻辑下沉到子方法**，命名即文档，常量替代魔法值。

读注释能理解全流程，看代码不被实现细节淹没。

## 模板

```python
async def submit_order(self, req: SubmitReq, user_id: int) -> OrderResp:
    # 前置校验
    OrderValidator.validate_submit(req)

    # 步骤 1：查询购物车并验证库存
    cart = await self._load_cart_with_stock_check(req.cart_id, user_id)

    # 步骤 2：计算最终价格（含优惠券、积分抵扣）
    price = self._price_calculator.calculate_final(cart, req.coupon, req.points)

    # 步骤 3：扣库存
    await self._inventory.deduct(cart.items)

    # 步骤 4：生成订单实体并落库
    order = Order.from_cart(cart, price, req)
    await self._repo.save(order)

    # 步骤 5：触发支付
    await self._payment.charge(order)

    # 步骤 6：转换并返回
    return OrderAdapter.to_resp(order)
```

## 注释约定

| 注释类型 | 例 |
|--------|------|
| 前置校验 | `# 前置校验` |
| 步骤编号 | `# 步骤 1：<语义>` |
| 关键决策 | `# 决策：先扣 bonus 后扣 base` |
| 临时 hack 标注 | `# TODO(2026-Q3): xxx` |

## 不要写

| 反例 | 说明 |
|------|------|
| `# 调用 user.id` | 无信息量，命名已说明 |
| `# 这里循环` | 代码已表达 |
| 英文 inline 注释（如 `# init`） | Quill 团队用中文注释 |

## 子方法的命名

子方法名表达**意图**而非**实现**：

```python
# ✅ 意图
cart = await self._load_cart_with_stock_check(req.cart_id, user_id)

# ❌ 实现
cart = await self._query_cart_and_validate_stock(req.cart_id, user_id)
```

## 步骤数量

- 5-7 步最佳
- 超过 10 步 → 拆 sub-flow（再抽一层 Service 方法）
- 少于 3 步 → 可能不需要 pipeline 风格

## 反例

```python
# ❌ 一个方法包打天下，无注释，难读
async def submit(req, user_id):
    cart = await Cart.filter(id=req.cart_id).first()
    if not cart: raise ApiException("...")
    for item in cart.items:
        stock = await Stock.filter(sku=item.sku).first()
        if stock.qty < item.qty: raise ApiException("...")
    # ... 60 行下沉
```

## 自检

- [ ] 主方法 ≤ 30 行？
- [ ] 每步前有中文注释？
- [ ] 子方法名表达意图不是实现？
- [ ] 5-7 步？
- [ ] 实现细节下沉到子方法 / Validator / Adapter？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`validator-converter-split.md`](./validator-converter-split.md) · [`ppt-outline-pipeline.md`](./ppt-outline-pipeline.md)
- 配套：[`../ddd-layering/service-orchestration.md`](../ddd-layering/service-orchestration.md)

