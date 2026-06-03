---
name: lang-typescript-coercion-index
description: JS 相等判断与隐式类型转换的坑（=== / NaN / typeof null / sort / parseInt radix）索引。Use when 写相等判断 / 数值解析 / 数组排序结果不对 / 真值判断踩坑时。
parent: ../index.md
children:
  - { name: equality-and-coercion, path: equality-and-coercion.md, tag: skill, note: 强制 === / Number.isNaN / sort 比较器 / parseInt radix }
when_to_descend: |
  写相等判断、数值解析、数组排序、真值判断时下钻。
  涉及 == / NaN 比较 / typeof null / [].sort() / parseInt → equality-and-coercion。
---

# TypeScript · 相等与类型转换

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| equality-and-coercion | skill | 强制 === / Number.isNaN / sort 比较器 / parseInt radix |

## 何时下钻

- 写相等判断：选 `===` 还是 `==`，对象/`null` 怎么比。
- 数值解析：`parseInt` / `Number` / `NaN` 判定。
- 数组排序：`[].sort()` 默认按字符串排导致数字乱序。
- 真值判断：`0 / '' / null / undefined / NaN` 的 falsy 行为。

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../typing/index.md`](../typing/index.md) · [`../naming/index.md`](../naming/index.md)
- 跨引：[`../../javascript/index.md`](../../javascript/index.md)
