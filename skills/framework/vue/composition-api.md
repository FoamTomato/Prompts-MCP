---
name: vue-composition-api
description: "Vue3 组件一律用 script setup 组合式写法，可复用有状态逻辑抽 composable。Use when 写或改 .vue 组件 / 选组合式 vs Options API / 跨组件复用逻辑 / 类型化 defineProps·defineEmits 时。"
parent: ./index.md
paths:
- frontend/src/**/*.vue
- frontend/src/**/*.ts
triggers:
  keywords:
  - script setup
  - composition-api
  - composable
  - defineProps
  - defineEmits
  - defineExpose
  - useXxx
  - 组合式 API
effort: medium
context: inline
version: '1.0'
---
# Vue3 · 组合式 API 与 script setup

## 规则

决策点：**新代码一律组合式；逻辑放哪、要不要抽 composable**。

| 场景 | 选择 |
|------|------|
| 任何新 `.vue` 组件 | `<script setup lang="ts">` 组合式，**禁** `export default { data(){} }` |
| 跨组件复用**有状态**逻辑（计数 / 拉取 / 鼠标位置 / 表单） | 抽 composable `useXxx`（对标 React 自定义 hook） |
| 仅本组件用的逻辑 | 留在 `<script setup>` 顶层，按关注点分段 |
| 纯函数转换 / 校验（无响应式状态） | 抽 `utils/` 纯函数，不是 composable |
| Options API | **仅维护遗留组件**，不写新的 |

- 顶层逻辑按**关注点**组织：每段一行注释点明意图，读注释＝读流程。
- `defineProps` / `defineEmits` / `defineExpose` 一律**泛型类型化**，不传运行时对象。
- composable 内部同样早返回 + 步骤注释；返回 `ref` / `computed` 而非解构后的裸值（解构丢响应见 `./reactivity.md`）。

## 反例

```vue
<!-- ❌ 新组件用 Options API；props 无类型；逻辑散落各选项 -->
<script>
export default {
  props: ['userId'],
  data() { return { user: null, loading: false } },
  async created() {
    this.loading = true
    this.user = await fetchUser(this.userId)
    this.loading = false
  },
}
</script>
```

## 正例

```vue
<!-- ✅ script setup + 类型化 props/emit + 复用逻辑下沉 composable -->
<script setup lang="ts">
import { computed } from 'vue'
import { useUser } from '@/composables/useUser'

// 1. 类型化 props 与 emit（泛型，非运行时对象）
const props = defineProps<{ userId: string }>()
const emit = defineEmits<{ loaded: [user: User] }>()

// 2. 有状态拉取逻辑下沉 composable
const { user, loading } = useUser(props.userId, (u) => emit('loaded', u))

// 3. 派生展示值用 computed
const title = computed(() => (loading.value ? '加载中…' : user.value?.name ?? '未知'))
</script>
```

```ts
// composables/useUser.ts —— useXxx 命名，返回 ref/computed
import { ref, watchEffect, type Ref } from 'vue'

export function useUser(userId: string, onLoaded?: (u: User) => void) {
  // 1. 声明响应式状态
  const user = ref<User | null>(null)
  const loading = ref(false)

  // 2. id 变化即重新拉取（早返回守卫空 id）
  watchEffect(async () => {
    if (!userId) return
    loading.value = true
    user.value = await fetchUser(userId)
    loading.value = false
    if (user.value) onLoaded?.(user.value)
  })

  // 3. 暴露只读结果给组件
  return { user, loading } as { user: Ref<User | null>; loading: Ref<boolean> }
}
```

## 自检

- [ ] 新组件用 `<script setup lang="ts">`，没有 `data(){return}` Options 写法？
- [ ] `defineProps` / `defineEmits` / `defineExpose` 用泛型类型化？
- [ ] 跨组件复用的有状态逻辑抽成了 `useXxx` composable？
- [ ] composable 返回 `ref` / `computed`，未提前解构成裸值？
- [ ] 顶层逻辑按关注点分段，每段有意图注释，嵌套 ≤1 层？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟（ref/reactive/computed/watch 与解构丢响应）：[`./reactivity.md`](./reactivity.md)
- 平行对照（React 自定义 hook 顺序与规则）：[`../react/hook/index.md`](../react/hook/index.md)
