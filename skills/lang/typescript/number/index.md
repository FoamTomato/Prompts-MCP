---
name: lang-typescript-number-index
description: TypeScript 数字处理索引，管两件事：金额浮点精度（算对，整数分 / decimal.js）+ Intl 格式化（显示对，千分位 / 货币 / 百分比）。Use when 写 / 评审金额、价格、数字展示代码。
parent: ../index.md
children:
  - { name: float-precision, path: float-precision.md, tag: skill, note: 金额禁浮点直算 / 整数分 / decimal.js }
  - { name: format, path: format.md, tag: skill, note: Intl.NumberFormat 千分位 / 货币 / 百分比 }
when_to_descend: |
  写 / 评审金额、价格、数字展示代码。
  算钱（加减乘除 / 比较）→ float-precision。
  显示数字（千分位 / 货币符号 / 百分比）→ format。
---

# TypeScript · 数字处理

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| float-precision | skill | 金额禁浮点直算，整数分存储 / decimal.js 运算 |
| format | skill | Intl.NumberFormat 做千分位 / 货币 / 百分比展示 |

## 何时下钻

- 算钱：金额加减乘除、对账、比较金额相等 → [`float-precision.md`](float-precision.md)。
- 展示数字：列表 / 详情页渲染价格、金额、百分比、大数字千分位 → [`format.md`](format.md)。
- 一条链路常同时命中两者：先用 float-precision 算对，再用 format 显示对。

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../naming/index.md`](../naming/index.md) · [`../typing/index.md`](../typing/index.md) · [`../style/index.md`](../style/index.md)
- 框架配套：[`../../../framework/antd/`](../../../framework/antd/index.md)
