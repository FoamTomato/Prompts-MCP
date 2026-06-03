---
name: react-re-render-minimization
description: 消除多余 re-render — 先定位再 memo、稳定 prop 引用、内联 object/array/fn prop 反模式。Use when 子组件无谓重渲染 / 手写 React.memo 或 useMemo/useCallback / 排查 re-render 性能。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - re-render
  - 重渲染
  - React.memo
  - useMemo
  - useCallback
  - 内联 prop
  - referential equality
effort: medium
context: inline
version: '1.0'
---
# React · 消除多余 re-render

## 规则

决策点:**默认不手动 memo;先用 Profiler 定位到具体子组件无谓重渲染,再针对性优化。** 顺序如下:

| 步骤 | 做什么 | 注意 |
|------|--------|------|
| 1 | React DevTools Profiler 录制,定位真正重渲染的子组件 | 没测量就 memo = 瞎优化 |
| 2 | 检查父传下的 **内联 prop** 是否每次新引用 | `style={{}}` / `data={[]}` / `onClick={()=>{}}` 都是 |
| 3 | 子组件包 `React.memo`,父侧用 `useMemo`/`useCallback` 稳定引用 | 三件套必须配套,缺一失效 |

**前置:** 本条讲**手写** memo 的定位与做法。项目若启用 React 19 Compiler,要不要手写、能否删手写,见 [`../react19/react-compiler-memo.md`](../react19/react-compiler-memo.md)。

**何时不优化:** 渲染廉价(纯文本/几个节点)、列表很短时,手动 memo 是负收益(比较开销 + 心智负担 > 收益)。**先测量再决定。**

**禁:** render 阶段调 `setState`(`setX()` 直接写在函数体)→ 触发渲染循环。状态派生用计算,副作用进 `useEffect`/事件回调。

## 反例 · 正例

```tsx
// ❌ 内联 prop:每次父渲染都造新引用,React.memo(Child) 永远失效
function Toolbar({ items }: { items: Item[] }) {
  return <Child style={{ padding: 8 }} data={[]} onClick={() => save()} />;
}

// ✅ 三件套:常量提组件外 + useMemo 稳定值 + useCallback 稳定回调
const PANEL_STYLE = { padding: 8 } as const;

function Toolbar({ items }: { items: Item[] }) {
  // 派生数据 useMemo 稳定引用(>3 行计算应下沉 utils 纯函数)
  const sortedItems = useMemo(() => sortItemsByWeight(items), [items]);
  // 回调 useCallback 稳定引用
  const handleSave = useCallback(() => save(), []);
  return <Child style={PANEL_STYLE} data={sortedItems} onClick={handleSave} />;
}
```

详见 [`re-render-minimization.examples.md`](./re-render-minimization.examples.md):内联 prop bug 完整 before/after、三件套修复。

## 自检

- [ ] 先用 Profiler 定位了具体重渲染的子组件,而非全局盲目 memo?
- [ ] 若项目启用了 React Compiler,先看 react-compiler-memo 再决定要不要手写?
- [ ] 传给 `React.memo` 子组件的 prop 没有内联 `{}`/`[]`/`()=>{}`(新引用)?
- [ ] `React.memo` + `useMemo`/`useCallback` 三件套配套使用,没有只包一半?
- [ ] 渲染廉价/列表短的组件没有过度 memo(测量证明有收益才加)?
- [ ] render 阶段没有调用 `setState`(无渲染循环)?

## 相关

- 父:[`./index.md`](./index.md)
- 兄弟:[`state-completeness.md`](./state-completeness.md)
- 跨引:[`../performance/index.md`](../performance/index.md)(React 性能整体策略)· [`../react19/index.md`](../react19/index.md)(React 19 新能力/Compiler)· [`../hook/order-and-rules.md`](../hook/order-and-rules.md)(Hook 规则与依赖数组)
