---
name: react-region-error-isolation
description: 区域/widget 级 RegionBoundary 隔离 — 在路由级 ErrorBoundary 之上为每个独立栅格区域再包一层细粒度 boundary,单格崩只塌该格。Use when 写仪表盘/多 widget 页面 / 决定 boundary 放置粒度 / 评审栅格区域降级。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - RegionBoundary
  - 区域级隔离
  - widget boundary
  - 栅格降级
  - 细粒度 boundary
  - 单格崩塌
effort: medium
context: inline
version: '1.0'
---
# React · 区域级错误隔离

## 规则

**决策点:boundary 放在哪一层、放多少个。** 路由级与区域级分工互补,本叶只管放置粒度,boundary 实现见兄弟 [`error-boundary.md`](./error-boundary.md)。

| 粒度 | 组件 | 崩溃影响面 | 用在 |
|------|------|-----------|------|
| 路由级(粗) | `ErrorBoundary` | 整页降级为错误页 | page 根节点,见 error-boundary.md |
| 区域级(细) | `RegionBoundary` | 仅该区域降级为小卡,其余区域照常 | 栅格里每个独立 widget |

粒度准则:**一个 boundary = 一个可独立失败的功能单元**。过细则 fallback 卡片噪声泛滥,过粗则失去隔离意义。

`RegionBoundary` 是 `ErrorBoundary` 的薄封装,默认 fallback 是与区域同尺寸的小卡(非全页错误页);配合 `Suspense`——boundary 接 `throw`,`Suspense` 接 pending。

## 反例

```tsx
// 反例:整页一个 boundary,任一 widget 抛错全页塌成错误页
<ErrorBoundary>
  <Row gutter={16}>
    <Col span={12}><RevenueWidget /></Col>
    <Col span={12}><TrafficWidget /></Col>
  </Row>
</ErrorBoundary>
```

## 正例

```tsx
// src/components/RegionBoundary.tsx —— 薄封装,默认 fallback 为同尺寸小卡
import { type ReactNode } from "react";
import { Card, Button, Result } from "antd";
import { ErrorBoundary } from "@/components/ErrorBoundary";

interface Props {
  children: ReactNode;
  title?: string;
}

export function RegionBoundary({ children, title = "该模块" }: Props) {
  // 区域级 fallback:占位与原区域同尺寸,只降级该格不塌全页
  const renderFallback = (_error: Error, reset: () => void) => (
    <Card size="small" styles={{ body: { height: "100%" } }}>
      <Result
        status="warning"
        subTitle={`${title}加载失败`}
        extra={<Button size="small" onClick={reset}>重试</Button>}
      />
    </Card>
  );

  // 委托给底层 ErrorBoundary,仅替换 fallback 渲染策略
  return <ErrorBoundary fallback={renderFallback}>{children}</ErrorBoundary>;
}
```

```tsx
// src/pages/DashboardPage.tsx —— 栅格里每格独立隔离
import { Row, Col, Skeleton } from "antd";
import { Suspense } from "react";
import { RegionBoundary } from "@/components/RegionBoundary";

export function DashboardPage() {
  // 每个 Col 独立包 RegionBoundary + Suspense:boundary 接 throw、Suspense 接 pending
  const widgets = [
    { key: "revenue", title: "营收", node: <RevenueWidget /> },
    { key: "traffic", title: "流量", node: <TrafficWidget /> },
  ];

  // 数组方法链生成栅格,单格崩只塌该格
  return (
    <Row gutter={16}>
      {widgets.map(({ key, title, node }) => (
        <Col key={key} span={12}>
          <RegionBoundary title={title}>
            <Suspense fallback={<Skeleton active />}>{node}</Suspense>
          </RegionBoundary>
        </Col>
      ))}
    </Row>
  );
}
```

## 自检

- [ ] 路由根已有 `ErrorBoundary`,本叶只在其内层加 `RegionBoundary`?
- [ ] 每个可独立失败的 widget/栅格区域单独包一层,而非整页共用一个?
- [ ] fallback 是与区域同尺寸的小卡 + 重试,而非全页错误页?
- [ ] boundary 接同步 throw,pending 交给内层 `Suspense`?
- [ ] 粒度恰当:没有给一句话静态文本也套 boundary(过细)?

## 相关

- 父:[`./index.md`](./index.md)
- 兄弟(实现与路由级用法,本叶不重复):[`./error-boundary.md`](./error-boundary.md)
- 跨引(pending 占位):[`../feedback/skeleton-loading.md`](../feedback/skeleton-loading.md)
- 跨引(栅格布局):[`../layout/grid-system.md`](../layout/grid-system.md)
