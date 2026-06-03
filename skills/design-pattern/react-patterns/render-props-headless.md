---
name: react-render-props-headless
description: "render props 与 headless 组件:组件托管子树、把渲染权交给消费者,只给行为不给样式。Use when 组件需托管子树并插入消费者 JSX / 写虚拟列表渲染项 / 接 React Aria-TanStack Table 类 headless 库时。"
parent: ./index.md
paths:
- frontend/src/**/*.tsx
triggers:
  keywords:
  - render props
  - children as function
  - headless component
  - 无头组件
  - 渲染权
  - VirtualList
  - TanStack Table
  - React Aria
effort: medium
context: inline
version: '1.0'
---

# Design Pattern · render props 与 headless 组件

## 规则

**决策点:这段复用是"逻辑"还是"托管子树"?** 2025 默认逻辑复用走自定义 hook;render props 只在组件必须拥有子树渲染时机、又要插入消费者 JSX 时用。

| 诉求 | 用什么 | 理由 |
|------|--------|------|
| 复用 state/effect/订阅,UI 由调用方自由写 | 自定义 hook（[./custom-hook-extraction.md](./custom-hook-extraction.md)） | 无嵌套、无 wrapper、类型直观 |
| 组件持有子树、决定**何时/对每项**渲染,渲染内容交消费者 | children-as-function / render props | hook 拿不到"每个 item 的渲染插槽" |
| 给行为(键盘/选中/分页/定位)不给样式,消费者全权控制 DOM | headless 组件/hook | Downshift · React Aria · TanStack Table · Radix 模式 |

判据:**调用方需要把 JSX 插进组件管理的循环/虚拟窗口/受控插槽里 → render props/headless;否则 → hook。**

### 反例 —— 简单逻辑复用硬塞 render props(应改 hook)

```tsx
// 反例:只是复用一个 size 监听,却用 render props 制造嵌套与 wrapper
<WindowSize>
  {(size) => <Chart width={size.width} />}
</WindowSize>
// 应改为 hook,无嵌套、无多余节点:
const size = useWindowSize();
return <Chart width={size.width} />;
```

### 正例 —— 虚拟列表:组件托管窗口,渲染项交消费者

```tsx
// 行渲染:>3 行的派生下沉为纯函数,组件体保持平坦
const renderRow = (item: Item): ReactNode => <Row key={item.id} data={item} />;

export function ProductList({ items }: { items: Item[] }) {
  // 前置校验:空数据早返回
  if (items.length === 0) return <Empty />;

  // VirtualList 拥有滚动窗口与可见区计算,把"每项怎么画"以 children-as-function 交回消费者
  return (
    <VirtualList items={items} itemHeight={48}>
      {(item) => renderRow(item)}
    </VirtualList>
  );
}
```

```tsx
// headless 正例:hook 只吐行为与无障碍属性,样式与标签全由消费者决定
export function FilterSelect({ options }: { options: Option[] }) {
  // 取行为层:开合、选中、键盘导航、a11y props 全来自 headless hook
  const { isOpen, getToggleButtonProps, getMenuProps, getItemProps } = useSelect({ items: options });

  // 渲染层完全自定义:headless 不带任何样式
  return (
    <div>
      <button {...getToggleButtonProps()}>选择</button>
      <ul {...getMenuProps()} hidden={!isOpen}>
        {options.map((opt, i) => (
          <li key={opt.value} {...getItemProps({ item: opt, index: i })}>{opt.label}</li>
        ))}
      </ul>
    </div>
  );
}
```

## 自检

- [ ] 这段复用若只是 state/effect/订阅,是否已优先用自定义 hook 而非 render props?
- [ ] 用 render props 的唯一理由,是组件要托管子树并把每项/插槽渲染交回消费者?
- [ ] headless 层是否只产出行为与 a11y props、零样式,DOM 结构由消费者掌控?
- [ ] children-as-function 是否有稳定 key、>3 行渲染逻辑是否下沉为纯函数?
- [ ] 没有为"省一个 wrapper"的简单场景制造多余嵌套层级?

## 相关

- 默认逻辑复用优先级:[`./custom-hook-extraction.md`](./custom-hook-extraction.md)
- 组合式 API 邻模式:[`./compound-components.md`](./compound-components.md)
- 虚拟列表落地用法:[`../../framework/react/performance/list-virtualization.md`](../../framework/react/performance/list-virtualization.md)
- 本层路由:[`./index.md`](./index.md)
