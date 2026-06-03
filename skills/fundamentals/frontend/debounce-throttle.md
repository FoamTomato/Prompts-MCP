---
name: fundamentals-frontend-debounce-throttle
description: "防抖 debounce 与节流 throttle 的选型与封装 — 按场景选哪个 + 给多少时延 + React 里怎么固定函数引用。Use when 搜索框输入降频 / scroll-mousemove 降频 / 纠结用 debounce 还是 throttle / debounce 失效。"
parent: ./index.md
paths:
- frontend/src/**/*.ts
- frontend/src/**/*.tsx
- frontend/src/**/*.vue
triggers:
  keywords:
  - 防抖
  - 节流
  - debounce
  - throttle
  - 高频事件降频
  - 输入抖动降频
effort: low
context: inline
version: '1.0'
---

# Fundamentals 前端 · 防抖与节流(决策视角)

## 规则

**决策点：等"安静"才执行→ debounce；要"匀速限频"→ throttle。** 按场景查表，别凭感觉。

| 场景 | 选 | 时延 | 理由 |
|------|----|------|------|
| 搜索框 / 输入联想 / 表单远程校验 | debounce | 300ms | 停打字才发请求，省请求 |
| 窗口 `resize` 结束才重算布局 | debounce | 200ms | 拖拽中不算,松手才算 |
| `scroll` 滚动加载 / `mousemove` 拖拽 / 高频点击重算 | throttle | 16~100ms | 匀速响应,16ms≈60fps |
| 按钮防重复提交 | 都不是 | — | 见 [prevent-double-submit](../../framework/react/reliability/prevent-double-submit.md) |

> debounce：停止触发后等 N ms 才执行,期间再触发重新计时。throttle：每 N ms 最多执行一次。
> 时延为业界参考,需按交互手感自测。

封装为 `utils` 纯函数,组件里只调用、不内联实现。React 优先用 `useDeferredValue` 替代 debounce(见 [concurrent-rendering](../../framework/react/react19/concurrent-rendering.md))；必须 debounce 时用 `useMemo` 固定引用,`useEffect` 卸载时 `cancel`。

### 反例：每次 render 重建 debounce → 计时器立刻被丢弃,防抖失效

```tsx
function Search() {
  const [kw, setKw] = useState('');
  // 反例:每次渲染都 new 一个 debounced 函数,旧定时器被丢,等于没防抖
  const onChange = debounce((v: string) => fetchList(v), 300);
  return <Input value={kw} onChange={(e) => { setKw(e.target.value); onChange(e.target.value); }} />;
}
```

### 正例 React：useMemo 固定引用 + 卸载 cancel

```tsx
// utils/debounce.ts —— 纯函数,带 cancel,组件里不内联
export function debounce<A extends unknown[]>(fn: (...a: A) => void, wait: number) {
  let timer: ReturnType<typeof setTimeout> | undefined;
  const run = (...args: A) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), wait);
  };
  run.cancel = () => clearTimeout(timer);
  return run;
}

function Search({ onQuery }: { onQuery: (kw: string) => void }) {
  const [kw, setKw] = useState('');
  // 用 useMemo 固定 debounced 引用,跨 render 复用同一个定时器
  const debouncedQuery = useMemo(() => debounce(onQuery, 300), [onQuery]);
  // 卸载时取消挂起的定时器,避免内存泄漏与卸载后 setState
  useEffect(() => debouncedQuery.cancel, [debouncedQuery]);
  // 输入即时回显,查询走防抖
  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const next = e.target.value;
    setKw(next);
    debouncedQuery(next);
  };
  return <Input value={kw} onChange={handleChange} placeholder="搜索" />;
}
```

### 正例 Vue3：scroll 用 throttle，组合式封装

```vue
<script setup lang="ts">
import { throttle } from '@/utils/throttle';
// 滚动到底加载,throttle 100ms 匀速触发,避免每像素都判断
const onScroll = throttle((e: Event) => {
  const el = e.target as HTMLElement;
  // 触底判定下沉为纯函数,组件只读结果
  if (reachedBottom(el)) emit('loadMore');
}, 100);
onBeforeUnmount(() => onScroll.cancel?.());
</script>
```

## 自检

- [ ] 选型先查表：等"安静"用 debounce、要"匀速限频"用 throttle，没凭感觉
- [ ] debounce/throttle 实现是 `utils` 纯函数，组件里只调用未内联
- [ ] React 里 debounced 函数用 `useMemo`/`useRef` 固定引用，没每次 render 重建
- [ ] 能用 `useDeferredValue` 的输入降频场景优先用它替代 debounce
- [ ] 组件卸载时 `cancel` 挂起定时器，时延已按手感自测
- [ ] 触底/校验等 >3 行逻辑下沉为纯函数

## 相关

- 上层维度：[`./index.md`](./index.md)
- 按钮防重(非降频)：[`../../framework/react/reliability/prevent-double-submit.md`](../../framework/react/reliability/prevent-double-submit.md)
- React19 替代方案：[`../../framework/react/react19/concurrent-rendering.md`](../../framework/react/react19/concurrent-rendering.md)
- 高频事件为何卡：[`./rendering-pipeline.md`](./rendering-pipeline.md)
