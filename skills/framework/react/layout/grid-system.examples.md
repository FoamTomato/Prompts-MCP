# antd Row/Col 栅格 · 房规五件套全量页面骨架

> 五件套:`Layout` 整页框架 → `Row gutter` 响应式分列 → 每 `Col` 包 `RegionBoundary`(区域 ErrorBoundary)+ `Suspense fallback={<Skeleton/>}` → 列表区 `Skeleton/Empty/错误` 三态分流。
> 全程注释驱动流水线编排:组件体只做编排,逻辑下沉 hook/converter/utils。

## RegionBoundary:区域级 ErrorBoundary + Suspense 复合包裹

```tsx
// src/components/RegionBoundary.tsx
// 房规:每个 Col 内容用本组件兜,单区域崩溃只塌这一格,不连累整页
import { Suspense, type ReactNode } from "react";
import { Skeleton } from "antd";
import { ErrorBoundary } from "@/components/ErrorBoundary";

interface Props {
  children: ReactNode;
  // loading 占位:房规用 Skeleton,不用全屏 Spin
  fallback?: ReactNode;
}

export function RegionBoundary({ children, fallback }: Props) {
  // 先错误兜底,再异步占位:崩溃走 ErrorState,挂起走 Skeleton
  return (
    <ErrorBoundary>
      <Suspense fallback={fallback ?? <Skeleton active paragraph={{ rows: 4 }} />}>
        {children}
      </Suspense>
    </ErrorBoundary>
  );
}
```

## 列表区三态分流:Skeleton / Empty / 错误

```tsx
// src/pages/dashboard/components/OrderListPanel.tsx
import { Card, Skeleton, Empty, Result, List } from "antd";
import { useOrderList } from "../hooks/useOrderList";

interface Props {
  // 由外层筛选条传入,用于区分"无数据"与"筛选无结果"
  hasFilter: boolean;
}

export function OrderListPanel({ hasFilter }: Props) {
  // 取数:loading / error / 数据 三态由 hook 统一吐出
  const { items, isLoading, isError, refetch } = useOrderList();

  // 早返回 1:加载中 → Skeleton 占位(房规不用全屏 Spin)
  if (isLoading) {
    return <Card><Skeleton active paragraph={{ rows: 6 }} /></Card>;
  }
  // 早返回 2:请求出错 → Result 错误态 + 重试,与"无数据"区分
  if (isError) {
    return (
      <Card>
        <Result status="error" title="加载失败" extra={<a onClick={() => refetch()}>重试</a>} />
      </Card>
    );
  }
  // 早返回 3:零数据 → Empty,并按 hasFilter 区分无数据 / 筛选无结果
  if (items.length === 0) {
    return (
      <Card>
        <Empty description={hasFilter ? "无匹配结果,换个筛选条件" : "暂无订单"} />
      </Card>
    );
  }
  // 正常态:数据驱动渲染,map 出列表项,禁手写 for
  return (
    <Card>
      <List
        dataSource={items}
        renderItem={(item) => <List.Item key={item.id}>{item.title}</List.Item>}
      />
    </Card>
  );
}
```

## 全量页面骨架:Layout → 响应式 Row gutter → 每 Col 包 RegionBoundary

```tsx
// src/pages/dashboard/index.tsx
import { Layout, Row, Col } from "antd";
import { RegionBoundary } from "@/components/RegionBoundary";
import { useDashboardFilter } from "./hooks/useDashboardFilter";
import { FilterBar } from "./components/FilterBar";
import { StatCardsRegion } from "./components/StatCardsRegion";
import { TrendChartRegion } from "./components/TrendChartRegion";
import { OrderListPanel } from "./components/OrderListPanel";

const { Header, Content } = Layout;

// 房规 gutter 口径:屏越大间距越大;[水平, 垂直] 双向控间距
const GUTTER = { xs: 8, sm: 16, md: 24, lg: 32 } as const;

export default function DashboardPage() {
  // 筛选态集中到 hook,组件体只做编排
  const { filter, hasFilter, setFilter } = useDashboardFilter();

  // 整页框架:Header 放筛选条,Content 用栅格分列
  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Header>
        {/* 筛选条:受控,改动驱动下方各区重新取数 */}
        <FilterBar value={filter} onChange={setFilter} />
      </Header>

      <Content style={{ padding: 24 }}>
        {/* 第一行:统计卡片,响应式 4 列 → 2 列 → 整行 */}
        <Row gutter={GUTTER}>
          <Col xs={24} sm={12} md={6}>
            <RegionBoundary><StatCardsRegion metric="pv" filter={filter} /></RegionBoundary>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <RegionBoundary><StatCardsRegion metric="cvr" filter={filter} /></RegionBoundary>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <RegionBoundary><StatCardsRegion metric="ret" filter={filter} /></RegionBoundary>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <RegionBoundary><StatCardsRegion metric="gmv" filter={filter} /></RegionBoundary>
          </Col>
        </Row>

        {/* 第二行:左趋势图 + 右订单列表;窄屏堆叠,宽屏 2:1 分栏 */}
        <Row gutter={GUTTER} style={{ marginTop: 24 }}>
          <Col xs={24} lg={16}>
            <RegionBoundary><TrendChartRegion filter={filter} /></RegionBoundary>
          </Col>
          <Col xs={24} lg={8}>
            {/* 列表区自管 Skeleton/Empty/错误三态,无需再套 Suspense 兜 loading */}
            <RegionBoundary fallback={null}>
              <OrderListPanel hasFilter={hasFilter} />
            </RegionBoundary>
          </Col>
        </Row>
      </Content>
    </Layout>
  );
}
```
