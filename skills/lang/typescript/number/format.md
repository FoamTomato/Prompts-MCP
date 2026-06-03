---
name: number-format
description: 用 Intl.NumberFormat 做千分位 / 货币 / 百分比展示，禁手写正则加逗号或手拼 ¥。Use when
  渲染金额价格 / 显示百分比 / 大数字加千分位 / 格式化货币符号。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - Intl.NumberFormat
  - 千分位
  - 货币格式化
  - formatCurrency
  - currencyDisplay
  - percent format
effort: low
context: inline
version: '1.0'
---
# TypeScript · 数字显示格式化

## 规则

决策点：展示任何数字一律走 `Intl.NumberFormat`，禁手写正则加逗号 / 手拼 `¥` 符号。locale 显式传 `'zh-CN'`，小数位用 `minimum/maximumFractionDigits` 控制。

| style | 用途 | 关键参数 | 输入约定 |
|-------|------|---------|---------|
| `decimal` | 千分位整数 / 小数 | `maximumFractionDigits` | 原值 `1234567.5` |
| `currency` | 货币(带符号) | `currency: 'CNY'` + `currencyDisplay` | 元为单位 `1234.5` |
| `percent` | 百分比 | `maximumFractionDigits` | **0~1 小数**(`0.1234` → `12.34%`) |

性能:formatter 实例较重,**模块级缓存复用**,不在 render / 循环里 `new`。

## 反例

```ts
// ❌ 手写正则加千分位 — 漏负号 / 小数 / 边界
const bad1 = String(amount).replace(/\B(?=(\d{3})+(?!\d))/g, ',');

// ❌ 手拼货币符号 — locale 不一致、小数位失控
const bad2 = '¥' + amount.toFixed(2);

// ❌ 百分比当 0~100 传 — 多乘 100 出错
const bad3 = new Intl.NumberFormat('zh-CN', { style: 'percent' }).format(12.34);

// ❌ render 里 new formatter — 每次渲染重建实例
const Cell = ({ v }: { v: number }) =>
  <span>{new Intl.NumberFormat('zh-CN').format(v)}</span>;
```

## 正例

```ts
// src/utils/number-format.ts — 模块级缓存 formatter 实例
const decimalFmt = new Intl.NumberFormat('zh-CN', {
  maximumFractionDigits: 2,
});
const currencyFmt = new Intl.NumberFormat('zh-CN', {
  style: 'currency',
  currency: 'CNY',
  currencyDisplay: 'symbol',
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});
const percentFmt = new Intl.NumberFormat('zh-CN', {
  style: 'percent',
  maximumFractionDigits: 2,
});

// 千分位:1234567.5 → "1,234,567.5"
export const formatDecimal = (n: number): string => decimalFmt.format(n);

// 货币:1234.5 → "¥1,234.50"
export const formatCurrency = (n: number): string => currencyFmt.format(n);

// 百分比:输入是 0~1 小数,0.1234 → "12.34%"
export const formatPercent = (ratio: number): string => percentFmt.format(ratio);
```

```tsx
// 组件体只做编排:校验 → 取值 → 渲染
import { formatCurrency, formatPercent } from '@/utils/number-format';

interface PriceCellProps {
  price: number | null;
  discountRatio: number;
}

const PriceCell: React.FC<PriceCellProps> = ({ price, discountRatio }) => {
  // 前置校验:空值早返回占位
  if (price == null) return <span>--</span>;

  // 格式化金额与折扣率(util 内已缓存 formatter)
  const priceText = formatCurrency(price);
  const discountText = formatPercent(discountRatio);

  return <span>{priceText}（{discountText}）</span>;
};
```

## 自检

- [ ] 展示数字全部走 `Intl.NumberFormat`,没有正则加逗号 / `'¥' +` 拼接?
- [ ] locale 显式传 `'zh-CN'`,没靠运行环境默认?
- [ ] percent 输入是 0~1 小数,不是 0~100?
- [ ] formatter 实例模块级缓存,没在 render / 循环里 `new`?
- [ ] 小数位用 `minimum/maximumFractionDigits` 控制,不用 `toFixed` 再格式化?

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟:算钱(加减乘除 / 比较)去 [`./float-precision.md`](./float-precision.md);本 skill 只管显示。
- 配套:antd 表格列渲染 [`../../../framework/antd/index.md`](../../../framework/antd/index.md)
