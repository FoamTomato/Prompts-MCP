---
name: react19-data-fetching-with-suspense
description: React19 用 use(promise)+Suspense 声明式读已建 promise/context，非取数层。Use when 读上游传下的 promise / 条件读 context / 配 Suspense+ErrorBoundary 边界 / 纠结 use 还是 useQuery。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - use(promise)
  - Suspense
  - ErrorBoundary
  - 声明式取数
  - 条件读 context
  - React19
effort: high
context: inline
version: '1.0'
---
# React19 · use() + Suspense 声明式取数

## 规则

决策点：**`use(promise)` 不是取数层，TanStack Query 仍是客户端取数默认**。`use()` 只用来「在渲染里同步读出一个别处已建好的 promise / context」。

| 你手上有什么 | 用什么 |
|--------------|--------|
| 要发起一次 HTTP 请求（缓存/去重/retry/失效） | `useQuery`（[server-state-tanstack](../state/server-state-tanstack.md)） |
| 上游已建好的 promise（props/context/loader 传下来） | `use(promise)` + `<Suspense>` |
| RSC 从服务端传下来的 promise | `use(promise)`（本栈 Vite SPA 无 RSC runtime，几乎用不到） |
| 条件 / 循环里读 context 或 promise | `use()`（Hook 规则唯一例外，见 [order-and-rules](../hook/order-and-rules.md)） |

要点：
- `use()` 可写在 `if` / 循环 / 早返回之后——它是 React19 对 Hook 调用顺序规则的**唯一例外**，普通 Hook 仍不可条件调用。
- 读 promise 必落在 `<Suspense fallback>` 内：pending 由 Suspense 接管；reject 由外层 `<ErrorBoundary>` 接管。**两者成对出现，缺一不可**。
- promise **必须在更外层稳定创建并缓存**（query/loader/context），不要在渲染体内 `use(fetch(...))`——每次渲染新建 promise 会无限挂起。

## 反例 → 正例

```tsx
// ❌ 用 use(fetch()) 顶替 useQuery：丢缓存/去重/retry/失效，且每渲染新建 promise → 无限 pending
function TextbookList() {
  const data = use(fetch("/api/textbooks").then(r => r.json()));
  return data.map((tb: Textbook) => <TextbookCard key={tb.id} textbook={tb} />);
}

// ✅ 取数仍走 TanStack Query（缓存/去重/retry 由 query 层负责）
function TextbookList() {
  // 服务端数据：交给 useQuery，suspense:true 让它接入 Suspense 边界
  const { data } = useSuspenseQuery({ queryKey: ["textbooks"], queryFn: textbooksApi.list });
  return data.map(tb => <TextbookCard key={tb.id} textbook={tb} />);
}
```

```tsx
// ✅ use() 的正经用途：读上游已建好的 promise，配条件读 context
function Profile({ userPromise }: { userPromise: Promise<User> }) {
  // 条件读 context：use() 允许写在 if 之后（Hook 顺序规则的唯一例外）
  if (process.env.NODE_ENV === "development") {
    const theme = use(ThemeContext);
    console.debug("theme", theme);
  }
  // 同步读出上游 promise：pending 抛给 Suspense，reject 抛给 ErrorBoundary
  const user = use(userPromise);
  return <UserCard user={user} />;
}
```

## 自检

- [ ] 发请求场景用了 `useQuery`/`useSuspenseQuery`，没有用 `use(fetch())` 顶替 query 层？
- [ ] `use(promise)` 读的是上游稳定缓存的 promise，没在渲染体内新建？
- [ ] 读 promise 处外层同时有 `<Suspense fallback>`（pending）与 `<ErrorBoundary>`（reject）？
- [ ] 条件/循环里只对 `use()` 这么写，其余 Hook 仍在顶层无条件调用？

## 相关

- 父：[`./index.md`](./index.md)
- 取数默认层：[`../state/server-state-tanstack.md`](../state/server-state-tanstack.md) · [`../hook/no-fetch-in-use-effect.md`](../hook/no-fetch-in-use-effect.md)
- Hook 规则例外：[`../hook/order-and-rules.md`](../hook/order-and-rules.md)
- 完整边界样例：[`data-fetching-with-suspense.examples.md`](data-fetching-with-suspense.examples.md)
