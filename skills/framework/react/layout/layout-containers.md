---
name: react-layout-containers
description: antd 布局容器选型房规——Layout/Space/Flex/Divider 各自管什么 + 选哪个 + 页面骨架模式。Use when 搭页面外壳/想用裸 div+手写 flex 排列/纠结 Space 还是 Flex/要加分隔线时。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - Layout Header Sider Content Footer
  - Space
  - Flex
  - Divider
  - hasSider
  - 布局容器
  - 页面骨架
  - 容器选型
effort: medium
context: inline
version: '1.0'
---
# React · antd 布局容器选型

## 规则

**房规:页面外壳与元素排列一律用 antd 布局容器,禁 `<div style={{display:flex}}>` 裸 div + 手写 flex 拼版。** 按下表选容器,选不出再回退裸 div。

| 容器 | 管什么 | 关键 props |
|------|--------|-----------|
| `<Layout>` | 页面外壳(顶/侧/主/底框架) | `Header` `Sider` `Content` `Footer` / `hasSider` |
| `<Space>` | 一行/一列**等距**排小元素(按钮组、标签、图标) | `size` `direction` `wrap` |
| `<Flex>` | 需 `align` / `justify` 的弹性排列(两端对齐、撑满、垂直居中) | `align` `justify` `gap` `vertical` |
| `Row/Col` | 24 栅格分列 / 响应式 → 见 [`./grid-system.md`](./grid-system.md) | `gutter` `span` `xs/sm/md/lg` |
| `<Divider>` | 区块/元素间分隔线 | `orientation` `type="vertical"` |

**决策树**:
- 是整页骨架(有顶栏/侧栏/页脚)→ `<Layout>`
- 一组小元素**等距**摆开,不关心对齐 → `<Space>`
- 要 `justify`(两端/居中)或 `align`(垂直对齐)或撑满剩余 → `<Flex>`
- 要分多列/响应式 → `Row/Col`
- 只是加条分隔线 → `<Divider>`

**Space vs Flex**:等距列表(间距统一、自动 gap)用 `Space`;弹性盒(一端贴边一端撑开、垂直居中)用 `Flex`。需要 `justify-content: space-between` 必然是 `Flex`,不是 `Space`。

## 反例 · 正例

```tsx
// 反例:裸 div + 手写 flex 拼标题栏,无语义、间距硬编码
function PageHeader() {
  return (
    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
      <h2>订单列表</h2>
      <div style={{ display: "flex", gap: 8 }}>
        <Button>导出</Button>
        <Button type="primary">新建</Button>
      </div>
    </div>
  );
}
```

```tsx
// 正例:Flex 管两端对齐,Space 管按钮组等距
import { Flex, Space, Button } from "antd";

function PageHeader() {
  // 标题与操作区两端对齐、垂直居中 → Flex
  // 一组按钮等距排 → Space
  return (
    <Flex justify="space-between" align="center">
      <h2>订单列表</h2>
      <Space size="small">
        <Button>导出</Button>
        <Button type="primary">新建</Button>
      </Space>
    </Flex>
  );
}
```

```tsx
// 页面骨架:Layout 五件套(顶+侧+主+底)。外层竖向包顶栏与「侧+主」,内层 hasSider 横向承载侧栏与内容
import { Layout } from "antd";

const { Header, Sider, Content, Footer } = Layout;

function AppShell() {
  return (
    <Layout>
      <Header>顶栏</Header>
      <Layout hasSider>
        <Sider width={200}>侧栏导航</Sider>
        <Content>主内容区</Content>
      </Layout>
      <Footer>页脚版权</Footer>
    </Layout>
  );
}
```

```tsx
// Divider:行内竖线分隔操作项,块间横线带标题
<Space split={<Divider type="vertical" />}><a>编辑</a><a>删除</a></Space>
<Divider orientation="left">基本信息</Divider>
```

## 自检

- [ ] 排版用 antd 容器(Layout/Space/Flex),而非裸 div + 手写 `display:flex`?
- [ ] 整页骨架用 `<Layout>` 五件套,内层「侧+主」加了 `hasSider`?
- [ ] 等距小元素用 `<Space size>`,需 `justify/align` 才升级到 `<Flex>`?
- [ ] 要 `space-between` / 撑满剩余空间时,确认用的是 `<Flex>` 而非 `<Space>`?
- [ ] 多列/响应式没硬塞进 Flex,而是走 `Row/Col`(见 grid-system)?
- [ ] 分隔线用 `<Divider>`(竖线 `type="vertical"`),而非手画 border?

## 相关

- 父:[`./index.md`](./index.md)
- 兄弟:[`./grid-system.md`](./grid-system.md)(Row/Col 24 栅格分列 / 响应式)
- 跨引:[`../component/spacing-typography.md`](../component/spacing-typography.md)(间距口径)· [`../../antd/index.md`](../../antd/index.md)(antd 组件总览)
