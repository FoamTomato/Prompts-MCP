---
name: design-color-usage
description: 配色按 60-30-10 分配(主中性/次表面/强调)，强调色仅留给 CTA·链接·激活，hover/active 比基色深 10-15%。Use when 分配各色占比 / 定主色辅色强调色 / 评审配色是否失衡时。
parent: ./index.md
paths:
  - "**/*.tsx"
  - "**/*.vue"
  - "**/*.css"
  - "**/*.scss"
  - "**/*.html"
triggers:
  keywords:
    - 配色比例
    - 60-30-10
    - color usage
    - color palette
    - 强调色
    - accent color
    - 主色辅色
effort: low
version: "1.0"
---

# Color · 60-30-10 配色

> 这里管「各色占多少、用在哪」。具体角色如何 token 化见 design-language；现成配色档案见 reference。

## 60-30-10 比例

| 占比 | 角色 | 用在 |
|------|------|------|
| **60%** | 主导中性色 | 页面背景、大面积留白 |
| **30%** | 次级表面色 | 导航、卡片、分区 |
| **10%** | 强调色 | **仅** CTA、链接、激活态、关键标记 |

强调色一旦超过 ~10% 就会失去「强调」意义，整页变吵。

## 状态色与衍生

- **hover / active 比基色深 10-15%**（或加透明度叠层），保证可点感。
- 语义状态色（成功/警告/错误/信息）自成一组，**不复用品牌强调色**当警告。
- 状态禁纯色编码 —— 配图标或文字（见 [`accessibility.md`](accessibility.md)）。

## 用角色而非裸 hex

页面里写语义角色，不写颜色字面量：

```css
/* ✅ 语义角色 */
color: var(--text-primary);
background: var(--surface);
border: 1px solid var(--border);

/* ❌ 裸 hex 散落，换肤即崩 */
color: #1e293b;
```

角色清单与三层 token 模型见 [`../design-language/tokens-and-theming.md`](../design-language/tokens-and-theming.md)。

## 自检

- [ ] 背景/表面/强调大致落在 60/30/10？
- [ ] 强调色只用于 CTA·链接·激活，没铺满页面？
- [ ] hover/active 比基色深 10-15%？
- [ ] 警告未复用品牌色，状态不靠纯色区分？
- [ ] 用语义角色而非散落裸 hex？

## 相关

- 父：[`./index.md`](./index.md)
- 角色 token 化 + 现成配色档案：[`../design-language/tokens-and-theming.md`](../design-language/tokens-and-theming.md)
- 对比度底线：[`accessibility.md`](accessibility.md)
