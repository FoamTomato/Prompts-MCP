---
name: vue-pinia
description: "Vue3 全局状态管理 Pinia — defineStore 组合式 setup store，storeToRefs 解构保响应式。Use when 写 defineStore / 跨组件读全局 store / 解构 store 丢响应式 / actions 改 state。"
parent: ./index.md
paths:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.ts"
triggers:
  keywords:
  - Pinia
  - defineStore
  - storeToRefs
  - setup store
  - 全局状态
  - 跨组件共享
  - getters
  - actions
effort: medium
context: inline
version: '1.0'
---

# Vue3 · Pinia 全局状态管理

## 规则

**先判定状态归属,够用即停,别一上来就 Pinia:**

| 场景 | 选谁 | 理由 |
|------|------|------|
| 组件内自用 | `ref`/`reactive` | 局部态不外泄 |
| 父子 / 几层内共享 | `props` down + `emit` up | 单向数据流,见 ../../fundamentals/frontend/state-management-thinking.md |
| 跨组件 / 跨路由共享客户端态 | **Pinia** | 唯一数据源,替代 Vuex |
| 服务端态(接口数据) | **query 层,不进 store** | 缓存/失效归 query,塞 store 要手动同步 |

**store 写法只用组合式 setup store**(对齐组件 `script setup` 心智):
- `state` → `ref()`;`getters` → `computed()`;`actions` → 普通 `function`。
- `return` 暴露的即 store 的公开 API;不 return 的为私有。
- **组件里解构 store 必走 `storeToRefs`**:它只把 state/getter 转 ref 保响应式,action 仍直接从 store 取(详见 ./reactivity.md 解构丢响应坑)。

### 反例 · 直接解构 store 丢响应式

```ts
import { useCartStore } from '@/stores/cart'
const store = useCartStore()
// ❌ 直接解构:count/total 退化为一次性快照,store 更新后视图不刷新
const { count, total } = store
// ❌ 把 action 也 storeToRefs:action 是函数无需转 ref,这样反而调不动
```

### 正例 · setup store 定义 + storeToRefs 解构

```ts
// stores/cart.ts —— 组合式 setup store
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { calcCartTotal } from '@/utils/cart'

export const useCartStore = defineStore('cart', () => {
  // 1. state 用 ref:基本类型 / 数组皆可
  const items = ref<CartItem[]>([])
  // 2. getter 用 computed:派生值只读、自动缓存,纯计算下沉 utils
  const total = computed(() => calcCartTotal(items.value))
  const count = computed(() => items.value.length)
  // 3. action 用普通 function:不可变替换而非原地 mutate
  const addItem = (item: CartItem) => { items.value = [...items.value, item] }
  // 4. return 暴露的即公开 API
  return { items, total, count, addItem }
})
```

```vue
<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useCartStore } from '@/stores/cart'

const store = useCartStore()
// 1. state / getter 走 storeToRefs 解构,保住响应式
const { items, total, count } = storeToRefs(store)
// 2. action 直接从 store 取,无需 storeToRefs
const { addItem } = store
</script>

<template>
  <p>共 {{ count }} 件,合计 {{ total }}</p>
  <button @click="addItem(newItem)">加入</button>
</template>
```

## 自检

- [ ] 先按归属梯子判定:组件内 ref / 父子 props+emit / 跨组件才上 Pinia?
- [ ] 服务端接口数据归 query 层,没塞进 store 手动同步?
- [ ] store 用组合式 setup store:state=ref、getter=computed、action=function?
- [ ] 组件里解构 state/getter 走了 `storeToRefs`,没有 `const { x } = store`?
- [ ] action 直接从 store 取,没被 `storeToRefs` 包?
- [ ] action 里走不可变替换,>3 行计算下沉 utils 纯函数?

## 相关

- 父:[`./index.md`](./index.md)
- 兄弟:[`./reactivity.md`](./reactivity.md)(解构丢响应式 / ref·computed 选型)
- 兄弟:[`./composition-api.md`](./composition-api.md)(`script setup` 心智一致)
- 决策视角:[`../../fundamentals/frontend/state-management-thinking.md`](../../fundamentals/frontend/state-management-thinking.md)(状态归属梯 / 服务端态不进 store)
- 流水线风格:[`../../lang/java/pipeline-style/index.md`](../../lang/java/pipeline-style/index.md)
