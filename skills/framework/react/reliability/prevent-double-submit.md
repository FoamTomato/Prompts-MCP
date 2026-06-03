---
name: react-prevent-double-submit
description: 提交类操作前端防重复提交 — 用 isPending 锁住按钮 + 非幂等带 Idempotency-Key。Use when 写表单/下单/支付提交 / 按钮被连点重复请求 / 评审 onClick 直接 await 无锁。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - 防重复提交
  - double-submit
  - Idempotency-Key
  - isPending
  - 按钮 loading 锁
  - submit
effort: medium
context: inline
version: '1.0'
---
# React · 防重复提交

## 规则

决策点：**提交类操作（下单/支付/创建）必须在前端加“提交中态锁”防双击，但去重的最终保证在后端**。三招：

| 招式 | 做法 | 说明 |
|------|------|------|
| 按钮锁 | `<Button loading={isPending} disabled={isPending}>` | 提交期间禁用，UI 层挡住连点 |
| 锁源 | 用 `useMutation` 的 `isPending` 当锁 | 不要自己 `useState` 管 loading，状态机交给 Query |
| 幂等键 | 非幂等操作请求头带 `Idempotency-Key` | 同一键重试只生效一次，后端识别 |

前端只做 UI 层防抖；真正幂等去重靠后端（见[相关](#相关)），不可只靠前端锁。

### 反例 — 裸 onClick 直接 await，无锁

```tsx
// ❌ 双击=两次下单：没有提交中态，按钮始终可点
function PayButton({ orderId }: { orderId: string }) {
  return (
    <Button
      type="primary"
      onClick={async () => {
        await ordersApi.pay(orderId); // 第一次未返回前可再次点击
        message.success("支付成功");
      }}
    >
      支付
    </Button>
  );
}
```

### 正例 — isPending 锁 + Idempotency-Key

幂等键生成下沉到 util 纯函数：

```ts
// src/utils/idempotency.ts
export function newIdempotencyKey(): string {
  // 每次发起一笔提交生成一个唯一键，重试复用同一键
  return crypto.randomUUID();
}
```

```tsx
import { Button, message } from "antd";
import { useMutation } from "@tanstack/react-query";
import { newIdempotencyKey } from "@/utils/idempotency";
import { ordersApi } from "@/api/orders";

function PayButton({ orderId }: { orderId: string }) {
  // 锁源：isPending 由 useMutation 维护，不自己 useState 管 loading
  const { mutate, isPending } = useMutation({
    mutationFn: (key: string) =>
      ordersApi.pay(orderId, { headers: { "Idempotency-Key": key } }),
    onSuccess: () => message.success("支付成功"),
    onError: () => message.error("支付失败，请重试"),
  });

  // 编排：本次提交生成幂等键并发起
  const handlePay = () => mutate(newIdempotencyKey());

  // loading + disabled 双重锁住按钮，提交期间挡住连点
  return (
    <Button type="primary" loading={isPending} disabled={isPending} onClick={handlePay}>
      支付
    </Button>
  );
}
```

> 表单场景同理：`<Form onFinish>` 配 `<Button htmlType="submit" loading={isPending} disabled={isPending}>`。

## 自检

- [ ] 提交按钮 `loading={isPending}` 且 `disabled={isPending}`？
- [ ] 锁源用 `useMutation` 的 `isPending`，没有自己 `useState` 管 loading？
- [ ] 非幂等操作（下单/支付/创建）请求头带 `Idempotency-Key`？
- [ ] 没有出现裸 `onClick={async () => await ...}` 无锁提交？
- [ ] 清楚前端锁只防双击，去重最终靠后端幂等？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`race-condition-cancellation.md`](./race-condition-cancellation.md) · [`effect-cleanup-leak.md`](./effect-cleanup-leak.md)
- 跨引：[`../state/server-state-tanstack.md`](../state/server-state-tanstack.md)（isPending 锁源）· [`../../../fundamentals/distributed-theory/idempotent-design.md`](../../../fundamentals/distributed-theory/idempotent-design.md)（后端幂等去重）
