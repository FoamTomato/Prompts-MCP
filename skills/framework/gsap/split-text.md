---
name: gsap-split-text
description: SplitText 文字逐字/词/行入场 — 选拆分粒度、stagger 入场、必须 revert 清理、字体加载后再 split。Use when 标题或 Hero 文案做逐字逐行动画 / 文字入场布局回流错位 / SplitText 清理与 reduced-motion 降级时。
parent: ./index.md
paths:
- frontend/src/animations/**/*.ts
- frontend/src/**/*.tsx
triggers:
  keywords:
  - SplitText
  - 文字动画
  - 逐字入场
  - split.revert
  - 字体加载断行
  - document.fonts.ready
  - 逐行
effort: medium
context: inline
version: '1.0'
---
# GSAP · SplitText 文字入场

> `import { SplitText } from "gsap/SplitText"` 直接可用，注册见 [`plugin-registration.md`](./plugin-registration.md)。

## 三步

1. **选对粒度**：chars（逐字，短标题）/ words（逐词，句子）/ lines（逐行，段落）。正文用 lines，不用 chars。
2. **stagger 入场**：拆完对 `split.chars`/`words`/`lines` 做 `from` + stagger。
3. **务必 revert 清理**：SplitText 会往 DOM 插一堆 `<div>`，不 revert 会污染文本（复制、SEO、屏读器全受影响）。

## 标准用法

```ts
// src/animations/hero.ts
import gsap from "gsap";
import { SplitText } from "gsap/SplitText";
import { D, E } from "./tokens";

export function splitHeroTitle(el: HTMLElement): () => void {
  const split = new SplitText(el, { type: "lines" });   // 逐行
  gsap.from(split.lines, {
    yPercent: 100,
    autoAlpha: 0,
    duration: D.slow,
    ease: E.out,
    stagger: 0.08,
  });
  return () => split.revert();        // 返回清理函数
}
```

组件侧用 useGSAP，把 revert 交给清理：

```tsx
useGSAP(() => {
  const cleanup = splitHeroTitle(titleRef.current!);
  return cleanup;                     // useGSAP 卸载时调用
}, { scope: rootRef });
```

## 字体加载后再 split（关键）

字体未加载完就 split，行宽按 fallback 字体算，真字体到位后**断行位置变了 → 错位**。等字体就绪：

```ts
await document.fonts.ready;           // 字体就位后再 new SplitText(...)
```

## reduced-motion 降级

减弱动效时**不拆字**，整段一次 fade：

```ts
if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  gsap.from(el, { autoAlpha: 0, duration: 0.1 });   // 不 split，整体淡入
  return () => {};
}
```

## 反例

```ts
// ❌ 正文段落逐字 —— 几百个 char 动画，又卡又花
new SplitText(p, { type: "chars" });  // 长文本用 lines

// ❌ 不 revert —— DOM 留满 <div>，用户复制出来支离破碎、屏读器读乱
const split = new SplitText(el, { type: "chars" });
gsap.from(split.chars, { ... });      // 缺 split.revert()

// ❌ 字体没加载就 split —— 真字体到位后断行错位
new SplitText(el, { type: "lines" }); // 应先 await document.fonts.ready
```

## 自检

- [ ] 粒度按文本长度选（短标题 chars，段落 lines）？
- [ ] 拿到清理函数并在卸载时 `split.revert()`？
- [ ] split 前 `await document.fonts.ready`？
- [ ] reduced-motion 时退化为整段 fade、不拆字？
- [ ] 用 `autoAlpha` 而非纯 `opacity`？

## 相关

- 父：[`./index.md`](./index.md)
- 先注册插件：[`plugin-registration.md`](./plugin-registration.md)
- 进视口才触发文字入场：[`scrolltrigger.md`](./scrolltrigger.md)
- 文字入场配在哪些组件（规约）：[`../../design/component-patterns/entrance-patterns.md`](../../design/component-patterns/entrance-patterns.md)
