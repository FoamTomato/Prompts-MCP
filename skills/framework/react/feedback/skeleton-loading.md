---
name: react-skeleton-loading
description: React 加载态用 Skeleton 骨架屏保留页面结构，不用全屏 Spin 蒙层、不返回 null 白屏。Use when 接 isLoading 渲染占位 / 选 Skeleton vs Spin vs Suspense fallback / 列表卡片加载防跳动时。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - Skeleton
  - 骨架屏
  - Skeleton.Image
  - Skeleton.Button
  - 全屏 Spin
  - Suspense fallback
  - isLoading 占位
effort: medium
context: inline
version: '1.0'
---
# React · Skeleton 骨架屏

## 规则

**房规**:加载态用 `<Skeleton>` 占位保留页面结构,不用全屏 `<Spin>` 蒙层,也不在 `isLoading` 时 `return null` 白屏。Skeleton 形状必须贴合真实内容,加 `active` 走微光动效。

Skeleton 形状贴合内容表:

| 真实内容 | 占位组件 |
|---------|---------|
| 文本段落 | `<Skeleton paragraph={{ rows }} />` |
| 图片/封面 | `<Skeleton.Image active />` |
| 按钮 | `<Skeleton.Button active />` |
| 头像 | `<Skeleton.Avatar active />` |
| 输入框 | `<Skeleton.Input active />` |

Skeleton vs Spin vs Suspense fallback 决策表:

| 场景 | 选择 |
|------|------|
| 首屏 / 区域**已知结构**的数据加载 | **Skeleton**(房规默认),形状贴合内容 |
| 短操作、按钮内反馈(提交/保存) | `<Button loading>` 而非全屏 Spin |
| 懒加载路由 / 分包组件 | `<Suspense fallback={<SkeletonGrid />}>` |

接 `isLoading` 时早返回结构化骨架,且骨架放进与真实数据**同一套栅格**(每个 `<Col>` 放一张骨架卡),让加载前后布局不跳动。

## 反例

```tsx
function TextbookList() {
  const { data, isLoading } = useQuery({ queryKey: ["textbooks"], queryFn: api.list });

  // ❌ 全屏 Spin 蒙层:遮住整页、布局丢失、加载完瞬间撑开抖动
  if (isLoading) return <Spin spinning fullscreen />;
  // ❌ return null:白屏一片,用户以为页面坏了
  // if (isLoading) return null;

  return <Row gutter={[16, 16]}>{data.map(tb => <TextbookCard key={tb.id} item={tb} />)}</Row>;
}
```

## 正例

```tsx
import { Row, Col } from "antd";
import { useQuery } from "@tanstack/react-query";
import { textbooksApi } from "@/api/textbooks";
import { SkeletonCard, SkeletonGrid } from "./SkeletonCard";

function TextbookList() {
  // 取服务端数据
  const { data, isLoading } = useQuery({ queryKey: ["textbooks"], queryFn: textbooksApi.list });

  // 加载态:返回与真实布局同栅格的结构化骨架,加载前后不跳动
  if (isLoading) return <SkeletonGrid count={6} />;

  // 数据态:同一套 Row/Col 栅格渲染真实卡片
  return (
    <Row gutter={[16, 16]}>
      {data.map(tb => (
        <Col key={tb.id} xs={24} sm={12} lg={8}>
          <TextbookCard item={tb} />
        </Col>
      ))}
    </Row>
  );
}
```

> SkeletonCard / SkeletonGrid 的完整实现见 [`skeleton-loading.examples.md`](./skeleton-loading.examples.md):骨架卡形状贴合真实卡片,SkeletonGrid 用同栅格布 N 个。

## 自检

- [ ] 加载态用 Skeleton 占位,没有全屏 Spin 蒙层?
- [ ] `isLoading` 没有 `return null` 白屏?
- [ ] Skeleton 形状贴合真实内容(图用 Image / 按钮用 Button / 头像用 Avatar)?
- [ ] 加了 `active` 动效?
- [ ] 骨架与真实数据同一套栅格,加载前后布局不跳动?
- [ ] 懒加载路由的 Suspense fallback 用 Skeleton 而非 Spin?

## 相关

- 父:[`./index.md`](./index.md)
- 兄弟:[`empty-state.md`](./empty-state.md)(零数据用 Empty,区分无数据/筛空/出错三态)
- 数据源:[`../state/server-state-tanstack.md`](../state/server-state-tanstack.md)(useQuery 的 isLoading)
- 骨架→真数据怎么切(crossfade,别硬切闪一下):[`../../../design/component-patterns/entrance-patterns.md`](../../../design/component-patterns/entrance-patterns.md)
- 示例:[`skeleton-loading.examples.md`](./skeleton-loading.examples.md)
