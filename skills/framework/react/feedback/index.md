---
name: framework-react-feedback-index
description: React 数据反馈态使用约定:Skeleton 骨架屏加载 + Empty 空态。房规:loading 用 Skeleton 不用全屏 Spin,零数据用 Empty 并区分无数据/筛空/出错三态。
parent: ../index.md
children:
  - { name: skeleton-loading, path: skeleton-loading.md, tag: skill, note: Skeleton 骨架屏 vs Spin/Suspense }
  - { name: empty-state, path: empty-state.md, tag: skill, note: Empty 空态 + 无数据/筛空/出错三分 }
when_to_descend: |
  渲染数据加载态或零数据态时下钻。房规:loading 用 Skeleton 占位、不用全屏 Spin;零数据用 Empty,并区分无数据 / 筛选无结果 / 请求出错三态。
---

# React Feedback · 子项索引

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| skeleton-loading | skill | Skeleton 骨架屏 vs Spin/Suspense |
| empty-state | skill | Empty 空态 + 无数据/筛空/出错三分 |

## 何时下钻

- 数据加载占位 → `skeleton-loading.md`:房规优先 Skeleton,不用全屏 Spin
- 列表/详情零数据 → `empty-state.md`:用 Empty 并区分无数据 / 筛选无结果 / 请求出错三态

## 链接

- 上层:[`../index.md`](../index.md)
- 平行:[`../error-handling/index.md`](../error-handling/index.md) · [`../state/index.md`](../state/index.md)
