---
name: lang-typescript-null-safety-index
description: TypeScript 空值安全索引：可选链 ?. 取值 / 空值合并 ?? 设默认 / ?? vs || 陷阱 / null vs undefined。Use when 取可空属性 / 设默认值 / 处理后端可空字段
parent: ../index.md
children:
  - { name: optional-chaining-nullish, path: optional-chaining-nullish.md, tag: skill, note: "?. 取值 + ?? 默认值 + ?? vs || 陷阱" }
when_to_descend: |
  取可空属性（user?.profile?.name）。
  设默认值（count ?? 0）。
  处理后端可空字段（null vs undefined）。
---

# TypeScript · 空值安全

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| optional-chaining-nullish | skill | ?. 取值 + ?? 默认值 + ?? vs \|\| 陷阱 |

## 何时下钻

- 取可空属性 `user?.profile?.name` 防止访问 undefined 报错。
- 设默认值 `count ?? 0`，需保留 0 / '' / false 等假值。
- 处理后端可空字段，区分 null 与 undefined 的语义。

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../typing/index.md`](../typing/index.md) · [`../naming/index.md`](../naming/index.md) · [`../error-handling/index.md`](../error-handling/index.md)
