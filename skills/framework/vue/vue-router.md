---
name: vue-router
description: "Vue Router 用 createRouter+createWebHistory，路由 component 懒加载 import()，鉴权放全局 beforeEach 早返回。Use when 配置路由表 / 加鉴权守卫 / 取 params·query / meta 标权限时。"
parent: ./index.md
paths:
- frontend/src/**/*.vue
- frontend/src/**/*.ts
triggers:
  keywords:
  - vue-router
  - createRouter
  - createWebHistory
  - beforeEach
  - useRoute
  - 路由守卫
  - 路由懒加载
  - meta
effort: medium
context: inline
version: '1.0'
---
# Vue Router · 路由配置与鉴权守卫

## 规则

决策点：**鉴权放哪、路由怎么拆、参数怎么传**。

| 场景 | 选择 |
|------|------|
| 创建路由 | `createRouter({ history: createWebHistory(), routes })`，**禁** hash 模式除非部署受限 |
| 页面组件 | `component: () => import('@/views/X.vue')` 懒加载分包（对标 React code-splitting） |
| 登录态 / 角色鉴权 | **全局** `router.beforeEach`，**禁**每个组件各写一遍 |
| 标记需鉴权的路由 | `meta: { requiresAuth: true, roles: [...] }`，守卫读 `to.meta` 判定 |
| 路径强关联资源（`/user/:id`） | `params`；可选筛选 / 分页 | `query` |

- 守卫体**早返回**：先放行公开路由，再判登录、判角色，每分支必 **`return`**（true / 跳转对象 / next）。
- `query` 取出**全是字符串**，数字 / 布尔需转换，>3 行转换下沉 `utils` 纯函数。
- 用 `to.matched.some(r => r.meta.requiresAuth)` 判权限，覆盖嵌套路由。
- 坑：守卫某分支漏 `next` / 漏 `return` → 导航永久挂起页面卡白；`query.page` 是 `"2"` 不是 `2`，先 `Number()`。

## 反例

```ts
// ❌ 守卫漏 next；组件直接同步 import 不分包；query 当数字用
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !isLogin()) {
    // 漏 next() / 漏 return —— 导航卡死，页面永远白屏
  }
  next()
})
const page = route.query.page + 1 // "2" + 1 === "21"
```

## 正例

```ts
// router/index.ts —— createWebHistory + 懒加载 + meta 标权限
import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  // 1. 公开页：不标 requiresAuth
  { path: '/login', component: () => import('@/views/Login.vue') },
  // 2. 受保护页：懒加载分包 + meta 标记权限与角色
  { path: '/admin', component: () => import('@/views/Admin.vue'), meta: { requiresAuth: true, roles: ['admin'] } },
]

const router = createRouter({ history: createWebHistory(), routes })

// 3. 全局鉴权守卫：早返回，每分支必 return next
router.beforeEach((to) => {
  // 公开路由直接放行
  const needAuth = to.matched.some((r) => r.meta.requiresAuth)
  if (!needAuth) return true
  // 未登录跳登录页并带回跳地址
  if (!isLogin()) return { path: '/login', query: { redirect: to.fullPath } }
  // 角色不足跳 403
  if (!hasRole(to.meta.roles as string[] | undefined)) return { path: '/403' }
  // 校验通过放行
  return true
})

export default router
```

```vue
<!-- 组件内取参：params 直接用，query 转换下沉 utils 纯函数 -->
<script setup lang="ts">
import { useRoute } from 'vue-router'
import { parsePageQuery } from '@/utils/route'

const route = useRoute()
// 1. 路径资源标识用 params
const userId = route.params.id as string
// 2. query 全是字符串，分页参数下沉纯函数转换
const { page, size } = parsePageQuery(route.query)
</script>
```

```ts
// utils/route.ts —— query 字符串转数字的纯函数
export function parsePageQuery(q: Record<string, unknown>) {
  // 兜底默认值并转 Number，避免字符串拼接
  const page = Number(q.page ?? 1)
  const size = Number(q.size ?? 20)
  return { page, size }
}
```

## 自检

- [ ] `createRouter` 用 `createWebHistory`，页面组件全是 `() => import()` 懒加载？
- [ ] 鉴权只在全局 `beforeEach`，未在各组件重复写？
- [ ] 守卫每条分支都 `return`（true / 跳转对象 / next），无挂起路径？
- [ ] 受保护路由用 `meta.requiresAuth`，并以 `to.matched.some` 覆盖嵌套？
- [ ] `query` 取值转换成数字 / 布尔，>3 行转换下沉 `utils` 纯函数？

## 相关

- 父：[`./index.md`](./index.md)
- 跨引（懒加载分包 / 构建产物切分）：[`../../fundamentals/frontend/build-tooling.md`](../../fundamentals/frontend/build-tooling.md)
