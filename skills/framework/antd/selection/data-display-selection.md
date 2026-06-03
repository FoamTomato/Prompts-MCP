---
name: antd-data-display-selection
description: 数据展示选型，按数据形状定承载组件 Table / List / Descriptions / Card / Tree。Use when 呈现数据纠结 Table 还是 List / 展示单实体属性该用 Descriptions / 浏览封面卡在 Card 栅格与 List grid 间犹豫。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
triggers:
  keywords:
  - Table
  - List
  - Descriptions
  - Card
  - Tree
  - 数据展示
  - 数据形状
  - data display
effort: medium
context: inline
version: '1.0'
---
# antd · 数据展示选型

## 规则

决策点先看数据形状，再看交互诉求。

| 数据形状 | 选 | 判据 |
|---------|----|-----|
| 同构行 × 多可比列，要排序/筛选/分页 | `Table` | 列要横向对齐、跨行比较 |
| 竖向流，每项 1-2 字段 + 富自定义渲染 | `List` | 卡片块堆叠、无列对齐诉求 |
| 单实体的键值属性 | `Descriptions` | 一条记录的详情面板 |
| 视觉差异化、可浏览项（封面 + 元信息） | `Card` 栅格 | 缩略图驱动浏览 |
| 父子层级、可展开收起 | `Tree` | 嵌套节点导航 |

补充两条近义辨析：

- **Table vs List**：列要横向对比对齐 → `Table`；每项是独立卡片块、列宽无意义 → `List`。
- **Card 栅格 vs List grid**：标准元信息卡用 `List` 的 `grid` 属性即可；高度差异化的业务卡（特殊封面/徽章/交互）→ 自研外壳，见 [`../when-antd-vs-custom.md`](../when-antd-vs-custom.md)。

服务端分页见 [`../table/pagination-server-side.md`](../table/pagination-server-side.md)；`rowKey` 用稳定 id 见 [`../table/row-key-stable.md`](../table/row-key-stable.md)。

## 反例·正例

```tsx
// 反例：单条记录的键值属性硬塞进单行 Table —— 列语义被浪费，详情面板该用 Descriptions
function UserDetailBad({ user }: { user: User }) {
  const columns = [
    { title: '姓名', dataIndex: 'name' },
    { title: '邮箱', dataIndex: 'email' },
    { title: '部门', dataIndex: 'dept' },
  ];
  return <Table rowKey="id" columns={columns} dataSource={[user]} pagination={false} />;
}
```

```tsx
// 正例：单实体键值属性用 Descriptions
function UserDetail({ user }: { user: User }) {
  // 步骤 1：把领域对象拍平成 Descriptions 条目（>3 行转换下沉到 converter）
  const items = toUserDescItems(user);

  // 步骤 2：编排只读详情面板，body 内无嵌套逻辑
  return (
    <Descriptions title="用户详情" column={2} bordered items={items} />
  );
}
```

```tsx
// 正例：同构行多列要排序分页 → Table，rowKey 用稳定 id，分页交给服务端
function OrderTable({ data, total, onPageChange }: OrderTableProps) {
  // 步骤 1：列定义声明可比字段与排序能力
  const columns = buildOrderColumns();

  // 步骤 2：编排表格，分页受控、页码变化回调上抛
  return (
    <Table
      rowKey="orderId"
      columns={columns}
      dataSource={data}
      pagination={{ total, onChange: onPageChange }}
    />
  );
}
```

```tsx
// 正例：可浏览的标准元信息项 → List 的 grid,避免手写栅格 div
function TemplateGallery({ templates }: { templates: Template[] }) {
  // 步骤 1：渲染单项,响应式列数交给 grid,不手写 for
  const renderItem = (t: Template) => (
    <List.Item key={t.id}>
      <Card cover={<img alt={t.name} src={t.cover} />}>{t.name}</Card>
    </List.Item>
  );

  // 步骤 2：编排栅格列表
  return (
    <List grid={{ gutter: 16, xs: 1, sm: 2, md: 3, lg: 4 }} dataSource={templates} renderItem={renderItem} />
  );
}
```

## 自检

- [ ] 选型先问数据形状（同构行 / 竖向流 / 单实体 / 浏览项 / 层级），再问交互诉求。
- [ ] 单条记录详情用 `Descriptions`,没有把它塞进单行 `Table`。
- [ ] 要列对齐和跨行比较才用 `Table`；卡片块堆叠用 `List`。
- [ ] 标准元信息卡用 `List` 的 `grid`,没有手写栅格 div。
- [ ] 高度差异化的业务卡走自研外壳,而非硬撑 antd `Card`。
- [ ] `Table` 已用稳定 `rowKey` 且分页走服务端。

## 相关

- 父：[`./index.md`](./index.md)
- 前置：[`../when-antd-vs-custom.md`](../when-antd-vs-custom.md)（差异化业务卡何时自研）
- 跨引：[`../table/pagination-server-side.md`](../table/pagination-server-side.md) · [`../table/row-key-stable.md`](../table/row-key-stable.md)
- 兄弟：[`./input-selection.md`](./input-selection.md)（采集值而非只读呈现时改用输入选型）
