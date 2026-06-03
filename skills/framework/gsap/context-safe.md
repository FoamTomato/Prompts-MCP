---
name: gsap-context-safe
description: useGSAP 的 contextSafe — 点击/setTimeout/异步里建的动画不被 scope 自动清理，必须 contextSafe 包裹。Use when 事件回调里写 gsap.to / 切路由后动画残留报错 / 选择器命中了组件外元素 / 交互动画卸载没清理时。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
triggers:
  keywords:
  - contextSafe
  - 事件回调动画
  - can't set property null
  - 动画卸载泄漏
  - 点击动画
  - gsap event handler cleanup
effort: medium
context: inline
version: '1.0'
---
# GSAP · contextSafe 交互动画

## 一句话规则

`useGSAP(() => {...})` 回调**执行那一刻**创建的动画才自动进 scope、自动清理。**之后**才触发的动画（点击 / `setTimeout` / `await` 后 / 任何延迟），scope 抓不到，必须用 `contextSafe` 包裹。

```tsx
const { contextSafe } = useGSAP({ scope: rootRef });   // ① 拿到 contextSafe

// ② 事件回调里的动画，包一层
const onClick = contextSafe(() => {
  gsap.to(".box", { rotation: 180, duration: D.base, ease: E.out });
});

return <button ref={rootRef} onClick={onClick}>转</button>;
```

## 为什么

useGSAP 用 `gsap.context()` 收集动画。同步阶段（hook 跑的时候）创建的会被登记，组件卸载自动 revert。但点击发生在「以后」，那时 context 已收尾——不包 contextSafe 的话：

- 动画**不随组件卸载清理** → 内存泄漏、切走后仍在跑、报 `can't set property on null`。
- 选择器**不被 scope 限定** → `".box"` 命中全页面而非组件内。

## 两种写法

```tsx
// 写法 A：onClick 等 JSX 事件用此（默认选这个）
const onClick = contextSafe(() => gsap.to(".box", { x: 100 }));

// 写法 B：需要手动 addEventListener 时用此（GSAP 把 contextSafe 作为第二参传入）
useGSAP((context, contextSafe) => {
  const onClick = contextSafe!(() => gsap.to(".box", { x: 100 }));
  buttonRef.current!.addEventListener("click", onClick);
  // 手动 addEventListener 时，useGSAP 会自动帮你移除监听
}, { scope: rootRef });
```

手动 `addEventListener` 在 useGSAP callback 里挂的，卸载时也会自动 `removeEventListener`——但前提是回调 contextSafe 化。

## 反例

```tsx
// ❌ 事件回调里裸 gsap.to —— 不清理、选择器逃出 scope
function Card() {
  useGSAP(() => {}, { scope: ref });
  const onClick = () => gsap.to(".box", { x: 100 });   // 漏 contextSafe
  return <div ref={ref} onClick={onClick}>...</div>;
}

// ❌ setTimeout / await 之后建动画也一样要包
const onSave = contextSafe(async () => {
  await api.save();
  gsap.to(".toast", { y: 0 });   // ✅ 整个 async 包在 contextSafe 内
});
```

## 自检

- [ ] 点击 / 延迟 / async 后创建的动画都 `contextSafe` 包了？
- [ ] contextSafe 从 `useGSAP({scope})` 返回值或第二参拿，而非自己造？
- [ ] 提供了 `scope: ref`，让选择器限定在组件内？
- [ ] 没有在事件回调里写裸 `gsap.to()`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟（同步阶段动画）：[`use-gsap-hook.md`](./use-gsap-hook.md)
- 集中 timeline：[`timeline-organization.md`](./timeline-organization.md)
