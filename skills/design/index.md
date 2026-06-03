---
name: design-index
description: UI 设计维度 — 通用规范(a11y/间距/字体/配色) + 主题风格(bento 默认/flat/wes/glass·极简等) + 设计语言 token + 组件模式。Use when 写前端页面 / 选视觉风格 / 定项目设计系统 token / 评审 UI 还原时。
parent: ../index.md
children:
  - { name: foundations, path: foundations/index.md, tag: folder, note: 跨风格通用硬规范 — WCAG 2.2 a11y / 8pt 间距 / 模块化字阶 / 60-30-10 配色 / 响应式断点 }
  - { name: theme, path: theme/index.md, tag: folder, note: 主题风格库 — 默认 bento，指定则切 flat-design / wes-anderson / 其它 }
  - { name: design-language, path: design-language/index.md, tag: folder, note: 三层 token 模型 + 换肤 + 「为项目定一套设计语言」方法论 }
  - { name: component-patterns, path: component-patterns/index.md, tag: folder, note: 跨风格组件落地 — 按钮层级 / 卡片与面板 / 动效 }
when_to_descend: |
  任务涉及前端「长什么样」：写新页面/组件、还原设计稿、选视觉风格、定配色字体间距、为项目沉淀设计系统 token。
  与 framework/react·antd 的区别：那边管「框架/组件库怎么用」，本维度管「视觉规范与风格」，二者常同时下钻。
---

# Design · UI 设计维度

> 7 个工程维度之外，本维度专管前端「视觉规范与风格」。任何「写页面 / 还原稿 / 选风格 / 定 token」的任务从这里下钻。

## 按你正在做的事下钻

| 你在做什么 | 进哪个 |
|-----------|-------|
| 写新页面/组件，要守对比度·间距·字阶·配色·响应式 | [foundations/](foundations/index.md) |
| 不知道用什么视觉风格 / 要切 bento·flat·wes-anderson | [theme/theme-selection](theme/theme-selection.md) |
| 已定风格，要它的配色·圆角·阴影·栅格细则 | [theme/](theme/index.md) 下对应风格叶子 |
| 给项目定一套设计系统（token / 灰阶 / 品牌色 / 换肤） | [design-language/](design-language/index.md) |
| 写按钮·卡片·动效，要跨风格通用落地约定 | [component-patterns/](component-patterns/index.md) |

## 主题风格默认规则

**用户指定主题 → 用对应风格；未指定 → 默认 bento。** 详见 [theme/theme-selection](theme/theme-selection.md)。

## 与外部 skill 的分工

本维度给「项目锚定、可检索命中的硬规约 + 三套常用主题」。需要更大的检索库或审美方向把控时，改用外部 skill：

| 需求 | 改用 | 本维度给 |
|------|------|---------|
| 浏览 50+ 风格 / 21 配色 / 50 字体配对 / 图表选型，按关键词检索 | `ui-ux-pro-max` | bento/flat/wes-anderson 三套 + 冷门风格一行速查导流 |
| 从零定审美方向、避开通用「AI 味」 | `frontend-design` | 可落地的硬规范与 token 模型 |

> 冲突时本维度（项目约定）优先。

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../framework/react/index.md`](../framework/react/index.md)（组件库用法）· [`../framework/antd/index.md`](../framework/antd/index.md)
- 写 skill 规约：[`../habit/skill-authoring/index.md`](../habit/skill-authoring/index.md)
