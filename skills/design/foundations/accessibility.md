---
name: design-accessibility
description: WCAG 2.2 无障碍底线 — 对比度 4.5:1/3:1、触控目标 24/44px、:focus-visible、prefers-reduced-motion、状态禁纯色编码。Use when 选配色 / 定按钮尺寸 / 写焦点样式 / 加动效 / 评审 UI 可访问性时。
parent: ./index.md
paths:
  - "**/*.tsx"
  - "**/*.vue"
  - "**/*.css"
  - "**/*.scss"
  - "**/*.html"
triggers:
  keywords:
    - 无障碍
    - 可访问性
    - a11y
    - 对比度
    - WCAG
    - accessibility
    - contrast ratio
    - 触控目标
    - focus-visible
    - prefers-reduced-motion
effort: low
version: "1.0"
---

# Accessibility · WCAG 2.2 底线

> 任何风格都不得突破这些数字。对比度是最常见的违规项，先过这关。

## 对比度（AA 必达）

| 内容 | 最低对比度 | 备注 |
|------|-----------|------|
| 正文 / 普通文本 | **4.5:1** | vs 背景 |
| 大字（≥24px 常规，或 ≥18.66px 粗体） | **3:1** | |
| 非文本 UI（边框 / 图标 / focus ring / 图表色段） | **3:1** | 与相邻色，SC 1.4.11 |
| AAA 目标 | 7:1 正文 / 4.5:1 大字 | 追求更高时 |

- 免除：禁用态控件、纯装饰文本、logo。
- 反例：`#999` on `#fff` = 2.85:1（不达标）；浅灰占位符最易踩。

## 触控目标

| 级别 | 尺寸 | 来源 |
|------|------|------|
| AA 最低 | **≥24×24 CSS px**，或与相邻目标间距 ≥24px | SC 2.5.8 |
| AAA | **≥44×44 CSS px** | SC 2.5.5 |
| 平台底线（主操作按钮用） | Apple 44×44pt / Material 48×48dp | HIG / M3 |

行内文字链接、浏览器原生控件免除。

## 键盘焦点

- 每个可交互元素必须有**可见焦点指示**（SC 2.4.7）；**禁 `outline:none` 不补替代**。
- 用 `:focus-visible`（仅键盘触发，不打扰鼠标用户）；focus ring 与相邻色 ≥3:1。
- 焦点元素不被吸顶/浮层遮挡（SC 2.4.11）；tab 顺序符合逻辑。

## 文本间距可覆盖（SC 1.4.12）

用户强制下列设置时**内容不得破版/截断** → 别把文字锁进固定高容器：

行高 1.5× · 段距 2× · 字距 0.12em · 词距 0.16em。

## 动效与状态

- 尊重 `prefers-reduced-motion: reduce`，包住非必要动效（视差/缩放/装饰过渡）；JS 侧用 `matchMedia('(prefers-reduced-motion: reduce)')` 镜像判断。
- 闪烁 ≤3 次/秒（SC 2.3.1）。
- 拖拽手势须有单击替代（SC 2.5.7）。
- **状态禁纯色编码** —— 成功/警告/错误必须配图标或文字（约 8% 男性红绿色弱）。

## 自检

- [ ] 正文 ≥4.5:1、大字与非文本 UI ≥3:1？
- [ ] 触控目标 ≥24px（主操作 ≥44px）？
- [ ] 有 `:focus-visible` 可见焦点，没裸 `outline:none`？
- [ ] 文字未锁死在固定高容器，间距可覆盖？
- [ ] 动效有 `prefers-reduced-motion` 兜底，状态不靠纯色？

## 相关

- 父：[`./index.md`](./index.md)
- 配色角色（保证 on-X 配对达标）：[`color-usage.md`](color-usage.md)
- 动效兜底写法：[`../component-patterns/motion-and-animation.md`](../component-patterns/motion-and-animation.md)
