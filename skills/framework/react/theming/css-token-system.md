---
name: react-css-token-system
description: CSS 变量 Token 系统 — 单一可信源 ConfigProvider
parent: ./index.md
paths:
  - "frontend/src/styles/**/*.css"
  - "frontend/src/**/*.tsx"
triggers:
  keywords: [CSS variable, --token, ConfigProvider]
effort: medium
context: inline
version: "1.0"
---

# React · CSS Token 系统

## 单一可信源

颜色 / 圆角 / 字号 / 动画时长**只来自一处** — antd `ConfigProvider.theme.token` + `tokens.css`。

```
main.tsx (antdTheme.token)  ←─── 唯一可信源 ───→  tokens.css
                                      ↓
                            所有组件 + GSAP 都从 CSS 变量读
```

## 完整 tokens.css

```css
/* src/styles/tokens.css */
:root {
  /* ===== 品牌色 ===== */
  --accent:        #3b82f6;
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-danger:  #ef4444;
  --color-info:    #3b82f6;

  /* ===== 文字层级 ===== */
  --text-strong:     #0f172a;
  --text-primary:    #334155;
  --text-secondary:  #64748b;
  --text-tertiary:   #94a3b8;
  --text-disabled:   #cbd5e1;

  /* ===== 背景 ===== */
  --bg-base:       #ffffff;
  --bg-container:  #ffffff;
  --bg-layout:     #f8fafc;
  --bg-elevated:   #ffffff;
  --bg-hover:      #f1f5f9;
  --bg-active:     #e2e8f0;

  /* ===== 边框 ===== */
  --border:         #e5e7eb;
  --border-soft:    #f1f5f9;
  --border-strong:  #cbd5e1;

  /* ===== 圆角 ===== */
  --radius-xs:  4px;
  --radius-sm:  6px;
  --radius-md:  8px;
  --radius-lg:  12px;
  --radius-xl:  16px;

  /* ===== 间距（8px 网格） ===== */
  --space-xs:   4px;
  --space-sm:   8px;
  --space-md:   16px;
  --space-lg:   24px;
  --space-xl:   32px;
  --space-2xl:  48px;

  /* ===== 字号 ===== */
  --text-xs:   11px;
  --text-sm:   12px;
  --text-md:   13px;
  --text-lg:   14px;
  --text-xl:   16px;
  --text-2xl:  20px;

  /* ===== 字重 ===== */
  --font-regular:  400;
  --font-medium:   500;
  --font-semibold: 600;
  --font-bold:     700;

  /* ===== 控件高度 ===== */
  --control-height-sm: 30px;
  --control-height:    36px;
  --control-height-lg: 40px;

  /* ===== 动画时长（与 GSAP 一致） ===== */
  --duration-fast:  0.15s;
  --duration-mid:   0.24s;
  --duration-slow:  0.4s;

  /* ===== 字体 ===== */
  --font-sans: -apple-system, BlinkMacSystemFont, "PingFang SC", "Segoe UI", system-ui, sans-serif;
  --font-mono: ui-monospace, "JetBrains Mono", Menlo, monospace;
}
```

## antd 镜像注入

```ts
// src/main.tsx
const cssVar = (n: string) =>
  getComputedStyle(document.documentElement).getPropertyValue(n).trim();

const antdTheme = {
  token: {
    colorPrimary:   cssVar("--accent")        || "#3b82f6",
    colorSuccess:   cssVar("--color-success") || "#10b981",
    colorWarning:   cssVar("--color-warning") || "#f59e0b",
    colorError:     cssVar("--color-danger")  || "#ef4444",
    borderRadius:   8,
    borderRadiusLG: 12,
    borderRadiusSM: 6,
    fontFamily:     cssVar("--font-sans"),
    fontSize:       13,
    motionDurationFast: "0.15s",
    motionDurationMid:  "0.24s",
    motionDurationSlow: "0.4s",
  },
};
```

## GSAP 动画时长 token

```ts
// src/animations/tokens.ts
export const D = {
  micro:  0.15,    // 与 --duration-fast
  base:   0.24,    // 与 --duration-mid
  slow:   0.4,     // 与 --duration-slow
  hero:   0.6,
} as const;
```

## 暗色主题切换（未来）

```css
[data-theme="dark"] {
  --bg-base:    #0f172a;
  --bg-layout:  #1e293b;
  --text-strong: #f8fafc;
  /* ... 仅改变量，组件不变 */
}
```

## 自检

- [ ] tokens.css 是颜色 / 圆角 / 字号的唯一来源？
- [ ] antd theme.token 镜像 tokens.css 值？
- [ ] 组件用 CSS 变量，不硬编码？
- [ ] GSAP 时长与 CSS `--duration-*` 数值一致？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`palette-principles.md`](./palette-principles.md) · [`palette-types.md`](./palette-types.md)
- 配套：[`../../antd/setup/config-provider.md`](../../antd/setup/config-provider.md)

