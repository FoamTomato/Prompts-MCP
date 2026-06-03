---
name: react-race-condition-cancellation
description: 异步取数结果乱序覆盖的两种防护 — AbortController 真取消 / stale-result guard 忽略非最新响应。Use when 写搜索框联想或滚动翻页取数 / 排查后发请求被先到响应覆盖 / 自写 fetch 而非用 TanStack Query 时。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - 竞态
  - 乱序
  - race condition
  - AbortController
  - stale-result guard
  - 陈旧结果丢弃
  - 请求取消
  - 搜索联想
effort: high
context: inline
version: '1.0'
---
# React · 异步竞态与请求取消

## 规则

**任何用 async 结果调 setState 的地方，都要假设响应会乱序到达**：搜索框快速输入 `app` → `apple`，`app` 的响应可能晚于 `apple`；滚动翻页 page2 → page3，page2 的响应可能晚于 page3。先到的旧结果会覆盖后到的新结果，UI 卡在过期数据上。

| 你的取数方式 | 怎么防乱序 |
|------------|-----------|
| **TanStack Query / SWR**（首选） | 默认已处理：缓存 / 去重 / 切 queryKey 时自动取消旧请求，无需手写 |
| 自写 `fetch` / axios | **必须显式上以下两种之一** |
| 方案 A · AbortController | 新请求发起前 `controller.abort()` 真取消旧请求，旧响应进 catch 不 setState |
| 方案 B · stale-result guard | 给每次请求打标（最新 query 值 / 递增 seq），响应回来时比对，非最新就丢弃 |

两种解法**二选一**即可，不必都上。`debounce` 只减少请求量，**不解决乱序**——300ms 内两次输入仍会发两个请求、仍可能乱序，不能替代取消或 guard。

## 反例 → 正例

```tsx
// ❌ async 结果直接 setState，无 guard 无取消：app 晚于 apple 到达会覆盖
function SearchBox() {
  const [list, setList] = useState<Item[]>([]);
  // 每次输入都发请求，谁先到谁覆盖 —— 结果可能是过期的 "app"
  const onChange = (kw: string) => {
    searchApi.query(kw).then(setList);
  };
  return <Input onChange={(e) => onChange(e.target.value)} />;
}
```

```tsx
// ✅ stale-result guard：用 ref 记最新关键词，响应回来比对，非最新直接丢弃
function SearchBox() {
  const [list, setList] = useState<Item[]>([]);
  // 记录当前最新一次请求的关键词，作为有效性判据
  const latestKwRef = useRef("");

  const onChange = async (kw: string) => {
    // 标记本次为最新请求
    latestKwRef.current = kw;
    // 取数
    const items = await searchApi.query(kw);
    // 守卫：响应回来时若已不是最新关键词，丢弃结果不 setState
    if (latestKwRef.current !== kw) return;
    setList(items);
  };

  return <Input onChange={(e) => onChange(e.target.value)} />;
}
```

完整可运行的两种写法（useEffect + AbortController 真取消、依赖驱动的 stale guard）见 [`race-condition-cancellation.examples.md`](./race-condition-cancellation.examples.md)。

## 自检

- [ ] 每处 async 结果 setState 都已假设响应乱序，上了取消或 guard 之一？
- [ ] 优先用 TanStack Query / SWR，确认其切 key 自动取消已覆盖本场景？
- [ ] 自写 fetch 的搜索联想 / 滚动翻页，明确选了 AbortController 或 stale guard？
- [ ] 没有把 debounce 当作防乱序手段（它只减请求量）？
- [ ] AbortController 方案在 useEffect cleanup / 下次请求前调了 `abort()`？

## 相关

- 父：[`./index.md`](./index.md)
- 配套：[`../state/server-state-tanstack.md`](../state/server-state-tanstack.md)（首选方案，默认已处理取消去重）
- 配套：[`../hook/no-fetch-in-use-effect.md`](../hook/no-fetch-in-use-effect.md)（别在 useEffect 裸 fetch，走 useQuery）
- 跨引：[`../../../lang/typescript/closure/pitfalls.md`](../../../lang/typescript/closure/pitfalls.md)（异步回调捕获引用非快照，guard 比对要用 ref）
