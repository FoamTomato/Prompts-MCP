---
name: react-component-structure
description: React 组件文件结构模板（props/hooks/jsx 三段）。Use when 写 React 组件 / 改 .tsx 文件 /
  评审 PR 时。
parent: ./index.md
paths:
- frontend/src/components/**/*.tsx
- frontend/src/features/**/*.tsx
- frontend/src/pages/**/*.tsx
triggers:
  keywords:
  - React
  - 组件
  - Component
  - tsx
effort: medium
context: inline
version: '1.0'
---
# React · 组件结构模板

## 三段式结构

```tsx
import { useState, useMemo, useRef } from "react";
import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import { D, E } from "@/animations/tokens";
import { Button } from "@/components/Button";
import type { Textbook } from "@/types/textbook";

// 1. Props 类型（export 便于复用）
export interface TextbookCardProps {
  textbook: Textbook;
  selected?: boolean;
  onSelect: (id: string) => void;
}

// 2. 组件实现
export function TextbookCard({ textbook, selected = false, onSelect }: TextbookCardProps) {
  // 2.1 hooks（按顺序：state → ref → derived → effect → animation → callback）
  const [hovered, setHovered] = useState(false);
  const root = useRef<HTMLDivElement>(null);

  const subtitle = useMemo(
    () => `${textbook.subject} · ${textbook.grade}`,
    [textbook.subject, textbook.grade]
  );

  useGSAP(() => {
    gsap.to(root.current, {
      scale: selected ? 1.02 : 1,
      duration: D.micro,
      ease: E.out,
    });
  }, { scope: root, dependencies: [selected] });

  // 2.2 JSX
  return (
    <div
      ref={root}
      role="button"
      tabIndex={0}
      aria-pressed={selected}
      className={`textbook-card ${selected ? "is-selected" : ""}`}
      onClick={() => onSelect(textbook.id)}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <h3>{textbook.name}</h3>
      <p>{subtitle}</p>
      {hovered && <Button size="sm">查看章节</Button>}
    </div>
  );
}
```

## 关键约定

- Props 类型 export，便于外部测试 / 复用
- 默认值用解构（`selected = false`），不用 `defaultProps`（已弃用）
- 事件 props 命名 `on<Event>`，调用方变量命名 `handle<Event>`
- 交互元素必须有 `role` / `aria-*` / 键盘事件
- 一个 `.tsx` 文件一个主导出组件（小辅助允许在同文件内但不 export）

## hooks 顺序约束

详见 [`../hook/order-and-rules.md`](../hook/order-and-rules.md)。

## 自检

- [ ] Props 类型 export？
- [ ] 默认值用解构？
- [ ] 一文件一主组件？
- [ ] 交互元素有 role / aria / 键盘事件？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`folder-layering.md`](./folder-layering.md) · [`button-naming.md`](./button-naming.md)

