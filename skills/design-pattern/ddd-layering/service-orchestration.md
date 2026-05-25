---
name: ddd-service-orchestration
description: Service 编排层 — 注释驱动的流水线方法
parent: ./index.md
paths:
  - "backend/services/**/*.py"
  - "py/services/**/*.py"
triggers:
  keywords: [Service, 编排, 流水线]
effort: medium
context: inline
version: "1.0"
---

# DDD · Service 编排

## 规则

Service 负责**业务流程编排**：校验 → 加载领域对象 → 调用领域方法 → 持久化 → 返回。

## 流水线方法结构

```python
async def submit_order(self, req: SubmitOrderReq, user_id: int) -> OrderResp:
    """提交订单 — 6 步编排"""

    # 1. 参数与权限校验
    OrderValidator.validate_submit(req)

    # 2. 加载购物车并校验库存
    cart = await self._load_cart_with_stock_check(req.cart_id, user_id)

    # 3. 计算最终价格（含优惠、积分）
    price = self._price_calculator.calculate(cart, req.coupon, req.points)

    # 4. 扣库存
    await self._inventory.deduct(cart.items)

    # 5. 生成订单
    order = Order.from_cart(cart, price, req)
    await self._repo.save(order)

    # 6. 触发支付
    await self._payment.charge(order)

    logger.info(f"提交订单完成 - order_id={order.id} user_id={user_id} amount={price.total}")
    return OrderAdapter.to_resp(order)
```

## 注释驱动

每步前一行中文注释，**读注释即懂全流程**。Reviewer 看注释能判断是否合理。

## 五个抽象（独立成类 / 函数）

| 抽象 | 何时抽 | 命名 |
|------|------|------|
| **Validator** | 参数校验 ≥ 3 行 | `OrderValidator.validate_*` |
| **Converter** | 字段映射 ≥ 5 行 | `OrderConverter.to_*` / `OrderAdapter.to_*` |
| **PriceCalculator** | 业务计算独立 | 注入到 Service |
| **Repository** | 持久化 | `OrderRepository.save` |
| **GatewayService** | 调外部 API | `PaymentService.charge` |

Service 主流程只调用，不内嵌。

## 反例

```python
# ❌ 编排里堆 50 行字段映射
async def submit_order(req, user_id):
    cart = await Cart.filter(id=req.cart_id).first()
    ...
    # 50 行字段映射
    result = {
        "id": order.id,
        "title": order.title,
        ...   # 50 个字段
    }
    return result

# ✅ 抽 Adapter
result = OrderAdapter.to_resp(order)
return result
```

## 异常处理三件套

```python
async def submit_order(req, user_id):
    try:
        # ... 6 步编排
        return result
    except ApiException:
        raise   # 业务异常透传
    except Exception as e:
        logger.exception(f"提交订单失败 - user_id={user_id}: {e}")
        raise ApiException(msg="提交失败，请重试")
```

详见 [`../../lang/python/error-handling/api-exception.md`](../../lang/python/error-handling/api-exception.md)。

## 自检

- [ ] Service 方法 ≤ 30 行？
- [ ] 每步有中文注释？
- [ ] 参数校验 / 字段映射 / 计算独立抽出？
- [ ] 不直接写 SQL（通过 Repository）？
- [ ] 异常三件套完整？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`controller-thin.md`](./controller-thin.md) · [`domain-pure.md`](./domain-pure.md) · [`repository-thin.md`](./repository-thin.md)
- 配套：[`../pipeline/method-as-flow.md`](../pipeline/method-as-flow.md) · [`../pipeline/validator-converter-split.md`](../pipeline/validator-converter-split.md)

