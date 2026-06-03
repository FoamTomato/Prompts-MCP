---
name: closure-pitfalls
description: TypeScript 三类原生闭包坑 — 循环 var 共享绑定打末值 / 异步回调捕获引用非快照 / 长生命周期闭包持有大对象致内存泄漏。Use when 写循环内回调 / 写定时器或事件监听 / 设计缓存闭包持有 DOM 或大对象时。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - 闭包
  - closure
  - setTimeout
  - addEventListener
  - clearInterval
  - WeakMap
  - 循环变量捕获
  - memory leak
effort: medium
context: inline
version: '1.0'
---
# TypeScript · 原生闭包三坑

## 规则

闭包捕获的是**变量绑定**，不是值快照；决策点见下表。

| 坑 | 现象 | 解 |
|----|------|----|
| 循环 var 共享绑定 | `for(var i)` 内 setTimeout 全打末值 | 用 `let` 块级,每轮一新绑定;或 IIFE 传参 |
| 异步回调捕获引用 | 回调执行时读到的是变更后的值 | 入参传值快照,或 `const` 冻结当轮值 |
| 长生命周期闭包持有引用 | 全局缓存/未解绑监听/未清定时器 钉住大对象或 DOM | `removeEventListener` · `clearInterval` · `WeakMap` 弱引用 |

> 本 skill 只覆盖原生闭包;React Hooks 的 stale closure(依赖数组/useRef)见 framework/react,不在此。

## 坑1 循环变量捕获

```ts
// ❌ var 函数级单一绑定 — 三个回调共享同一个 i,循环结束 i===3,全打 3
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 0);
}

// ✅ let 块级 — 每轮迭代新建绑定,各自捕获 0/1/2
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 0);
}

// ✅ 必须留 var 时,用 IIFE 把当轮值作实参传入,形成独立作用域
for (var j = 0; j < 3; j++) {
  ((captured: number) => setTimeout(() => console.log(captured), 0))(j);
}
```

## 坑2 异步回调捕获引用而非快照

```ts
// ❌ 闭包捕获 user 这个绑定;await 期间外部改写,回调读到的是改写后的值
async function track(user: { id: string }): Promise<void> {
  setTimeout(() => report(user.id), 1000);
  user = await refreshUser(user.id); // 重新赋值,1s 后回调读到新 user
}

// ✅ 进回调前用 const 冻结当轮值快照,异步期间外部变更不影响
async function track(user: { id: string }): Promise<void> {
  // 快照当前 id,脱离后续对 user 的重新赋值
  const snapshotId = user.id;
  setTimeout(() => report(snapshotId), 1000);
  await refreshUser(snapshotId);
}
```

## 坑3 长生命周期闭包内存泄漏

```tsx
import { useEffect, useRef } from 'react';

// ❌ 监听器/定时器闭包钉住组件级大对象,卸载后仍驻留 → 泄漏
function attachLeaky(node: HTMLElement, payload: BigData): void {
  node.addEventListener('scroll', () => consume(payload)); // 没解绑
  setInterval(() => consume(payload), 1000);               // 没清
}

// ✅ 持有具名引用,生命周期结束显式释放;effect return 即清理钩子
function useScrollGuard(node: HTMLElement, payload: BigData): void {
  useEffect(() => {
    // 具名函数与定时器 id,供后续精确解绑
    const onScroll = (): void => consume(payload);
    const timer = window.setInterval(() => consume(payload), 1000);
    node.addEventListener('scroll', onScroll);
    // 卸载时解绑监听 + 清定时器,断开闭包对 payload 的强引用
    return () => {
      node.removeEventListener('scroll', onScroll);
      clearInterval(timer);
    };
  }, [node, payload]);
}

// ✅ 全局缓存用 WeakMap,key(DOM/对象)无外部引用时连同 value 一并被回收
const domMetaCache = new WeakMap<HTMLElement, BigData>();
```

## 自检

- [ ] 循环内创建回调/闭包,用了 `let` 或 IIFE,没残留 `for(var i)`?
- [ ] 异步回调依赖的变量,在注册前用 `const` 快照,而非捕获会被重新赋值的绑定?
- [ ] 每个 `addEventListener` 有配对 `removeEventListener`、每个定时器有 `clearInterval`?
- [ ] 缓存 DOM/大对象的全局结构用了 `WeakMap` 而非长驻 `Map`?

## 相关

- 父：[`./index.md`](./index.md)
- 跨引：[`../async/no-floating-promise.md`](../async/no-floating-promise.md)
