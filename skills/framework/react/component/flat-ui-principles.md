---
name: react-flat-ui-principles
description: 扁平化设计形态 — 无阴影/边框层次/纯色/状态完备
parent: ./index.md
paths:
  - "frontend/src/**/*.tsx"
  - "frontend/src/**/*.css"
triggers:
  keywords: [扁平化, flat, 无阴影, border]
effort: medium
context: inline
version: "1.0"
---

# React · 扁平化 UI 形态

## 七大原则

| 原则 | 规则 |
|------|------|
| **无阴影** | 默认 `box-shadow: none`，用 border 代替层次 |
| **纯色填充** | background 用 solid，禁止 `linear-gradient` 作主背景（CTA 按钮例外） |
| **边框定义层次** | `1px solid var(--border)` 区分区域 |
| **字重建立层级** | 标题 `600-700`，正文 `400-500`，辅助 `400` |
| **留白即设计** | padding/gap 宽松，宁可空也不挤 |
| **状态必须完备** | 默认 / 悬停 / 焦点 / 激活 / 加载 / 禁用 / 错误 / 空态 |
| **动效克制** | 过渡 150~250ms，禁止超 400ms |

## 范例

```css
.textbook-card {
  background: var(--bg-container);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  transition: border-color 0.15s, transform 0.15s;
  box-shadow: none;            /* 无阴影 */
}

.textbook-card:hover {
  border-color: var(--border-strong);
  transform: translateY(-2px);   /* 用位移代替阴影 */
}

.textbook-card.is-selected {
  border-color: var(--accent);
  background: var(--accent-50);
}
```

## 与 antd 边界

| 通用 primitive | 自研 |
|--------------|------|
| Form / Modal / Table / DatePicker / Select | 课件卡 / 试卷卡 / 三级联动 / 编辑器画布 |
| message / notification / Tooltip | 主页 Hero / 控制台 CTA |

通用走 antd，业务差异化大的自研。详见 [`../../antd/boundary/when-antd-vs-custom.md`](../../antd/boundary/when-antd-vs-custom.md)。

## 反例

```css
/* ❌ 默认阴影 */
.card { box-shadow: 0 4px 12px rgba(0,0,0,0.1); }

/* ❌ 主背景渐变 */
.page { background: linear-gradient(...); }

/* ❌ 字号靠尺寸不靠字重 */
.section-title { font-size: 32px; font-weight: 400; }

/* ❌ 过渡超 400ms */
.card { transition: all 0.6s; }
```

## 自检

- [ ] 默认无阴影？
- [ ] 主背景纯色？
- [ ] 字重建立层级？
- [ ] 8 种状态都设计了？
- [ ] 过渡 ≤ 250ms？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`state-completeness.md`](./state-completeness.md) · [`spacing-typography.md`](./spacing-typography.md)

