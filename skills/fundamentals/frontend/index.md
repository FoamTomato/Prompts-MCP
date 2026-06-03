---
name: fundamentals-frontend-index
description: "前端内功维度（写成规约+决策，非八股）— 浏览器渲染 / 事件循环 / HTTP 缓存 / 跨域 / 防抖节流 / 模块化 / 构建 / 状态管理思想。Use when 排查渲染卡顿 / 异步执行顺序 / 缓存不更新 / 跨域 / 打包体积 / 选状态管理方案时。"
parent: ../index.md
children:
  - { name: fundamentals-frontend-rendering-pipeline, path: rendering-pipeline.md, tag: skill, note: "重排 / 重绘 / 合成层 — 何时触发 reflow，怎么提到合成层避开主线程" }
  - { name: fundamentals-frontend-event-loop, path: event-loop.md, tag: skill, note: "宏任务 / 微任务执行顺序，promise vs setTimeout vs requestAnimationFrame 排序" }
  - { name: fundamentals-frontend-http-caching, path: http-caching.md, tag: skill, note: "强缓存（Cache-Control / Expires）vs 协商缓存（ETag / Last-Modified）怎么配" }
  - { name: fundamentals-frontend-cors-same-origin, path: cors-same-origin.md, tag: skill, note: "同源策略边界 / CORS 预检 / 凭证跨域 / 常见跨域报错定位" }
  - { name: fundamentals-frontend-debounce-throttle, path: debounce-throttle.md, tag: skill, note: "防抖 vs 节流何时用哪个 / 前后沿 / 取消与 flush" }
  - { name: fundamentals-frontend-module-systems, path: module-systems.md, tag: skill, note: "CommonJS / ESM / UMD 差异与互操作 / 静态分析与循环依赖" }
  - { name: fundamentals-frontend-build-tooling, path: build-tooling.md, tag: skill, note: "打包 / tree-shaking / bundle 拆分 / 体积治理决策" }
  - { name: fundamentals-frontend-state-management-thinking, path: state-management-thinking.md, tag: skill, note: "单向数据流 / 不可变 / 状态归属，何时上全局状态库" }
when_to_descend: |
  任务涉及「前端内功决策」：排查渲染卡顿 / 掉帧、看不懂 async 执行顺序、改了代码缓存不更新、跨域报错、输入/滚动事件需要防抖节流、CJS 与 ESM 互操作或循环依赖、bundle 体积过大要治理、纠结状态该放组件内还是全局库。
---

# Fundamentals · 前端内功维度

> 这里是「前端内功」，但一律写成**规约 + 工程决策**视角——回答「该怎么选 / 该怎么配 / 卡了怎么定位」，而非原理八股。
> 与 `framework/react/`、`lang/typescript/` 的「用法」互补：那边讲怎么写组件，这边讲为什么卡、异步为何乱序、缓存为何不更新、体积为何大。
> 性能/量级数字为业界参考，落地需自测。

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| rendering-pipeline | skill | 重排 / 重绘 / 合成层 — reflow 触发点与避坑 |
| event-loop | skill | 宏任务 / 微任务执行顺序与排序 |
| http-caching | skill | 强缓存 vs 协商缓存怎么配 |
| cors-same-origin | skill | 同源策略 / CORS 预检 / 跨域报错定位 |
| debounce-throttle | skill | 防抖 vs 节流何时用哪个 |
| module-systems | skill | CJS / ESM / UMD 差异与互操作 |
| build-tooling | skill | 打包 / tree-shaking / bundle 体积治理 |
| state-management-thinking | skill | 单向数据流 / 不可变 / 状态归属 |

## 何时下钻

| 你在做什么 | 进哪个 |
|-----------|-------|
| 页面卡顿 / 掉帧 / 滚动不顺，想知道哪步触发重排重绘、怎么提合成层 | [rendering-pipeline](rendering-pipeline.md) |
| 看不懂 `Promise` / `setTimeout` / `await` 谁先执行、微任务为何插队 | [event-loop](event-loop.md) |
| 改了文件浏览器不更新、或想配 `Cache-Control` / `ETag` 缓存策略 | [http-caching](http-caching.md) |
| 接口报 CORS 错、预检失败、带 cookie 跨域不通 | [cors-same-origin](cors-same-origin.md) |
| 搜索框 / `resize` / `scroll` 触发太频繁，要降频 | [debounce-throttle](debounce-throttle.md) |
| `require` 与 `import` 混用、循环依赖、库既要 CJS 又要 ESM | [module-systems](module-systems.md) |
| bundle 体积过大、tree-shaking 没生效、想拆 chunk | [build-tooling](build-tooling.md) |
| 状态该放组件内还是全局、要不要上 Redux/Zustand、为何要不可变 | [state-management-thinking](state-management-thinking.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行内功：[`../jvm/index.md`](../jvm/index.md) · [`../concurrency-internals/index.md`](../concurrency-internals/index.md) · [`../collection-internals/index.md`](../collection-internals/index.md) · [`../virtual-threads/index.md`](../virtual-threads/index.md) · [`../troubleshooting/index.md`](../troubleshooting/index.md) · [`../distributed-theory/index.md`](../distributed-theory/index.md)
- 用法侧（互补）：[`../../framework/react/performance/index.md`](../../framework/react/performance/index.md) · [`../../lang/typescript/index.md`](../../lang/typescript/index.md) · [`../../framework/react/index.md`](../../framework/react/index.md)
