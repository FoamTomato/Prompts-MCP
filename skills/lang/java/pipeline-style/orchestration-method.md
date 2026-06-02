---
name: java-orchestration-method
description: Service 业务方法写成流水线编排器 — 前置校验早返回 / 每步一行中文注释一次调用 / 中间变量 final / 无嵌套。Use when 写业务方法 / 重构深嵌套方法 / 评审方法体结构时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 流水线编排
  - 注释驱动
  - pipeline style
  - 编排方法
  - final 局部变量
  - 早返回
  - 逻辑下沉
effort: medium
context: inline
version: '1.0'
---
# Java · 方法即流水线编排器

> 本条只管「编排方法的方法体怎么组织」。转换/校验抽到哪见 [`extract-converter-validator.md`](./extract-converter-validator.md)。

## 规则

| 原则 | 要求 |
|------|------|
| 前置校验早返回 | 方法开头校验入参，不满足直接 `return`，避免深层嵌套 |
| 注释即大纲 | 每个处理步骤前一行 `// 中文注释` 说明意图，读注释=读流程 |
| 每步一调用 | 一步做一件事，顺序执行，**编排层无 if-else 嵌套超过 1 层** |
| 中间变量 final | 中间结果一律 `final`，表明赋值后不变（类字段不加） |
| 逻辑下沉 | 超过 3 行的转换/计算下沉 `XxxUtils` 静态方法；集合用 Stream；DTO 转换用 MapStruct |

## 正例：结构模板

```java
public OrderVO settle(SettleReq req) {
    // 前置校验
    if (req == null || req.getOrderId() == null) {
        log.warn("settle req or orderId is null");
        return null;
    }

    // 步骤1：查订单
    final OrderDO order = orderMapper.selectById(req.getOrderId());
    OrderValidator.assertExists(order, req.getOrderId());

    // 步骤2：查用户优惠券
    final List<CouponDO> coupons = couponService.listUsable(order.getUserId());

    // 步骤3：计算最终价格（逻辑下沉 Utils）
    final Money finalPrice = PriceUtils.calcFinal(order, coupons);

    // 步骤4：转换并返回（MapStruct）
    return OrderConvert.INSTANCE.toVO(order, finalPrice);
}
```

读方法体 = 读 4 行步骤注释就懂全流程。

## 反例：逻辑堆在编排层

```java
// ❌ 转换/计算/嵌套 if 全堆在方法体，读不懂主流程
public OrderVO settle(SettleReq req) {
    OrderDO order = orderMapper.selectById(req.getOrderId());
    if (order != null) {
        BigDecimal total = BigDecimal.ZERO;
        for (Item it : order.getItems()) {       // 手动循环
            total = total.add(it.getPrice());     // 计算逻辑该下沉
        }
        OrderVO vo = new OrderVO();
        vo.setTitle(order.getTitle());            // 20 行转换该交 MapStruct
        // ...
    }
}
```

## 自检

- [ ] 方法开头有前置校验 + 早返回，方法体是平坦顺序结构（嵌套 ≤1 层）？
- [ ] 每个步骤前有 `// 中文注释`？
- [ ] 所有中间变量加了 `final`？
- [ ] >3 行的转换/计算下沉了 Utils，集合用 Stream，DTO 转换用 MapStruct？
- [ ] 日志用 `log.warn` + 英文？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`extract-converter-validator.md`](./extract-converter-validator.md)（转换/校验抽去哪）
- 集合操作：[`../collections/stream-api.md`](../collections/stream-api.md)
- DTO 转换：[`../../../framework/mapstruct/index.md`](../../../framework/mapstruct/index.md)
- 逻辑下沉：[`../utils/utility-class-design.md`](../utils/utility-class-design.md)
