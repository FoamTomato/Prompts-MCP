---
name: solid-open-closed
description: 开闭原则 OCP — 对扩展开放对修改封闭，新增行为靠加实现类而非改 if-else 分支。Use when 加新类型要改老 switch / 设计可扩展点 / 评审频繁改动同一段分支代码时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 开闭原则
  - OCP
  - 扩展点
  - 多态替换分支
  - Open Closed
effort: medium
context: inline
version: '1.0'
---
# SOLID · 开闭原则 OCP

> 本条只管「加功能时改不改老代码」。具体用工厂选实现见 [`../factory/index.md`](../factory/index.md)，用策略替算法见 [`../strategy/index.md`](../strategy/index.md)。

## 规则

| 判据 | 要求 |
|------|------|
| 对扩展开放 | 新需求靠**新增类/实现**满足 |
| 对修改封闭 | 不改动已测试稳定的老代码（避免回归风险） |
| 抽象做支点 | 用接口/抽象类锁定不变契约，变化点放到实现里 |
| 信号 | 每加一种类型都要改同一处 `if/switch` → 该上多态 |

## 正例：新增不改老码

```java
public interface DiscountRule {
    BigDecimal apply(Order order);
}

@Component
public class VipDiscount implements DiscountRule { /* ... */ }
@Component
public class CouponDiscount implements DiscountRule { /* ... */ }

// 编排层只依赖抽象；新增 NewYearDiscount 只加一个类，本类不动
@Service
public class PriceService {
    private final List<DiscountRule> rules;   // Spring 注入全部实现
    public BigDecimal finalPrice(Order order) {
        BigDecimal price = order.getAmount();
        for (DiscountRule rule : rules) {
            price = price.subtract(rule.apply(order));
        }
        return price;
    }
}
```

## 反例：开关分支

```java
// ❌ 每加一种折扣都要改这个 switch（修改封闭被破坏）
public BigDecimal finalPrice(Order order, String type) {
    if ("vip".equals(type))        { /* ... */ }
    else if ("coupon".equals(type)){ /* ... */ }
    else if ("newyear".equals(type)){ /* 新增就改这里 */ }
    // 改动有回归风险，且违反 SRP
}
```

## 自检

- [ ] 新增一种行为时，是加新类还是改老的 if/switch？
- [ ] 编排层只依赖接口/抽象类，不依赖具体实现？
- [ ] 不变契约抽到了接口，变化点都在实现里？
- [ ] 没有「每加一种类型都要改同一处分支」的坏味道？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`single-responsibility.md`](./single-responsibility.md)（先拆职责才好扩展）
- 实现手段：[`../strategy/index.md`](../strategy/index.md) · [`../factory/index.md`](../factory/index.md)
