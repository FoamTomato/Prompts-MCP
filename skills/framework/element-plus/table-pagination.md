---
name: element-plus-table-pagination
description: "ElTable 列定义 + ElPagination 服务端分页约定：data 只放当前页、换页触发请求。Use when 用 ElTable 渲染列表 / 接 ElPagination 做分页 / 决定前端还是服务端分页 / 设置 row-key 时。"
parent: ./index.md
paths:
- frontend/src/**/*.vue
- frontend/src/**/*.ts
triggers:
  keywords:
  - ElTable
  - el-table
  - ElPagination
  - el-pagination
  - row-key
  - 服务端分页
  - current-change
  - el-table-v2
effort: medium
context: inline
version: '1.0'
---

# element-plus · ElTable 与服务端分页

## 规则

决策点:**分页一律走服务端,`data` 只放当前页数据,禁止全量灌入再前端 `slice`。**

| 场景 | 做法 |
|------|------|
| 列定义 | `<el-table :data="rows">` + `<el-table-column prop label />` |
| 翻页 / 改页大小 | `@current-change` / `@size-change` 触发请求,传 `page` / `size` |
| 行唯一标识 | `row-key="id"` 用稳定业务 id,禁用数组 index |
| 数据量 > 1w 行 | 改用虚拟滚动 `el-table-v2`(仍服务端分页) |
| total 来源 | 取后端返回的总数,绑 `:total="total"` |

React 生态等价见 [`../antd/table/pagination-server-side.md`](../antd/table/pagination-server-side.md)。

### 反例 — 全量数据前端 slice 分页

```vue
<script setup lang="ts">
const all = ref<User[]>([])          // 反例:一次拉全量,数据大时卡顿且占内存
// 反例:前端 slice,后端 total 失真,无法增量加载
const rows = computed(() => all.value.slice((page.value - 1) * size.value, page.value * size.value))
onMounted(async () => { all.value = await fetchAllUsers() })
</script>
<template>
  <!-- 反例:row-key 用 index,排序/删除后错位 -->
  <el-table :data="rows" :row-key="(_, i) => i">
    <el-table-column prop="name" label="姓名" />
  </el-table>
  <el-pagination :total="all.length" /> <!-- total 取本地长度,失真 -->
</template>
```

### 正例 — current-change 触发服务端查询(流水线编排)

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchUsers } from '@/api/user'      // 取数下沉到 api 层纯函数
import type { User } from '@/types/user'

const rows = ref<User[]>([])
const total = ref(0)
const page = ref(1)
const size = ref(10)
const loading = ref(false)

// 拉取当前页:换页/改页大小/初始化统一走这里
const load = async () => {
  loading.value = true                                   // 进入加载态
  // 仅请求当前页,服务端返回当页数据 + 总数
  const { list, total: count } = await fetchUsers({ page: page.value, size: size.value })
  rows.value = list                                      // 回填当页数据
  total.value = count                                    // 回填总数
  loading.value = false                                  // 退出加载态
}

// 翻页:更新页码后重新取数
const onCurrentChange = (next: number) => { page.value = next; load() }

// 改页大小:回到第一页后重新取数
const onSizeChange = (next: number) => { size.value = next; page.value = 1; load() }

onMounted(load)
</script>

<template>
  <el-table :data="rows" v-loading="loading" row-key="id">
    <el-table-column prop="name" label="姓名" />
    <el-table-column prop="email" label="邮箱" />
  </el-table>
  <el-pagination
    v-model:current-page="page"
    v-model:page-size="size"
    :total="total"
    :page-sizes="[10, 20, 50]"
    layout="total, sizes, prev, pager, next"
    @current-change="onCurrentChange"
    @size-change="onSizeChange"
  />
</template>
```

## 自检

- [ ] `data` 只绑当前页数据,没有 `slice`/`filter` 做前端分页
- [ ] `@current-change` / `@size-change` 各触发一次服务端请求,带上 `page` / `size`
- [ ] `:total` 取后端总数,不是 `data.length`
- [ ] `row-key` 用稳定业务 id,不是数组 index
- [ ] 改页大小时已 reset 到第 1 页
- [ ] 万级以上行评估改用 `el-table-v2` 虚拟滚动

## 相关

- 上层:[`./index.md`](./index.md)
- 同域:[`./form-validation.md`](./form-validation.md)
- 对照(React 等价):[`../antd/table/pagination-server-side.md`](../antd/table/pagination-server-side.md) / [`../antd/table/row-key-stable.md`](../antd/table/row-key-stable.md)
