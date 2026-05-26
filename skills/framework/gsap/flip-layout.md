---
name: gsap-flip-layout
description: Flip 插件 — 列表重排 / 模式切换的稳态动画。Use when 写 TS 业务代码 / 评审涉及 `flip-layout` 的
  PR。
parent: ./index.md
paths:
- frontend/src/animations/**/*.ts
- frontend/src/**/*.tsx
triggers:
  keywords:
  - Flip
  - gsap.Flip
  - layout animation
  - 列表重排
  - 模式切换
  - 式切换的
effort: medium
context: inline
version: '1.0'
---
# GSAP · Flip 插件

## 何时用

Flip 适用于"**元素从位置 A 平滑过渡到位置 B**"且 A → B 之间 DOM 结构变化的场景：

- 列表重排（如拖拽换位）
- 模式切换（如卡片放大到模态视图）
- Tab 切换时下划线滑动
- 网格 → 列表布局切换

## 安装注册

```ts
// src/main.tsx
import gsap from "gsap";
import { Flip } from "gsap/Flip";
gsap.registerPlugin(Flip);
```

## 标准用法

```ts
import gsap from "gsap";
import { Flip } from "gsap/Flip";
import { D, E } from "@/animations/tokens";

function reorderCards(scope: HTMLElement, newOrder: string[]) {
  const cards = scope.querySelectorAll(".card");

  // 1. 记录初始状态
  const state = Flip.getState(cards);

  // 2. 改变 DOM（如重排 / className 切换）
  applyNewOrder(newOrder);

  // 3. Flip 自动从旧状态过渡到新状态
  Flip.from(state, {
    duration: D.slow,
    ease: E.inOut,
    stagger: 0.02,
    absolute: true,    // 移动期间用 position: absolute 让元素脱离布局
  });
}
```

## React + dnd-kit 集成

```tsx
import { DndContext, DragEndEvent } from "@dnd-kit/core";
import { SortableContext, arrayMove } from "@dnd-kit/sortable";
import { Flip } from "gsap/Flip";

function SortableSlides() {
  const [slides, setSlides] = useState(initialSlides);
  const containerRef = useRef<HTMLDivElement>(null);

  const handleDragEnd = (e: DragEndEvent) => {
    if (!e.over || e.active.id === e.over.id) return;
    const oldIdx = slides.findIndex(s => s.id === e.active.id);
    const newIdx = slides.findIndex(s => s.id === e.over!.id);

    const state = Flip.getState(containerRef.current!.querySelectorAll(".slide"));
    setSlides(arrayMove(slides, oldIdx, newIdx));

    requestAnimationFrame(() => {
      Flip.from(state, { duration: D.base, ease: E.out, stagger: 0.02, absolute: true });
    });
  };

  return (
    <DndContext onDragEnd={handleDragEnd}>
      <SortableContext items={slides}>
        <div ref={containerRef}>
          {slides.map(s => <SortableSlide key={s.id} {...s} />)}
        </div>
      </SortableContext>
    </DndContext>
  );
}
```

## 用例

| 场景 |
|------|
| 拖拽换章节顺序 |
| 拖拽换幻灯片 |
| 控制台过滤切换布局 |
| 大纲转编辑器（hero 转场） |

## 自检

- [ ] 注册了 Flip 插件？
- [ ] 状态变化前 `Flip.getState`？
- [ ] 状态变化后下一帧 `Flip.from`？
- [ ] 用 `absolute: true` 避免影响周围元素布局？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`draggable.md`](./draggable.md) · [`use-gsap-hook.md`](./use-gsap-hook.md)
