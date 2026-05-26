---
name: gsap-draggable
description: '框架约定 · gsap: Draggable 插件 — 画布拖拽 / 自定义拖拽组件'
parent: ./index.md
paths:
- frontend/src/animations/**/*.ts
- frontend/src/features/editor/**/*.tsx
triggers:
  keywords:
  - Draggable
  - gsap.Draggable
  - 拖拽
effort: medium
context: inline
version: '1.0'
---
# GSAP · Draggable 插件

## 何时用

GSAP Draggable 是 Quill 编辑器画布元素拖拽的标准方案。性能优于自写 mousemove handler。

## 适用场景

| 场景 | 模块 |
|------|------|
| 编辑器画布元素移动 | ppt_generator M6 |
| 演示模式画笔绘制 | present_mode P5 |
| 自定义滑动控件（非 antd Slider） | （较少） |
| 列表反向拖拽（DnD） | 用 dnd-kit + Flip 更好（见 [`flip-layout.md`](./flip-layout.md)） |

## 安装

```ts
// src/main.tsx
import gsap from "gsap";
import { Draggable } from "gsap/Draggable";
gsap.registerPlugin(Draggable);
```

## 编辑器画布元素拖拽

```ts
// src/animations/editor.ts
import { Draggable } from "gsap/Draggable";

export function createElementDraggable(
  target: HTMLElement,
  bounds: HTMLElement,
  onDragEnd: (x: number, y: number) => void,
) {
  return Draggable.create(target, {
    type: "x,y",
    bounds,
    inertia: false,                 // 编辑场景禁惯性，要精确停在松手位置
    onPress() {
      target.style.cursor = "grabbing";
    },
    onRelease() {
      target.style.cursor = "grab";
      onDragEnd(this.x, this.y);    // this 是 Draggable 实例
    },
  })[0];
}
```

## React 集成

```tsx
import { useGSAP } from "@gsap/react";
import { createElementDraggable } from "@/animations/editor";

function CanvasElement({ id, x, y, onMove }: Props) {
  const ref = useRef<HTMLDivElement>(null);
  const canvasRef = useContext(CanvasRef);

  useGSAP(() => {
    if (!ref.current || !canvasRef.current) return;
    gsap.set(ref.current, { x, y });

    const drag = createElementDraggable(
      ref.current,
      canvasRef.current,
      (nx, ny) => onMove(id, nx, ny),
    );

    return () => drag.kill();
  }, { scope: ref });

  return <div ref={ref} className="canvas-element">...</div>;
}
```

## 多选拖拽

```ts
Draggable.create(targets, {   // 数组 → 每个元素独立 drag
  type: "x,y",
});
```

## 禁惯性

| inertia | 何时 |
|---------|------|
| `false` | 编辑器（要精确停在松手位置） |
| `true`  | 卡片轻量滑动（如演示模式画笔） |

`inertia: true` 需要安装 InertiaPlugin（付费）或 GSAP Public 的 ThrowProps 替代。

## 自检

- [ ] 注册了 Draggable 插件？
- [ ] bounds 限制拖拽范围？
- [ ] onRelease 触发持久化？
- [ ] 编辑场景禁惯性？
- [ ] 卸载时 drag.kill()？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`flip-layout.md`](./flip-layout.md)

