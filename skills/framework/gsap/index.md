---
name: framework-gsap-index
description: GSAP 动画库使用约定索引（原则 / useGSAP / Timeline / FLIP / Draggable / Reduced Motion）
parent: ../index.md
children:
  - { name: principles, path: principles.md, tag: leaf, note: 单一引擎 / 集中管理 / GPU 友好 / 时长克制 }
  - { name: use-gsap-hook, path: use-gsap-hook.md, tag: leaf, note: useGSAP hook 用法 + 清理 }
  - { name: timeline-organization, path: timeline-organization.md, tag: leaf, note: Timeline 编排 / 标签 / 嵌套 }
  - { name: flip-layout, path: flip-layout.md, tag: leaf, note: FLIP 布局过渡动画 }
  - { name: draggable, path: draggable.md, tag: leaf, note: Draggable 拖拽交互 }
  - { name: reduced-motion, path: reduced-motion.md, tag: leaf, note: prefers-reduced-motion 兼容 }
when_to_descend: |
  写 / 改 `frontend/src/animations/**/*.ts` 或在 .tsx 中调用 gsap / useGSAP / Timeline / Flip / Draggable。
---

# GSAP · 动画库使用约定

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| principles | 叶子 | 单一引擎 / 集中管理 / GPU 友好 / 时长克制 |
| use-gsap-hook | 叶子 | `useGSAP` hook 在 React 中的用法 + 清理 |
| timeline-organization | 叶子 | Timeline 编排 / 标签 / 嵌套子时间线 |
| flip-layout | 叶子 | FLIP 技术做布局过渡 |
| draggable | 叶子 | Draggable 拖拽交互 |
| reduced-motion | 叶子 | `prefers-reduced-motion` 兼容 |

## 何时下钻

- 首次接触动画文件 → `principles.md` 打底
- 在 React 组件里写动画 → `use-gsap-hook.md`
- 多步骤序列 / 复合动画 → `timeline-organization.md`
- 列表重排 / 卡片位移过渡 → `flip-layout.md`
- 拖拽 / 排序交互 → `draggable.md`
- 无障碍 / 用户偏好减少动效 → `reduced-motion.md`

## 下钻决策表

| 任务 | 选哪个子项 |
|------|----------|
| 写新的 `*.animations.ts` | principles + use-gsap-hook + timeline-organization |
| 卡片网格重排过渡 | flip-layout + principles |
| 大纲步骤拖拽排序 | draggable + use-gsap-hook |
| 已有动画做无障碍兼容 | reduced-motion |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../react/index.md`](../react/index.md) · [`../antd/index.md`](../antd/index.md)
