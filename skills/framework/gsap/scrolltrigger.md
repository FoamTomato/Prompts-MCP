---
name: gsap-scrolltrigger
description: ScrollTrigger 进视口触发与滚动驱动 — once 入场 vs scrub 联动、start/end、布局后 refresh、useGSAP 自动清理。Use when 元素滚到视口才入场 / 滚动驱动进度条或视差 / ScrollTrigger 位置算错 / 切路由后触发器残留时。
parent: ./index.md
paths:
- frontend/src/animations/**/*.ts
- frontend/src/**/*.tsx
triggers:
  keywords:
  - ScrollTrigger
  - 进视口入场
  - 滚动驱动
  - toggleActions
  - scrub
  - start end
  - 视口触发位置算错
  - ScrollTrigger.refresh
effort: medium
context: inline
version: '1.0'
---
# GSAP · ScrollTrigger

## 两种用法别混

| 模式 | 配置 | 用在 |
|------|------|------|
| **一次性入场** | `toggleActions` 或 `once: true` | 卡片/区块滚到视口淡入（最常见） |
| **滚动驱动联动** | `scrub: true`（或数字=平滑） | 进度条、视差、长图逐帧 |

**判断规则**：入场动画（滚到即触发、放完即停）用 `once`/`toggleActions`；只有进度必须跟随滚动位置连续变化（进度条/视差/逐帧）才用 `scrub`。scrub 把每帧绑到滚动，性能与体感都更重，不是默认选项。

## 一次性入场（首选）

```ts
// src/animations/home.ts
import gsap from "gsap";
import { D, E } from "./tokens";

export function revealOnScroll(s: gsap.utils.Selector): void {
  gsap.from(s(".rec-card"), {
    y: 20,
    autoAlpha: 0,                 // autoAlpha = opacity + visibility，避免隐藏元素仍可点
    duration: D.slow,
    ease: E.out,
    stagger: 0.06,
    scrollTrigger: {
      trigger: s(".rec-grid"),
      start: "top 80%",          // 元素顶到达视口 80% 处触发
      once: true,                // 只放一次，回滚不重播
    },
  });
}
```

组件侧用 `useGSAP({ scope })` 调用——scope 卸载时**自动 kill 所有 ScrollTrigger**，无需手动清理：

```tsx
useGSAP(() => revealOnScroll(gsap.utils.selector(rootRef)), { scope: rootRef });
```

## 滚动驱动（scrub）

```ts
gsap.to(s(".progress"), {
  scaleX: 1,
  transformOrigin: "left center",
  ease: "none",                  // scrub 必须 linear，否则与滚动脱节
  scrollTrigger: { trigger: s("article"), start: "top top", end: "bottom bottom", scrub: true },
});
```

## 必须 refresh 的场景

DOM/布局在 ScrollTrigger 创建后变化（异步数据撑高、图片加载、字体回流、折叠展开），位置会算错：

```ts
ScrollTrigger.refresh();         // 数据/图片就位后调一次
```

## 反例

```ts
// ❌ 入场用了 scrub —— 卡片随滚动来回淡入淡出，像故障
scrollTrigger: { trigger: ".card", scrub: true }   // 入场该用 once: true

// ❌ 手动 useEffect 建 ScrollTrigger 不 kill —— 切路由后残留，报错/重复触发
useEffect(() => { ScrollTrigger.create({ ... }); }, []);   // 用 useGSAP({scope})

// ❌ 异步数据撑开页面后不 refresh —— start 位置停留在旧高度，触发时机全错
```

## 自检

- [ ] 入场用 `once`/`toggleActions`，不是滥用 `scrub`？
- [ ] scrub 动画 `ease: "none"`？
- [ ] 用 `useGSAP({ scope })` 让 ScrollTrigger 自动清理（不手动 useEffect）？
- [ ] 异步内容/图片就位后调了 `ScrollTrigger.refresh()`？
- [ ] 隐藏入场用 `autoAlpha` 而非纯 `opacity`？

## 相关

- 父：[`./index.md`](./index.md)
- 先注册插件：[`plugin-registration.md`](./plugin-registration.md)
- 兄弟：[`use-gsap-hook.md`](./use-gsap-hook.md) · [`timeline-organization.md`](./timeline-organization.md)
- 入场该配哪种（规约）：[`../../design/component-patterns/entrance-patterns.md`](../../design/component-patterns/entrance-patterns.md)
