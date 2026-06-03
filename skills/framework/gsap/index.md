---
name: framework-gsap-index
description: GSAP 动画库使用约定索引（原则 / 插件注册 / useGSAP / contextSafe / Timeline / ScrollTrigger / SplitText / FLIP / Draggable / Reduced Motion）
parent: ../index.md
children:
  - { name: principles, path: principles.md, tag: leaf, note: 单一引擎 / 集中管理 / GPU 友好 / 时长克制 }
  - { name: plugin-registration, path: plugin-registration.md, tag: leaf, note: registerPlugin 集中注册一次、先于动画执行；插件直接 import 无需 token }
  - { name: use-gsap-hook, path: use-gsap-hook.md, tag: leaf, note: useGSAP hook 用法 + 清理 }
  - { name: context-safe, path: context-safe.md, tag: leaf, note: 事件回调/延迟动画用 contextSafe 包裹 }
  - { name: timeline-organization, path: timeline-organization.md, tag: leaf, note: Timeline 编排 / 标签 / 嵌套 }
  - { name: scrolltrigger, path: scrolltrigger.md, tag: leaf, note: 进视口入场 / 滚动驱动 / refresh }
  - { name: split-text, path: split-text.md, tag: leaf, note: SplitText 文字逐字/词/行入场 }
  - { name: flip-layout, path: flip-layout.md, tag: leaf, note: FLIP 布局过渡动画 }
  - { name: draggable, path: draggable.md, tag: leaf, note: Draggable 拖拽交互 }
  - { name: reduced-motion, path: reduced-motion.md, tag: leaf, note: prefers-reduced-motion 兼容 }
when_to_descend: |
  写 / 改 `frontend/src/animations/**/*.ts` 或在 .tsx 中调用 gsap / useGSAP / Timeline / ScrollTrigger / SplitText / Flip / Draggable。
---

# GSAP · 动画库使用约定

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| principles | 叶子 | 单一引擎 / 集中管理 / GPU 友好 / 时长克制 |
| plugin-registration | 叶子 | registerPlugin 集中注册一次、先于动画执行；插件直接 import 无需 token |
| use-gsap-hook | 叶子 | `useGSAP` hook 在 React 中的用法 + 清理 |
| context-safe | 叶子 | 事件回调 / 延迟动画用 `contextSafe` 包裹 |
| timeline-organization | 叶子 | Timeline 编排 / 标签 / 嵌套子时间线 |
| scrolltrigger | 叶子 | 进视口入场 / 滚动驱动 / refresh |
| split-text | 叶子 | SplitText 文字逐字/词/行入场 |
| flip-layout | 叶子 | FLIP 技术做布局过渡 |
| draggable | 叶子 | Draggable 拖拽交互 |
| reduced-motion | 叶子 | `prefers-reduced-motion` 兼容 |

## 何时下钻

- 首次接触动画文件 → `principles.md` 打底
- 首次引入某插件（ScrollTrigger/Flip/SplitText）→ `plugin-registration.md`
- 在 React 组件里写动画 → `use-gsap-hook.md`
- 点击 / 延迟 / async 后才触发的动画 → `context-safe.md`
- 多步骤序列 / 复合动画 → `timeline-organization.md`
- 滚到视口才入场 / 滚动驱动进度 → `scrolltrigger.md`
- 标题/文案逐字逐行入场 → `split-text.md`
- 列表重排 / 卡片位移过渡 → `flip-layout.md`
- 拖拽 / 排序交互 → `draggable.md`
- 无障碍 / 用户偏好减少动效 → `reduced-motion.md`

## 下钻决策表

| 任务 | 选哪个子项 |
|------|----------|
| 首次接入 GSAP / 加新插件 | principles + plugin-registration |
| 写新的 `*.animations.ts` | principles + use-gsap-hook + timeline-organization |
| 区块滚到视口才淡入 | scrolltrigger + use-gsap-hook |
| 标题/Hero 文字逐行入场 | split-text + plugin-registration |
| 点击/悬停触发的交互动画 | context-safe + use-gsap-hook |
| 卡片网格重排过渡 | flip-layout + principles |
| 大纲步骤拖拽排序 | draggable + use-gsap-hook |
| 已有动画做无障碍兼容 | reduced-motion |

## 链接

- 上层：[`../index.md`](../index.md)
- 动效设计规约（时长/曲线/入场/stagger/reduced-motion 底线，先看）：[`../../design/component-patterns/motion-and-animation.md`](../../design/component-patterns/motion-and-animation.md)
- 每类组件配哪种入场（规约，先看）：[`../../design/component-patterns/entrance-patterns.md`](../../design/component-patterns/entrance-patterns.md)
- 平行：[`../react/index.md`](../react/index.md) · [`../antd/index.md`](../antd/index.md)
