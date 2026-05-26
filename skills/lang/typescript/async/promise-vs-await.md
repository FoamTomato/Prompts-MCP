---
name: typescript-promise-vs-await
description: 优先 async/await — 仅 then/catch 用于副作用编排
parent: ./index.md
paths:
- frontend/**/*.ts
- frontend/**/*.tsx
triggers:
  keywords:
  - async
  - await
  - then
  - catch
  - 优先
  - 用于副作
  - 于副作用
effort: medium
context: inline
version: '1.0'
---
# TypeScript · async/await vs .then

## 规则

**优先 async/await**。`.then` / `.catch` 仅在以下场景用：
1. 顶层副作用编排（如 `init().catch(handleStart)`）
2. 与同步代码混合的小段
3. fire-and-forget（也需配合 `void` / `.catch`）

## 等价对比

```ts
// .then 风格 — 嵌套加深
function loadUser(id: string) {
  return fetchUser(id)
    .then(user => fetchOrders(user.id))
    .then(orders => orders.filter(o => o.active))
    .catch(err => { console.error(err); return []; });
}

// async/await — 线性
async function loadUser(id: string) {
  try {
    const user = await fetchUser(id);
    const orders = await fetchOrders(user.id);
    return orders.filter(o => o.active);
  } catch (err) {
    console.error(err);
    return [];
  }
}
```

## 并发：await 多个 Promise

```ts
// ❌ 串行（无依赖却串）
const user = await fetchUser(id);
const config = await fetchConfig();     // 与 user 无关，应该并发

// ✅ 并发
const [user, config] = await Promise.all([fetchUser(id), fetchConfig()]);
```

## 顶层 Promise（合法的 .then 场景）

```ts
// main.tsx — 启动期副作用
void initializeApp()
  .then(() => console.log("ready"))
  .catch(err => {
    console.error("boot failed", err);
    showFatalErrorUI(err);
  });
```

## 自检

- [ ] 业务逻辑用 async/await 不用 then 链？
- [ ] 多个无依赖请求用 `Promise.all` 并发？
- [ ] 顶层 promise 加了 `.catch` 或 `void`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`no-floating-promise.md`](./no-floating-promise.md)

