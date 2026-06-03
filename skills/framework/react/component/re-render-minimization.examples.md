# React · 消除多余 re-render 示例

## 1. 内联 prop bug —— before

`React.memo` 看起来包了,实际每次父渲染 `style`/`data`/`onClick` 都是新引用,浅比较恒不相等,子组件每次都重渲染。

```tsx
import { memo, useState } from "react";

interface ItemPanelProps {
  style: React.CSSProperties;
  data: number[];
  onClick: () => void;
}

// 子组件包了 memo,但下面父侧全是内联 prop,memo 形同虚设
const ItemPanel = memo(function ItemPanel({ style, data, onClick }: ItemPanelProps) {
  return (
    <div style={style} onClick={onClick}>
      {data.length} 项
    </div>
  );
});

function Dashboard() {
  const [tick, setTick] = useState(0);

  // ❌ tick 每秒变化触发父渲染,下面三个 prop 全是新引用 → ItemPanel 每次都重渲染
  return (
    <div>
      <button onClick={() => setTick(t => t + 1)}>tick {tick}</button>
      <ItemPanel style={{ padding: 8 }} data={[]} onClick={() => console.log("hit")} />
    </div>
  );
}
```

## 2. 三件套修复 —— after

常量提到组件外,派生值 `useMemo`,回调 `useCallback`;`tick` 变化时三个 prop 引用都稳定,`ItemPanel` 不再无谓重渲染。

```tsx
import { memo, useCallback, useMemo, useState } from "react";

// 静态 style 提到组件外,引用永远稳定
const PANEL_STYLE: React.CSSProperties = { padding: 8 };

// >3 行的派生计算下沉为纯函数,组件体只做编排
function buildVisibleIds(rows: Row[]): number[] {
  return rows.filter(r => r.visible).map(r => r.id);
}

const ItemPanel = memo(function ItemPanel({ style, data, onClick }: ItemPanelProps) {
  return (
    <div style={style} onClick={onClick}>
      {data.length} 项
    </div>
  );
});

function Dashboard({ rows }: { rows: Row[] }) {
  const [tick, setTick] = useState(0);

  // 派生数据:仅 rows 变化时重算,引用稳定
  const visibleIds = useMemo(() => buildVisibleIds(rows), [rows]);
  // 回调:依赖为空,引用稳定
  const handleHit = useCallback(() => console.log("hit"), []);

  // 编排:tick 变化触发父渲染,但传给 ItemPanel 的三个 prop 引用都不变
  return (
    <div>
      <button onClick={() => setTick(t => t + 1)}>tick {tick}</button>
      <ItemPanel style={PANEL_STYLE} data={visibleIds} onClick={handleHit} />
    </div>
  );
}
```

## 3. React 19 Compiler 版 —— 去掉手写 memo

项目启用 React Compiler 后,编译器自动 memo 组件与派生值/回调,手写三件套冗余。代码回归直白,只需保证内联 prop 仍写成可被编译器分析的稳定形态。

```tsx
import { useState } from "react";

// Compiler 启用:不写 memo / useMemo / useCallback,编译期自动处理
function ItemPanel({ data, onClick }: { data: number[]; onClick: () => void }) {
  return <div onClick={onClick}>{data.length} 项</div>;
}

function Dashboard({ rows }: { rows: Row[] }) {
  const [tick, setTick] = useState(0);

  // 派生值直接算,编译器自动缓存
  const visibleIds = rows.filter(r => r.visible).map(r => r.id);
  // 回调直接定义,编译器自动稳定
  const handleHit = () => console.log("hit");

  // 编排:无手写 memo,Compiler 保证 ItemPanel 不被无谓重渲染
  return (
    <div>
      <button onClick={() => setTick(t => t + 1)}>tick {tick}</button>
      <ItemPanel data={visibleIds} onClick={handleHit} />
    </div>
  );
}
```
