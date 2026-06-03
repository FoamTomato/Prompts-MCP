---
name: react19-effect-event
description: React19.2+ 用 useEffectEvent 把「读最新值但不该触发重跑」的非响应式逻辑移出 effect 依赖。Use when effect 上报埋点要读最新 props/state / 依赖放会变的值致频繁重跑 / 省略依赖致 stale closure / 纠结变量该不该进依赖。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - useEffectEvent
  - 非响应式依赖
  - stale closure
  - 陈旧闭包
  - effect 依赖数组
  - 埋点上报
effort: high
context: inline
version: '1.0'
---
# React19 · useEffectEvent 修陈旧闭包

## 规则

决策点：**effect 要读某值的最新值，但该值变化不该触发 effect 重跑（非响应式）→ 抽到 `useEffectEvent`，且不放进依赖数组**。需 React **19.2+**。

| effect 里读的值 | 它该触发重跑吗 | 处理 |
|-----------------|----------------|------|
| 真正决定「何时重订阅/重连」的值（url、roomId） | 是，响应式 | 放进依赖数组 |
| 只是「重跑时顺手读一下最新」的值（最新 props/state/埋点参数） | 否，非响应式 | 抽进 `useEffectEvent`，不进依赖 |

要点：
- `useEffectEvent` 返回的函数**永远闭包到最新值**，调用它不算建立响应式依赖，故依赖数组里**不放它**。
- 它**只能在 effect 内部调用**，不能传给子组件、不能当普通事件处理器（onClick 用普通函数即可）。
- 别用它来糊「依赖列不全的 lint 警告」——只有「确实非响应式」的值才抽出去；真正的响应式依赖仍要老实进数组。

## 反例 → 正例

```tsx
// ❌ 把会变的 plan 放进依赖：plan 一变就重连，url 没变也重连 → 频繁重跑
function ChatRoom({ url, plan }: { url: string; plan: Plan }) {
  useEffect(() => {
    const conn = createConnection(url);
    conn.on("connected", () => track("connected", { plan }));
    conn.connect();
    return () => conn.disconnect();
  }, [url, plan]); // plan 变也重连
}

// ❌ 省略 plan 躲重跑:连接里读到的永远是首次渲染的 plan(stale closure)
function ChatRoom({ url, plan }: { url: string; plan: Plan }) {
  useEffect(() => {
    const conn = createConnection(url);
    conn.on("connected", () => track("connected", { plan })); // 永远第一次的 plan
    conn.connect();
    return () => conn.disconnect();
  }, [url]); // eslint-disable 掩盖
}
```

```tsx
// ✅ plan 非响应式:抽进 useEffectEvent,只在 url 变时重连,埋点读最新 plan
function ChatRoom({ url, plan }: { url: string; plan: Plan }) {
  // 非响应式逻辑:上报埋点要读最新 plan,但 plan 变不该重连
  const onConnected = useEffectEvent(() => {
    track("connected", { plan }); // 调用时拿到最新 plan
  });

  // effect 只依赖真正响应式的 url:url 变才重连
  useEffect(() => {
    const conn = createConnection(url);
    conn.on("connected", onConnected); // effect 内调用,不进依赖
    conn.connect();
    return () => conn.disconnect();
  }, [url]); // 仅 url,无 plan/onConnected,lint 通过
}
```

## 自检

- [ ] 抽出去的值确实「非响应式」(只想读最新、不想触发重跑),而非为躲 lint 硬塞?
- [ ] 真正决定重跑时机的响应式值(url/roomId)仍老实留在依赖数组?
- [ ] `useEffectEvent` 返回的函数没进依赖数组,且只在 effect 内部调用(没传子组件/没当 onClick)?
- [ ] 项目 React 版本 ≥ 19.2,确认 API 稳定可用?

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`data-fetching-with-suspense.md`](./data-fetching-with-suspense.md) · [`concurrent-rendering.md`](./concurrent-rendering.md)
- Hook 依赖规则：[`../hook/order-and-rules.md`](../hook/order-and-rules.md)
- 闭包陷阱原理：[`../../../lang/typescript/closure/pitfalls.md`](../../../lang/typescript/closure/pitfalls.md)
