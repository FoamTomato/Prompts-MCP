---
name: gsap-use-gsap-hook
description: useGSAP({ scope, dependencies }) hook 模板。Use when 写 React 组件 / 改 .tsx
  文件 / 评审涉及 `use-gsap-hook` 的 PR。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/animations/**/*.ts
triggers:
  keywords:
  - useGSAP
  - scope
  - dependencies
  - 模板
effort: medium
context: inline
version: '1.0'
---
# GSAP · useGSAP hook

## 规则

React 组件内的 GSAP 动画**必须**用 `useGSAP` hook。不要手动 `useEffect + gsap.to + kill`。

## 标准用法

```tsx
import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import { D, E } from "@/animations/tokens";

function TextbookCard({ selected }: { selected: boolean }) {
  const rootRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    gsap.to(rootRef.current, {
      scale: selected ? 1.02 : 1,
      duration: D.micro,
      ease: E.out,
    });
  }, { scope: rootRef, dependencies: [selected] });

  return <div ref={rootRef}>...</div>;
}
```

## scope 的作用

`scope: rootRef` 让该 hook 内创建的所有 GSAP 动画 / ScrollTrigger 自动被收集到此 scope。组件卸载时**自动 kill**，不需手动清理。

## dependencies vs revertOnUpdate

```tsx
// 默认：dependencies 变化 → 重跑 callback（旧动画自动 kill + 新动画生效）
useGSAP(() => { ... }, { scope: rootRef, dependencies: [selected] });

// revertOnUpdate: dependencies 变化 → 先回滚旧动画再重跑
useGSAP(() => { ... }, {
  scope: rootRef,
  dependencies: [selected],
  revertOnUpdate: true,
});
```

通常默认即可。`revertOnUpdate` 用于"动画必须从初始态开始"的场景。

## 从 features 调集中 timeline

```tsx
// src/animations/home.ts
export function buildHomeHeroTimeline(scope: gsap.utils.Selector): gsap.core.Timeline {
  const tl = gsap.timeline({ defaults: { duration: D.base, ease: E.out } });
  tl.from(scope(".hero-title"), { y: 30, opacity: 0 })
    .from(scope(".hero-sub"), { y: 20, opacity: 0 }, "-=0.1")
    .from(scope(".hero-cta"), { scale: 0.8, opacity: 0 }, "-=0.05");
  return tl;
}
```

```tsx
// src/pages/HomePage.tsx
import { useGSAP } from "@gsap/react";
import { buildHomeHeroTimeline } from "@/animations/home";

function HomePage() {
  const rootRef = useRef<HTMLDivElement>(null);

  useGSAP((ctx, contextSafe) => {
    const tl = buildHomeHeroTimeline(gsap.utils.selector(rootRef));
    return () => tl.kill();   // 可选 — scope 已经管理
  }, { scope: rootRef });

  return <div ref={rootRef}>...</div>;
}
```

## 反例

```tsx
// ❌ 手动 useEffect + gsap.to
useEffect(() => {
  const tween = gsap.to(elem, { scale: 1.02, duration: 0.15 });
  return () => tween.kill();
}, [selected]);

// ✅ useGSAP
useGSAP(() => {
  gsap.to(elem, { scale: 1.02, duration: 0.15 });
}, { scope: ref, dependencies: [selected] });
```

## 自检

- [ ] 组件内的 GSAP 都用 useGSAP？
- [ ] 提供 scope: ref？
- [ ] dependencies 列出影响动画的变量？
- [ ] 不手动 kill（除非有特殊原因）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`principles.md`](./principles.md) · [`timeline-organization.md`](./timeline-organization.md)

