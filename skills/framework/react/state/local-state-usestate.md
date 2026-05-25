---
name: react-local-state-usestate
description: 局部状态用 useState — 不要泄漏到 store
parent: ./index.md
paths:
  - "frontend/src/**/*.tsx"
triggers:
  keywords: [useState, 本地状态]
effort: medium
context: inline
version: "1.0"
---

# React · 局部状态 useState

## 规则

仅当前组件使用、不涉及网络的状态用 `useState`。**不要泄漏到 Zustand**。

## 适用场景

```tsx
function TextbookCard() {
  const [hovered, setHovered] = useState(false);          // 仅本卡片关心 hover
  const [expanded, setExpanded] = useState(false);        // 仅本卡片展开折叠
  const [editing, setEditing] = useState(false);          // 本组件编辑态
}
```

## 何时升级到 Zustand

| 触发 | 升级 |
|------|------|
| 兄弟组件需要读同一状态 | → Zustand（避免 props drilling） |
| 父组件需要触发子组件状态 | → Zustand 或 imperative ref |
| 切页面后需要保留 | → Zustand + persist 或 query state |
| 与服务端数据同步 | → useQuery |

## useReducer 何时用

状态机 / 多动作收敛时用 useReducer：

```tsx
type Action =
  | { type: "open"; data: Slide }
  | { type: "edit"; patch: Partial<Slide> }
  | { type: "save" }
  | { type: "close" };

function reducer(state: EditorState, action: Action): EditorState {
  switch (action.type) {
    case "open":  return { mode: "editing", slide: action.data };
    case "edit":  return { ...state, slide: { ...state.slide, ...action.patch } };
    case "save":  return { ...state, dirty: false };
    case "close": return { mode: "idle", slide: null };
  }
}

const [state, dispatch] = useReducer(reducer, { mode: "idle", slide: null });
```

## 反例

```tsx
// ❌ 三层 props drilling
<A>
  <B count={count} setCount={setCount}>
    <C count={count} setCount={setCount}>
      <D count={count} setCount={setCount} />
    </C>
  </B>
</A>

// ✅ 升级到 Zustand
```

```tsx
// ❌ 整个表单状态用 useState 散开
const [title, setTitle] = useState("");
const [pages, setPages] = useState(10);
const [theme, setTheme] = useState("");
const [difficulty, setDifficulty] = useState("");
// 8+ 字段散落

// ✅ react-hook-form + zod 集中
const { control, handleSubmit } = useForm({ resolver: zodResolver(Schema) });
```

## 自检

- [ ] 状态仅本组件用？是 → useState
- [ ] 跨组件共享？→ Zustand
- [ ] 服务端数据？→ useQuery
- [ ] 多动作收敛？→ useReducer
- [ ] 表单？→ react-hook-form + zod

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`server-state-tanstack.md`](./server-state-tanstack.md) · [`client-state-zustand.md`](./client-state-zustand.md)

