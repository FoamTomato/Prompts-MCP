---
name: framework-react-a11y-index
description: React 无障碍约定索引：语义 HTML / ARIA 属性 / label 关联，以及键盘可达 / tab 顺序 / 焦点管理。Use when 写无障碍交互 / 表单可访问性 / 弹窗焦点陷阱 / 键盘导航
parent: ../index.md
children:
  - { name: semantic-and-aria, path: semantic-and-aria.md, tag: skill, note: 语义标签 + ARIA + label 关联 }
  - { name: keyboard-focus, path: keyboard-focus.md, tag: skill, note: 键盘可达 + tab 顺序 + Modal 焦点陷阱 }
when_to_descend: |
  写无障碍交互 / 表单 / 弹窗时下钻。
  对比度不在此处 —— 见 theming/palette-principles；动效降级见 gsap/reduced-motion。
---

# React · 无障碍约定

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| semantic-and-aria | skill | 语义标签 + ARIA 属性 + label 与控件关联 |
| keyboard-focus | skill | 键盘可达 + tab 顺序 + Modal 焦点陷阱 |

## 何时下钻

- 选语义标签 / 补 ARIA 角色与状态 / 把 label 关联到表单控件 → `semantic-and-aria.md`
- 保证键盘可操作 / 控制 tab 顺序 / 弹窗里做焦点陷阱与还原 → `keyboard-focus.md`

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../component/index.md`](../component/index.md) · [`../theming/index.md`](../theming/index.md)
- 跨引：对比度见 [`../theming/palette-principles.md`](../theming/palette-principles.md);动效降级见 [`../gsap/reduced-motion.md`](../gsap/reduced-motion.md)
