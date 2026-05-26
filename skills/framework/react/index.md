---
name: framework-react-index
description: React 组件 / Hook / 状态 / 错误处理 / 主题 五大类使用约定索引
parent: ../index.md
children:
  - { name: component, path: component/index.md, tag: folder, note: 组件结构 / 命名 / 文件夹分层 }
  - { name: hook, path: hook/index.md, tag: folder, note: 自定义 Hook 规范 / useEffect 边界 }
  - { name: state, path: state/index.md, tag: folder, note: 状态分层（local / context / zustand） }
  - { name: error-handling, path: error-handling/index.md, tag: folder, note: ErrorBoundary / 异步错误捕获 }
  - { name: theming, path: theming/index.md, tag: folder, note: 主题色板 / dark mode / token }
when_to_descend: |
  写 / 改 `frontend/src/**/*.tsx`、`frontend/src/**/*.ts` 中 React 组件、Hook、状态、主题相关代码。
---

# React · 使用约定

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| component | 文件夹 | 组件结构 / 命名 / 分层 |
| hook | 文件夹 | 自定义 Hook + useEffect 边界 |
| state | 文件夹 | 状态分层选型 |
| error-handling | 文件夹 | ErrorBoundary + 异步错误 |
| theming | 文件夹 | 主题色板与 token |

## 何时下钻

- 写新组件 → `component/index.md` 起步
- 抽取共享逻辑成 Hook → `hook/index.md`
- 数据流跨多层 → `state/index.md` 选型
- 边界异常处理 → `error-handling/index.md`
- 配色 / 暗色模式 → `theming/index.md`

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../antd/index.md`](../antd/index.md) · [`../gsap/index.md`](../gsap/index.md)
