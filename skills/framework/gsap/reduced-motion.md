---
name: gsap-reduced-motion
description: prefers-reduced-motion 降级 — fade-only 或瞬时切换
parent: ./index.md
paths:
- frontend/src/animations/**/*.ts
triggers:
  keywords:
  - prefers-reduced-motion
  - reduced-motion
  - a11y
  - 或瞬时切换
effort: medium
context: inline
version: '1.0'
---
# GSAP · prefers-reduced-motion 降级

## 规则

监听用户系统偏好 `prefers-reduced-motion: reduce`，开启时**降级动画**：

- 复杂转场 → fade-only
- 长时长 → 缩短到 100ms 以下
- stagger → 同时出现

## 全局监听

```ts
// src/main.tsx
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
gsap.defaults({
  duration: reduceMotion ? 0.05 : 0.24,
});

// 监听变化（用户运行时切换）
window.matchMedia("(prefers-reduced-motion: reduce)").addEventListener("change", (e) => {
  gsap.defaults({ duration: e.matches ? 0.05 : 0.24 });
});
```

## 局部降级

```ts
// src/animations/home.ts
import gsap from "gsap";
import { D, E } from "./tokens";

const reduced = () => window.matchMedia("(prefers-reduced-motion: reduce)").matches;

export function buildHeroIntroTimeline(s: gsap.utils.Selector): gsap.core.Timeline {
  if (reduced()) {
    // 降级：所有元素同时 fade in
    return gsap.timeline().from(s(".hero-title, .hero-sub, .hero-cta"), {
      opacity: 0,
      duration: 0.1,
    });
  }

  // 完整版
  const tl = gsap.timeline({ defaults: { duration: D.base, ease: E.out } });
  tl.from(s(".hero-title"), { y: 30, opacity: 0 })
    .from(s(".hero-sub"), { y: 20, opacity: 0 }, "-=0.1")
    .from(s(".hero-cta"), { scale: 0.8, opacity: 0 }, "-=0.05");
  return tl;
}
```

## CSS 配合

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## 测试

```
# macOS
System Settings → Accessibility → Display → "Reduce Motion"

# Chrome DevTools
开发者工具 → ⋮ → More tools → Rendering → "Emulate CSS media feature prefers-reduced-motion"
```

## 何时必须支持

| 场景 | 必须 |
|------|------|
| Public 教育产品（含儿童 / 老人用户） | ✅ |
| WCAG AA 合规要求 | ✅ |
| Quill 全产品 | ✅ |

## 自检

- [ ] 全局 gsap.defaults 监听了 reduced motion？
- [ ] 复杂转场有降级路径？
- [ ] CSS 也加了 @media 兜底？
- [ ] DevTools 模拟 reduce-motion 通过？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`principles.md`](./principles.md)

