---
name: gsap-timeline-organization
description: timeline 集中 animations/<feature>.ts — 组件只调用。Use when 写 TS 业务代码 / 评审涉及
  `timeline-organization` 的 PR。
parent: ./index.md
paths:
- frontend/src/animations/**/*.ts
triggers:
  keywords:
  - timeline
  - gsap.timeline
  - animations/
  - 集中
  - 组件只调用
effort: medium
context: inline
version: '1.0'
---
# GSAP · timeline 组织

## 规则

**所有 timeline 集中在 `src/animations/<feature>.ts`**，组件只 import 并调用，不在组件文件里写 `gsap.timeline()`。

## 目录约定

```
src/animations/
├── tokens.ts          # D / E 时长 / ease 常量
├── home.ts            # 主页相关
├── outline.ts         # 大纲页
├── editor.ts          # 编辑器
├── task-waiting.ts    # 任务等待
├── present.ts         # 演示模式
└── dashboard.ts       # 控制台
```

## 单个 timeline 文件模板

```ts
// src/animations/home.ts
import gsap from "gsap";
import { D, E } from "./tokens";

type Selector = gsap.utils.Selector;

export function buildHeroIntroTimeline(s: Selector): gsap.core.Timeline {
  const tl = gsap.timeline({ defaults: { duration: D.base, ease: E.out } });
  tl.from(s(".hero-title"), { y: 30, opacity: 0 })
    .from(s(".hero-sub"), { y: 20, opacity: 0 }, "-=0.1")
    .from(s(".hero-cta"), { scale: 0.8, opacity: 0 }, "-=0.05");
  return tl;
}

export function buildCardStaggerTimeline(s: Selector): gsap.core.Timeline {
  return gsap.timeline().from(s(".rec-card"), {
    y: 20,
    opacity: 0,
    duration: D.slow,
    ease: E.out,
    stagger: 0.05,
  });
}
```

## 组件调用

```tsx
// src/pages/HomePage.tsx
import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import { buildHeroIntroTimeline, buildCardStaggerTimeline } from "@/animations/home";

function HomePage() {
  const rootRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    const s = gsap.utils.selector(rootRef);
    const intro = buildHeroIntroTimeline(s);
    const cards = buildCardStaggerTimeline(s);
    intro.add(cards, "-=0.1");
  }, { scope: rootRef });

  return <div ref={rootRef}>...</div>;
}
```

## 为什么集中

- **复用**：多个组件共用同一 timeline 风格（如卡片 stagger）
- **可测试**：timeline 是纯函数，可单测
- **维护**：调时长、ease 只改一处
- **可读**：组件文件不被动画细节淹没

## 反例

```tsx
// ❌ 组件里写复杂 timeline
function HeroSection() {
  useGSAP(() => {
    const tl = gsap.timeline();
    tl.from(".title", { y: 30, opacity: 0, duration: 0.24, ease: "power2.out" })
      .from(".sub", { y: 20, opacity: 0, duration: 0.24, ease: "power2.out" }, "-=0.1")
      .from(".cta", { scale: 0.8, opacity: 0, duration: 0.24, ease: "power2.out" }, "-=0.05");
    // 散落在组件内，难复用难维护
  }, ...);
}
```

## 自检

- [ ] 组件文件里没有 `gsap.timeline()`？
- [ ] timeline 都在 `src/animations/`？
- [ ] 时长 / ease 用 `D` / `E` 常量？
- [ ] timeline 函数有返回值（便于组合）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`use-gsap-hook.md`](./use-gsap-hook.md)

