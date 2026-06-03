---
name: vue-sfc-structure
description: ".vue 单文件组件三块固定顺序 script setup·template·style scoped，样式默认 scoped 防污染。Use when 新建或改 .vue 组件 / 排块顺序 / 声明 props·emits / 抽 composable / template 太重时。"
parent: ./index.md
paths:
- frontend/src/**/*.vue
- frontend/src/**/*.ts
triggers:
  keywords:
  - SFC 结构
  - script setup
  - style scoped
  - defineProps
  - defineEmits
  - composable
  - PascalCase 组件名
  - 内联表达式
effort: low
context: inline
version: '1.0'
---
# Vue · SFC 单文件组件结构

## 规则

决策点：块顺序、样式作用域、逻辑下沉位置三者固定，按下表落位。

| 维度 | 规约 | 理由 |
|------|------|------|
| 块顺序 | `<script setup lang="ts">` → `<template>` → `<style scoped>` | 逻辑先行，读组件先看依赖与状态 |
| 样式作用域 | `<style>` 默认必带 `scoped` | 不 scoped 则全局污染，跨组件互相覆盖 |
| 组件命名 | 多词 PascalCase（`UserCard` 非 `card`） | 与原生标签区分，避免冲突 |
| props/emits | `defineProps<T>()` / `defineEmits<T>()` 类型声明 | 编译期类型校验，禁运行时对象写法 |
| 复杂逻辑 | >3 行的转换/计算抽 composable（`useXxx`） | template 保持薄，逻辑可复用可测 |
| 列表渲染 | `v-for` 必带 `:key` 用稳定业务 id | 见 react/component/key-stability，禁 index |

`<script setup>` 顶层即组件作用域：顶层声明的变量/函数/import 自动暴露 template，无需 return。

### 反例 · template 塞大量内联表达式

```vue
<!-- 内联过滤+格式化+拼接，逻辑散在 template 无法复用、难测 -->
<template>
  <div v-for="(u, i) in users.filter(x => x.active).sort((a,b)=>b.score-a.score)" :key="i">
    {{ u.firstName + ' ' + u.lastName }} — {{ (u.score * 100).toFixed(1) }}%
  </div>
</template>
```

### 正例 · computed 下沉 + 薄 template + composable

```ts
// frontend/src/composables/useRankedUsers.ts —— 排序/格式化逻辑下沉为纯 composable
import { computed, type Ref } from 'vue';
import type { User } from '@/types/user';

interface RankedUser { id: string; displayName: string; scoreText: string; }

// 工具纯函数：单个用户 → 展示模型
const toRankedUser = (u: User): RankedUser => ({
  id: u.id,
  displayName: `${u.firstName} ${u.lastName}`,
  scoreText: `${(u.score * 100).toFixed(1)}%`,
});

export function useRankedUsers(users: Ref<User[]>) {
  // 派生：过滤活跃 → 按分降序 → 映射展示模型
  const rankedUsers = computed<RankedUser[]>(() =>
    users.value
      .filter((u) => u.active)
      .sort((a, b) => b.score - a.score)
      .map(toRankedUser),
  );

  return { rankedUsers };
}
```

```vue
<script setup lang="ts">
// 顶层即组件作用域：声明即暴露给 template，无需 return
import { toRef } from 'vue';
import { useRankedUsers } from '@/composables/useRankedUsers';
import type { User } from '@/types/user';

// props 用类型声明，编译期校验
const props = defineProps<{ users: User[] }>();
const emit = defineEmits<{ select: [id: string] }>();

// 复杂派生逻辑下沉 composable，组件体保持平坦
const { rankedUsers } = useRankedUsers(toRef(props, 'users'));
</script>

<template>
  <!-- template 薄：只读派生结果、:key 用稳定 id -->
  <div v-for="user in rankedUsers" :key="user.id" @click="emit('select', user.id)">
    {{ user.displayName }} — {{ user.scoreText }}
  </div>
</template>

<style scoped>
div { cursor: pointer; } /* scoped 隔离，不污染全局 */
</style>
```

## 自检

- [ ] 块顺序 `<script setup>` → `<template>` → `<style scoped>`
- [ ] `<style>` 带 `scoped`，无全局污染
- [ ] 组件名多词 PascalCase
- [ ] props/emits 用 `defineProps<T>` / `defineEmits<T>` 类型声明
- [ ] template 内无大段内联表达式，>3 行逻辑抽 computed/composable
- [ ] `v-for` 带 `:key` 且为稳定业务 id（非 index）

## 相关

- [`composition-api.md`](composition-api.md) —— script setup 写法 / props·emit 声明细节
- [`reactivity.md`](reactivity.md) —— computed / ref 选型
- [`../react/component/key-stability.md`](../react/component/key-stability.md) —— 列表 key 稳定性对照
