---
name: react-a11y-semantic-and-aria
description: React 语义 HTML 与 ARIA 约定：优先原生语义元素，ARIA 仅补缺。Use when 选语义标签 / 给自研控件补 role 与状态 / 关联 label 与表单控件 / 图标按钮加无障碍名
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - 语义 HTML
  - ARIA
  - role
  - aria-label
  - aria-pressed
  - aria-live
  - label htmlFor
  - 表单关联
  - 图标按钮
  - 装饰图 alt
effort: medium
context: inline
version: '1.0'
---
# React · 语义 HTML 与 ARIA

## 规则

决策点：能用原生语义元素就别上 ARIA。**no ARIA 好过 bad ARIA** —— 错的 role 比没有更伤可达性。

| 场景 | 首选 | 补什么 |
|------|------|--------|
| 点击操作 | `<button>` | 无；自带 role/键盘 |
| 导航 / 主内容 / 列表 | `<nav>`/`<main>`/`<ul><li>` | 无；自带地标语义 |
| 自研 toggle（非原生 input） | `<button>` | `role` 视情况 + `aria-pressed={on}` |
| 自研 tablist | 容器 | `role="tablist"` / 项 `role="tab"` `aria-selected` |
| 图标按钮（无可见文字） | `<button>` | `aria-label="删除"` |
| 装饰性图片 | `<img>` | `alt=""`（空串，读屏跳过） |
| 动态更新区（轮询/异步结果） | 区域容器 | `aria-live="polite"` |

表单 label 关联：`<label htmlFor={id}>` 显式绑，或 `<label>` 直接包裹控件。antd `Form.Item label` 自动处理关联，无需手写；自研 `input` 必须显式 `htmlFor`+`id`。

antd 多数组件（Button/Tabs/Menu/Modal）自带正确 role，直接用即可；自研壳层（见 [when-antd-vs-custom](../../antd/when-antd-vs-custom.md)）要自己补齐 role 与状态。

## 反例·正例

```tsx
// 反例：div 当按钮 —— 无 role、无键盘、读屏读不出可点
const ToggleBad = ({ on, onToggle }: { on: boolean; onToggle: () => void }) => (
  <div className="toggle" onClick={onToggle}>{on ? "开" : "关"}</div>
);

// 反例：图标按钮无可访问名 —— 读屏只念出 "button"
const DeleteBad = ({ onDelete }: { onDelete: () => void }) => (
  <button onClick={onDelete}><DeleteOutlined /></button>
);
```

```tsx
import { Button } from "antd";
import { DeleteOutlined } from "@ant-design/icons";

// 正例：自研 toggle 用 button，状态走 aria-pressed
const Toggle = ({ on, onToggle }: { on: boolean; onToggle: () => void }) => (
  // 原生 button 自带 role/键盘；aria-pressed 暴露开关态给读屏
  <button type="button" aria-pressed={on} onClick={onToggle}>
    {on ? "开" : "关"}
  </button>
);

// 正例：图标按钮补 aria-label 作可访问名
const DeleteButton = ({ onDelete }: { onDelete: () => void }) => (
  <Button aria-label="删除" icon={<DeleteOutlined />} onClick={onDelete} />
);

// 正例：自研 input 显式关联 label
const SearchField = ({ value, onChange }: { value: string; onChange: (v: string) => void }) => (
  <>
    <label htmlFor="kw">关键词</label>
    {/* htmlFor 与 input id 对齐，点 label 聚焦控件 */}
    <input id="kw" value={value} onChange={(e) => onChange(e.target.value)} />
  </>
);
```

## 自检

- [ ] 可点元素是 `<button>`/`<a>` 而非 `<div onClick>`（自带 role 与键盘）？
- [ ] 用了原生语义标签（`nav`/`main`/`ul`），没有为 div 硬贴 ARIA role？
- [ ] 自研 toggle 暴露 `aria-pressed`、tab 暴露 `aria-selected`，状态随交互更新？
- [ ] 纯图标按钮都有 `aria-label`？装饰图 `alt=""`？
- [ ] 表单控件都有关联 label（antd `Form.Item label` 或自研 `htmlFor`+`id`）？
- [ ] 异步/轮询更新的区域包了 `aria-live`？
- [ ] 没有为偷懒补错的 role（no ARIA 好过 bad ARIA）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`keyboard-focus.md`](./keyboard-focus.md)（键盘可达 / tab 顺序 / 焦点陷阱）
- 控件→必需 ARIA 矩阵：[`semantic-and-aria.reference.md`](./semantic-and-aria.reference.md)
- 跨引：自研 vs antd 取舍见 [`../../antd/when-antd-vs-custom.md`](../../antd/when-antd-vs-custom.md)
- 跨引：对比度见 [`../theming/palette-principles.md`](../theming/palette-principles.md)
