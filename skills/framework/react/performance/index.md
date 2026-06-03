---
name: framework-react-performance-index
description: React 前端性能优化索引：长列表虚拟化、路由/组件代码分割懒加载、Core Web Vitals 之 CLS 布局抖动治理。Use when 列表滚动卡顿 / 首屏加载慢 / 页面布局抖动 / Lighthouse 性能评分优化
parent: ../index.md
children:
  - { name: list-virtualization, path: list-virtualization.md, tag: skill, note: 长列表/表格虚拟滚动只渲染可视区 }
  - { name: code-splitting, path: code-splitting.md, tag: skill, note: 路由/组件 lazy + Suspense 按需加载拆包 }
  - { name: web-vitals-cls, path: web-vitals-cls.md, tag: skill, note: CLS 布局抖动：占位骨架/尺寸预留 }
when_to_descend: |
  长列表滚动卡顿、DOM 节点过多 → list-virtualization；
  首屏 bundle 过大 / 加载慢 → code-splitting；
  页面元素跳动、Lighthouse CLS 红 → web-vitals-cls。
  仅渲染次数过多(memo/useMemo)走 ../component/re-render-minimization，与本层正交。
---

# React Performance · 子项索引

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| list-virtualization | skill | 长列表/表格虚拟滚动，只渲染可视区 DOM |
| code-splitting | skill | 路由/组件 lazy + Suspense 按需加载拆包 |
| web-vitals-cls | skill | CLS 布局抖动治理：占位骨架与尺寸预留 |

## 何时下钻

- 列表/表格滚动卡顿、DOM 节点数千级 → [`list-virtualization.md`](list-virtualization.md)
- 首屏 bundle 体积大、加载白屏久 → [`code-splitting.md`](code-splitting.md)
- 页面元素加载时跳动、Lighthouse CLS 偏高 → [`web-vitals-cls.md`](web-vitals-cls.md)

## 链接

- 上层：[`../index.md`](../index.md)
- 正交：[`../component/index.md`](../component/index.md)（re-render-minimization 管渲染次数 memo，本层管渲染量/加载/布局）
