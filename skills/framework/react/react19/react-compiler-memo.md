---
name: react19-react-compiler-memo
description: React Compiler 开启后自动记忆化，默认不再手写 useMemo/useCallback/React.memo，仅保留三类例外。Use when 纠结要不要加 memo / 删手写 useCallback / 确认 Compiler 是否启用。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - React Compiler
  - 自动记忆化
  - useMemo
  - useCallback
  - React.memo
  - babel-plugin-react-compiler
  - eslint-plugin-react-compiler
  - bail-out
effort: medium
context: inline
version: '1.0'
---
# React19 · React Compiler 自动记忆化

## 规则

决策点：**Compiler 是否启用** 决定要不要手写记忆化。Compiler 是 opt-in，先确认构建里装了 `babel-plugin-react-compiler` 或 vite 插件，再决策。

| Compiler 状态 | 默认做法 | 例外 / 备注 |
|---------------|---------|------------|
| **开启** | 删掉 useMemo / useCallback / React.memo，编译期自动加 | 仅保留下方三类 |
| **关闭** | 手写记忆化规则照旧 | 见 [hook/order-and-rules](../hook/order-and-rules.md)、[component/re-render-minimization](../component/re-render-minimization.md) |

Compiler 开启时，仅以下三类**保留手写**:
- (a) 非 React API / effect 依赖需引用稳定（如裸 `addEventListener`、传给非 React 库的回调）。
- (b) 编译器看不到的、实测昂贵的计算（profile 证实，非臆测）。
- (c) 被 Compiler bail-out 的组件（破坏 Rules-of-React 而跳过编译，查 `eslint-plugin-react-compiler` 告警）。

前提：**Rules-of-React 纯度**是 Compiler 工作的前提——渲染期无副作用、不可变更 props/state，否则该组件被 bail-out，记忆化失效。

### 反例：Compiler 项目里到处 useCallback "以防万一"

```tsx
// 反例：Compiler 已开，所有回调仍手写 useCallback，噪音且与编译输出重复
const Toolbar = ({ items }: ToolbarProps) => {
  // 多余：Compiler 会自动稳定引用
  const handleSave = useCallback(() => saveItems(items), [items]);
  // 多余:简单 map 不属于昂贵计算
  const labels = useMemo(() => items.map((it) => it.label), [items]);
  return <ButtonGroup onSave={handleSave} labels={labels} />;
};
```

### 正例：编排平坦，记忆化交给编译器，仅例外手写

```tsx
const Toolbar = ({ items, chart }: ToolbarProps) => {
  // 步骤1:普通回调直接定义,Compiler 自动记忆,无需 useCallback
  const handleSave = () => saveItems(items);

  // 步骤2:简单派生直接算,Compiler 自动记忆,无需 useMemo
  const labels = items.map((it) => it.label);

  // 步骤3:例外(b)实测昂贵计算,profile 证实才保留 useMemo;重计算下沉纯函数
  const heatmap = useMemo(() => buildHeatmap(chart), [chart]);

  // 步骤4:例外(a)传给非 React 图表库需引用稳定,保留 useCallback
  const onZoom = useCallback((scale: number) => chart.zoom(scale), [chart]);

  return <ButtonGroup onSave={handleSave} labels={labels} heatmap={heatmap} onZoom={onZoom} />;
};
```

## 自检

- [ ] 已确认构建里装了 React Compiler 插件(babel/vite)，再做删/留决策。
- [ ] Compiler 开:已删除"以防万一"的 useMemo/useCallback/React.memo。
- [ ] 保留的每处记忆化都归属三类例外之一(非 React 引用稳定 / profile 实测昂贵 / bail-out 组件)。
- [ ] 已查 `eslint-plugin-react-compiler` 告警，确认目标组件未被 bail-out。
- [ ] 保留的记忆化对应组件满足 Rules-of-React 纯度(渲染期无副作用、不变更 props/state)。
- [ ] Compiler 关:按手写记忆化规则处理，未误删必要的 memo。

## 相关

- 父:[`./index.md`](./index.md)
- 兄弟:[`./data-fetching-with-suspense.md`](./data-fetching-with-suspense.md) · [`./form-actions.md`](./form-actions.md)
- 跨引:[`../hook/order-and-rules.md`](../hook/order-and-rules.md)(Compiler 关时的 useMemo 摆位) · [`../component/re-render-minimization.md`](../component/re-render-minimization.md)(手写 memo 的定位与稳定 prop)
