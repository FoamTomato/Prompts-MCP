---
name: design-theme-other-styles
description: 冷门视觉风格一行速查 — glassmorphism / neumorphism / neo-brutalism / minimalism / claymorphism 的本质、何时用、一条 CSS 线索。Use when 用户指定上述风格 / 快速判断某风格适不适合 / 需要导向风格大全时。
parent: ./index.md
paths:
  - "**/*.tsx"
  - "**/*.vue"
  - "**/*.css"
  - "**/*.html"
triggers:
  keywords:
    - 玻璃拟态
    - glassmorphism
    - 新拟物
    - neumorphism
    - 粗野主义
    - brutalism
    - 极简
    - minimalism
    - 黏土
    - claymorphism
effort: low
version: "1.0"
---

# Other Styles · 冷门风格速查

> 三套主力风格之外的常见选项。每条给本质 + 何时用/不用 + 一条 CSS 线索；要深入或浏览更多风格转外部 `ui-ux-pro-max`。

## Glassmorphism · 玻璃拟态

- 本质：彩色背景上的磨砂半透明面板。
- 用：hero / 浮层焦点；**仅单个焦点层，勿层层叠**（GPU 负担 + 对比度风险）。
- CSS：`background: rgba(255,255,255,.15); backdrop-filter: blur(10px);`（带 `-webkit-`）+ `border: 1px solid rgba(255,255,255,.3)`。

## Neumorphism · 新拟物

- 本质：同色表面挤压出的「软 UI」，双向阴影。
- ⚠️ **慎用** —— 同色低对比，常不达 WCAG，仅小范围装饰。
- CSS：`box-shadow: 8px 8px 16px #b8bec7, -8px -8px 16px #fff;`（按下用双 inset）。

## Neo-Brutalism · 新粗野

- 本质：反精致、块面、高对比；粗黑边 + 硬偏移阴影。
- 用：个性/创意/活动页；**不用于信任/奢侈/政务**。
- CSS：`border: 3px solid #000; box-shadow: 4px 4px 0 #000;`（零模糊），2-3 饱和色，避免黄底青字这类低对比。

## Minimalism / Swiss · 极简

- 本质：靠留白 + 排版传达层级，1-2 中性色 + 1 强调，少边框少阴影。
- 用：内容优先、长青默认，可与 bento / flat 叠加；**不用于密集数据应用**。
- CSS：大量 `margin`/`gap` + 8pt 网格 + 克制的 `box-shadow`。

## Claymorphism · 黏土

- 本质：胖嘟嘟 3D 黏土，大圆角 + 外阴影 + 内高光。
- 用：儿童/教育/趣味；可放对比背景上（不像 neumorphism 限同色）。
- CSS：`border-radius: 32px; box-shadow: 0 12px 24px rgba(0,0,0,.15), inset 0 -6px 10px rgba(0,0,0,.1), inset 0 6px 10px rgba(255,255,255,.6);`

## 自检

- [ ] 选定风格仍过对比度/触控/间距底线（neumorphism 尤其留意对比度）？
- [ ] 一个项目只用一套主风格，没混搭？
- [ ] 需要更多风格/配色/字体大全时转了 `ui-ux-pro-max`？

## 相关

- 父：[`./index.md`](./index.md)
- 选风格决策：[`theme-selection.md`](theme-selection.md)
- 通用底线：[`../foundations/index.md`](../foundations/index.md)
