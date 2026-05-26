---
name: react-no-business-in-useEffect
description: 禁在 useEffect 拉数据 — 用 TanStack Query；useEffect 仅做 DOM 同步/订阅
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - useEffect
  - fetch
  - useQuery
  - 拉数据
  - 仅做
  - 同步
effort: medium
context: inline
version: '1.0'
---
# React · 禁在 useEffect 拉数据

## 规则

**useEffect 不能用来拉服务端数据**。所有 API 请求一律走 TanStack Query 的 `useQuery` / `useMutation`。

## 反例 → 正例

```tsx
// ❌ useEffect + fetch
function TextbookList() {
  const [data, setData] = useState<Textbook[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    setLoading(true);
    fetch("/api/textbooks")
      .then(r => r.json())
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);
  // 缺：缓存、去重、retry、cancel、stale 标记
}

// ✅ useQuery
function TextbookList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["textbooks"],
    queryFn: () => textbooksApi.list(),
    staleTime: 5 * 60 * 1000,
  });
  // useQuery 自动处理：缓存 / 去重 / retry / cancel / stale / focus refetch
}
```

## useEffect 仅用于这些场景

| 用途 | 例子 |
|------|------|
| DOM 同步 | 操作 ref / 第三方 lib 初始化 |
| 订阅 / 取消订阅 | WebSocket / EventEmitter / window.addEventListener |
| 计时器 | setInterval / setTimeout（含 cleanup） |
| 副作用：localStorage / 第三方 SDK | analytics / sentry |
| 真正与 React 状态无关的全局协调 | 路由变化时的标题更新 |

```tsx
// ✅ DOM 同步
useEffect(() => {
  document.title = `编辑 - ${title}`;
}, [title]);

// ✅ 订阅
useEffect(() => {
  const handler = (e: KeyboardEvent) => { ... };
  window.addEventListener("keydown", handler);
  return () => window.removeEventListener("keydown", handler);
}, []);
```

## SSE 例外

SSE 是流式订阅，不是普通 fetch，**继续用 useEffect 实现**（参考 `useSSE.ts`），不用 useQuery。

## 自检

- [ ] 没有 `useEffect + fetch` 拉数据？
- [ ] 服务端状态用 useQuery？
- [ ] useEffect 仅做 DOM / 订阅 / 计时 / 副作用？
- [ ] useEffect 都有 cleanup 函数？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`order-and-rules.md`](./order-and-rules.md)
- 配套：[`../state/server-state-tanstack.md`](../state/server-state-tanstack.md)

