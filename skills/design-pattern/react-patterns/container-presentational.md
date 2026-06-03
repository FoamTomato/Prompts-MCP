---
name: react-container-presentational
description: "把取数+状态逻辑(容器/hook)与纯渲染(展示组件,只收 props 无副作用)分离,展示层易测易复用易 Storybook。Use when 取数与渲染揉在一个大组件 / 想让展示组件可单测可 Storybook / 同一份 UI 复用于多个数据源时。"
parent: ./index.md
paths:
- frontend/src/**/*.tsx
triggers:
  keywords:
  - container presentational
  - 容器组件
  - 展示组件
  - presentational component
  - 取数与渲染分离
  - 纯渲染组件
effort: low
context: inline
version: '1.0'
---
# Design Pattern · 容器/展示分离

## 规则

**决策点:这段代码在"拿数据"还是在"画 UI"?** 拿数据→容器(自定义 hook 承载逻辑);画 UI→展示组件(纯函数、只收 props、零副作用)。

| 层 | 职责 | 约束 |
|----|------|------|
| 容器 | 取数、订阅、状态、回调编排 | 现代做法用 `useXxx` hook 承载,不再写 class 容器 |
| 展示 | 把 props 渲染成 JSX | 纯函数、无 `useEffect`/`fetch`/全局状态,回调一律 props 注入 |

逻辑下沉到 hook 见 [`./custom-hook-extraction.md`](./custom-hook-extraction.md)。**何时不必拆:** 极简组件(一处取数 + 几行 JSX、不复用、无需单测/Storybook)别硬拆,徒增间接层。

## 反例:取数与渲染耦合在一个大组件

```tsx
// ❌ 请求、loading、渲染全堆一起:无法单独测 UI,也无法在 Storybook 喂假数据
function OrderList() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(false);
  useEffect(() => {
    setLoading(true);
    fetch("/api/orders").then((r) => r.json()).then((d) => { setOrders(d); setLoading(false); });
  }, []);
  if (loading) return <Spin />;
  return <List dataSource={orders} renderItem={(o) => <List.Item>{o.title}</List.Item>} />;
}
```

## 正例:useOrders hook(容器) + 纯展示组件

```tsx
// frontend/src/features/order/useOrders.ts —— 容器逻辑:取数 + 状态,不含任何 JSX
import { useEffect, useState } from "react";
import { fetchOrders } from "@/api/order";

interface OrdersState {
  orders: Order[];
  loading: boolean;
}

export function useOrders(): OrdersState {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // 取消令牌:卸载时中断在途请求
    const ctrl = new AbortController();
    // 取数:请求下沉 api 层纯函数,signal 透传以支持取消
    setLoading(true);
    fetchOrders(ctrl.signal).then((list) => {
      setOrders(list);
      setLoading(false);
    });
    return () => ctrl.abort();
  }, []);

  return { orders, loading }; // 多个相关项→返回对象,展示侧按需解构
}
```

```tsx
// frontend/src/features/order/OrderListView.tsx —— 纯展示:只收 props,无副作用,易测易 Storybook
interface OrderListViewProps {
  orders: Order[];
  loading: boolean;
}

export function OrderListView({ orders, loading }: OrderListViewProps) {
  // 前置:加载中早返回,渲染体保持平坦
  if (loading) return <Spin />;
  // 渲染:列表用 antd renderItem 映射,不手写 for
  return (
    <List
      dataSource={orders}
      renderItem={(order) => <List.Item key={order.id}>{order.title}</List.Item>}
    />
  );
}

// 装配:容器 hook 喂数据给纯展示组件,各司其职
function OrderListPage() {
  const { orders, loading } = useOrders();
  return <OrderListView orders={orders} loading={loading} />;
}
```

## 自检

- [ ] 展示组件是纯函数?(无 `useEffect`/`fetch`/全局状态读写,数据与回调全经 props)
- [ ] 取数与状态逻辑收敛在 `useXxx` hook(而非 class 容器),副作用有清理函数取消在途请求?
- [ ] 展示组件能脱离真实接口单测、能在 Storybook 喂假数据?
- [ ] 极简且不复用的组件没有为拆而拆?

## 相关

- 父:[`./index.md`](./index.md)
- 逻辑承载:[`./custom-hook-extraction.md`](./custom-hook-extraction.md)
- 目录分层:[`../../framework/react/component/folder-layering.md`](../../framework/react/component/folder-layering.md)
