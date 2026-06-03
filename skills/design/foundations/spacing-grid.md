---
name: design-spacing-grid
description: 间距用 8pt 主网格(8/16/24/32...)，密集/数据 UI 与微间距才下探 4pt，禁奇数像素。Use when 定 padding/margin/gap / 排版留白 / 评审间距是否成体系时。
parent: ./index.md
paths:
  - "**/*.tsx"
  - "**/*.vue"
  - "**/*.css"
  - "**/*.scss"
  - "**/*.html"
triggers:
  keywords:
    - 间距
    - 8pt 网格
    - spacing grid
    - spacing system
    - 8-point grid
    - padding margin
    - 留白
    - 布局栅格
effort: low
version: "1.0"
---

# Spacing · 8pt 网格

> 所有间距落在一套数列上，界面才「成体系」而非随手定值。

## 主网格：8 的倍数

`8 · 16 · 24 · 32 · 40 · 48 · 56 · 64`

- 组件内 padding、元素间 gap、section 间距一律取这套值。
- 给一组语义命名，避免散落魔数：

```css
:root {
  --space-1: 8px;
  --space-2: 16px;
  --space-3: 24px;
  --space-4: 32px;
  --space-6: 48px;
  --space-8: 64px;
}
```

## 子网格：4pt（克制使用）

仅在两种场景下探到 4 的倍数（4 / 12 / 20）：

- **密集 / 数据型 UI**：表格、紧凑表单、工具栏。
- **微间距**：图标到文字 4px、紧凑标签簇 12px。

非密集场景不要用 4pt，否则节奏变碎。

## 硬禁止

- ❌ 奇数像素（5px / 7px / 13px）—— 在 1.5x 屏渲染出半像素模糊。
- ❌ 同一界面混用多套数列（一会 8 一会 10 一会 15）。
- ❌ 用 margin 硬怼对齐而不走 gap / 网格。

## 留白节奏

| 层级 | 间距档 |
|------|-------|
| 元素内/相邻小元素 | 8 / 16 |
| 卡片内 padding | 16 / 24 / 32 |
| section 之间 | 48 / 64（+，越大越「高级」） |

## 自检

- [ ] 所有间距是 8 的倍数（密集场景才用 4 的倍数）？
- [ ] 没有奇数像素值？
- [ ] 间距走了命名变量而非散落魔数？
- [ ] section 间距明显大于元素间距，留白有层次？

## 相关

- 父：[`./index.md`](./index.md)
- 间距 token 化：[`../design-language/tokens-and-theming.md`](../design-language/tokens-and-theming.md)
- 字阶（与间距同属节奏体系）：[`typography-scale.md`](typography-scale.md)
