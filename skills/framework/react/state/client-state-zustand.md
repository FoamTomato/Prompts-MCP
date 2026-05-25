---
name: react-client-state-zustand
description: 客户端全局状态 Zustand + immer middleware
parent: ./index.md
paths:
  - "frontend/src/stores/**/*.ts"
  - "frontend/src/**/*.tsx"
triggers:
  keywords: [Zustand, store, create, immer]
effort: medium
context: inline
version: "1.0"
---

# React · 全局客户端状态 Zustand

## 规则

跨组件共享、非来自后端的状态用 Zustand + immer middleware。

## Store 模板

```ts
// src/stores/editor.ts
import { create } from "zustand";
import { immer } from "zustand/middleware/immer";

interface EditorState {
  selectedSlideId: string | null;
  selectedElementIds: string[];
  zoom: number;
  rightPanelTab: "design" | "style" | "ai" | "animation";

  selectSlide: (id: string) => void;
  selectElements: (ids: string[]) => void;
  setZoom: (z: number) => void;
  setRightPanelTab: (tab: EditorState["rightPanelTab"]) => void;
}

export const useEditorStore = create<EditorState>()(
  immer((set) => ({
    selectedSlideId: null,
    selectedElementIds: [],
    zoom: 1,
    rightPanelTab: "design",

    selectSlide: (id) => set((s) => {
      s.selectedSlideId = id;
      s.selectedElementIds = [];
    }),
    selectElements: (ids) => set((s) => { s.selectedElementIds = ids; }),
    setZoom: (z) => set((s) => { s.zoom = Math.max(0.25, Math.min(4, z)); }),
    setRightPanelTab: (tab) => set((s) => { s.rightPanelTab = tab; }),
  }))
);
```

## 使用：只订阅必需字段

```tsx
// ❌ 订阅整个 store（任何字段变化都重渲染）
const store = useEditorStore();

// ✅ 只订阅 zoom
const zoom = useEditorStore(s => s.zoom);
const setZoom = useEditorStore(s => s.setZoom);

// ✅ 多个字段用 shallow 比较
import { useShallow } from "zustand/react/shallow";
const { selectedSlideId, zoom } = useEditorStore(useShallow(s => ({
  selectedSlideId: s.selectedSlideId,
  zoom: s.zoom,
})));
```

## 拆分原则

按页面 / 领域拆，**单 store 字段不超过 15 个**。Quill 主要 stores：

| Store | 职责 |
|-------|------|
| `useSessionStore` | 匿名 session、用户偏好 |
| `useEditorStore` | 编辑器选中 / 缩放 / Tab |
| `useUndoStore` | 撤销栈 |
| `usePresentStore` | 演示模式状态机 |

## 持久化（按需）

```ts
import { persist } from "zustand/middleware";

export const useSessionStore = create<SessionState>()(
  persist(
    immer((set) => ({ ... })),
    { name: "quill-session" }
  )
);
```

## 反例

```ts
// ❌ 跨页面塞进一个大 store
export const useGlobalStore = create(() => ({
  // 50+ 字段，散漫到处用
}));

// ❌ 服务端数据塞进 zustand
export const useStore = create(() => ({
  textbooks: [],   // 应该用 useQuery
  loadTextbooks: async () => { ... }
}));
```

## 自检

- [ ] 一个 store 字段 ≤ 15？
- [ ] 只订阅需要的字段（用 selector）？
- [ ] 不把服务端数据塞 zustand？
- [ ] 跨字段访问用 useShallow？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`server-state-tanstack.md`](./server-state-tanstack.md) · [`local-state-usestate.md`](./local-state-usestate.md)

