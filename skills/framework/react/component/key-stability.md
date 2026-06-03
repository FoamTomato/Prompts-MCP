---
name: react-key-stability
description: 列表 .map 渲染的 key 必用稳定业务 id，禁数组 index、禁 Math.random()。Use when 写
  .map 列表渲染 / 行内态(输入/展开/选中)增删排序后跳行 / 列表项丢状态丢动画。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - key
  - 列表 key
  - 稳定业务 id
  - index 作 key
  - Math.random
  - map 渲染
  - reconciliation
effort: low
context: inline
version: '1.0'
---
# React · 列表 key 用稳定业务 id

## 规则

`.map` 渲染列表时，`key` **必须**用稳定的业务 id；**禁用数组 index、禁用 `Math.random()`**。

| key 取值 | 后果 | 判定 |
|----------|------|------|
| 业务 id（`x.id` / `x.uuid`） | diff 正确，状态跟随数据移动 | ✅ |
| 无 id → 稳定组合键 `${x.type}-${x.code}` | 同上，前提是组合在列表内唯一且不随渲染变 | ✅ |
| 数组 index `(x, i) => i` | 增删/排序后位置复用错位 → 行内态（输入值/展开/选中）跳行 | ❌ |
| `Math.random()` / `Date.now()` | 每次渲染 key 全变 → 整列 remount，丢输入态、丢动画、丢焦点 | ❌ |

## 反例 → 正例

```tsx
// ❌ index 作 key：删第一行后，后续行复用错位，行内输入值跳到别行
{items.map((x, i) => (
  <Row key={i} item={x} />
))}

// ❌ random 作 key：每次父组件 re-render 都全量 remount，input 焦点/动画丢失
{items.map(x => (
  <Row key={Math.random()} item={x} />
))}

// ✅ 用业务稳定 id
{items.map(x => (
  <Row key={x.id} item={x} />
))}

// ✅ 无 id 时用稳定组合键（列表内唯一、不随渲染变）
{items.map(x => (
  <Row key={`${x.type}-${x.code}`} item={x} />
))}
```

完整编排：列表项带行内态时，状态必须按 id 索引，才能在增删后跟随数据。

```tsx
function EditableRowList({ rows }: { rows: Row[] }) {
  // 1. 展开态按业务 id 索引，而非按下标 —— 数据增删时状态跟着 id 走
  const [expandedIds, setExpandedIds] = useState<Set<string>>(new Set());

  // 2. 切换某行展开（纯函数下沉，组件体只做编排）
  const handleToggle = (id: string) => setExpandedIds(toggleId(expandedIds, id));

  // 3. map 渲染，key 用稳定 id；行内态从 Set 派生，不依赖渲染顺序
  return (
    <div>
      {rows.map(row => (
        <EditableRow
          key={row.id}
          row={row}
          expanded={expandedIds.has(row.id)}
          onToggle={() => handleToggle(row.id)}
        />
      ))}
    </div>
  );
}

// utils：>3 行集合转换下沉为纯函数
function toggleId(set: Set<string>, id: string): Set<string> {
  const next = new Set(set);
  next.has(id) ? next.delete(id) : next.add(id);
  return next;
}
```

## 与 antd Table 的关系

`<Table>` 不在 children 里手写 `key`，而是用 `rowKey` 指定稳定 id —— 同样禁 index/random，见 [`../../antd/table/row-key-stable.md`](../../antd/table/row-key-stable.md)。

## 自检

- [ ] `.map` 的 key 是业务稳定 id（不是 index、不是 `Math.random()`）？
- [ ] 无 id 时用列表内唯一且不随渲染变的组合键 `${a}-${b}`？
- [ ] 列表项带行内态（输入/展开/选中）时，状态按 id 索引而非按下标？
- [ ] antd `<Table>` 用 `rowKey` 而非手写 key？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`re-render-minimization.md`](./re-render-minimization.md)、[`derived-state.md`](./derived-state.md)
- 跨引：[`../../antd/table/row-key-stable.md`](../../antd/table/row-key-stable.md)
