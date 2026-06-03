---
name: design-motion-and-animation
description: 动效约定 — 入场 translateY+fade、列表 stagger、hover 时长、标准/弹性曲线，并强制 prefers-reduced-motion 兜底。Use when 加入场/hover 动画 / 定过渡时长曲线 / 处理减弱动效偏好时。
parent: ./index.md
paths:
  - "**/*.tsx"
  - "**/*.vue"
  - "**/*.css"
  - "**/*.html"
triggers:
  keywords:
    - 动效
    - 动画
    - animation
    - motion
    - 入场动画
    - stagger
    - prefers-reduced-motion
    - 缓动曲线
effort: low
version: "1.0"
---

# Motion · 动效与动画

> 动效服务于「告知变化」，不是炫技。统一曲线与时长，并永远给 reduced-motion 兜底。

## 曲线与时长

| 名 | 值 | 用 |
|----|----|----|
| 标准 | `cubic-bezier(.4,0,.2,1)` | 布局过渡、滑块移动 |
| 弹性 | `cubic-bezier(.22,1,.36,1)` | 卡片入场、缩放 |

| 动作 | 时长 |
|------|------|
| hover/状态切换 | .15s |
| 滑块/位移 | .25s |
| 卡片/区块入场 | .4-.5s |
| stagger 间隔 | .04-.08s / 项 |

## 入场与 stagger

```css
.enter {
  opacity:0;
  animation: enter .5s cubic-bezier(.22,1,.36,1) forwards;
  animation-delay: calc(var(--i,0) * .06s);   /* 列表逐项 stagger */
}
@keyframes enter { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }
```

只动 `transform` / `opacity`（合成层，不触发重排/重绘）。

## 强制 reduced-motion 兜底

每处非必要动效都要被这条包住：

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: .01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: .01ms !important;
  }
}
```

JS 侧同理用 `matchMedia('(prefers-reduced-motion: reduce)').matches` 跳过 JS 动画。

## 禁止

- ❌ 闪烁 >3 次/秒（癫痫风险）。
- ❌ 动 `width`/`height`/`top`/`left` 做动画（重排卡顿）—— 用 `transform`。
- ❌ 无限自动循环的大幅动效干扰阅读。

## 自检

- [ ] 曲线/时长取自统一档位，没散落随手值？
- [ ] 入场只动 transform/opacity，列表有 stagger？
- [ ] 有全局 `prefers-reduced-motion` 兜底，JS 动画也判断了？
- [ ] 无 >3 次/秒闪烁、无 width/left 类重排动画？

## 相关

- 父：[`./index.md`](./index.md)
- 减弱动效与闪烁底线：[`../foundations/accessibility.md`](../foundations/accessibility.md)
- 用 GSAP 实现落地：[`../../framework/gsap/index.md`](../../framework/gsap/index.md)
- 风格各自的入场风味：[`../theme/index.md`](../theme/index.md)
