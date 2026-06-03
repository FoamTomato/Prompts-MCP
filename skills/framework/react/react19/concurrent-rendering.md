---
name: react19-concurrent-rendering
description: React 并发渲染防卡顿 — useTransition 标记非紧急更新 / useDeferredValue 延迟昂贵派生值。Use when tab 切换或筛选 apply 卡顿 / 受控输入传昂贵列表掉帧 / 加微 loading 不阻塞输入 / 替换 setTimeout debounce
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - useTransition
  - useDeferredValue
  - startTransition
  - isPending
  - 并发渲染
  - 输入卡顿
  - 非紧急更新
effort: medium
context: inline
version: '1.0'
---
# React19 · 并发渲染防卡顿

## 规则

**决策点：你拥有触发重更新的 setter，还是只收到一个快变的值？** 按这个分叉选 API，别混用。

| 你手里有什么 | 选型 | 怎么用 |
|-------------|------|--------|
| 拥有触发重更新的 setter（tab 切换、筛选 apply、排序） | `useTransition` | `startTransition(() => setX(next))` 包裹 setter，拿 `isPending` 显示微 loading |
| 只收到一个快变值、包不到 setter（受控 input 的 value 传给昂贵列表） | `useDeferredValue` | `const deferred = useDeferredValue(value)`，把 `deferred` 喂给昂贵子树 |

- 紧急更新（输入框回显、点击高亮）走普通 state，永远不延迟，保证不掉帧。
- `isPending`/旧值期间渲染 `<Spin>` 或降透明度，给"正在算"的反馈，但输入本身不被阻塞。
- 这是**调度优先级**手段，不替代服务端分页 / 虚拟化：列表本身太大仍要 `react-window` + 后端分页降数据量。

## 反例 · 正例

```tsx
// ❌ 反例：手写 setTimeout debounce 延迟昂贵列表，状态/清理样板多
function ProductSearch({ all }: { all: Product[] }) {
  const [text, setText] = useState('');
  const [query, setQuery] = useState('');
  useEffect(() => {
    const t = setTimeout(() => setQuery(text), 300); // 手动 debounce
    return () => clearTimeout(t);                     // 还得清定时器
  }, [text]);
  return <HeavyList items={filterBy(all, query)} />;  // 延迟仍是固定 300ms
}
```

```tsx
// ✅ 正例 A：只有值 → useDeferredValue，受控输入即时回显、昂贵列表延迟派生
function ProductSearch({ all }: { all: Product[] }) {
  const [text, setText] = useState('');
  // 1. 派生延迟值：text 突变时 deferred 暂留旧值，让输入先渲染
  const deferredText = useDeferredValue(text);
  // 2. 昂贵过滤只跟 deferred 走（filterBy 是纯函数，下沉到 utils）
  const items = useMemo(() => filterBy(all, deferredText), [all, deferredText]);
  // 3. 列表落后于输入时降透明度，提示正在算，但不阻塞打字
  const isStale = text !== deferredText;
  return (
    <>
      <Input value={text} onChange={(e) => setText(e.target.value)} allowClear />
      <div style={{ opacity: isStale ? 0.6 : 1 }}>
        <HeavyList items={items} />
      </div>
    </>
  );
}
```

```tsx
// ✅ 正例 B：拥有 setter（tab 切换）→ useTransition 包裹，isPending 显示微 loading
function ReportTabs({ tabs }: { tabs: TabConf[] }) {
  const [active, setActive] = useState(tabs[0].key);
  // 1. 拿到标记非紧急更新的入口
  const [isPending, startTransition] = useTransition();
  // 2. 切 tab 时把昂贵的 active 更新标记为非紧急，旧 tab 内容保留可交互
  const onChange = (key: string) => startTransition(() => setActive(key));
  // 3. pending 时给微 loading,切换不阻塞当前界面
  return (
    <>
      <Tabs activeKey={active} items={tabs} onChange={onChange} />
      {isPending && <Spin size="small" />}
      <HeavyPanel tabKey={active} />
    </>
  );
}
```

## 自检

- [ ] 拥有 setter（tab/筛选/排序）用 useTransition + startTransition 包裹，而非 useDeferredValue？
- [ ] 只收到受控值、包不到 setter，才用 useDeferredValue 延迟派生?
- [ ] 紧急更新（输入回显/点击高亮）走普通 state，没被一起延迟？
- [ ] 用 isPending / 旧值对比显示微 loading，且输入不被阻塞？
- [ ] 没用 setTimeout 手写 debounce 来"模拟"延迟更新？
- [ ] 列表数据量大时，另配服务端分页 / 虚拟化降量，没把并发 API 当性能银弹？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`react-compiler-memo.md`](react-compiler-memo.md)（昂贵派生的 useMemo 何时可省）· [`data-fetching-with-suspense.md`](data-fetching-with-suspense.md)
- 跨引：[`../../antd/index.md`](../../antd/index.md)（Input / Tabs / Spin 组件）
