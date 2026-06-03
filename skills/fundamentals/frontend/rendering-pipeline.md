---
name: fundamentals-frontend-rendering-pipeline
description: "浏览器渲染管线的三档代价（重排 reflow / 重绘 repaint / 合成 composite）与改样式的决策。Use when 页面卡顿掉帧 / 滚动拖动不顺 / 频繁改样式 / 批量改 DOM 触发布局抖动 / 想用 GPU 提合成层时。"
parent: ./index.md
paths:
- frontend/src/**/*.ts
- frontend/src/**/*.tsx
- frontend/src/**/*.vue
triggers:
  keywords:
  - 重排
  - 重绘
  - 合成层
  - reflow
  - repaint
  - layout thrashing
  - transform
  - will-change
  - offsetWidth
  - 布局抖动
effort: medium
context: inline
version: '1.0'
---
# Fundamentals 前端 · 渲染管线与重排重绘合成层

## 规则

**决策点：动一个样式前先判定它落在哪一档——能只动 `transform`/`opacity` 就别碰几何属性。**

管线顺序：JS → Style → Layout(布局) → Paint(绘制) → Composite(合成)。改的属性越靠前，回滚的步骤越多、越贵。

| 想动什么 | 触发哪档 | 代价 | 怎么做 |
|---------|---------|------|-------|
| 位移 / 缩放 / 旋转 | 合成 composite | 最低，走 GPU 不占主线程 | 用 `transform: translate/scale/rotate`，不用 `top`/`left` |
| 显隐(参与动画) | 合成 composite | 最低 | 用 `opacity`，不用频繁切 `display` |
| 颜色 / 背景 / 阴影 / 圆角 | 重绘 repaint | 中,跳过 Layout | 可接受,但大面积重绘仍卡 |
| 宽高 / `top`/`left`/`margin`/字号 | 重排 reflow | 最高,牵连兄弟与父子重新布局 | 尽量避免;必须改则批量一次性 |
| 一次改多个几何属性 | 多次重排 | 叠加放大 | 切 class 一次性改,或 `DocumentFragment` 离屏拼装 |

要点：
- **位移用 `transform`**，不用 `top`/`left`——后者每帧重排。
- **layout thrashing(布局抖动)**：在循环里「读几何(`offsetWidth`/`offsetTop`/`getBoundingClientRect`)→ 立即写 style」会强制同步重排,反复读写=反复重排。解法：**先批量读，再批量写**。
- **批量 DOM**：拼好节点用 `DocumentFragment` 一次 append；多处样式合并成一次 class 切换。
- `will-change`/`translateZ(0)` 可主动提合成层，但**占显存别滥用**——只给真正高频动画的元素加，动画结束移除。

## 反例 · 正例

```ts
// 反例:循环里读 offsetHeight(读)后立刻写 style.height(写) —— 每次迭代强制同步重排,N 次抖动
function shrinkAll(items: HTMLElement[]): void {
  items.forEach((el) => {
    el.style.height = `${el.offsetHeight / 2}px`; // 读→写交替,layout thrashing
  });
}

// 反例:逐条 append 到已挂载节点,每次都重排
function renderList(parent: HTMLElement, names: string[]): void {
  names.forEach((name) => {
    const li = document.createElement('li');
    li.textContent = name;
    parent.appendChild(li); // 每次 append 触发一次布局
  });
}
```

```ts
// 正例:先全部读,再全部写 —— 一次重排
function shrinkAll(items: HTMLElement[]): void {
  // 第一步:批量读取所有高度(只读,不触发同步重排)
  const heights: readonly number[] = items.map((el) => el.offsetHeight);
  // 第二步:批量写入,集中在写阶段
  items.forEach((el, i) => {
    el.style.height = `${heights[i] / 2}px`;
  });
}

// 正例:DocumentFragment 离屏拼装,一次 append
function renderList(parent: HTMLElement, names: string[]): void {
  // 第一步:在内存碎片里拼装,不触碰渲染树
  const fragment = document.createDocumentFragment();
  names.forEach((name) => {
    const li = document.createElement('li');
    li.textContent = name;
    fragment.appendChild(li);
  });
  // 第二步:一次性插入,仅触发一次布局
  parent.appendChild(fragment);
}

// 正例:位移动画走合成层,不用 top/left
function slideIn(el: HTMLElement): void {
  // 第一步:动画前提层(只对高频动画元素)
  el.style.willChange = 'transform';
  // 第二步:用 transform 位移,不触发重排重绘
  el.style.transform = 'translateX(0)';
  // 第三步:动画结束回收提层,释放显存
  el.addEventListener('transitionend', () => { el.style.willChange = 'auto'; }, { once: true });
}
```

## 自检

- [ ] 位移/缩放用 `transform` 而非 `top`/`left`/`width`/`height`?
- [ ] 动画显隐用 `opacity`/`visibility` 而非频繁 `display` 切换?
- [ ] 循环里没有「读几何属性后立即写 style」的读写交替(布局抖动)?
- [ ] 批量 DOM 改动用了 `DocumentFragment` 或一次性 class 切换?
- [ ] `will-change`/`translateZ` 只加在真正高频动画元素上,且用完移除?

> 性能数字为业界参考,落地需自测(Performance 面板看 Layout/Paint/Composite 耗时)。

## 相关

- 用法侧·CLS 布局抖动治理：[`../../framework/react/performance/web-vitals-cls.md`](../../framework/react/performance/web-vitals-cls.md)
- 动画落地·GSAP 原则：[`../../framework/gsap/principles.md`](../../framework/gsap/principles.md)
- 上层：[`./index.md`](./index.md)
