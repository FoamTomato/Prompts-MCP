---
name: react-empty-state
description: antd Empty 零数据空态房规 — 数据为 0 行必须显式渲染空态而非 null/空白,且区分无数据/筛空/出错三态。Use when 列表或详情零数据 / 筛选搜索命中 0 条 / 判断该渲染空态还是错误态 / 评审 return null 空白页。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - Empty 空态
  - 零数据态
  - 无数据空白
  - 筛选无结果
  - empty state
  - PRESENTED_IMAGE_SIMPLE
  - EmptyState
effort: medium
context: inline
version: '1.0'
---
# React · Empty 空态

## 规则

**决策点:数据 0 行时渲染什么、三种"空"如何区分。** 房规:`length === 0` 必须显式渲染空态组件,**禁止 `return null` / 空白页** —— 用户分不清是没数据还是页面坏了。

三种"空"语义不同,文案与 CTA 必须区分:

| 场景 | 判定条件 | 文案 | CTA |
|------|---------|------|-----|
| 从未有数据 | 无 filter 且 `length === 0` | "还没有内容" | 主按钮:新建(`type="primary"`) |
| 筛选/搜索为空 | 有 filter 命中 0 条 | "没有匹配结果" | 次按钮:清空筛选(`type="default"`) |
| 出错≠空 | `error` 非空 | —— | 不当空态处理,走 `ErrorState` |

渲染优先级严格按 **`isLoading` → Skeleton → `error` → ErrorState → `length === 0` → Empty → 数据**,四态互斥早返回。空 ≠ 加载 ≠ 错误。

antd:`<Empty description image>` + `children` 放 CTA;紧凑场景用 `image={Empty.PRESENTED_IMAGE_SIMPLE}`。自定义 `EmptyState` 收敛 icon/title/description/action 四件套,统一三态判定。

## 反例

```tsx
// 反例:0 行直接 return null —— 页面空白,用户以为坏了,且没区分筛空/出错
function List({ data }: { data?: Item[] }) {
  if (!data?.length) return null;
  return <Table dataSource={data} />;
}
```

## 正例(骨架)

```tsx
// 四态互斥早返回:加载→错误→零数据(按 filter 区分)→数据
if (isLoading) return <Skeleton active />;
if (error) return <ErrorState error={error} />;
if (data.length === 0) {
  // 三态判定下沉纯函数 resolveEmptyKind,组件只做编排
  const kind = resolveEmptyKind(Boolean(keyword));
  return <EmptyState {...emptyPropsByKind[kind]} />;
}
return <ItemTable dataSource={data} />;
```

完整 `EmptyState` 组件 + `resolveEmptyKind` 纯函数 + 页面编排:[`./empty-state.examples.md`](./empty-state.examples.md)。

## 自检

- [ ] `length === 0` 是否显式渲染空态,而非 `return null` / 空白?
- [ ] 是否按有无 filter 区分"还没有内容"(主 CTA 新建)与"没有匹配结果"(次 CTA 清空筛选)?
- [ ] 出错是否走 `ErrorState` 而非误当空态?
- [ ] 渲染顺序是否为 isLoading→Skeleton→error→ErrorState→length===0→Empty→数据,四态互斥早返回?
- [ ] 三态判定是否下沉纯函数,组件体只做编排?

## 相关

- 父:[`./index.md`](./index.md)
- 兄弟(加载占位):[`./skeleton-loading.md`](./skeleton-loading.md)
- 跨引(出错态 ≠ 空态):[`../error-handling/region-error-isolation.md`](../error-handling/region-error-isolation.md)
