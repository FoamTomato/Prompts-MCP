---
name: design-tokens-and-theming
description: 三层 token 模型(primitive/semantic/component) + 组件只消费语义 token + 覆盖 5-8 个核心变量换肤 + light-dark 策略。Use when 搭 CSS 变量体系 / 做主题换肤 / 配深色模式 / 评审 token 分层时。
parent: ./index.md
paths:
  - "**/*.css"
  - "**/*.scss"
  - "**/*.tsx"
  - "**/*.vue"
  - "**/tokens*.*"
triggers:
  keywords:
    - 设计 token 分层
    - token 三层模型
    - 语义 token
    - semantic token
    - 换肤
    - theming
    - CSS 变量
    - 深色模式
    - 暗色模式
    - dark mode
    - light-dark
effort: medium
version: "1.0"
---

# Tokens & Theming · 三层 token 与换肤

> 颜色/间距/字号不直接写进组件，而是经三层 token 引用 —— 改一层映射即整体换肤。

## 三层模型

| 层 | 是什么 | 例子 |
|----|--------|------|
| **primitive / reference** | 原始值（裸 hex/数值） | `--color-blue-600: #0052CC` |
| **semantic / system** | 角色别名（指向 primitive） | `--color-interactive: var(--color-blue-600)` |
| **component** | 组件局部（指向 semantic） | `--button-bg: var(--color-interactive)` |

**铁律：组件只消费 semantic / component token，绝不写裸 hex。** 这样改 semantic 映射就能整体换肤。

## 语义角色清单

`surface` / `surface-elevated` / `text-primary` / `text-secondary` / `interactive`(+`-hover`/`-active`，深 10-15%) / `success` / `warning` / `error` / `info` / `border`。

每个填充角色配一个 `on-` 内容色（`primary`/`on-primary`、`surface`/`on-surface`），保证文字始终达对比度。

## 换肤：只覆盖核心 semantic 变量

```css
:root {
  --color-blue-600: #0052CC;                  /* primitive */
  --color-interactive: var(--color-blue-600); /* semantic */
  --button-bg: var(--color-interactive);      /* component */
}
[data-theme="luxury"] { --color-interactive: #6E1423; }   /* 换品牌只改 1 个语义变量 */
```

一次换肤应只重定义 **~5-8 个核心 semantic 变量**（核心色 5-7、间距档 1-7、字号档 3-4）。组件用 fallback 链兜底：`background: var(--button-bg, var(--color-surface));`。

## Light / Dark

| 方式 | 适用 |
|------|------|
| `@media (prefers-color-scheme)` | 零 JS 自动 |
| `[data-theme]` + localStorage | 手动切换 |
| `light-dark(光, 暗)` + `color-scheme: light dark` | 现代浏览器，免媒体查询 |

生产建议「自动检测 + 手动覆盖」组合。

## 自检

- [ ] 三层分明，组件只引用 semantic/component，无裸 hex？
- [ ] 填充角色都有配对的 `on-` 内容色？
- [ ] 换肤只需覆盖 5-8 个核心变量？
- [ ] 深色模式用 prefers + data-theme 组合，非手翻所有颜色？

## 详细参考

- 完整变量表 + Style Dictionary / W3C DTCG 互换格式：[`tokens-and-theming.reference.md`](tokens-and-theming.reference.md)

## 相关

> 本条是**框架无关的三层模型权威入口**；具体栈的落地见下方两条。

- 父：[`./index.md`](./index.md)
- 配色比例：[`../foundations/color-usage.md`](../foundations/color-usage.md)
- 一套完整设计语言怎么定：[`design-language.md`](design-language.md)
- antd 落地（ConfigProvider token）：[`../../lang/typescript/style/design-tokens.md`](../../lang/typescript/style/design-tokens.md)
- React 落地（tokens.css 单一可信源 ↔ antd ↔ GSAP 镜像）：[`../../framework/react/theming/css-token-system.md`](../../framework/react/theming/css-token-system.md)
