---
name: antd-table-pagination-server
description: Table 分页一律走服务端 — 禁前端全量
parent: ./index.md
paths:
  - "frontend/src/**/*.tsx"
  - "frontend/src/api/**/*"
triggers:
  keywords: [Table, pagination, 分页]
effort: medium
context: inline
version: "1.0"
---

# antd · Table 服务端分页

## 规则

数据行数 > 50 时**强制走服务端分页**，禁前端 `dataSource` 一次性塞所有行。

## 反例 → 正例

```tsx
// ❌ 前端全量分页
const { data } = useQuery({ queryKey: ["users"], queryFn: () => usersApi.listAll() });
// listAll 返回 5000 行
<Table dataSource={data} pagination={{ pageSize: 20 }} />
// 5000 行全 mount 在 DOM 之外，仅页面层级是 20 行

// ✅ 服务端分页
function UserTable() {
  const [page, setPage] = useState(1);
  const [size, setSize] = useState(20);

  const { data, isLoading } = useQuery({
    queryKey: ["users", page, size],
    queryFn: () => usersApi.list({ page, size }),
    keepPreviousData: true,   // 切页时保留旧数据避免闪烁
  });

  return (
    <Table
      rowKey="id"
      dataSource={data?.items}
      loading={isLoading}
      pagination={{
        current: page,
        pageSize: size,
        total: data?.total ?? 0,
        showSizeChanger: true,
        pageSizeOptions: [10, 20, 50, 100],
        showTotal: (t) => `共 ${t} 条`,
        onChange: (p, s) => { setPage(p); setSize(s); },
      }}
    />
  );
}
```

## 后端 API 约定

```
GET /api/users?page=1&size=20&sort=created_at:desc&filter[subject]=math

{
  "items": [...],
  "total": 5000,
  "page": 1,
  "size": 20
}
```

## 排序 / 筛选也下推服务端

```tsx
const [sort, setSort] = useState<{ field?: string; order?: "asc" | "desc" }>({});

const { data } = useQuery({
  queryKey: ["users", page, size, sort],
  queryFn: () => usersApi.list({ page, size, ...sort }),
});

<Table
  onChange={(_pag, _filters, sorter) => {
    // sorter 可能是数组（多列）或单列
    if (Array.isArray(sorter)) return;
    setSort({
      field: sorter.field as string,
      order: sorter.order === "ascend" ? "asc" : "desc",
    });
  }}
  ...
/>
```

## keepPreviousData

切页时旧数据保留，避免闪烁。新数据到达后替换。**强烈推荐开启**。

## 自检

- [ ] 行数 > 50 一律服务端分页？
- [ ] queryKey 含 page / size / sort / filter？
- [ ] 排序 / 筛选下推服务端？
- [ ] 开启 keepPreviousData？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`row-key-stable.md`](./row-key-stable.md)

