---
name: fundamentals-frontend-state-management-thinking
description: "状态管理思想 — 单向数据流(props down / events up)、不可变更新、状态归属与单一数据源(决策视角)。Use when 纠结状态放组件内还是全局库 / setState 不触发更新 / 子组件想改父状态 / 服务端数据要不要进 store。"
parent: ./index.md
paths:
- frontend/src/**/*.ts
- frontend/src/**/*.tsx
- frontend/src/**/*.vue
triggers:
  keywords:
  - 单向数据流
  - 不可变更新
  - 状态归属
  - single source of truth
  - immutable
  - props down events up
  - state colocation
effort: medium
context: inline
version: '1.0'
---

# Fundamentals 前端 · 状态管理思想(决策视角)

## 规则

**核心决策:状态放哪 + 怎么改。** 三条铁律按下表落地,别凭习惯随手 mutate 或一上来就全局。

| 决策点 | 准则 | 反模式 |
|--------|------|--------|
| 数据流向 | 状态自上而下流(props down)、事件自下而上冒(events up) | 子组件直接改父状态 |
| 更新方式 | 不可变:新对象/数组替换,不原地 mutate | `arr.push` / `obj.x=1` 后期望重渲染 |
| 状态归属 | 能局部就局部,跨组件才提升/全局 | 啥都塞全局 store |
| 数据源 | 单一数据源(single source of truth) | 同一份数据存两处,手动同步 |

**状态归属决策梯(从轻到重,够用即停):**

| 范围 | React | Vue3 | 何时升级 |
|------|-------|------|----------|
| 单组件内 | `useState`/`useReducer` | `ref`/`reactive` | 默认起点,见 [local-state-usestate](../../framework/react/state/local-state-usestate.md) |
| 父子几层共享 | 状态提升到最近公共父 | 同左 | 提升后 props 传超 3 层才考虑下一档 |
| 跨树/全局客户端态 | Context / Zustand | Pinia | 见 [client-state-zustand](../../framework/react/state/client-state-zustand.md) · [vue](../../framework/vue/index.md) |
| 服务端态(接口数据) | TanStack Query | Query 层 | 归 query 层,**不进**全局 store,见 [server-state-tanstack](../../framework/react/state/server-state-tanstack.md) |

> 不可变之于框架:React 靠**引用比较**判变化(`prev === next` 则跳过重渲染),原地 mutate 引用没变 → 不更新;Vue3 `reactive` 虽可变量也能触发,但仍建议**可预测的整体替换**,便于追踪与时间旅行调试。

### 反例:子组件改父传入对象 + 原地 mutate → 父不知情、引用未变不重渲染

```tsx
function Child({ user }: { user: User }) {
  // 反例:直接 mutate 父级对象 —— 父持有同一引用,React 判定"没变",不重渲染
  const onRename = () => { user.name = 'new'; };
  return <button onClick={onRename}>{user.name}</button>;
}
```

### 正例 React:events up + 不可变替换

```tsx
// utils/user.ts —— >3 行的更新下沉为纯函数,返回新对象不碰旧的
export const renameUser = (u: User, name: string): User => ({ ...u, name });

function Parent() {
  const [user, setUser] = useState<User>(initialUser);
  // 事件向上冒:子组件只发意图,父级是唯一数据源,负责产出新引用
  const handleRename = (name: string) => setUser((prev) => renameUser(prev, name));
  return <Child user={user} onRename={handleRename} />;
}

function Child({ user, onRename }: { user: User; onRename: (n: string) => void }) {
  // 子组件不持有状态、不 mutate,只把事件冒上去
  return <button onClick={() => onRename('new')}>{user.name}</button>;
}
```

### 正例 Vue3:reactive 也走可预测替换,派生用 computed 不另存

```vue
<script setup lang="ts">
import { ref, computed } from 'vue';
const list = ref<Item[]>([]);
// 不可变更新:整体替换而非 list.value.push,更新路径单一可追踪
const addItem = (item: Item) => { list.value = [...list.value, item]; };
// 派生状态用 computed 实时算,绝不另存一份 state(否则两份数据要手动同步)
const activeCount = computed(() => list.value.filter((i) => i.active).length);
</script>
```

## 自检

- [ ] 数据流单向:props down / events up,子组件不直接改父状态
- [ ] 更新走不可变:新对象/数组替换,无原地 `push`/属性赋值后期望重渲染
- [ ] 状态归属按梯子选:能局部就局部,跨组件才提升,跨树才上 Context/Zustand/Pinia
- [ ] 服务端态归 query 层,没塞进全局 store
- [ ] 单一数据源:同一份数据没存两处手动同步
- [ ] 派生值用 `useMemo`/`computed` 实时算,没另存为 state(见相关)
- [ ] >3 行的更新/转换下沉为 utils 纯函数

## 相关

- 上层维度:[`./index.md`](./index.md)
- 派生状态别存(专项):[`../../framework/react/component/derived-state.md`](../../framework/react/component/derived-state.md)
- 局部态:[`../../framework/react/state/local-state-usestate.md`](../../framework/react/state/local-state-usestate.md)
- 全局客户端态:[`../../framework/react/state/client-state-zustand.md`](../../framework/react/state/client-state-zustand.md)
- 服务端态:[`../../framework/react/state/server-state-tanstack.md`](../../framework/react/state/server-state-tanstack.md)
- Vue 状态:[`../../framework/vue/index.md`](../../framework/vue/index.md)
