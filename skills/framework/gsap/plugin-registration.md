---
name: gsap-plugin-registration
description: GSAP 插件注册纪律 — registerPlugin 集中在入口、先于动画执行；插件从 gsap/<Plugin> 直接 import。Use when 首次引入 ScrollTrigger/Flip/SplitText / 插件报 "not registered" / 注册散落或晚于动画时。
parent: ./index.md
paths:
- frontend/src/**/*.ts
- frontend/src/**/*.tsx
triggers:
  keywords:
  - registerPlugin
  - 插件注册
  - plugin registration
  - 集中注册
  - 注册顺序
  - not registered
  - register once
effort: low
context: inline
version: '1.0'
---
# GSAP · 插件注册

## 规则

**所有插件在应用入口集中注册一次**，不在组件 / animations 文件里各注册各的。注册必须先于任何动画执行。

```ts
// src/animations/register.ts —— 唯一注册点
import gsap from "gsap";
import { useGSAP } from "@gsap/react";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { Flip } from "gsap/Flip";
import { Draggable } from "gsap/Draggable";
import { SplitText } from "gsap/SplitText";

gsap.registerPlugin(useGSAP, ScrollTrigger, Flip, Draggable, SplitText);
```

```ts
// src/main.tsx —— 入口顶部 import，保证注册先于动画执行
import "@/animations/register";
```

`registerPlugin` 幂等可重复调，但**重复调用 = 注册点散落**，定位「到底注册没」会很痛。

## 插件 import 路径

所有插件直接从 `gsap/<Plugin>` 子路径具名 import，无需 token 或私有 npm 源。

| 插件 | import 路径 |
|-----|-----------|
| ScrollTrigger | `gsap/ScrollTrigger` |
| Flip | `gsap/Flip` |
| Draggable | `gsap/Draggable` |
| SplitText | `gsap/SplitText` |

核心 tween（`gsap.to/from/timeline`）**不是插件，无需注册**。各插件用途见各自叶子：[scrolltrigger](./scrolltrigger.md) · [flip-layout](./flip-layout.md) · [split-text](./split-text.md) · [draggable](./draggable.md)。

## 反例

```ts
// ❌ 在组件里临时注册 —— 散落多处，每次渲染都跑一遍
function Hero() {
  gsap.registerPlugin(ScrollTrigger);   // 应在入口统一注册
}

// ❌ 忘注册就用 —— 控制台 "ScrollTrigger is not registered"，动画静默失效
import { ScrollTrigger } from "gsap/ScrollTrigger";
ScrollTrigger.create({ ... });          // 没 registerPlugin，无效
```

## 自检

- [ ] 所有 `registerPlugin` 收敛在唯一入口文件？
- [ ] `useGSAP` 也注册了（React 项目）？
- [ ] 入口在 main 顶部 import，先于动画执行？
- [ ] 没在组件 / 渲染路径里重复 registerPlugin？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`scrolltrigger.md`](./scrolltrigger.md) · [`split-text.md`](./split-text.md) · [`flip-layout.md`](./flip-layout.md)
