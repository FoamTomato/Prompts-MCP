---
name: framework-vue-index
description: "Vue3 组合式 API 使用约定索引 — setup / 响应式(ref·reactive·computed·watch) / SFC 结构 / Pinia / Router / 生命周期与响应式丢失坑。Use when 写或改 .vue 组件 / 用组合式 API / 配 Pinia 状态 / 配 Vue Router 路由时。"
parent: ../index.md
children:
  - { name: composition-api, path: composition-api.md, tag: skill, note: "setup 与 script setup 写法 / 顶层逻辑组织 / props·emit 声明" }
  - { name: reactivity, path: reactivity.md, tag: skill, note: "ref vs reactive 选型 / computed / watch vs watchEffect / 解构丢响应" }
  - { name: sfc-structure, path: sfc-structure.md, tag: skill, note: "单文件组件 template·script setup·style 块顺序 / scoped / defineOptions" }
  - { name: pinia, path: pinia.md, tag: skill, note: "defineStore setup 写法 / state·getter·action / storeToRefs 解构" }
  - { name: vue-router, path: vue-router.md, tag: skill, note: "路由表 / 守卫 / useRoute·useRouter / 懒加载 / 动态参数" }
  - { name: lifecycle-and-pitfalls, path: lifecycle-and-pitfalls.md, tag: skill, note: "onMounted 等钩子时机 / reactive 解构与重赋值丢响应 / watch 时机坑" }
when_to_descend: |
  写 / 改 `src/**/*.vue` 组件、用组合式 API(setup/ref/reactive/computed/watch)、配 Pinia 状态、配 Vue Router 路由、排查响应式丢失或生命周期钩子时机问题。
---

# Vue3 · 组合式 API 使用约定

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| composition-api | skill | setup / script setup 写法 / props·emit 声明 |
| reactivity | skill | ref vs reactive / computed / watch / 解构丢响应 |
| sfc-structure | skill | SFC 块顺序 / scoped / defineOptions |
| pinia | skill | defineStore / state·getter·action / storeToRefs |
| vue-router | skill | 路由表 / 守卫 / useRoute·useRouter / 懒加载 |
| lifecycle-and-pitfalls | skill | 钩子时机 / 解构重赋值丢响应 / watch 时机坑 |

## 何时下钻

- 写新组件骨架 / 选 setup 还是 script setup / 声明 props·emit → `composition-api.md`
- 该用 ref 还是 reactive / 派生值用 computed / 副作用用 watch → `reactivity.md`
- 排 `<template>` `<script setup>` `<style scoped>` 块 / 组件命名 → `sfc-structure.md`
- 跨组件共享状态 / 全局 store / storeToRefs 解构 → `pinia.md`
- 配路由表 / 路由守卫 / 编程式跳转 / 路由懒加载 → `vue-router.md`
- 钩子里取不到 DOM / reactive 解构后数据不更新 / watch 不触发 → `lifecycle-and-pitfalls.md`

## 链接

- 上层：[`../index.md`](../index.md)
- 平行对照（React 同类约定）：[`../react/index.md`](../react/index.md)
- 配套 UI 组件库：[`../element-plus/index.md`](../element-plus/index.md)
