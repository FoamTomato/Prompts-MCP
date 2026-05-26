---
name: antd-table-row-key
description: Table rowKey 必用稳定 id，禁用 index。Use when 写 React 组件 / 改 .tsx 文件 / 评审涉及
  `row-key-stable` 的 PR。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
triggers:
  keywords:
  - Table
  - rowKey
  - key
  - 必用稳定
effort: medium
context: inline
version: '1.0'
---
# antd · Table rowKey 用稳定 id

## 规则

`<Table rowKey="id">` **必须**用业务稳定 id，禁用 `index`。

## 反例 → 正例

```tsx
// ❌ rowKey 用 index
<Table rowKey={(_, i) => i} dataSource={items} columns={...} />
// 删除一行后 React diff 会错乱，行内状态（展开 / 选中 / 编辑态）跳行

// ❌ rowKey 用 Math.random
<Table rowKey={() => Math.random()} ... />
// 每次渲染 key 都变，所有行重新 mount

// ✅ rowKey 用业务 id
<Table rowKey="id" dataSource={items} columns={...} />
<Table rowKey={r => r.uuid} ... />
```

## 完整模板

```tsx
import { Table } from "antd";
import type { TableColumnsType } from "antd";

interface Textbook {
  id: string;
  name: string;
  subject: string;
  grade: string;
  created_at: string;
}

const columns: TableColumnsType<Textbook> = [
  { title: "课本名", dataIndex: "name", key: "name", ellipsis: true },
  { title: "学科", dataIndex: "subject", key: "subject", width: 100 },
  { title: "年级", dataIndex: "grade", key: "grade", width: 100 },
  {
    title: "创建时间",
    dataIndex: "created_at",
    key: "created_at",
    width: 180,
    render: (v: string) => dayjs(v).format("YYYY-MM-DD HH:mm"),
  },
  {
    title: "操作",
    key: "action",
    width: 160,
    render: (_, r) => (
      <Space>
        <Button size="small" onClick={() => handleEdit(r.id)}>编辑</Button>
        <Button size="small" danger onClick={() => handleDelete(r.id)}>删除</Button>
      </Space>
    ),
  },
];

<Table<Textbook>
  rowKey="id"
  dataSource={data}
  columns={columns}
  loading={isLoading}
  pagination={{ ... }}
/>
```

## 列 key

`columns` 数组里每个 column 也要有 `key`（如 dataIndex 不唯一）。

## expandedRowKeys 等

行内状态用 rowKey 关联：

```tsx
const [expanded, setExpanded] = useState<string[]>([]);

<Table
  rowKey="id"
  expandable={{
    expandedRowKeys: expanded,
    onExpandedRowsChange: (keys) => setExpanded(keys as string[]),
  }}
/>
```

## 自检

- [ ] rowKey 是业务稳定 id（不是 index / random）？
- [ ] columns 数组里每个有 key？
- [ ] expandedRowKeys / selectedRowKeys 与 rowKey 类型对齐？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`pagination-server-side.md`](./pagination-server-side.md)

