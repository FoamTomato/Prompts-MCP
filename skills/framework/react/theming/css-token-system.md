---
name: react-css-token-system
description: React CSS 变量 Token 单一可信源 — tokens.css ↔ antd theme.token ↔ GSAP duration 三者镜像。Use when 配置 antd theme / 新增颜色或圆角 / 接入暗色模式 / 评审硬编码颜色 PR。
parent: ./index.md
paths:
  - "frontend/src/styles/**/*.css"
  - "frontend/src/**/*.tsx"
  - "frontend/src/main.tsx"
triggers:
  keywords:
    - CSS variable
    - CSS 变量
    - design token
    - 设计 token
    - tokens.css
    - ConfigProvider
    - antd theme
    - 单一可信源
    - single source of truth
effort: medium
version: "1.0"
---

# React · CSS Token 系统

## 单一可信源原则

颜色 / 圆角 / 字号 / 字重 / 间距 / 动画时长 **只来自一处**：项目根的 `tokens.css`。所有消费方都**镜像**它，不重新定义：

```
tokens.css  (唯一定义点)
    │
    ├──→ antd ConfigProvider.theme.token  (main.tsx 启动时读 CSS var 注入)
    ├──→ 业务组件 .tsx / .css            (直接用 var(--accent) 等)
    └──→ GSAP animations/tokens.ts      (镜像同样的数值)
```

## 规则

1. **只在 `tokens.css` 定义实际值**（hex / px / 秒），其他地方一律 `var(--xxx)`。
2. **antd `theme.token` 在 `main.tsx` 启动时**读取 CSS 变量注入（用 `getComputedStyle`），不要硬编码同样的颜色。
3. **GSAP `D = {micro, base, slow, hero}`** 时长数值必须与 CSS `--duration-fast/mid/slow` 一致，不要写两份不同的。
4. **新增 token 类别**（如 shadow / opacity）先加到 `tokens.css`，再同步到 antd theme + animations。
5. **暗色模式**用 `[data-theme="dark"] :root` 覆盖变量，组件代码零改动。

## 命名规约

| 类别 | 前缀 | 例 |
|------|------|----|
| 品牌色 | `--accent` / `--color-*` | `--accent`, `--color-danger` |
| 文字 | `--text-*` | `--text-primary`, `--text-secondary` |
| 背景 | `--bg-*` | `--bg-base`, `--bg-hover` |
| 边框 | `--border*` | `--border`, `--border-strong` |
| 圆角 | `--radius-*` | `--radius-sm`, `--radius-lg` |
| 间距 | `--space-*`（8px 网格） | `--space-md` = 16px |
| 字号 | `--text-xs/sm/md/lg/xl/2xl` | `--text-lg` = 14px |
| 时长 | `--duration-fast/mid/slow` | `--duration-mid` = 0.24s |

## 自检

- [ ] tokens.css 是颜色 / 圆角 / 字号 / 间距 / 时长 / 字体的**唯一**来源？
- [ ] antd `theme.token` 通过 `getComputedStyle` 镜像 CSS 变量，不硬编码？
- [ ] 业务组件全程用 `var(--xxx)`，找不到硬编码 `#3b82f6` / `0.24s` 之类？
- [ ] GSAP `D.micro/base/slow` 数值与 `--duration-*` 完全一致？
- [ ] 新加颜色 / 圆角 / 字号必经 tokens.css，不在组件里直写？

## 详细参考

- 完整 tokens.css 模板 + antd 注入 + GSAP 镜像 + 暗色模式片段：[`./css-token-system.examples.md`](./css-token-system.examples.md)

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`palette-principles.md`](./palette-principles.md) · [`palette-types.md`](./palette-types.md)
- 配套：[`../../antd/setup/config-provider.md`](../../antd/setup/config-provider.md)
