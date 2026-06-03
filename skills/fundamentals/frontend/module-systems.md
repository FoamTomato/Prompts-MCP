---
name: fundamentals-frontend-module-systems
description: "模块化体系 CJS/ESM/UMD 的工程选型与互操作 — 新代码用 ESM，CJS 仅遗留 Node 工具，UMD 仅浏览器 script 库。Use when 选模块格式 / CJS 与 ESM 互操作报错 / 配 package.json type 与 exports 时。"
parent: ./index.md
paths:
- frontend/src/**/*.ts
- frontend/src/**/*.tsx
- frontend/src/**/*.vue
triggers:
  keywords:
  - ESM
  - CommonJS
  - UMD
  - 模块化
  - import
  - exports 字段
  - esModuleInterop
  - require is not defined
effort: low
context: inline
version: '1.0'
---
# Fundamentals · 模块化体系 CJS/ESM/UMD 选型

> 决策点：写新代码、引依赖、发布库时该选哪种模块格式，以及混用时的互操作坑。
> 一句话：**新代码一律 ESM**；CJS 仅遗留与 Node 传统工具；UMD 仅给浏览器 `<script>` 标签的发布库。

## 规则

| 场景 | 选 | 为什么 |
|------|----|--------|
| 前端业务新代码 | **ESM** `import`/`export` | 静态可分析→tree-shake，浏览器/打包器原生 |
| 库要被打包器消费 | ESM（保留 `import`） | 让下游 tree-shake，体积最小 |
| Node CLI / 旧脚手架 / 老 config | CJS `require`/`module.exports` | 动态加载、Node 传统生态 |
| 发布库给浏览器 `<script src>` 直接用 | UMD | 同时兼容 AMD/CJS/全局变量 |
| 同时服务打包器与裸 `<script>` | ESM + UMD 双产物 | `exports` 走 ESM，`<script>` 走 UMD |

要点：
- ESM 是**静态**的（顶层 import 在解析期确定），所以能 tree-shake、能并行加载；动态用 `import()`。
- CJS 是**运行时**的（`require` 是函数调用，可放在条件里），无法静态 tree-shake。
- UMD 是一段自适应包装，检测环境后挂到 AMD/CJS/`window`——仅当目标是裸浏览器引入时才需要。
- 纯 ESM 写法约束见 [`../../lang/typescript/module/esm-only.md`](../../lang/typescript/module/esm-only.md)。

## 反例 · 正例

```ts
// ❌ 新前端代码用 CommonJS：打包器无法 tree-shake，且 Vite 下报 "require is not defined"
const { fetchArticles } = require("@/api/articles");
module.exports = { listView };

// ✅ ESM：静态导入，可摇树
import { fetchArticles } from "@/api/articles";
export { listView };
```

CJS↔ESM 互操作的 default 差异（最常见坑）：

```ts
// CJS 模块 module.exports = fn 在 ESM 里默认整体是 default
// ✅ esModuleInterop 开启后
import dayjs from "dayjs";          // CJS 默认导出
import { Buffer } from "node:buffer"; // Node 内置具名

// ❌ 关掉 interop / 误用：拿到的是带 __esModule 标记的命名空间对象
import * as dayjs from "dayjs";
dayjs();                            // TypeError: dayjs is not a function
```

`package.json` 字段决定整包模块系统与入口解析：

```jsonc
{
  "type": "module",                 // .js 文件按 ESM 解析；不写则按 CJS
  "exports": {                      // 条件导出，优先级高于 main/module
    ".": {
      "import": "./dist/index.mjs", // 打包器/ESM 走这里
      "require": "./dist/index.cjs" // require() 走这里
    }
  }
}
```

```ts
// 坑：type:module 下写 require → "require is not defined in ES module scope"
// 坑：CJS 文件里写顶层 import → "Cannot use import statement outside a module"
// 解法：保持单一格式；要混用就靠扩展名 .mjs(ESM) / .cjs(CJS) 或 exports 条件分流
```

构建产物格式与双包配置见 [`./build-tooling.md`](./build-tooling.md)。

## 自检

- [ ] 新代码全用 `import`/`export`，无 `require`/`module.exports`？
- [ ] 引 CJS 库用默认导入而非 `import * as`（`esModuleInterop: true`）？
- [ ] `package.json` 的 `type` 与文件扩展名/写法一致，无 import/require 混用报错？
- [ ] 发布库：打包器入口走 `exports.import`，裸 `<script>` 才出 UMD？
- [ ] 用 UMD 仅因目标是浏览器直接引入，而非默认选项？

## 相关

- 父：[`./index.md`](./index.md)
- 纯 ESM 写法规约：[`../../lang/typescript/module/index.md`](../../lang/typescript/module/index.md) · [`../../lang/typescript/module/esm-only.md`](../../lang/typescript/module/esm-only.md)
- 构建产物/tree-shaking：[`./build-tooling.md`](./build-tooling.md)
