---
name: react-state-completeness
description: 组件状态完备 — 默认/悬停/焦点/激活/加载/禁用/错误/空态。Use when 写 React 组件 / 改 .tsx 文件 / 评审涉及
  `state-completeness` 的 PR。
parent: ./index.md
paths:
- frontend/src/components/**/*.tsx
- frontend/src/features/**/*.tsx
triggers:
  keywords:
  - 状态
  - hover
  - focus
  - disabled
  - loading
  - empty
effort: medium
context: inline
version: '1.0'
---
# React · 8 种状态完备

## 规则

每个交互组件必须显式实现 **8 种状态**，缺一不可：

| # | 状态 | 触发 | 视觉 |
|---|------|------|------|
| 1 | 默认 | 加载完成无交互 | 标准 border + bg |
| 2 | 悬停 | mouse enter | border 加深 + transform translateY(-2px) |
| 3 | 焦点 | tab 聚焦 | outline 2px accent |
| 4 | 激活 | mouse down / 选中 | border-color: accent + bg: accent-50 |
| 5 | 加载 | data fetching | Skeleton 占位 / Spin 蒙层 |
| 6 | 禁用 | aria-disabled / disabled | opacity 0.5 + cursor: not-allowed |
| 7 | 错误 | API 失败 / 校验失败 | red border + error message |
| 8 | 空态 | 数据 0 行 | EmptyState 组件 + CTA |

## 模板

```tsx
function ArticleList() {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["articles"],
    queryFn: () => articlesApi.list(),
  });

  // 5. 加载
  if (isLoading) return <SkeletonGrid count={6} />;

  // 7. 错误
  if (error) {
    return (
      <ErrorState
        title="加载失败"
        description={error.message}
        action={<Button onClick={() => refetch()}>重试</Button>}
      />
    );
  }

  // 8. 空态
  if (!data || data.length === 0) {
    return (
      <EmptyState
        icon={<BookIcon />}
        title="还没有内容"
        description="浏览目录开始你的第一份内容"
        action={<Button type="primary">浏览目录</Button>}
      />
    );
  }

  // 1-4. 默认 / 悬停 / 焦点 / 激活 在每个卡片内
  return (
    <div className="grid">
      {data.map(item => <ArticleCard key={item.id} article={item} />)}
    </div>
  );
}
```

## 反例

```tsx
// ❌ 只考虑成功路径
if (!data) return null;   // 加载 / 错误 / 空态全没有
return <Grid items={data} />;

// ❌ 加载用旋转 spinner 占满屏（用户不知道结构）
if (isLoading) return <FullScreenSpin />;

// ✅ 用 Skeleton 保留结构
if (isLoading) return <SkeletonGrid count={6} />;
```

## 推荐公共组件

- `<Skeleton>` / `<SkeletonGrid>` — `frontend/src/components/Skeleton.tsx`
- `<ErrorState>` — `frontend/src/components/ErrorState.tsx`
- `<EmptyState>` — `frontend/src/features/dashboard/EmptyState.tsx`

## 自检

- [ ] 8 种状态各有实现（或明确决策"本组件无 X 状态因为 Y"）？
- [ ] 加载用 Skeleton 不用全屏 Spin？
- [ ] 错误状态可重试（不是死页）？
- [ ] 空态有 CTA 引导用户下一步？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`flat-ui-principles.md`](./flat-ui-principles.md)
