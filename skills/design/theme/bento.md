---
name: design-theme-bento
description: Bento 便当格风格 — 模块化卡片网格、varied span、统一 gap、圆角 16-20、hairline 边框 + soft hover。Use when 默认风格 / 做仪表盘·产品展示·作品集 / 排混合重要度首页时。
parent: ./index.md
paths:
  - "**/*.tsx"
  - "**/*.vue"
  - "**/*.css"
  - "**/*.html"
triggers:
  keywords:
    - bento
    - 便当格
    - bento grid
    - 卡片网格
    - 模块化网格
    - Apple 风
    - dashboard 风格
effort: medium
version: "1.0"
---

# Bento · 便当格（默认风格）

> 本仓**默认风格**。大小不一的模块卡片拼成「乱中有序」的整体（Apple 发布会观感）。
> 完整 token / 卡片组件 / 栅格变体见 [`bento.reference.md`](bento.reference.md)。

## 本质

模块化、分区化的卡片网格：每张卡是一个独立信息块，跨度不同但 gap 统一，整体规整。

## 何时用 / 不用

| 适合 | 不适合 |
|------|--------|
| 仪表盘、产品功能展示、作品集、混合重要度首页 | 长文阅读（要线性流） |
| 一屏内并列多个不同权重的信息块 | 顺序步骤（网格弱化先后） |
| | 密集数据（用真表格，别塞卡片） |

## 关键 CSS 线索

```css
.bento {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;                 /* 统一 gap，不要忽大忽小 */
}
.bento__item--wide { grid-column: span 2; }
.bento__item--tall { grid-row: span 2; }
.bento__item--full { grid-column: 1 / -1; }

.bento__card {
  border-radius: 20px;       /* 16-24，Apple 偏 16-20 */
  border: 1px solid var(--border);   /* hairline */
  background: var(--surface);
  transition: transform .2s, box-shadow .2s;  /* 只动 transform/opacity */
}
.bento__card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(0,0,0,.08);    /* soft hover */
}
```

## 要点

- **gap 全程统一**（16 或 24），靠卡片跨度而非间距制造节奏。
- 圆角 16-24px；边框 hairline；默认无阴影，hover 才浮起。
- 响应式：`≤1024px` 降 2 列、`≤768px` 降 1 列（见 [`../foundations/responsive-breakpoints.md`](../foundations/responsive-breakpoints.md)）。
- hover 只动 `transform`/`box-shadow`，别动布局属性（防重排）。

## 自检

- [ ] 用 grid + span 控制卡片大小，gap 统一？
- [ ] 圆角 16-24、hairline 边框、默认无阴影 hover 才浮起？
- [ ] 没把密集表格/长文硬塞进 bento？
- [ ] 降列断点正确，hover 不触发重排？

## 详细参考

- 完整 token / 卡片组件 / 栅格变体：[`bento.reference.md`](bento.reference.md)

## 相关

- 父：[`./index.md`](./index.md)
- 卡片通用约定：[`../component-patterns/card-and-surface.md`](../component-patterns/card-and-surface.md)
- 通用底线：[`../foundations/index.md`](../foundations/index.md)
