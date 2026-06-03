---
name: lang-typescript-index
description: TypeScript 语言级规则索引（命名 / typing / async / module / style / error-handling）
parent: ../index.md
children:
  - { name: naming, path: naming/index.md, tag: folder, note: 文件名 / interface vs type / 命名风格 }
  - { name: typing, path: typing/index.md, tag: folder, note: strict mode / no any }
  - { name: async, path: async/index.md, tag: folder, note: no floating promise / async vs then }
  - { name: module, path: module/index.md, tag: folder, note: ESM only / barrel export }
  - { name: style, path: style/index.md, tag: folder, note: design tokens / 样式约定 }
  - { name: error-handling, path: error-handling/index.md, tag: folder, note: ApiError 子类 / Asserts 工具 / ErrorBoundary / 表单错误处理 }
  - { name: modern-syntax, path: modern-syntax/index.md, tag: folder, note: ES2022+ 数组对象新方法 / TS satisfies / using 资源管理 }
  - { name: number, path: number/index.md, tag: folder, note: 金额浮点精度 / Intl 数字货币格式化 }
  - { name: closure, path: closure/index.md, tag: folder, note: 循环 var 捕获 / setTimeout 闭包 / 内存泄漏 }
  - { name: null-safety, path: null-safety/index.md, tag: folder, note: 可选链 / 空值合并 / null vs undefined }
  - { name: datetime, path: datetime/index.md, tag: folder, note: new Date 解析 / 月份 0 起 / 时区 DST / dayjs }
  - { name: coercion, path: coercion/index.md, tag: folder, note: 相等 === / NaN / sort / parseInt 类型转换坑 }
  - { name: css, path: css/index.md, tag: folder, note: z-index/stacking/overflow/flex/sticky 布局陷阱 }
  - { name: types, path: types/index.md, tag: folder, note: 泛型 / 工具类型 / 类型守卫 / 判别联合 / enum / as const / d.ts }
when_to_descend: |
  写 / 改 .ts / .tsx 文件。
  错误处理任务（fetcher / 表单 / ErrorBoundary）→ error-handling。
  样式层叠 / 定位 / 溢出陷阱（z-index / overflow / sticky / flex）→ css。
  设计可复用类型 / 收窄联合 / 工具类型 → types。
---

# TypeScript · 语言级规则

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| naming | 文件夹 | 文件名 / interface / type alias / 命名风格 |
| typing | 文件夹 | strict mode + 禁 any |
| async | 文件夹 | 禁 floating promise / async vs then |
| module | 文件夹 | ESM only / barrel export |
| style | 文件夹 | design tokens / 样式约定 |
| error-handling | 文件夹 | ApiError + Asserts + ErrorBoundary + 表单错误 |
| modern-syntax | 文件夹 | ES2022+ 数组对象新方法 + TS satisfies / using |
| number | 文件夹 | 金额浮点精度 + Intl 数字货币格式化 |
| closure | 文件夹 | 循环 var 捕获 / setTimeout 闭包 / 内存泄漏 |
| null-safety | 文件夹 | 可选链 / 空值合并 / null vs undefined |
| datetime | 文件夹 | new Date 解析 / 月份 0 起 / 时区 DST / dayjs |
| coercion | 文件夹 | 相等 === / NaN / sort / parseInt 类型转换坑 |
| css | 文件夹 | z-index/stacking/overflow/flex/sticky 布局陷阱 |
| types | 文件夹 | 泛型 / 工具类型 / 类型守卫 / 判别联合 / enum / as const / d.ts |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../python/index.md`](../python/index.md) · [`../sql/index.md`](../sql/index.md) · [`../javascript/index.md`](../javascript/index.md)
- 框架配套：[`../../framework/react/`](../../framework/react/index.md) · [`../../framework/antd/`](../../framework/antd/index.md)
