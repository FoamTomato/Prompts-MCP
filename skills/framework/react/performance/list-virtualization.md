---
name: react-list-virtualization
description: 长列表虚拟化只渲染可视区(windowing)，用 react-window FixedSizeList(等高最快)。Use when 列表项 >1000 渲染卡顿 / DOM 节点数千级 / 接无限滚动 / 优化滚动性能。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - 虚拟化
  - 长列表
  - windowing
  - react-window
  - FixedSizeList
  - overscanCount
  - 无限滚动
  - InfiniteLoader
effort: high
context: inline
version: '1.0'
---
# React · 长列表虚拟化

## 规则

决策点:**列表项 > 1000 且滚动卡顿才上虚拟化,只渲染可视区(windowing)。** 等高用 `react-window` 的 `FixedSizeList`(最快),按下表配置:

| 关注点 | 做法 | 不做会怎样 |
|--------|------|-----------|
| 只渲染可视区 | `FixedSizeList` 按 `itemSize` 算窗口,DOM 仅几十行 | 数千 DOM 节点,滚动掉帧 |
| 防滚动空白闪 | `overscanCount={5}` 多渲染上下若干行 | 快速滚动露白块 |
| 行身份稳定 | `itemKey={(i, data) => data[i].id}` 用业务 id | index 当 key,数据变动错位复用 |
| 行不无谓重渲染 | Row 组件 `React.memo` | 滚动时每行全量重渲染 |
| renderer 引用稳定 | Row 提到组件外,**禁内联** `children={(props)=>...}` | 每次渲染新引用,memo 失效 |

**何时不上:** 短列表(几十~几百项)不要虚拟化 —— 测量/定位开销 + 失去原生查找/无障碍 > 收益,是**负收益**。先量再上。

**配合无限滚动:** 用 `react-window-infinite-loader` 包裹,`onItemsRendered` 中末项接近总数时触发 `fetch` 下一页;`itemCount` 设为 `已加载 + (hasMore ? 1 : 0)` 给末尾留 loading 行。**这是滚动加载,不替代服务端分页** —— 后端仍走分页接口。

**禁:** 不等高列表硬塞 `FixedSizeList`(行会被裁切/重叠)→ 改用 `VariableSizeList` 并缓存高度。

## 反例 · 正例

```tsx
// ❌ 全量渲染 + 内联 Row + index 当 key:数千 DOM、滚动卡、memo 失效
<List height={600} itemCount={items.length} itemSize={48} width="100%">
  {({ index, style }) => <div style={style}>{items[index].name}</div>}
</List>

// ✅ Row 提外 + React.memo + 稳定 itemKey + overscan
const Row = React.memo(({ index, style, data }: ListChildComponentProps<Item[]>) => {
  // 取当前行数据,渲染仅几个节点
  const item = data[index];
  return <div style={style}>{item.name}</div>;
});

function BigList({ items }: { items: Item[] }) {
  // 可视区列表:等高用 FixedSizeList,itemData 透传数据给 memo Row
  return (
    <FixedSizeList
      height={600}
      width="100%"
      itemCount={items.length}
      itemSize={48}
      itemData={items}
      overscanCount={5}
      itemKey={(index, data) => data[index].id}
    >
      {Row}
    </FixedSizeList>
  );
}
```

详见 [`list-virtualization.examples.md`](./list-virtualization.examples.md):FixedSizeList + memo Row 完整版、无限滚动 InfiniteLoader 接入。

## 自检

- [ ] 确认列表项 > 1000 且实测滚动卡顿才上虚拟化(短列表不上)?
- [ ] 等高场景用 `FixedSizeList`,不等高才换 `VariableSizeList`?
- [ ] 配了 `overscanCount`(防滚动露白)?
- [ ] `itemKey` 用稳定业务 id,不是 index?
- [ ] Row 组件包了 `React.memo`,且 Row 提到组件外(无内联 renderer)?
- [ ] 接无限滚动时 `onItemsRendered` 触发的是分页 `fetch`,没用虚拟化替代服务端分页?

## 相关

- 父:[`./index.md`](./index.md)
- 兄弟:[`code-splitting.md`](./code-splitting.md) · [`web-vitals-cls.md`](./web-vitals-cls.md)
- 跨引:[`../component/re-render-minimization.md`](../component/re-render-minimization.md)(Row memo / 稳定引用)· [`../../antd/table/pagination-server-side.md`](../../antd/table/pagination-server-side.md)(无限滚动不替代服务端分页)
