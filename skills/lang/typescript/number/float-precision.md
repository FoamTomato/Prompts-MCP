---
name: number-float-precision
description: 金额禁 number 直算 — 整数分存算 / decimal.js 任意精度 / EPSILON 比较。Use when 写金额加减乘除 / 对账校验 / 比较金额相等 / 处理汇率税率链式计算
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - float precision
  - decimal.js
  - Number.EPSILON
  - toFixed
  - 浮点精度
  - 整数分
  - 金额计算
effort: high
context: inline
version: '1.0'
---
# TypeScript · 金额浮点精度

## 规则

**金额 / 货币禁用 `number` 直接 `+ − × ÷`**。IEEE754 用二进制浮点表示，`0.1`、`0.2`、`1.005` 这类十进制小数无法被二进制精确表示，直算必然累积误差。

选型决策表(从上往下匹配):

| 场景 | 方案 |
|------|------|
| 钱(加减乘除 / 对账 / 比较) | **整数分**:`Math.round(x * 100)` 存与算，展示再 `/ 100`(首选) |
| 任意精度 / 汇率 / 税率链式计算 | `decimal.js` · `big.js` |
| 纯展示(不参与计算) | 交给 [`format.md`](format.md) 的 `Intl.NumberFormat` |

## 反例 → 正例

```ts
// ❌ number 直算:二进制无法精确表示十进制
0.1 + 0.2;                 // 0.30000000000000004,不等于 0.3
(0.1 + 0.2) === 0.3;       // false
(1.005).toFixed(2);        // "1.00" —— 1.005 实际存为 1.00499...,被截断
```

```ts
// ✅ 整数分:换算成整数分后做整数运算,误差归零
import type { OrderItem } from "@/types/order";

// 单位元转整数分,Math.round 消除换算误差
const toCents = (yuan: number): number => Math.round(yuan * 100);
// 整数分转展示用元字符串
const toYuan = (cents: number): string => (cents / 100).toFixed(2);

function sumOrderCents(items: OrderItem[]): number {
  // 每项单价转分 × 数量,得到该项小计(整数分)
  const lineCents = items.map((item) => toCents(item.price) * item.quantity);
  // 整数分求和,全程整数运算无浮点误差
  return lineCents.reduce((total, cents) => total + cents, 0);
}
```

```ts
// ✅ 任意精度 / 汇率税率链式:用 decimal.js
import Decimal from "decimal.js";

function calcWithTax(amount: number, rate: number, tax: number): string {
  // 链式乘汇率再乘税率,Decimal 全程十进制精确运算
  const result = new Decimal(amount).mul(rate).mul(new Decimal(1).plus(tax));
  // 末端定点到分再转字符串展示
  return result.toFixed(2);
}
```

**浮点比较禁 `a === b`**:

```ts
// ❌ 浮点直接相等判断
(0.1 + 0.2) === 0.3;                       // false

// ✅ 误差容忍比较(小数值)
Math.abs((0.1 + 0.2) - 0.3) < Number.EPSILON;   // true

// ✅ 大数失效时改用相对误差(EPSILON 是 1 附近的绝对精度,大数下绝对差恒大于它)
const closeEnough = (a: number, b: number): boolean =>
  Math.abs(a - b) <= Number.EPSILON * Math.max(Math.abs(a), Math.abs(b));
```

> `toFixed` 返回**字符串**,只能用于最终展示,不能再参与计算(`"1.00" + 1 === "1.001"`)。要继续算就回到整数分或 `decimal.js`。

## 自检

- [ ] 金额计算没有对 `number` 直接 `+ − × ÷`?
- [ ] 钱用整数分(`Math.round(x * 100)`)存算,展示才 `/ 100`?
- [ ] 汇率 / 税率 / 任意精度链式计算用了 `decimal.js` / `big.js`?
- [ ] 浮点比较用 `Math.abs(a - b) < EPSILON`(大数改相对误差),没有 `a === b`?
- [ ] `toFixed` 结果只用于展示,没有当数字二次计算?

## 相关

- 父:[`./index.md`](./index.md)
- 兄弟:[`format.md`](./format.md) —— 算对之后用 `Intl.NumberFormat` 显示对
- 跨引:[`../typing/no-any.md`](../typing/no-any.md) —— 金额类型用 `number` / `Decimal`,禁 `any`
