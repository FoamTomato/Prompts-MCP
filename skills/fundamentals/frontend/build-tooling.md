---
name: fundamentals-frontend-build-tooling
description: "构建打包与 Tree-shaking 体积治理决策 — Vite 开发走 esbuild+原生 ESM、生产走 Rollup 打包，摇树靠 ESM 静态分析删未用导出。Use when bundle 超预算 / tree-shaking 没生效 / 引整库要改按需 / 找哪个 chunk 大时。"
parent: ./index.md
paths:
- frontend/src/**/*.ts
- frontend/src/**/*.tsx
- frontend/src/**/*.vue
triggers:
  keywords:
  - tree-shaking
  - bundle 体积
  - Vite
  - Rollup
  - esbuild
  - sideEffects
  - 按需导入
  - rollup-plugin-visualizer
  - 摇树
effort: medium
context: inline
version: '1.0'
---
# Fundamentals · 构建打包与 Tree-shaking 体积治理

> 决策点：bundle 太大 / 摇树没删掉死代码时，先确认摇树前提，再按「按需 > 分割 > 压缩」排优先级治理。
> 一句话：**Vite 开发用 esbuild + 原生 ESM 求快，生产交 Rollup 打包；tree-shaking 靠 ESM 静态分析，前提是 ESM 导入 + 无副作用 + 按需。**

## 规则

减体积优先级（自上而下逐项做，别一上来就只盯压缩）：

| 优先级 | 手段 | 收益 / 关键 |
|--------|------|------------|
| 1 按需导入 | `import { x } from 'lib'` 而非整库 / `import *` | 直接少打死代码，前提是库导出 ESM |
| 2 代码分割 | 路由级 / 重组件 `import()` 拆 chunk | 降首屏，详见 [`../../framework/react/performance/code-splitting.md`](../../framework/react/performance/code-splitting.md) |
| 3 压缩 | esbuild/terser minify + gzip/brotli | 最后一道，挤不出结构性收益 |

Tree-shaking 三个前提（缺一摇不动）：
- **用 ESM 导入**：CJS 库是运行时 `require`，静态分析不了，整包打入；摇树只对 ESM 生效。
- **模块无副作用**：库在 `package.json` 标 `"sideEffects": false`（或列白名单如 `["*.css"]`），打包器才敢删未用导出。
- **按需引用**：导入具名成员，别 `import *`（整命名空间被视为全用）。

工具分工：开发态 Vite 用 esbuild 转译 + 浏览器原生 ESM 不打包（启动快、HMR 快）；生产态走 Rollup 真打包做摇树 / 分包 / 压缩——**所以「dev 正常、build 后体积爆/行为变」要按 Rollup 产物排查**。

## 反例 · 正例

```ts
// ❌ 整库导入：lodash 是 CJS + 有副作用，整包 ~70KB 全打进来
import _ from "lodash";
const ids = _.uniq(rawIds);

// ❌ import * 破坏摇树：整个命名空间被当作"全用了"，删不掉
import * as icons from "@/icons";
const icon = icons.Search;

// ✅ 按需具名导入：只打用到的导出（lodash-es 是 ESM 版，可摇树）
import { uniq } from "lodash-es";
const ids = uniq(rawIds);

// ✅ 直接指向子路径，绕开 barrel 聚合
import Search from "@/icons/Search";
```

发布自己的库时声明无副作用，让下游摇树：

```jsonc
// package.json —— 没有运行时副作用就标 false；只有 CSS/polyfill 有副作用时列白名单
{
  "sideEffects": false
  // 或: "sideEffects": ["*.css", "./src/polyfill.ts"]
}
```

体积排查：用 visualizer 出火焰图，先找最大的几块再动手。

```ts
// vite.config.ts —— 前置：仅 analyze 模式挂插件，避免污染常规构建
import { defineConfig } from "vite";
import { visualizer } from "rollup-plugin-visualizer";

export default defineConfig(({ mode }) => {
  // 步骤1：判定是否分析模式
  const isAnalyze = mode === "analyze";
  // 步骤2：按需挂载 visualizer（gzipSize 看真实传输体积，treemap 看占比）
  const analyzePlugins = isAnalyze
    ? [visualizer({ open: true, gzipSize: true, template: "treemap" })]
    : [];
  // 步骤3：返回配置，插件列表平铺
  return { plugins: [...analyzePlugins] };
});
```

## 自检

- [ ] 引第三方库用具名按需导入，无 `import *` 整库 / 无整包默认导入大库？
- [ ] 大库优先选 ESM 版本（如 `lodash-es`/`date-fns`），CJS-only 库已知会整包打入？
- [ ] 自己发布的库 `package.json` 标了 `sideEffects`（无副作用→false）？
- [ ] barrel `index.ts` 聚合导出没把整目录拖进首屏？详见 [`../../lang/typescript/module/barrel-export.md`](../../lang/typescript/module/barrel-export.md)
- [ ] 体积治理顺序为「按需 → 分割 → 压缩」，而非只压缩？
- [ ] 体积异常已用 `rollup-plugin-visualizer` 定位到具体大块，再动手？

## 相关

- 父：[`./index.md`](./index.md)
- 模块格式前提（CJS 摇不动 / ESM 才能摇）：[`./module-systems.md`](./module-systems.md)
- 代码分割（优先级 2）：[`../../framework/react/performance/code-splitting.md`](../../framework/react/performance/code-splitting.md)
- barrel 聚合拖累首屏：[`../../lang/typescript/module/barrel-export.md`](../../lang/typescript/module/barrel-export.md)
