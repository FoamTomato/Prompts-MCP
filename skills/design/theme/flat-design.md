---
name: design-theme-flat
description: 扁平化 2.0 风格 — 纯色/双色填充、几何图标、单层 soft shadow 恢复可点感、4-8 圆角、大留白。Use when 做 SaaS·内容站·移动端 / 要简洁高性能 a11y 优先 / 用户指定扁平风时。
parent: ./index.md
paths:
  - "**/*.tsx"
  - "**/*.vue"
  - "**/*.css"
  - "**/*.html"
triggers:
  keywords:
    - 扁平化
    - flat design
    - flat 2.0
    - 扁平风
    - 纯色填充
    - 几何图标
    - 简洁风格
effort: medium
version: "1.0"
---

# Flat Design · 扁平化 2.0

> 「几乎全平」：2D 纯色为底，仅加恰到好处的浅阴影/渐变恢复可点感。务实的现代默认观感。

## 本质

干净 2D + 鲜明色块，去掉拟物纹理；用**单层浅阴影**而非多层立体感来表达层级与可点。

## 何时用 / 不用

| 适合 | 不适合 |
|------|--------|
| SaaS、内容站、移动端 | 需要触感/奢华的拟物realism（用 clay/skeuo） |
| 性能与无障碍优先的产品 | 追求最大差异化（用 brutalism） |

## 关键 CSS 线索

```css
.flat-card {
  background: var(--surface);          /* 纯色填充 */
  border-radius: 8px;                  /* 4-8，克制 */
  box-shadow: 0 2px 8px rgba(0,0,0,.08);   /* 单层 soft，无内/双阴影 */
}
.flat-btn {
  background: var(--interactive);      /* 纯色，或 2-stop 渐变强调 */
  border-radius: 6px;
  transition: background .15s ease;
}
.flat-btn:hover { background: var(--interactive-hover); }   /* 仅变色 */
```

## 要点

- 填充用纯色或双色；强调可用**两色线性渐变**，不堆多色。
- 阴影**只一层、浅**（`0 1px 3px rgba(0,0,0,.12)` 或 `0 2px 8px rgba(0,0,0,.08)`）；禁内阴影/双阴影。
- 圆角克制 4-8px；图标用几何线性图标，不用拟物图标。
- 大留白 + 鲜明色块构成层级，hover 仅变色/透明度。

## 自检

- [ ] 纯色/双色填充，无拟物纹理？
- [ ] 阴影只有单层且浅，没堆内/双阴影？
- [ ] 圆角 4-8、图标几何线性？
- [ ] 配色仍过 60-30-10 与对比度底线？

## 相关

- 父：[`./index.md`](./index.md)
- 按钮层级：[`../component-patterns/button-hierarchy.md`](../component-patterns/button-hierarchy.md)
- 通用底线：[`../foundations/index.md`](../foundations/index.md)
