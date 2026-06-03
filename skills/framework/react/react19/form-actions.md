---
name: react19-form-actions
description: React 19 表单 Actions 三件套 useActionState / useOptimistic / useFormStatus 替手写 onSubmit。Use when 写原生 form 提交 / 要 pending-error 三元组 / 乐观更新回滚 / 子按钮取 pending
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - useActionState
  - useOptimistic
  - useFormStatus
  - form action
  - 表单 Actions
  - 乐观更新
effort: high
context: inline
version: '1.0'
---
# React19 · 表单 Actions

## 规则

**决策点：原生 form Action 还是 antd Form + useMutation？** 按表单形态选，别混用。

| 表单形态 | 选型 | 理由 |
|---------|------|------|
| antd `<Form>`（带 rules/校验/message） | `useMutation`（见跨引） | 复用 antd 校验链 + message 反馈，Action 接不进 antd 校验态 |
| 原生 `<form action={fn}>`、简单/渐进增强 | `useActionState` | 免 onSubmit/preventDefault/loading 样板，无 JS 也能提交 |

三件套职责：
- `useActionState(action, initial)` → 拿 `[result, formAction, isPending]` 三元组，`<form action={formAction}>` 提交即跑，pending/error/result 全托管。
- `useOptimistic(realValue, reducer)` → 提交瞬间先渲染乐观值，action reject 自动回滚到 realValue。
- `useFormStatus()` → 子组件（如提交按钮）就近读 `{ pending }`，免从父层 prop 钻透。

## 反例 · 正例

```tsx
// ❌ 反例：useState 手包 action 的 loading / error，preventDefault 样板
function CommentBox() {
  const [pending, setPending] = useState(false);
  const [error, setError] = useState<string>();
  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setPending(true);              // 手动管 pending
    const res = await postComment(new FormData(e.currentTarget));
    if (res.error) setError(res.error);
    setPending(false);             // 多处 set，易漏 finally
  }
  return <form onSubmit={onSubmit}>...</form>;
}
```

```tsx
// ✅ 正例：useActionState 托管三元组，编排即流程
function CommentBox() {
  // 1. action 返回 result，pending 由 hook 托管
  const [state, formAction, isPending] = useActionState(submitComment, null);
  // 2. action 绑到原生 form，提交即触发
  return (
    <form action={formAction}>
      <input name="text" required />
      {/* 3. 错误来自上一次 action 的返回值 */}
      {state?.error && <Alert type="error" message={state.error} />}
      <SubmitButton />
    </form>
  );
}

// ✅ 子按钮就近取 pending，免父层钻透
function SubmitButton() {
  // 1. 同一 form 内任意子组件可读提交态
  const { pending } = useFormStatus();
  // 2. 编排：pending 时禁用并转圈
  return <Button htmlType="submit" loading={pending} disabled={pending}>发送</Button>;
}
```

完整 useActionState + useOptimistic 自动回滚样例见 [`form-actions.examples.md`](form-actions.examples.md)。

## 自检

- [ ] antd `<Form>` 走的是 useMutation 而非 useActionState？
- [ ] 原生 form 用 `action={formAction}`，没手写 onSubmit/preventDefault？
- [ ] pending/error 来自 useActionState 三元组，没用 useState 手包 loading？
- [ ] 提交按钮用 useFormStatus 取 pending，没从父层 prop 钻透？
- [ ] 乐观更新经 useOptimistic，依赖其自动回滚而非手写 try/catch 复原？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`data-fetching-with-suspense.md`](data-fetching-with-suspense.md) · [`concurrent-rendering.md`](concurrent-rendering.md)
- 跨引：[`../state/server-state-tanstack.md`](../state/server-state-tanstack.md)（antd Form 提交走 useMutation）· [`../../antd/form/validator-pattern.md`](../../antd/form/validator-pattern.md)（antd 校验链）
