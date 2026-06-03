---
name: typescript-design-tokens
description: CSS 变量 / Token 系统 — 颜色单一可信源 ConfigProvider。Use when 写 React 组件 / 改 .tsx
  文件 / 评审涉及 `design-tokens` 的 PR。
parent: ./index.md
paths:
- frontend/src/styles/**/*.css
- frontend/src/**/*.tsx
triggers:
  keywords:
  - design token
  - CSS 变量
  - ConfigProvider
effort: medium
context: inline
version: '1.0'
---
# TypeScript · Design Tokens

## 规则

颜色 / 圆角 / 字体 / 动画时长**只能从单一来源消费**——通过 antd `ConfigProvider.theme.token` 注入 CSS 变量，所有组件读 CSS 变量。

## Token 来源（唯一可信源）

```ts
// src/main.tsx
const antdTheme = {
  token: {
    colorPrimary:    "#3b82f6",
    colorSuccess:    "#10b981",
    colorWarning:    "#f59e0b",
    colorError:      "#ef4444",
    borderRadius:    8,
    borderRadiusLG:  12,
    fontFamily:      '-apple-system, "PingFang SC", system-ui, sans-serif',
    fontSize:        13,
    motionDurationFast: "0.15s",
    motionDurationMid:  "0.24s",
    motionDurationSlow: "0.4s",
  },
};

<ConfigProvider theme={antdTheme} locale={zhCN}>
  <App />
</ConfigProvider>
```

## CSS 变量层（覆盖 antd 没暴露的）

```css
/* src/styles/tokens.css */
:root {
  /* 文字层级 */
  --text-strong:    #0f172a;
  --text-primary:   #334155;
  --text-secondary: #64748b;
  --text-tertiary:  #94a3b8;
  --text-disabled:  #cbd5e1;

  /* 背景 */
  --bg-page:        #f8fafc;
  --bg-container:   #ffffff;
  --bg-hover:       #f1f5f9;
  --bg-active:      #e2e8f0;

  /* 边框 */
  --border:         #e5e7eb;
  --border-strong:  #cbd5e1;

  /* 间距 */
  --space-xs:  4px;
  --space-sm:  8px;
  --space-md:  16px;
  --space-lg:  24px;
  --space-xl:  32px;

  /* 圆角（与 antd 一致） */
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
}
```

## 组件内使用

```tsx
// ✅ CSS 变量
<div style={{ color: "var(--text-primary)", padding: "var(--space-md)" }}>

// ✅ Module CSS
.card {
  background: var(--bg-container);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
}

// ❌ 硬编码颜色 — 改主题时漏改
<div style={{ color: "#334155" }}>

// ❌ 在多处定义同一个值
const PRIMARY = "#3b82f6";   // 应来自 token
```

## 与 GSAP 动画 token 协同

```ts
// src/animations/tokens.ts — 动画时长
export const D = {
  micro:  0.15,
  base:   0.24,
  slow:   0.4,
  hero:   0.6,
} as const;

export const E = {
  out:    "power2.out",
  inOut:  "power2.inOut",
  bounce: "back.out(1.7)",
} as const;
```

与 antd 的 `motionDurationFast/Mid/Slow` 数值对齐。

## 自检

- [ ] 没在组件里硬编码颜色值？
- [ ] 所有颜色来自 antd token 或 `tokens.css` 变量？
- [ ] 动画时长用 `D` 常量，不写魔法数字？
- [ ] 改主题色只需改 `main.tsx` + `tokens.css`？

## 相关

- 父：[`./index.md`](./index.md)
- 模型权威（框架无关三层 token / 换肤 / light-dark）：[`../../../design/design-language/tokens-and-theming.md`](../../../design/design-language/tokens-and-theming.md)
- 配套：[`../../../framework/antd/setup/config-provider.md`](../../../framework/antd/setup/config-provider.md) · [`../../../framework/react/theming/css-token-system.md`](../../../framework/react/theming/css-token-system.md)

