---
name: react-a11y-keyboard-focus
description: React 键盘可达与焦点管理：交互元素键盘可操作 / 可见焦点环 / tabIndex 指南 / 弹窗焦点陷阱与回焦。Use when 自研浮层做焦点陷阱 / 自定义控件加键盘操作 / 调 tabIndex / 弹窗关闭还焦 / 去掉焦点环
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - tabIndex
  - focus trap
  - 焦点陷阱
  - aria-modal
  - 键盘可达
  - onKeyDown
  - Escape
  - 焦点环
effort: high
context: inline
version: '1.0'
---
# React · 键盘可达与焦点管理

## 规则

决策点：**这个交互元素能否只用键盘完成全部操作，且焦点始终可见、可还原？**

| 场景 | 做法 |
|------|------|
| 交互元素（按钮 / 链接 / 自定义控件） | 键盘可达：Enter/Space 激活、Esc 关闭浮层 |
| 焦点可见 | 保留焦点环；若去 `outline` 必须补 `:focus-visible` 替代样式 |
| 自定义控件纳入 Tab 序 | `tabIndex={0}` |
| 程序聚焦但不进 Tab 序 | `tabIndex={-1}`（如 dialog 容器） |
| 正数 tabIndex | 禁用——打乱自然顺序 |
| antd Modal / Drawer | 默认已捕获焦点+关闭回焦，别重造 |
| 自研浮层 | 自己 trap focus，关闭时把焦点还给触发元素 |
| dialog 挂载 | 聚焦容器 + `role="dialog"` + `aria-modal="true"` |

## 反例

```tsx
// ❌ 全局去焦点环，键盘用户看不到光标在哪
*:focus { outline: none; }

// ❌ 自定义下拉键盘不可达：div 无 tabIndex、无键盘事件、无 role
<div className="dropdown" onClick={toggle}>选择</div>
```

## 正例

```tsx
import { Button } from "antd";

// 自定义可聚焦控件：纳入 Tab 序 + 键盘激活 + 语义角色
function ToggleChip({ label, onActivate }: { label: string; onActivate: () => void }) {
  // 键盘激活:Enter/Space 等价于点击
  const handleKeyDown = (e: React.KeyboardEvent) => activateOnEnterSpace(e, onActivate);
  return (
    <span
      role="button"
      tabIndex={0}                      // 纳入 Tab 序
      className="chip"                  // CSS 里用 :focus-visible 画焦点环
      onClick={onActivate}
      onKeyDown={handleKeyDown}
    >
      {label}
    </span>
  );
}
```

```tsx
// 自研浮层:trap focus + Esc 关闭 + 关闭回焦触发元素
function FocusTrapPanel({ open, onClose, triggerRef, children }: FocusTrapPanelProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  // 打开时:把焦点移入容器;关闭时:还焦给触发元素
  useEffect(() => {
    if (!open) return;
    containerRef.current?.focus();
    return () => triggerRef.current?.focus();
  }, [open, triggerRef]);

  // Esc 关闭 + Tab 在浮层内循环(逻辑下沉到 hook)
  const handleKeyDown = useFocusTrap(containerRef, { onEscape: onClose });

  if (!open) return null;
  return (
    <div
      ref={containerRef}
      role="dialog"
      aria-modal="true"                 // 屏幕阅读器进入模态语境
      tabIndex={-1}                     // 程序可聚焦,不进 Tab 序
      onKeyDown={handleKeyDown}
    >
      {children}
    </div>
  );
}
```

> `activateOnEnterSpace` / `useFocusTrap` 是下沉的纯函数 / hook,组件体只做编排。简单确认 / 复杂弹窗优先用 antd（焦点陷阱与回焦内建);动效配合 `prefers-reduced-motion` 降级,见 [`../gsap/reduced-motion.md`](../gsap/reduced-motion.md)。

## 自检

- [ ] 每个交互元素仅用键盘可完成操作（Enter/Space 激活、Esc 关闭）？
- [ ] 焦点环可见，没有裸 `outline:none` 而不补 `:focus-visible`？
- [ ] 自定义控件 `tabIndex={0}`、程序聚焦容器 `tabIndex={-1}`、无正数 tabIndex？
- [ ] 弹窗优先用 antd Modal/Drawer，没有重造焦点陷阱？
- [ ] 自研浮层 trap focus，关闭时焦点还给触发元素？
- [ ] dialog 容器 `role="dialog"` + `aria-modal="true"` 且挂载时聚焦？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`semantic-and-aria.md`](./semantic-and-aria.md)
- 跨引：弹窗选型见 [`../../antd/modal/confirm-vs-modal.md`](../../antd/modal/confirm-vs-modal.md)；动效降级见 [`../gsap/reduced-motion.md`](../gsap/reduced-motion.md)
