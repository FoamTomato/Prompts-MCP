---
name: datetime-pitfalls
description: 原生 Date 的五类坑(解析歧义/月份0起/setter可变/时区/DST算术)与统一用 dayjs 的约定。Use when 解析日期字符串 / 做日期加减 / 处理时区 DST / 选 Date 还是 dayjs 时。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - new Date
  - dayjs
  - getMonth
  - setDate
  - 时区
  - DST 夏令时
  - ISO-8601
  - 月份 0-indexed
  - 日期解析
effort: high
context: inline
version: '1.0'
---
# TypeScript · 原生 Date 五类坑

## 规则

**决策点：能不碰原生 `Date` 就不碰 —— 解析/运算/格式化全部走 `dayjs`(antd5 内置)。** 原生 `Date` 只在拿到 `Date` 实例时立刻 `dayjs(d)` 包一层。

| 坑 | 现象 | 规约 |
|----|------|------|
| 1 解析歧义 | `new Date("2024-01-02")` 按 **UTC** 零点;`new Date("2024/01/02")` 按**本地**零点;非 ISO 串结果**因引擎而异** | 禁用 `new Date(string)` 解析任意串,用 `dayjs(str, fmt)` 显式格式 |
| 2 月份 0 起 | `new Date(2024, 0, 1)` = 一月;`getMonth()` 返回 `0~11` | 用 `dayjs().month()`(仍 0 起,但 `.format('MM')` 安全)或直接 `format` |
| 3 setter 可变 | `d.setDate(d.getDate()+1)` **原地改** `d`,污染引用 | 视 Date 为不可变,`dayjs(d).add(1, 'day')` 返回新对象 |
| 4 时区 | `getHours()` 本地、`getUTCHours()` UTC,混用错位 | 前后端一律传 **ISO-8601 UTC** 串,展示时才 `.local()` |
| 5 DST 算术 | `t + 86400000` 在夏令时切换日**差 1 小时** | 禁手算毫秒,用 `dayjs(d).add(1, 'day')` 按日历加 |

## 反例

```typescript
// ❌ 坑1：解析歧义，同一天解析出不同时刻
const a = new Date("2024-01-02");   // UTC 零点
const b = new Date("2024/01/02");   // 本地零点，差一个时区
// ❌ 坑3：setter 原地改，污染外部引用
const tomorrow = new Date(order.createdAt);
tomorrow.setDate(tomorrow.getDate() + 1);  // order.createdAt 也被改了吗？心智负担
// ❌ 坑5：毫秒算术，DST 当天少/多一小时
const next = new Date(start.getTime() + 86400000);
```

## 正例

```typescript
import dayjs from "dayjs";
import customParseFormat from "dayjs/plugin/customParseFormat";
import utc from "dayjs/plugin/utc";

dayjs.extend(customParseFormat);
dayjs.extend(utc);

// 坑1：显式格式解析，杜绝引擎差异
const parsed = dayjs("2024/01/02", "YYYY/MM/DD");
// 坑3 + 坑5：不可变 + 按日历加，DST 安全
const tomorrow = dayjs(order.createdAt).add(1, "day");
// 坑4：传后端统一 UTC ISO-8601 串
const payload = { startAt: dayjs(start).utc().toISOString() };
// 坑2 + 坑4：展示时转本地再格式化（月份用 format 不手拼）
const display = dayjs(payload.startAt).local().format("YYYY-MM-DD HH:mm");
```

## 选型

| 库 | 结论 |
|----|------|
| **dayjs** | ✅ 本项目唯一标准(antd5 内置,零额外依赖) |
| moment | ❌ 体积大且官方停止维护,禁引入 |
| 原生 Date | ⚠️ 仅作 `dayjs(d)` 入参,不直接运算/解析 |
| Temporal | ⚠️ 仅前瞻关注,不用于生产 |

> locale 设置不在此处散落,统一走 [`antd/setup/install-and-locale`](../../../framework/antd/setup/install-and-locale.md)(`dayjs/locale/zh-cn` + antd `ConfigProvider`)。

## 自检

- [ ] 没有用 `new Date(string)` 解析任意字符串?改 `dayjs(str, fmt)`?
- [ ] 日期加减用 `dayjs().add()` 而非毫秒算术或 `setDate`?
- [ ] 传后端的时间是 UTC ISO-8601 串(`.utc().toISOString()`)?
- [ ] 月份没踩 0-indexed?展示用 `.format()` 不手拼 `getMonth()+1`?
- [ ] 没引入 moment?locale 走 antd setup 而非本文件?

## 相关

- 父:[`./index.md`](./index.md)
- 跨引(locale 配置):[`../../../framework/antd/setup/install-and-locale.md`](../../../framework/antd/setup/install-and-locale.md)
- 后端对应:[`../../java/datetime/index.md`](../../java/datetime/index.md)
