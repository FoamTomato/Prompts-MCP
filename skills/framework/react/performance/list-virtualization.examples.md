# React 长列表虚拟化 · 代码示例

## 1. FixedSizeList + memo Row(等高列表,基础版)

```tsx
import React, { useCallback } from "react";
import { FixedSizeList, type ListChildComponentProps } from "react-window";

interface User {
  id: string;
  name: string;
  email: string;
}

// Row 提到组件外 + React.memo:滚动时仅可视区行重渲染,且引用稳定不破坏 memo
const UserRow = React.memo(
  ({ index, style, data }: ListChildComponentProps<User[]>) => {
    // 取当前行数据,行体仅渲染几个节点
    const user = data[index];
    return (
      <div style={style} className="user-row">
        <span>{user.name}</span>
        <span>{user.email}</span>
      </div>
    );
  }
);
UserRow.displayName = "UserRow";

export function UserVirtualList({ users }: { users: User[] }) {
  // itemKey 用稳定业务 id:数据增删时按身份复用 DOM,不会错位
  const itemKey = useCallback(
    (index: number, data: User[]) => data[index].id,
    []
  );

  // 可视区列表:等高 48px,overscan 5 行防快速滚动露白
  return (
    <FixedSizeList
      height={600}
      width="100%"
      itemCount={users.length}
      itemSize={48}
      itemData={users}
      overscanCount={5}
      itemKey={itemKey}
    >
      {UserRow}
    </FixedSizeList>
  );
}
```

## 2. 接入无限滚动(react-window-infinite-loader + 服务端分页)

```tsx
import React, { useCallback, useState } from "react";
import { FixedSizeList, type ListChildComponentProps } from "react-window";
import InfiniteLoader from "react-window-infinite-loader";
import { useInfiniteQuery } from "@tanstack/react-query";
import { usersApi } from "@/api/users";

interface User {
  id: string;
  name: string;
}

const ROW_HEIGHT = 48;
const PAGE_SIZE = 50;

// Row 提外 + memo;末尾 loading 占位行单独判断
const UserRow = React.memo(
  ({ index, style, data }: ListChildComponentProps<User[]>) => {
    // 已加载行渲染数据,未加载位渲染 loading 占位
    const user = data[index];
    return <div style={style}>{user ? user.name : "加载中…"}</div>;
  }
);
UserRow.displayName = "UserRow";

export function InfiniteUserList() {
  const [containerHeight] = useState(600);

  // 数据仍走服务端分页接口:虚拟化只管渲染量,分页归后端
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage } =
    useInfiniteQuery({
      queryKey: ["users", "infinite"],
      queryFn: ({ pageParam = 1 }) =>
        usersApi.list({ page: pageParam, size: PAGE_SIZE }),
      getNextPageParam: (last) =>
        last.page * last.size < last.total ? last.page + 1 : undefined,
    });

  // 拍平各页为单一数组,交给 windowing 渲染
  const users = (data?.pages ?? []).flatMap((p) => p.items);

  // itemCount 末尾留一格给 loading 行(hasNextPage 时 +1)
  const itemCount = hasNextPage ? users.length + 1 : users.length;

  // 判断某行是否已加载:超出已加载长度即未加载
  const isItemLoaded = useCallback(
    (index: number) => !hasNextPage || index < users.length,
    [hasNextPage, users.length]
  );

  // 加载更多:正在拉取时返回 noop 避免重复触发
  const loadMoreItems = useCallback(
    () => (isFetchingNextPage ? Promise.resolve() : fetchNextPage().then(() => {})),
    [isFetchingNextPage, fetchNextPage]
  );

  // itemKey:已加载用业务 id,占位行用固定 key
  const itemKey = useCallback(
    (index: number) => users[index]?.id ?? `placeholder-${index}`,
    [users]
  );

  return (
    <InfiniteLoader
      isItemLoaded={isItemLoaded}
      itemCount={itemCount}
      loadMoreItems={loadMoreItems}
    >
      {({ onItemsRendered, ref }) => (
        <FixedSizeList
          ref={ref}
          height={containerHeight}
          width="100%"
          itemCount={itemCount}
          itemSize={ROW_HEIGHT}
          itemData={users}
          overscanCount={5}
          itemKey={itemKey}
          onItemsRendered={onItemsRendered}
        >
          {UserRow}
        </FixedSizeList>
      )}
    </InfiniteLoader>
  );
}
```
