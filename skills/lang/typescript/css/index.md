---
name: lang-typescript-css-index
description: CSS 布局陷阱索引（z-index / stacking context / overflow / flex / 100vh / sticky）。Use when 写或调 .tsx / .css / .scss 样式遇到层叠遮挡、溢出裁切、弹性挤压或定位失效问题。
parent: ../index.md
children:
  - { name: layout-traps, path: layout-traps.md, tag: skill, note: z-index 只对定位元素生效 / 父级建 stacking context / overflow 裁切 / flex min-width / sticky 失效 }
when_to_descend: |
  写或调 .tsx / .css / .scss 样式遇到层叠、溢出、弹性、定位问题。
  弹窗被遮挡 / 内容被裁切 / 子项压不下去 / sticky 不吸顶 → layout-traps。
---

# TypeScript · CSS 布局陷阱

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| layout-traps | skill | z-index 只对定位元素生效 / 父级建 stacking context / overflow 裁切 / flex min-width / sticky 失效 |

## 何时下钻

- z-index 调大仍被遮挡，或父级 transform/opacity/filter 建了新 stacking context。
- overflow:hidden/auto 把子元素裁切、阴影或下拉被切。
- flex 子项压不下去、文本不换行(缺 min-width:0)。
- 100vh 在移动端含地址栏溢出、需 dvh/svh。
- position:sticky 不吸顶(父级 overflow 或缺定位上下文)。

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../style/index.md`](../style/index.md) · [`../error-handling/index.md`](../error-handling/index.md)
- 框架配套：[`../../../framework/antd/index.md`](../../../framework/antd/index.md) · [`../../../framework/react/index.md`](../../../framework/react/index.md)
