---
name: lang-typescript-datetime-index
description: TypeScript 日期时间索引：原生 Date 解析/月份/setter/时区陷阱与 dayjs 操作约定。Use when 写日期解析 / 格式化 / 时区 DST / 日期运算
parent: ../index.md
children:
  - { name: pitfalls, path: pitfalls.md, tag: skill, note: new Date 解析 / 月份 0 起 / setter 原地改 / 时区 DST / 统一用 dayjs }
when_to_descend: 写日期解析、格式化、时区、日期运算
---

# TypeScript · 日期时间

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| pitfalls | skill | new Date 解析 / 月份 0 起 / setter 原地改 / 时区 DST / 统一用 dayjs |

## 何时下钻

- 解析字符串为日期、格式化日期为字符串
- 做日期加减、区间、起止边界运算
- 处理时区 / DST 跨界
- 选择原生 Date 还是 dayjs

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../style/index.md`](../style/index.md) · [`../async/index.md`](../async/index.md)
- 跨引：[`../../java/datetime/index.md`](../../java/datetime/index.md) · [`../../../framework/antd/setup/install-and-locale.md`](../../../framework/antd/setup/install-and-locale.md)
