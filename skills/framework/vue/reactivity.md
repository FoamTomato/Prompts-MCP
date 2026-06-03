---
name: vue-reactivity
description: "Vue3 响应式 API 选型 — ref / reactive / computed / watch·watchEffect。Use when 选 ref 还是 reactive / 解构 reactive 或 props 丢响应式 / 派生值用 computed / watch 不触发。"
parent: ./index.md
paths:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.ts"
triggers:
  keywords:
    - ref
    - reactive
    - computed
    - watch
    - watchEffect
    - toRefs
    - .value
    - 响应式丢失
    - 解构丢响应
    - 派生值
effort: high
context: inline
version: '1.0'
---

# Vue3 · 响应式 ref/reactive/computed/watch

## 规则

**先判定要的是「状态」还是「派生/副作用」,再选 API:**

| 需求 | 选谁 | 关键约束 |
|------|------|---------|
| 基本类型状态(number/string/boolean) | `ref` | JS 里用 `.value` 读写;模板里自动解包,不写 `.value` |
| 对象/数组状态 | `ref`(推荐,可整体重赋值)或 `reactive`(不可重赋值) | `reactive` 解构即丢响应,整体替换用 `ref` |
| 派生值(由别的响应式算出) | `computed` | 有缓存、只读;**禁止在 getter 里写副作用** |
| 副作用 · 显式依赖 + 要新旧值 | `watch` | 第一参列明源,回调拿 `(newVal, oldVal)` |
| 副作用 · 自动收集依赖 | `watchEffect` | 立即执行、回调内读到的响应式即依赖,拿不到旧值 |

核心坑(高频踩):
- **解构 `reactive` 对象会丢响应式** → 用 `toRefs(obj)` 解构,或不解构直接 `obj.x`。
- **`ref` 嵌在 `reactive` 里自动解包**(`state.count` 而非 `state.count.value`);但 **`ref` 放进数组/Map 不解包**,仍需 `.value`。
- **`watch` 监听对象内部深层属性需 `{ deep: true }`**;监听 `reactive` 对象自身已默认深层,监听 `ref` 包的对象不深层。
- `watch` 默认惰性,要首次即跑加 `{ immediate: true }`。

### 反例 · 解构 props / reactive 丢响应式

```ts
// ❌ 解构 props:user 变成一次性快照,父组件更新后子组件不刷新
const { user, list } = defineProps<{ user: User; list: Item[] }>()
// ❌ 解构 reactive:name/age 退化为普通值,后续赋值不触发视图
const state = reactive({ name: 'a', age: 1 })
const { name, age } = state
// ❌ computed 里塞副作用:每次重算都改外部状态,缓存语义被破坏
const total = computed(() => { saveLog(); return price.value * qty.value })
```

### 正例 · toRefs / computed / watch 流水线编排

```vue
<script setup lang="ts">
import { ref, reactive, computed, watch, toRefs } from 'vue'
import { calcOrderTotal, isValidQty } from '@/utils/order'

const props = defineProps<{ initialQty: number }>()

// 1. 基本类型状态用 ref:模板里自动解包,JS 里 .value
const qty = ref(props.initialQty)
const price = ref(0)

// 2. 关联的一组状态用 reactive 聚合;解构时走 toRefs 保住响应式
const form = reactive({ remark: '', coupon: '' })
const { remark, coupon } = toRefs(form)

// 3. 派生值用 computed:只读 + 自动缓存,纯函数下沉 utils
const total = computed(() => calcOrderTotal(price.value, qty.value, coupon.value))

// 4. 副作用且要新旧值 + 校验 → watch 显式声明依赖源
watch(qty, (next, prev) => {
  // 4a. 非法数量回滚到旧值,逻辑下沉 utils 纯函数
  if (!isValidQty(next)) qty.value = prev
})

// 5. 深层对象副作用 → watch 加 deep
watch(form, (next) => syncDraft(next), { deep: true })
</script>

<template>
  <!-- 模板里 ref 自动解包:写 qty / total,不写 .value -->
  <input v-model.number="qty" />
  <input v-model="remark" />
  <p>合计 {{ total }}</p>
</template>
```

## 自检

- [ ] 基本类型用 `ref` 且 JS 侧都带 `.value`?模板侧没多写 `.value`?
- [ ] 解构 `reactive` / `props` 处都过了 `toRefs` / `toRef`,没有直接 `const { x } = state`?
- [ ] 派生值用 `computed`,getter 内**无任何副作用**(无赋值/无请求/无 log)?
- [ ] 要新旧值用 `watch`,纯自动依赖用 `watchEffect`,选对了没?
- [ ] 监听深层对象属性加了 `{ deep: true }`?要首跑加了 `{ immediate: true }`?
- [ ] `ref` 被塞进数组/Map 的地方仍写了 `.value`?

## 相关

- 父:[`./index.md`](./index.md)
- 兄弟:[`./lifecycle-and-pitfalls.md`](./lifecycle-and-pitfalls.md)(钩子时机 / reactive 重赋值丢响应 / watch 触发时机坑)
- 兄弟:[`./composition-api.md`](./composition-api.md)(`script setup` / `defineProps` 声明)
- 跨维度:[`../../lang/java/pipeline-style/index.md`](../../lang/java/pipeline-style/index.md)(注释驱动流水线编排风格)
