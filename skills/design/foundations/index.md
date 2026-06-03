---
name: design-foundations-index
description: UI 通用硬规范索引 — 与视觉风格无关的底线：WCAG 2.2 无障碍 / 8pt 间距 / 模块化字阶 / 60-30-10 配色 / 响应式断点。Use when 写任意前端页面 / 评审 UI 是否达标 / 校对比度间距字阶时。
parent: ../index.md
children:
  - { name: accessibility, path: accessibility.md, tag: leaf, note: WCAG 2.2 对比度 / 触控目标 / focus-visible / reduced-motion }
  - { name: spacing-grid, path: spacing-grid.md, tag: leaf, note: 8pt 主网格 + 4pt 子网格 + 禁奇数像素 }
  - { name: typography-scale, path: typography-scale.md, tag: leaf, note: 模块化字阶比例 + 行长 45-75 字符 + 行高 1.5 }
  - { name: color-usage, path: color-usage.md, tag: leaf, note: 60-30-10 比例 + 语义角色 + 状态禁纯色编码 }
  - { name: responsive-breakpoints, path: responsive-breakpoints.md, tag: leaf, note: 断点降列策略 + 移动端触控目标 }
when_to_descend: |
  写任何前端页面/组件、或评审 UI 还原时的底线规约，与用什么视觉风格无关。
  风格层（bento/flat/wes-anderson）在这些规范之上叠加观感，但不得突破这里的硬底线。
  写新页面且用户未指定风格时，同时进 ../theme/theme-selection 取默认 bento。
---

# Foundations · 通用硬规范

> 这里是**与风格无关的底线**：无论 bento 还是 wes-anderson，对比度、间距、字阶、配色比例、响应式都得守住。
> 数字锚定 WCAG 2.2 与主流设计系统（Material 3 / Apple HIG），可直接照抄。

按你正在关心的维度下钻：

| 你在关心 | 进哪个 |
|---------|-------|
| 对比度够不够 / 触控目标多大 / 焦点可见 / 动效尊重偏好 | [accessibility](accessibility.md) |
| 间距用多少 / 8pt 还是 4pt | [spacing-grid](spacing-grid.md) |
| 字号阶梯怎么定 / 行长行高字重 | [typography-scale](typography-scale.md) |
| 各色占比 / 主色辅色强调色怎么分 | [color-usage](color-usage.md) |
| 断点设哪几档 / 移动端怎么降列 | [responsive-breakpoints](responsive-breakpoints.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 配色角色如何 token 化：[`../design-language/tokens-and-theming.md`](../design-language/tokens-and-theming.md)
- 动效细则：[`../component-patterns/motion-and-animation.md`](../component-patterns/motion-and-animation.md)
