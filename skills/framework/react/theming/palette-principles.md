---
name: react-palette-principles
description: 色板原则 60-30-10 / WCAG AA 对比度 / 饱和度克制。Use when 写 React 组件 / 改 .tsx 文件 /
  评审涉及 `palette-principles` 的 PR。
parent: ./index.md
paths:
- frontend/src/styles/**/*.css
- frontend/src/**/*.tsx
triggers:
  keywords:
  - palette
  - color
  - 对比度
  - WCAG
effort: medium
context: inline
version: '1.0'
---
# React · 色板原则

## 三大原则

| 原则 | 规则 |
|------|------|
| **60-30-10 法则** | 主背景 60% / 内容区 30% / 强调色 10% |
| **对比度合规（WCAG AA）** | 正文与背景 ≥ 4.5:1，大字 ≥ 3:1 |
| **饱和度克制** | UI 中避免饱和度 > 80% 的高纯色大面积铺色 |
| **语义色独立** | success/warning/danger/info 不与品牌色混用 |
| **层级 ≤ 3** | 最多 3 个有色彩倾向的层级，其余用中性色 |

## 示例主色

```css
:root {
  --accent:        #3b82f6;    /* 蓝（colorPrimary） */
  --color-success: #10b981;    /* 绿 */
  --color-warning: #f59e0b;    /* 琥珀 */
  --color-danger:  #ef4444;    /* 红 */
  --color-info:    #3b82f6;    /* info 与 primary 同源 */
}
```

## 中性色阶

```css
/* 灰阶（slate） */
--neutral-50:  #f8fafc;
--neutral-100: #f1f5f9;
--neutral-200: #e2e8f0;
--neutral-300: #cbd5e1;
--neutral-400: #94a3b8;
--neutral-500: #64748b;
--neutral-700: #334155;
--neutral-900: #0f172a;
```

## 对比度检查

```bash
# Lighthouse / aXe DevTools 自动检测
# 或在线工具：webaim.org/resources/contrastchecker/
```

| 文字层级 | 颜色 | 背景 #ffffff 对比度 |
|--------|-----|------------------|
| 标题 | `--neutral-900` (#0f172a) | 17.4 ✓ |
| 正文 | `--neutral-700` (#334155) | 10.5 ✓ |
| 辅助 | `--neutral-500` (#64748b) | 5.4 ✓（恰过 AA） |
| 占位 | `--neutral-400` (#94a3b8) | 3.3 ⚠（仅大字可用） |

## 60-30-10 实例（主页 HomePage）

| 比例 | 用途 | 颜色 |
|------|------|------|
| 60% | 页面背景 | `--neutral-50` (#f8fafc) |
| 30% | 卡片 / 内容区 | `#ffffff` |
| 10% | 主 CTA / 选中态 | `--accent` (#3b82f6) |

## 反例

```css
/* ❌ 4 个品牌色平铺 */
.tag-math    { background: red; }
.tag-chinese { background: green; }
.tag-english { background: orange; }
.tag-physics { background: purple; }

/* ✅ 用中性灰底 + 分类色边框 / 字 */
.tag {
  background: var(--neutral-100);
  border-left: 3px solid var(--category-color);
}
```

## 自检

- [ ] 60-30-10 比例符合？
- [ ] 正文对比度 ≥ 4.5:1？
- [ ] 无大面积饱和高纯色？
- [ ] 语义色与品牌色独立？

## 相关

- 父：[`./index.md`](./index.md)
- 配色比例与角色权威（框架无关 60-30-10 / 语义角色）：[`../../../design/foundations/color-usage.md`](../../../design/foundations/color-usage.md)
- 兄弟：[`palette-types.md`](./palette-types.md) · [`css-token-system.md`](./css-token-system.md)
