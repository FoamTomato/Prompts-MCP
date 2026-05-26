---
name: react-spacing-typography
description: 间距与字号 — 留白即设计 / 字重建立层级。Use when 写 React 组件 / 改 .tsx 文件 / 评审涉及 `spacing-typography`
  的 PR。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.css
triggers:
  keywords:
  - 间距
  - 字号
  - typography
  - spacing
effort: medium
context: inline
version: '1.0'
---
# React · 间距与字号

## 间距系统（8px 网格）

```css
--space-xs:  4px;
--space-sm:  8px;
--space-md:  16px;
--space-lg:  24px;
--space-xl:  32px;
--space-2xl: 48px;
```

## 字号系统

| Var | 值 | 用途 |
|-----|----|----|
| `--text-xs` | 11px | 元信息、标签 |
| `--text-sm` | 12px | 辅助文字、placeholder |
| `--text-md` | 13px | body 默认（与 antd fontSize 一致） |
| `--text-lg` | 14px | 强调文字、表单 label |
| `--text-xl` | 16px | 小标题 |
| `--text-2xl` | 20px | 卡片标题 |
| `--text-3xl` | 28px | 区块标题 |
| `--text-4xl` | 34px | 页面 Hero |

## 字重

```css
--font-light:    400;
--font-medium:   500;
--font-semibold: 600;
--font-bold:     700;
```

## 行高

```css
--lh-tight: 1.2;     /* 大标题 */
--lh-base:  1.5;     /* 正文 */
--lh-loose: 1.7;     /* 长篇阅读 */
```

## 应用：卡片标准

```css
.textbook-card {
  padding: var(--space-md);              /* 16 */
  gap: var(--space-sm);                  /* 8 */
}

.textbook-card__title {
  font-size: var(--text-lg);             /* 14 */
  font-weight: var(--font-semibold);     /* 600 */
  line-height: var(--lh-tight);          /* 1.2 */
  color: var(--text-strong);
}

.textbook-card__subtitle {
  font-size: var(--text-sm);             /* 12 */
  color: var(--text-tertiary);
}
```

## 留白原则

| 区域 | 边距 |
|------|------|
| 页面容器到内容 | `padding: var(--space-xl)` |
| Section 之间 | `gap: var(--space-2xl)` |
| 卡片间 | `gap: var(--space-md)` |
| 表单 Item 间 | `gap: var(--space-lg)` |
| 行内元素 | `gap: var(--space-sm)` |

## 反例

```css
/* ❌ 魔法数字 */
.card { padding: 13px 17px; }

/* ❌ 字号靠尺寸不靠字重 */
.title { font-size: 28px; font-weight: 400; }

/* ❌ 留白太挤 */
.section { padding: 4px 8px; gap: 2px; }
```

## 自检

- [ ] 间距 / 字号 / 字重用 CSS 变量？
- [ ] 8px 倍数网格？
- [ ] 标题用字重而非超大字号建立层级？
- [ ] 区块间留白足够（≥ 24px）？

## 相关

- 父：[`./index.md`](./index.md)
- 配套：[`flat-ui-principles.md`](./flat-ui-principles.md) · [`../theming/css-token-system.md`](../theming/css-token-system.md)

