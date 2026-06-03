# Empty 空态 · 完整示例

## 三态判定下沉为纯函数

```tsx
// src/utils/emptyKind.ts —— 三态判定下沉为纯函数,组件只读结果
export type EmptyKind = "no-data" | "no-match";

export function resolveEmptyKind(hasFilter: boolean): EmptyKind {
  // 有 filter 命中 0 → 筛空;否则从未有数据
  return hasFilter ? "no-match" : "no-data";
}
```

## EmptyState 组件:icon/title/description/action 四件套

```tsx
// src/components/EmptyState.tsx
import { type ReactNode } from "react";
import { Empty } from "antd";

interface Props {
  title: string;
  description?: string;
  action?: ReactNode;
}

export function EmptyState({ title, description, action }: Props) {
  // antd Empty:description 承载主文案,children 承载 CTA
  return (
    <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description={title}>
      {description}
      {action}
    </Empty>
  );
}
```

## 页面编排:四态互斥早返回

```tsx
// src/pages/ItemListPage.tsx —— 四态互斥早返回,空态区分无数据/筛空
import { Button, Skeleton } from "antd";
import { EmptyState } from "@/components/EmptyState";
import { ErrorState } from "@/components/ErrorState";
import { resolveEmptyKind } from "@/utils/emptyKind";

export function ItemListPage() {
  const { data, error, isLoading, keyword } = useItemQuery();

  // 1. 加载态:Skeleton 占位(详见兄弟 skeleton-loading.md)
  if (isLoading) return <Skeleton active />;

  // 2. 错误态:出错 ≠ 空,交给 ErrorState 不当空态
  if (error) return <ErrorState error={error} />;

  // 3. 零数据态:按是否有 filter 区分无数据 / 筛空
  if (data.length === 0) {
    const kind = resolveEmptyKind(Boolean(keyword));
    return kind === "no-match" ? (
      <EmptyState
        title="没有匹配结果"
        action={<Button onClick={clearFilter}>清空筛选</Button>}
      />
    ) : (
      <EmptyState
        title="还没有内容"
        action={<Button type="primary" onClick={openCreate}>新建</Button>}
      />
    );
  }

  // 4. 数据态:正常渲染列表
  return <ItemTable dataSource={data} />;
}
```
