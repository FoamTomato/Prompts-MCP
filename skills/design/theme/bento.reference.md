# Bento · 详细参考

主入口：[`bento.md`](bento.md)。本文是按需取用的完整 token、栅格变体与卡片组件，不重复主入口的规则。

## 1. Token 速查

```css
:root {
  /* 圆角 */
  --bento-radius: 20px;          /* 卡片默认 */
  --bento-radius-sm: 12px;       /* 小卡 / 内嵌块 */

  /* 间距（统一 gap 是 bento 的灵魂） */
  --bento-gap: 24px;             /* 桌面 */
  --bento-gap-sm: 16px;          /* 紧凑 / 移动 */
  --bento-pad: 24px;             /* 卡片内 padding */

  /* 描边与表面 */
  --bento-border: 1px solid var(--border);
  --bento-surface: var(--surface);
  --bento-surface-elevated: var(--surface-elevated);

  /* hover 阴影 */
  --bento-shadow-hover: 0 12px 32px rgba(0, 0, 0, .08);
}
```

> 颜色一律走语义角色（`--surface` / `--border` 等），不要在 bento 里写裸 hex。角色定义见 design-language/tokens-and-theming。

## 2. 栅格变体

### 4 列基础网格

```css
.bento {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(160px, auto);
  gap: var(--bento-gap);
}
```

### 跨度类

```css
.bento__item--wide   { grid-column: span 2; }   /* 半宽 */
.bento__item--wide-3 { grid-column: span 3; }    /* 3/4 宽 */
.bento__item--full   { grid-column: 1 / -1; }     /* 整行 */
.bento__item--tall   { grid-row: span 2; }        /* 双倍高 */
.bento__item--hero   { grid-column: span 2; grid-row: span 2; }  /* 焦点大块 */
```

### 自适应网格（少写 media query）

```css
.bento--auto {
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
}
```

### 响应式降列

```css
@media (max-width: 1024px) {
  .bento { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 768px) {
  .bento { grid-template-columns: 1fr; gap: var(--bento-gap-sm); }
  .bento__item--wide,
  .bento__item--wide-3,
  .bento__item--hero { grid-column: 1 / -1; }   /* 全部铺满单列 */
}
```

## 3. 卡片组件

```css
.bento__card {
  background: var(--bento-surface);
  border: var(--bento-border);
  border-radius: var(--bento-radius);
  padding: var(--bento-pad);
  overflow: hidden;
  transition: transform .2s ease, box-shadow .2s ease;
}
.bento__card:hover {
  transform: translateY(-2px);
  box-shadow: var(--bento-shadow-hover);
}

/* 强调卡（焦点 / CTA 类） */
.bento__card--accent {
  background: var(--surface-elevated);
  border-color: var(--accent-border);
}

/* 卡内结构 */
.bento__card-eyebrow { font-size: 12px; letter-spacing: .04em; color: var(--text-secondary); }
.bento__card-title   { font-size: 20px; font-weight: 600; color: var(--text-primary); }
.bento__card-body    { font-size: 14px; line-height: 1.5; color: var(--text-secondary); }
```

## 4. 入场动效（配合 reduced-motion）

```css
.bento__card {
  opacity: 0;
  animation: bento-enter .5s cubic-bezier(.22, 1, .36, 1) forwards;
  animation-delay: calc(var(--i, 0) * .05s);   /* stagger */
}
@keyframes bento-enter {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
@media (prefers-reduced-motion: reduce) {
  .bento__card { animation: none; opacity: 1; }
}
```

## 5. 常见错误

- gap 忽大忽小 → 破坏「规整」感，统一成一个值。
- 给每张卡都加默认阴影 → 显脏；阴影只在 hover。
- 把数据表格塞进卡片 → 用真 `<table>`。
- hover 改 `width`/`padding` → 触发重排，只改 `transform`/`box-shadow`。
