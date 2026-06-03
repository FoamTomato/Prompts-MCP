# React19 表单 Actions 完整样例

## useActionState：原生表单提交，托管 pending / error / result 三元组

```tsx
import { useActionState } from "react";
import { useFormStatus } from "react-dom";
import { Button, Input, Alert } from "antd";
import { feedbackApi } from "@/api/feedback";
import { parseFeedbackForm } from "@/utils/feedback-form";

type FeedbackState = { ok: true; id: string } | { ok: false; error: string } | null;

// action 是纯异步函数：入参 (上次 state, FormData)，出参新 state
async function submitFeedback(_prev: FeedbackState, formData: FormData): Promise<FeedbackState> {
  // 1. FormData → DTO 的解析+校验下沉 util，action 体只编排
  const dto = parseFeedbackForm(formData);
  // 2. 前置校验失败早返回错误态
  if (!dto.ok) return { ok: false, error: dto.message };
  // 3. 提交后端，失败转错误态
  const res = await feedbackApi.create(dto.value);
  if (!res.success) return { ok: false, error: res.message };
  // 4. 成功态带回 id
  return { ok: true, id: res.data.id };
}

export function FeedbackForm() {
  // 1. 三元组：result(上次返回) / formAction(绑 form) / isPending(提交中)
  const [state, formAction, isPending] = useActionState(submitFeedback, null);
  // 2. action 绑原生 form，提交即跑，无需 onSubmit/preventDefault
  return (
    <form action={formAction}>
      <Input name="title" placeholder="标题" required />
      <Input.TextArea name="content" placeholder="内容" rows={4} required />
      {/* 3. 错误态来自上次 action 返回 */}
      {state && !state.ok && <Alert type="error" message={state.error} showIcon />}
      {/* 4. 成功态反馈 */}
      {state?.ok && <Alert type="success" message={`已提交 #${state.id}`} showIcon />}
      <SubmitButton pendingHint={isPending} />
    </form>
  );
}

function SubmitButton({ pendingHint }: { pendingHint: boolean }) {
  // 1. useFormStatus 就近读提交态，免父层 prop 钻透
  const { pending } = useFormStatus();
  // 2. 编排：任一 pending 信号为真即禁用转圈
  return (
    <Button htmlType="submit" type="primary" loading={pending || pendingHint} disabled={pending}>
      提交
    </Button>
  );
}
```

## useOptimistic：乐观更新，action 出错自动回滚

```tsx
import { useActionState, useOptimistic } from "react";
import { List, Input, Button } from "antd";
import { todoApi } from "@/api/todo";
import { buildOptimisticTodo, appendTodo } from "@/utils/todo";

type Todo = { id: string; text: string; sending?: boolean };

export function TodoList({ todos }: { todos: Todo[] }) {
  // 1. 乐观态：reducer 把待发条目并入真实列表
  const [optimisticTodos, addOptimistic] = useOptimistic<Todo[], string>(
    todos,
    (current, text) => appendTodo(current, buildOptimisticTodo(text)),
  );

  // 2. action 内先推乐观值，再发请求；reject 时 React 自动回滚到 todos
  const [, formAction] = useActionState(async (_prev: null, formData: FormData) => {
    const text = String(formData.get("text") ?? "").trim();
    if (!text) return null;
    // 提交瞬间先渲染乐观条目
    addOptimistic(text);
    // 请求失败抛错 → optimisticTodos 自动丢弃乐观值
    await todoApi.create({ text });
    return null;
  }, null);

  // 3. 渲染乐观列表：sending 条目灰显
  return (
    <>
      <form action={formAction}>
        <Input name="text" placeholder="新增待办" />
        <Button htmlType="submit">添加</Button>
      </form>
      <List
        dataSource={optimisticTodos}
        renderItem={(todo) => (
          <List.Item style={{ opacity: todo.sending ? 0.5 : 1 }}>{todo.text}</List.Item>
        )}
      />
    </>
  );
}
```

## 对照：antd Form 仍走 useMutation（不接 Action）

```tsx
import { Form, Input, Button, message } from "antd";
import { useMutation } from "@tanstack/react-query";
import { profileApi } from "@/api/profile";

export function ProfileForm() {
  const [form] = Form.useForm();
  // 1. antd 校验链 + message 反馈交给 useMutation，Action 接不进 antd 校验态
  const { mutate, isPending } = useMutation({
    mutationFn: (values: ProfileDto) => profileApi.save(values),
    onSuccess: () => message.success("已保存"),
    onError: (e) => message.error(e.message),
  });
  // 2. onFinish 仅在 antd 校验通过后触发
  return (
    <Form form={form} layout="vertical" onFinish={(values) => mutate(values)}>
      <Form.Item name="nickname" label="昵称" rules={[{ required: true }]}>
        <Input />
      </Form.Item>
      <Button htmlType="submit" type="primary" loading={isPending}>保存</Button>
    </Form>
  );
}
```
