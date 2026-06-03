---
name: react-grid-system
description: antd Row/Col 24 栅格分列排版 + 响应式断点 + gutter 间距房规。Use when 页面要分多列/做响应式分栏/想用 flex 裸 div 拼多列/选 gutter 间距时。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - Row Col
  - 24 栅格
  - gutter
  - 响应式断点
  - span
  - offset push pull
  - 分列布局
  - grid
effort: medium
context: inline
version: '1.0'
---
# React · antd Row/Col 24 栅格

## 规则

**房规:每页用 `<Row><Col>` 栅格分列,禁 `display:flex` 裸 div 拼多列;一行总宽固定 24 列。** 基础写法 `<Row gutter={[h,v]}><Col span={n}>`,同行各 `span` 之和 ≤24,超出自动换行到下一行。

**响应式断点**(给 `Col` 配各档 `span`,跨档自动重排):

| 断点 | 宽度 | 含义 | 常用 span |
|------|------|------|-----------|
| xs | <576 | 手机竖 | 24(整行) |
| sm | ≥576 | 手机横 | 12(两列) |
| md | ≥768 | 平板 | 8(三列) |
| lg | ≥992 | 笔记本 | 6(四列) |
| xl | ≥1200 | 桌面 | 6 |
| xxl | ≥1600 | 宽屏 | 4(六列) |

**响应式 gutter(房规口径)**:`gutter={{ xs: 8, sm: 16, md: 24, lg: 32 }}`,屏越大间距越大;`gutter={[水平, 垂直]}` 同时控行内水平与换行后垂直间距。

**何时换行 vs 滚动**:列数随屏自适应、内容可堆叠 → 用断点 span 让 `Row` 换行;列宽固定不可压缩(宽表格/时间轴)→ 不靠栅格,外层套横向滚动容器。

## 反例 · 正例

```tsx
// 反例:裸 flex + 手写 style 拼三列,无栅格语义、不响应式
function StatRow() {
  return (
    <div style={{ display: "flex", gap: 16 }}>
      <div style={{ flex: 1 }}>访问量</div>
      <div style={{ flex: 1 }}>转化率</div>
      <div style={{ flex: 1 }}>留存</div>
    </div>
  );
}
```

```tsx
// 正例:Row/Col 24 栅格 + 响应式 span + 房规 gutter,数据驱动列
import { Row, Col, Card } from "antd";

const STATS = [
  { key: "pv", title: "访问量" },
  { key: "cvr", title: "转化率" },
  { key: "ret", title: "留存" },
] as const;

function StatRow() {
  // 用 map 渲染列,禁手写 for;窄屏整行、宽屏三列
  return (
    <Row gutter={{ xs: 8, sm: 16, md: 24, lg: 32 }}>
      {STATS.map((s) => (
        <Col key={s.key} xs={24} sm={12} md={8} lg={6}>
          <Card>{s.title}</Card>
        </Col>
      ))}
    </Row>
  );
}
```

```tsx
// offset:右移留白(8+offset8 让两块各占 1/3 居中)
<Row><Col span={8} offset={8}><Card>居中块</Card></Col></Row>

// push / pull:视觉换位,主内容渲染在前但展示在右
<Row>
  <Col span={18} push={6}><Card>主内容(展示在右)</Card></Col>
  <Col span={6} pull={18}><Card>侧栏(展示在左)</Card></Col>
</Row>
```

## 自检

- [ ] 多列布局用 `Row/Col`,而非 `display:flex` 裸 div?
- [ ] 同行 `span` 之和 ≤24(超出确认是想换行)?
- [ ] 列配了响应式断点 `xs/sm/md/lg`,而非写死单一 `span`?
- [ ] `gutter` 用房规口径 `{ xs:8, sm:16, md:24, lg:32 }` 或 `[水平,垂直]` 双向?
- [ ] 列由数据 `map` 出,而非手写重复 `<Col>`?

## 相关

- 父:[`./index.md`](./index.md)
- 兄弟:[`./layout-containers.md`](./layout-containers.md)(选 Layout/Space/Flex/Divider 容器)
- 全量页面骨架(五件套):[`./grid-system.examples.md`](./grid-system.examples.md)
- 跨引:[`../feedback/index.md`](../feedback/index.md)(列内 Skeleton/Empty)· [`../error-handling/error-boundary.md`](../error-handling/error-boundary.md)(区域 boundary)
