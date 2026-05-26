---
name: react-server-state-tanstack
description: 服务端状态用 TanStack Query — 缓存/重试/失效。Use when 写 React 组件 / 改 .tsx 文件 / 评审涉及
  `server-state-tanstack` 的 PR。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
- frontend/src/api/**/*
triggers:
  keywords:
  - TanStack
  - useQuery
  - useMutation
  - react-query
  - 服务端状态用
  - 失效
effort: medium
context: inline
version: '1.0'
---
# React · 服务端状态 TanStack Query

## 规则

凡是来自后端的数据，**一律**用 `useQuery` / `useMutation`。

## 标准用法

```tsx
import { useQuery } from "@tanstack/react-query";
import { textbooksApi } from "@/api/textbooks";

function TextbookList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["textbooks"],
    queryFn: () => textbooksApi.list(),
    staleTime: 5 * 60 * 1000,
  });

  if (isLoading) return <SkeletonGrid count={6} />;
  if (error) return <ErrorState onRetry={() => refetch()} />;
  return data?.map(tb => <TextbookCard key={tb.id} textbook={tb} />);
}
```

## queryKey 命名约定

```ts
["textbooks"]                          // 列表
["textbooks", { subject: "math" }]     // 带 filter
["textbook", id]                       // 详情
["textbook", id, "chapters"]           // 嵌套资源
```

## Mutation + 乐观更新

```tsx
const queryClient = useQueryClient();

const updateSlide = useMutation({
  mutationFn: (data: SlidePatch) => slidesApi.update(slideId, data),

  onMutate: async (data) => {
    await queryClient.cancelQueries({ queryKey: ["slide", slideId] });
    const prev = queryClient.getQueryData(["slide", slideId]);
    queryClient.setQueryData(["slide", slideId], (old: Slide) => ({ ...old, ...data }));
    return { prev };
  },

  onError: (_err, _data, ctx) => {
    queryClient.setQueryData(["slide", slideId], ctx?.prev);
    toast.error("保存失败，已恢复");
  },

  onSettled: () => {
    queryClient.invalidateQueries({ queryKey: ["slide", slideId] });
  },
});
```

## 全局配置

```tsx
// src/main.tsx
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000,
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

<QueryClientProvider client={queryClient}>...</QueryClientProvider>
```

## 禁忌

- ❌ `useEffect + fetch + useState`
- ❌ Redux Saga / Thunk 拉数据
- ❌ 一个 query 调多个 endpoint（拆成多个 query）

## 自检

- [ ] 服务端数据用 useQuery？
- [ ] queryKey 唯一可去重？
- [ ] mutation 有 onError 回滚？
- [ ] mutation 后 invalidateQueries 触发刷新？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`client-state-zustand.md`](./client-state-zustand.md) · [`local-state-usestate.md`](./local-state-usestate.md)

