---
name: vue-lifecycle-and-pitfalls
description: "Vue3 组合式生命周期钩子时机与高频坑 — onMounted/onUnmounted/onUpdated 及取数·DOM·清理放哪。Use when 钩子里取不到模板 ref / 监听定时器未清理泄漏 / 解构 reactive 丢响应 / 顶层 await 不渲染。"
parent: ./index.md
paths:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.ts"
triggers:
  keywords:
    - onMounted
    - onUnmounted
    - onUpdated
    - 生命周期
    - 模板引用
    - template ref
    - 副作用清理
    - 顶层 await
    - Suspense
    - addEventListener
effort: medium
context: inline
version: '1.0'
---

# Vue3 · 生命周期钩子时机与高频坑

## 规则

**先按「这件事必须在哪个时点做」选钩子,再决定清理放哪:**

| 要做的事 | 放哪 | 关键约束 |
|---------|------|---------|
| 取数请求 | `onMounted` 或 script setup 顶层 `await` | 顶层 `await` 让 setup 变异步,**父级必须包 `<Suspense>`** 否则不渲染 |
| DOM 操作 / 读模板 ref | `onMounted` | `ref()` 模板引用在 setup 同步阶段为 `null`,**挂载后才有值** |
| 解绑监听 / 清定时器 / 关 socket | `onUnmounted` | 凡在 setup/onMounted 注册的副作用,**必须在此对称清理**(对标 react effect-cleanup-leak) |
| DOM 更新后读新布局 | `onUpdated` 或 `nextTick()` | 慎用 `onUpdated`,任意响应式变更都触发,易死循环 |

核心坑(高频踩):
- **解构 `reactive` / `props` 丢响应** → 用 `toRefs` 或不解构,详见 `./reactivity.md`。
- **`watch` 默认浅** → 深层属性变更不触发,加 `{ deep: true }`;首次即跑加 `{ immediate: true }`。
- **`v-if` 与 `v-for` 不要同元素** → Vue3 中 `v-if` 优先级更高、拿不到 `v-for` 变量;拆成外层 `<template v-for>` 内层 `v-if`。
- **模板 ref 在 setup 同步阶段是 `null`** → 必须 `onMounted` 后访问。
- **异步 setup(顶层 await)需 `<Suspense>`** → 否则组件不渲染、无报错难排查。

### 反例 · onMounted 注册监听却不在 onUnmounted 解绑(内存泄漏)

```ts
// ❌ 只注册不清理:组件卸载后 handler 仍持有 vm,定时器仍在跑 → 泄漏
onMounted(() => {
  window.addEventListener('resize', onResize)
  timer = setInterval(poll, 1000)
})
```

### 正例 · 对称注册与清理(流水线编排)

```ts
import { ref, onMounted, onUnmounted } from 'vue'

const boxRef = ref<HTMLDivElement | null>(null)
const list = ref<Item[]>([])
let timer: number | undefined
// 把布局测量逻辑下沉为纯函数,onMounted/onResize 复用
const measure = (el: HTMLElement | null) => (el ? el.getBoundingClientRect().width : 0)
const width = ref(0)

const onResize = () => {
  // 重新测量宽度
  width.value = measure(boxRef.value)
}

onMounted(async () => {
  // 1. 取数:挂载后拉首屏列表
  list.value = await fetchList()
  // 2. DOM:此刻模板 ref 才有值,首次测量
  width.value = measure(boxRef.value)
  // 3. 副作用:注册监听与轮询
  window.addEventListener('resize', onResize)
  timer = window.setInterval(() => { list.value = [] }, 1000)
})

onUnmounted(() => {
  // 对称清理:解绑监听 + 清定时器,防泄漏
  window.removeEventListener('resize', onResize)
  if (timer) window.clearInterval(timer)
})
```

```vue
<!-- ✅ 顶层 await 的子组件,父级用 Suspense 包裹 -->
<Suspense>
  <AsyncDashboard />
  <template #fallback><Spin /></template>
</Suspense>
```

## 自检

- [ ] 在 onMounted/setup 注册的监听·定时器·socket,都有 onUnmounted 对称清理
- [ ] 取数放 onMounted 或顶层 await,DOM 操作 / 模板 ref 访问在 onMounted 后
- [ ] 用了顶层 await 的组件,父级已包 `<Suspense>`
- [ ] 没有 `v-if` 与 `v-for` 写在同一元素
- [ ] watch 深层属性已加 `{ deep: true }`,需首次执行已加 `{ immediate: true }`
- [ ] 没有解构 reactive / props 导致丢响应

## 相关

- [`./reactivity.md`](./reactivity.md) —— ref/reactive/watch 选型与解构丢响应
- [`./composition-api.md`](./composition-api.md) —— setup / script setup 顶层逻辑组织
- [`../../fundamentals/frontend/event-loop.md`](../../fundamentals/frontend/event-loop.md) —— nextTick 与微任务时序原理
