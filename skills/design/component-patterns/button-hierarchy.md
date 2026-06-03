---
name: design-button-hierarchy
description: 按钮四类层级 — 主(深)/CTA(品牌渐变)/描边次级/幽灵，各定 default·hover·active·focus·disabled 五态。Use when 写按钮组件 / 定一屏多按钮的主次 / 评审按钮交互态时。
parent: ./index.md
paths:
  - "**/*.tsx"
  - "**/*.vue"
  - "**/*.css"
  - "**/*.html"
triggers:
  keywords:
    - 按钮层级
    - button hierarchy
    - 主按钮
    - primary button
    - CTA
    - 幽灵按钮
    - 按钮状态
effort: low
version: "1.0"
---

# Button · 层级与五态

> 一屏里按钮的「视觉重量」要分级，且每类都定齐五个状态。

## 四类层级

| 类 | 用途 | 视觉 |
|----|------|------|
| **主按钮** | 页面级主操作（保存/提交） | 深色实底（如 `#1C1917`） |
| **CTA** | 关键转化（生成/升级/开始） | 品牌渐变或强调实底，**一屏至多 1 个** |
| **描边次级** | 次要操作（编辑/管理/详情） | 白底 + 品牌色描边 |
| **幽灵** | 中性轻操作（取消/更多） | 白底 + 中性细边 |

一屏只有一个最高优先级按钮；其余降级，避免「全是重按钮」。

## 五态（每类都要定）

| 态 | 要求 |
|----|------|
| default | 基础样式 |
| hover | 背景/边框比基色深 10-15%，或加 soft shadow |
| active | 再深一档 / 轻微下压 |
| focus | `:focus-visible` 可见焦点环，与相邻 ≥3:1 |
| disabled | 降透明/灰化 + `cursor:not-allowed`（免对比度要求） |

```css
.btn { border-radius:8px; height:34px; font-weight:600; transition:background .15s, box-shadow .15s; }
.btn:focus-visible { outline:2px solid var(--interactive); outline-offset:2px; }
.btn:disabled { opacity:.5; cursor:not-allowed; }

.btn--primary { background:var(--text-primary); color:#fff; }
.btn--cta     { background:var(--interactive); color:var(--on-interactive); }
.btn--cta:hover { background:var(--interactive-hover); box-shadow:0 4px 14px rgba(0,0,0,.18); }
.btn--outline { background:transparent; border:1px solid var(--interactive); color:var(--interactive); }
.btn--ghost   { background:transparent; border:1px solid var(--border); color:var(--text-secondary); }
```

## 自检

- [ ] 四类层级区分清楚，一屏只有一个最高优先级按钮？
- [ ] CTA 一屏至多一个？
- [ ] 五态都定了，focus 用 `:focus-visible` 且达 3:1？
- [ ] disabled 有 `not-allowed` 光标、不参与对比度要求？
- [ ] 颜色走语义 token 而非裸 hex？

## 相关

- 父：[`./index.md`](./index.md)
- 焦点与对比度底线：[`../foundations/accessibility.md`](../foundations/accessibility.md)
- 状态色 token：[`../design-language/tokens-and-theming.md`](../design-language/tokens-and-theming.md)
