---
name: typescript-no-floating-promise
description: 禁 floating promise — 必 await 或显式 .catch
parent: ./index.md
paths:
  - "frontend/**/*.ts"
  - "frontend/**/*.tsx"
triggers:
  keywords: [Promise, await, floating promise, unhandled]
effort: medium
context: inline
version: "1.0"
---

# TypeScript · 禁 floating promise

## 规则

任何 Promise 必须被 `await`、`.then`、`.catch`、`void` 或显式赋值。游离的 Promise 在错误时会触发 `unhandled rejection`，难以追溯。

## ESLint 配置

```json
{
  "rules": {
    "@typescript-eslint/no-floating-promises": "error"
  }
}
```

## 反例 → 正例

```ts
// ❌ floating — 错误被吞
async function clickHandler() {
  saveSlide(data);   // 没 await
}

// ✅ await
async function clickHandler() {
  await saveSlide(data);
}

// ✅ 故意 fire-and-forget — 加 void 表态
void saveAnalytics(event);

// ✅ 显式处理失败
saveSlide(data).catch(err => toast.error(err.message));
```

## 在事件回调里

```tsx
// ❌ React 事件回调声明同步，body async 调用没 await
<Button onClick={() => saveSlide(data)} />

// ✅ 加 void
<Button onClick={() => { void saveSlide(data); }} />

// ✅ 或者 async 回调（注意：React 不等待）
<Button onClick={async () => {
  try { await saveSlide(data); }
  catch (e) { toast.error(e.message); }
}} />
```

## 在 useEffect 里

```tsx
// ❌ useEffect 的回调不能 async
useEffect(async () => {
  await fetchData();
}, []);

// ✅ 内部包一层
useEffect(() => {
  void (async () => {
    try { await fetchData(); }
    catch (e) { ... }
  })();
}, []);

// ✅ 更好：用 TanStack Query 替代 useEffect 拉数据
```

## Promise.all / allSettled

```ts
// 多个并发 promise — 同样不能游离
const [a, b, c] = await Promise.all([fetchA(), fetchB(), fetchC()]);

// 允许部分失败用 allSettled
const results = await Promise.allSettled([...]);
results.forEach(r => {
  if (r.status === "rejected") logger.warn("partial failure", r.reason);
});
```

## 自检

- [ ] ESLint `no-floating-promises` 全绿？
- [ ] 事件回调 / setTimeout 内的 async 都用 `void`？
- [ ] useEffect 内不直接 async，包了一层 IIFE 或用 useQuery？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`promise-vs-await.md`](./promise-vs-await.md)

