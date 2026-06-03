# Skeleton 骨架屏 · 示例

## SkeletonCard — 形状贴合真实卡片

骨架卡逐块对应真实卡片的封面图 / 标题段 / 标签按钮,加载完不撑开抖动。

```tsx
import { Card, Skeleton, Space } from "antd";

// 真实卡片:封面图 + 标题 + 两行描述 + 一个标签按钮
function TextbookCard({ item }: { item: Textbook }) {
  return (
    <Card cover={<img src={item.cover} alt={item.title} />}>
      <Card.Meta title={item.title} description={item.summary} />
      <Button size="small">{item.subject}</Button>
    </Card>
  );
}

// 骨架卡:每一块都贴合上面的真实结构,且 active 走微光动效
function SkeletonCard() {
  return (
    <Card cover={<Skeleton.Image active style={{ width: "100%", height: 160 }} />}>
      {/* 标题段 + 两行描述:用 paragraph rows 占位 */}
      <Skeleton active title paragraph={{ rows: 2 }} />
      {/* 标签按钮:用 Skeleton.Button 占位,尺寸对齐真实按钮 */}
      <Space style={{ marginTop: 8 }}>
        <Skeleton.Button active size="small" />
      </Space>
    </Card>
  );
}
```

## SkeletonGrid — 用同栅格布 N 个骨架卡

与真实列表共用同一套 `Row` / `Col` 配置,保证加载前后零跳动。

```tsx
import { Row, Col } from "antd";
import { SkeletonCard } from "./SkeletonCard";

// 用与真实列表完全相同的 gutter / 断点,布 count 个骨架卡
function SkeletonGrid({ count = 6 }: { count?: number }) {
  // 由 count 生成定长占位数组(纯计算,不手写 for)
  const placeholders = Array.from({ length: count }, (_, i) => i);

  return (
    <Row gutter={[16, 16]}>
      {placeholders.map(i => (
        <Col key={i} xs={24} sm={12} lg={8}>
          <SkeletonCard />
        </Col>
      ))}
    </Row>
  );
}
```

## 头像 + 输入框骨架(表单/详情页)

```tsx
import { Skeleton, Space } from "antd";

// 个人信息块:头像 + 昵称段 + 一个输入框,逐块贴合真实表单
function ProfileSkeleton() {
  return (
    <Space direction="vertical" size="middle" style={{ width: "100%" }}>
      {/* 头像 */}
      <Skeleton.Avatar active size="large" shape="circle" />
      {/* 昵称 + 简介:单行标题 + 一行描述 */}
      <Skeleton active title paragraph={{ rows: 1 }} />
      {/* 输入框:撑满宽度,对齐真实 Input */}
      <Skeleton.Input active block />
    </Space>
  );
}
```

## 懒加载路由 — Suspense fallback 用 Skeleton

```tsx
import { lazy, Suspense } from "react";
import { SkeletonGrid } from "./SkeletonCard";

// 路由分包:懒加载页面组件
const TextbookPage = lazy(() => import("@/pages/TextbookPage"));

function TextbookRoute() {
  // 分包加载期间用结构化 Skeleton 占位,而非全屏 Spin
  return (
    <Suspense fallback={<SkeletonGrid count={6} />}>
      <TextbookPage />
    </Suspense>
  );
}
```
