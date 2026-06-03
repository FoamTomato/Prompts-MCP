---
name: framework-react-react19-index
description: React 19 新特性集合：use + Suspense 取数 / Actions 表单提交 / 并发渲染调度 / React Compiler 自动记忆化 / useEffectEvent。Use when 用 React19+ 新写法重构组件 / 替换 useEffect 取数为 Suspense / 表单改 Actions / 删手写 useMemo
parent: ../index.md
children:
  - { name: data-fetching-with-suspense, path: data-fetching-with-suspense.md, tag: skill, note: use(promise) + Suspense 边界取数，替代 useEffect+loading 态 }
  - { name: form-actions, path: form-actions.md, tag: skill, note: form action / useActionState / useFormStatus 提交，替代手写 onSubmit }
  - { name: concurrent-rendering, path: concurrent-rendering.md, tag: skill, note: useTransition / useDeferredValue 标记非紧急更新，防输入卡顿 }
  - { name: react-compiler-memo, path: react-compiler-memo.md, tag: skill, note: React Compiler 自动记忆化，何时不再手写 useMemo/useCallback/memo }
  - { name: effect-event, path: effect-event.md, tag: skill, note: useEffectEvent 把非响应式逻辑移出 effect 依赖，需 19.2+ }
when_to_descend: |
  用 React19+ 新写法时下钻。本仓 React 已升级到 19+，可直接用 use / Actions / 并发 API。
  房规：本栈是 Vite SPA，默认无 RSC，叶子按客户端组件写；useEffectEvent 需 React 19.2+ 才稳定可用；
  React Compiler 需在构建里手动开启（babel-plugin-react-compiler / vite 插件），未开则仍按需手写记忆化。
---

# React 19 · 新特性

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| data-fetching-with-suspense | 叶 | use(promise) + Suspense 取数 |
| form-actions | 叶 | Actions 表单提交三件套 |
| concurrent-rendering | 叶 | useTransition / useDeferredValue |
| react-compiler-memo | 叶 | Compiler 自动记忆化边界 |
| effect-event | 叶 | useEffectEvent 隔离非响应式逻辑 |

## 何时下钻

- 异步取数想去掉 loading/error 样板 → `data-fetching-with-suspense.md`
- 表单提交、乐观更新、pending 态 → `form-actions.md`
- 输入框 / 大列表过滤卡顿,要分优先级 → `concurrent-rendering.md`
- 想删手写 useMemo/useCallback/memo 或纠结要不要加 → `react-compiler-memo.md`
- effect 里读了 prop/state 又不想它进依赖数组 → `effect-event.md`

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../hook/index.md`](../hook/index.md) · [`../state/index.md`](../state/index.md) · [`../error-handling/index.md`](../error-handling/index.md)
- 跨引：[`../../antd/index.md`](../../antd/index.md)（表单组件配 Actions 用）
