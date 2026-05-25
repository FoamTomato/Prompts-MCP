---
name: gsap-principles
description: GSAP 核心原则 — 单一引擎 / 集中管理 / GPU 友好 / 时长克制
parent: ./index.md
paths:
  - "frontend/src/animations/**/*.ts"
  - "frontend/src/**/*.tsx"
triggers:
  keywords: [GSAP, gsap, useGSAP, timeline]
effort: medium
context: inline
version: "1.0"
---

# GSAP · 核心原则

## 6 条硬约束

| 原则 | 规则 |
|------|------|
| **单一引擎** | 仅用 GSAP，禁 Framer Motion / AnimeJS / React Spring / CSS transition（悬停 / 聚焦例外） |
| **集中管理** | 所有 timeline 定义在 `src/animations/<feature>.ts`，组件只调用，不写 `gsap.to()` |
| **自动清理** | 组件内必须用 `useGSAP({ scope })` hook，禁手动 `kill()` |
| **GPU 友好** | 只动 `x / y / scale / rotation / opacity`，禁动 `width / height / top / left` |
| **时长克制** | 悬停 150ms / 标准 240ms / 卡片入场 400ms / 复杂转场 ≤ 600ms |
| **可访问** | 监听 `prefers-reduced-motion`，开启时降级 fade-only 或瞬时 |

## 时长 token

```ts
// src/animations/tokens.ts
export const D = {
  micro:  0.15,   // hover / focus
  base:   0.24,   // tab 切换 / modal
  slow:   0.4,    // 卡片入场
  hero:   0.6,    // 大转场
} as const;

export const E = {
  out:    "power2.out",
  inOut:  "power2.inOut",
  bounce: "back.out(1.7)",
  elastic: "elastic.out(1, 0.5)",
} as const;
```

与 antd `motionDurationFast/Mid/Slow` 数值对齐。

## 为什么禁 Framer Motion / CSS transition

| 方案 | 问题 |
|------|------|
| Framer Motion | bundle 大、与 React 18 并发渲染兼容性问题 |
| AnimeJS / React Spring | 与 GSAP 重叠，没必要混栈 |
| CSS transition（复杂动画） | 时序难控、无法精确控制 stagger / sequence |
| CSS transition（简单悬停） | **允许**——悬停 / 聚焦的简单 fade / color 转换走 CSS |

## 为什么禁动 width/height/top/left

这些属性触发布局重排（reflow），性能差。`transform: translate3d` / `scale` 走 GPU 合成层。

```ts
// ❌ 重排
gsap.to(elem, { width: 300, duration: D.base });

// ✅ scale
gsap.set(elem, { transformOrigin: "left center" });
gsap.to(elem, { scaleX: 1.5, duration: D.base, ease: E.out });
```

## 自检

- [ ] 项目里没有其他动画库？
- [ ] 组件内不直接 `gsap.to()`（在 animations/ 集中）？
- [ ] 用 useGSAP hook 而非手动 kill？
- [ ] 只动 transform 类属性？
- [ ] 时长 ≤ 600ms？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`use-gsap-hook.md`](./use-gsap-hook.md) · [`timeline-organization.md`](./timeline-organization.md)

