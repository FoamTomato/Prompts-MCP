---
name: element-plus-setup-and-theme
description: "Element Plus 按需自动导入 + locale(zhCn) + 主题 CSS 变量/SCSS 定制。Use when 第一次接入 Element Plus / 配 locale 国际化 / 改主题色或暗色模式 / 评审全量引入体积问题时。"
parent: ./index.md
paths:
- frontend/src/**/*.vue
- frontend/src/**/*.ts
triggers:
  keywords:
  - 按需导入
  - ElementPlusResolver
  - unplugin-vue-components
  - el-config-provider
  - zhCn
  - "--el-color-primary"
  - 暗色模式
  - CSS 变量
effort: low
context: inline
version: '1.0'
---
# element-plus · 安装与主题

## 规则

**决策点：组件如何引入 + 主题怎么改。**

| 维度 | 决策 | 理由 |
|------|------|------|
| 引入方式 | 自动按需(`unplugin-vue-components` + `ElementPlusResolver`) | 摇树减体积,对照 [`../../fundamentals/frontend/build-tooling/index.md`](../../fundamentals/frontend/build-tooling/index.md) |
| 国际化 | `el-config-provider :locale="zhCn"` | 分页/日期/确认框中文 |
| 全局 size/zIndex | `el-config-provider` 上配,不逐组件传 | 单点配置 |
| 主题色 | CSS 变量覆盖 `--el-color-primary` 或 SCSS 变量 | 不改源码 |
| 暗色模式 | `<html class="dark">` + 引入 dark css vars | 官方约定类名 |

### 反例 —— 全量引入,首屏多打几百 KB

```ts
// ✗ main.ts:整包 import,无法摇树
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'   // ✗ 全量样式
app.use(ElementPlus)
```

### 正例 —— 自动按需(vite.config.ts)

```ts
// vite.config.ts
import Components from 'unplugin-vue-components/vite'
import AutoImport from 'unplugin-auto-import/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

export default defineConfig({
  plugins: [
    vue(),
    // 自动导入 ElMessage / ElLoading 等 API
    AutoImport({ resolvers: [ElementPlusResolver()] }),
    // 自动按需注册组件 + 对应样式(摇树)
    Components({ resolvers: [ElementPlusResolver()] }),
  ],
})
```

### 正例 —— 全局 config-provider(App.vue)

```vue
<!-- App.vue -->
<script setup lang="ts">
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import { useDark } from '@vueuse/core'

// 暗色模式:切换 html.dark 类,Element Plus dark vars 自动接管
const isDark = useDark()
</script>

<template>
  <!-- 单点注入 locale / size / zIndex,组件不再逐个传 -->
  <el-config-provider :locale="zhCn" size="default" :z-index="3000">
    <router-view />
  </el-config-provider>
</template>
```

### 正例 —— 主题色覆盖(styles/theme.scss,入口引入)

```scss
/* styles/theme.scss —— 覆盖 CSS 变量,不动 Element Plus 源码 */
:root {
  --el-color-primary: #3b82f6;
  --el-color-success: #10b981;
  --el-color-warning: #f59e0b;
  --el-color-danger:  #ef4444;
  --el-border-radius-base: 8px;
}
/* 暗色模式额外覆盖(配合 html.dark) */
import 'element-plus/theme-chalk/dark/css-vars.css';
```

## 自检

- [ ] 没有 `import ElementPlus from 'element-plus'` 全量引入
- [ ] vite 配了 `ElementPlusResolver`(Components + AutoImport)
- [ ] `el-config-provider` 注入 `zhCn`,且 size/zIndex 在此单点配置
- [ ] 主题改的是 `--el-color-*` CSS 变量 / SCSS 变量,未改源码
- [ ] 暗色模式通过 `html.dark` 类 + 引入 dark css-vars

## 相关

- 对照(React 生态等价):[`../antd/setup/config-provider.md`](../antd/setup/config-provider.md)
- 构建摇树:[`../../fundamentals/frontend/build-tooling/index.md`](../../fundamentals/frontend/build-tooling/index.md)
- 上层:[`./index.md`](./index.md)
