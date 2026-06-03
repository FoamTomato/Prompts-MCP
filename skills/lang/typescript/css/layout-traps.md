---
name: css-layout-traps
description: CSS 布局陷阱：z-index 生效条件 / stacking context / overflow 裁切 / flex min-width:0 / 100vh 抖动 / sticky 失效。Use when z-index 调大仍被遮挡 / 内容被裁切 / flex 撑破 / sticky 失效
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.css
- frontend/src/**/*.scss
triggers:
  keywords:
  - z-index 失效
  - 层叠上下文
  - stacking context
  - isolation isolate
  - overflow hidden 裁切
  - flex min-width
  - min-width 0
  - 100vh 抖动
  - dvh
  - position sticky 失效
  - will-change
effort: medium
context: inline
version: '1.0'
---
# TypeScript · CSS 布局陷阱

## 规则

决策点：z-index 调到 99999 仍被遮挡，多半是父级建了局部层叠上下文或被 overflow 裁切；按下表对症，禁魔法值。

| 现象 | 真因 | 解法 |
|------|------|------|
| z-index 写了不生效 | 元素 `position` 仍是 `static`（flex/grid item 除外，它们 z-index 直接生效） | 加 `position: relative` 或本就在 flex/grid 内 |
| 子元素 z-index 再大也压不过外层 | 父级有 `opacity<1` / `transform` / `filter` / `will-change` / `mix-blend-mode`，静默建了 stacking context，子 z-index 被局部化（生产最常见 z-index bug） | 把弹层 portal 到 body；或在该比较层显式 `isolation: isolate` 建可控上下文 |
| 子元素被切掉/阴影下拉被裁 | 祖先 `overflow: hidden/auto/scroll` 直接裁切，与 z-index 无关 | 该祖先改 `overflow: visible`，或把溢出内容 portal 出去 |
| flex 子项被长文本/大图撑破容器 | flex item 默认 `min-width: auto`，不会缩到内容以下 | 该 flex item 设 `min-width: 0`（纵向同理 `min-height: 0`） |
| 移动端满屏高度比视口高、滚动抖动 | `100vh` 含浏览器地址栏，地址栏收起后高度变化 | 用 `100dvh`（动态视口），降级写 `100vh` 兜底 |
| position: sticky 不吸顶 | 未写 `top`（或对应方向）；或最近滚动祖先 `overflow` 非 `visible`；或父高度不足 | 补 `top: 0`，确认滚动祖先 `overflow: visible` 且父级有足够高度 |

魔法值禁令：不写 `z-index: 99999`。层级用小整数 + `isolation: isolate` 把比较域圈在局部，跨域用 portal，不靠数值军备竞赛。

## 反例 · 正例

```scss
// ❌ 父级 transform 静默建 stacking context，子弹层 z-index 再大也飞不出去
.card {
  transform: translateZ(0);     // 为了开启 GPU 合成，副作用：新建层叠上下文
}
.card .dropdown { z-index: 99999; }   // 仍被同级后续卡片盖住，治标不治本
```

```scss
// ✅ 显式 isolation 建可控上下文 + 小整数层级；魔法值消失
.card { isolation: isolate; }           // 主动声明：本卡片是独立比较域
.card .dropdown { z-index: 10; }        // 域内小整数即可，不与全局打架
```

```scss
// ❌ flex 子项默认 min-width:auto，长 URL 不换行直接把容器撑破横向滚动
.row { display: flex; }
.row .title { overflow: hidden; text-overflow: ellipsis; }  // 省略号不生效，仍溢出

// ✅ flex 子项补 min-width:0，省略号才能正常裁断
.row .title { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
```

```tsx
// ✅ 移动端全屏弹层用 dvh，避开地址栏抖动；样式逻辑下沉，组件体只编排
import { CSSProperties } from "react";

// 下沉：满屏高度样式（>3 行计算挪出组件体），dvh 优先、vh 兜底
const fullHeightStyle: CSSProperties = {
  height: "100dvh",
  minHeight: "100vh",        // 不支持 dvh 的旧浏览器降级
  isolation: "isolate",       // 弹层本体独立层叠域，内部用小 z-index
};

export function FullScreenSheet({ children }: { children: React.ReactNode }) {
  // 单一职责：只负责挂载满屏容器，层级/高度全由 fullHeightStyle 决定
  return <div style={fullHeightStyle}>{children}</div>;
}
```

```scss
// ❌ sticky 缺 top、且滚动祖先 overflow:hidden —— 双重失效，根本不吸顶
.scroll-area { overflow: hidden; }
.scroll-area .toolbar { position: sticky; }   // 无 top + 祖先裁切，纹丝不动

// ✅ 补 top，滚动祖先放开 overflow，sticky 才生效
.scroll-area { overflow: visible; }
.scroll-area .toolbar { position: sticky; top: 0; z-index: 1; }
```

## 自检

- [ ] z-index 失效时，先确认该元素 `position` 非 `static`（或在 flex/grid 内）？
- [ ] 排查过父链上的 `opacity<1` / `transform` / `filter` / `will-change` 是否静默建了 stacking context？
- [ ] 子元素被裁切时，检查过祖先的 `overflow` 而非只调 z-index？
- [ ] flex/grid 子项长内容撑破容器时，加了 `min-width: 0`（或 `min-height: 0`）？
- [ ] 移动端全屏高度用 `100dvh` 并保留 `100vh` 兜底，没有裸 `100vh`？
- [ ] sticky 元素写了 `top`，且滚动祖先 `overflow: visible`、父级高度足够？
- [ ] 全程没有 `z-index: 99999` 魔法值，改用 `isolation: isolate` + 小整数 + portal？

## 相关

- 父：[`./index.md`](./index.md)
- 跨引：[`../../../framework/antd/index.md`](../../../framework/antd/index.md)（Modal / Dropdown 的 getPopupContainer 与 portal 层级）
- 跨引：[`../../../framework/react/index.md`](../../../framework/react/index.md)（createPortal 把弹层挂到 body 逃离局部层叠域）
