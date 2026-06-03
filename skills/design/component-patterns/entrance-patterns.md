---
name: design-entrance-patterns
description: 每类组件入场速查 — 弹窗/抽屉/下拉/手风琴/列表/tab/卡片/页面各配哪种入场与 transform-origin。Use when 给组件加出现动画 / 纠结弹窗抽屉怎么进场 / 定 dropdown origin / 列表用不用 stagger 时。
parent: ./index.md
paths:
  - "**/*.tsx"
  - "**/*.vue"
  - "**/*.css"
triggers:
  keywords:
    - 组件入场方式
    - 加载动效
    - entrance pattern
    - 弹窗动画
    - modal transition
    - dropdown 展开
    - stagger 列表
    - transform-origin
    - drawer 进场
    - 手风琴展开
    - 页面转场
effort: low
version: "1.0"
---
# Motion · 组件入场速查

> **决策点：某组件「出现」时配哪种入场。** 默认：**fade 打底 + 位移 y/x ≤20px 或 scale .96→1，列表才 stagger，强制 reduced-motion 兜底**。
> 时长/曲线档位见权威：[`motion-and-animation.md`](./motion-and-animation.md)；GSAP 实现中用 `D.micro/.base/.slow` 对应（值见 [`../../framework/gsap/principles.md`](../../framework/gsap/principles.md)）。本条只回答「每类组件配哪种」。

## 每组件默认入场

| 组件 | 推荐入场 | 时长 | transform-origin | 说明 |
|------|---------|------|------------------|------|
| **Modal / Dialog** | fade + `scale .96→1` | .25s | center | 遮罩同步 fade；关闭走反向，不能只 fade |
| **Drawer / 抽屉** | 离屏 slide + fade | .25s | 对应边（右抽屉 right） | 只动 `x`/`y`，不动 `left`/`right` |
| **Toast / 通知** | slide-in + fade | .15s | 入场角（顶/右） | 多条用 stagger .05 |
| **Dropdown / Popover / Menu** | fade + `scale .96→1` | .15s | **trigger 方位**（下方菜单=top） | origin 错=从中心炸开 |
| **Tooltip** | fade + 2px 位移 | .15s | 指向边 | 不加 scale 弹跳 |
| **Accordion / Collapse** | 高度 `0→auto` + 内容 fade | .25s | — | 用真实像素高度，不切 `display` |
| **Tab panel** | fade + 8px x 位移 | .15s | — | 切换轻快，不做大转场 |
| **List / Grid 批量** | `y20 + fade`，逐项 stagger | .4s | — | stagger .04–.08/项；首屏触发，翻页不重放 |
| **Card 单卡入场** | `y20 + fade` 或 `scale .96→1` | .4s | center | 进视口触发用 ScrollTrigger |
| **Skeleton → 内容** | 占位 fade-out 叠真数据 fade-in | .25s | — | crossfade，不硬切 |
| **Page / 路由切换** | 主区 `fade + y12` | .25s | — | 只动主内容，导航/壳不参与 |

## 三条关键细节

1. **Dropdown/Popover/Tooltip 的 origin 必须对齐 trigger 方位**：按钮下方菜单 origin 设 `top center`，否则从中心放大，视觉错位。
2. **Accordion 不切 `display`/直接跳高度**：用真实像素高度做过渡（GSAP `height:"auto"` 或 CSS `grid-template-rows: 0fr→1fr`）。
3. **列表 stagger 只在首屏触发**：翻页、筛选后不重放，否则每次操作都像页面重置。

## reduced-motion 降级（强制）

scale/slide 退化为最短时长 fade，stagger 退化为同时出现。CSS 与 JS 兜底写法见 [`motion-and-animation.md`](./motion-and-animation.md) 与 [`../foundations/accessibility.md`](../foundations/accessibility.md)。

## 自检

- [ ] 入场只动 `transform`/`opacity`，没动 `width`/`height`/`left`/`top`（accordion 高度除外，且用真实高度）？
- [ ] 时长取自权威档（.15/.25/.4s），没散落随手值？
- [ ] Dropdown/Popover/Tooltip 的 transform-origin 对齐了 trigger 方位？
- [ ] 列表 stagger 只在首屏，翻页/筛选没重放？
- [ ] 每条入场都有 reduced-motion 降级（退化为最短时长 fade）？

## 相关

- 父：[`./index.md`](./index.md)
- 时长/曲线/stagger 档位 + reduced-motion 底线（权威）：[`motion-and-animation.md`](./motion-and-animation.md)
- GSAP token 值（D.micro/.base/.slow 对应值）：[`../../framework/gsap/principles.md`](../../framework/gsap/principles.md)
- 用 GSAP 落地：[`../../framework/gsap/index.md`](../../framework/gsap/index.md)
- 加载占位本身（Skeleton 怎么搭）：[`../../framework/react/feedback/skeleton-loading.md`](../../framework/react/feedback/skeleton-loading.md)
