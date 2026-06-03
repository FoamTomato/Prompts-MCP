---
name: typescript-declaration-and-paths
description: "为无类型 JS 库补 .d.ts 声明文件并配 tsconfig paths 别名替代深相对路径。Use when 引入无类型第三方库报红 / 声明全局类型或挂载 window / 配置 @/ 别名 / import 出现 ../../.."
parent: ./index.md
paths:
- frontend/src/**/*.ts
- frontend/src/**/*.tsx
triggers:
  keywords:
  - declaration file
  - .d.ts
  - declare module
  - declare global
  - tsconfig paths
  - path alias
  - 声明文件
  - 路径别名
effort: low
context: inline
version: '1.0'
---
# TypeScript · 声明文件与路径别名

## 规则

**决策点一:无类型库补 `.d.ts`,绝不 `as any` 抹掉报红。** 声明文件只描述类型、不产 JS 代码。

| 场景 | 写法 | 放哪 |
|------|------|------|
| 第三方 JS 库无 `@types` | `declare module 'foo' { ... }` | `src/types/foo.d.ts` |
| 全局类型 / 挂 `window` | `declare global { interface Window { ... } }` | `src/types/global.d.ts` |
| 资源导入(`*.svg`/`*.css`) | `declare module '*.svg'` | `src/types/assets.d.ts` |

> `declare global` 必须写在一个 module(文件里有 `import`/`export`)内,否则视作普通脚本污染全局。

**决策点二:路径别名只配 `@/` 一个根指向 `src/`,别滥设多别名。** 多别名(`@components` `@utils` …)增加心智与配置维护成本,统一 `@/components` 即可。

```jsonc
// tsconfig.json —— 编译期类型解析
{ "compilerOptions": { "baseUrl": ".", "paths": { "@/*": ["src/*"] } } }
```

> 坑:`tsconfig paths` 只管类型检查,运行时/打包需同步配——否则编译过但跑起来「找不到模块」。
> - Vite:`resolve.alias` 配 `@` → `src`(或装 `vite-tsconfig-paths` 自动读)。
> - Jest:`moduleNameMapper` 配 `^@/(.*)$` → `<rootDir>/src/$1`(或 `ts-jest` 的 `pathsToModuleNameMapper`)。

## 反例 · 正例

```ts
// ❌ 反例:无类型库直接 any,丢掉一切类型与补全
import legacyChart from "legacy-chart"; // 报红 → 被迫 (legacyChart as any).render()

// ❌ 反例:深相对路径,目录一移全断
import { formatMoney } from "../../../../shared/utils/money";
```

```ts
// src/types/legacy-chart.d.ts —— 声明文件不产代码,只描述类型
declare module "legacy-chart" {
  // 声明库导出的形状,按需补关键方法即可
  export interface ChartOptions {
    data: number[];
    color?: string;
  }
  export function render(el: HTMLElement, options: ChartOptions): void;
}
```

```ts
// src/types/global.d.ts —— 全局类型挂载 window
// 文件需含 import/export 才构成 module,declare global 才生效
export {};
declare global {
  interface Window {
    __APP_VERSION__: string;
  }
}
```

```ts
// ✅ 业务文件:别名替代深相对,目录迁移不受影响
// 取格式化工具:统一从 @/ 根引入
import { formatMoney } from "@/shared/utils/money";
// 取声明过的库:类型与补全齐全
import { render } from "legacy-chart";

// 渲染图表:无前置校验,直接编排
const draw = (el: HTMLElement, data: number[]): void => render(el, { data });
```

## 自检

- [ ] 无类型库是补了 `.d.ts`(`declare module`)而非 `as any` 抹红?
- [ ] 全局类型放 `global.d.ts`,且文件含 `export {}` 让 `declare global` 生效?
- [ ] 路径别名只配 `@/` → `src/*` 一个根,没滥设多别名?
- [ ] `tsconfig paths` 配了后,Vite `resolve.alias` / Jest `moduleNameMapper` 也同步配了?
- [ ] import 里没再出现 `../../../..` 这类深相对路径?

## 相关

- 父:[`./index.md`](./index.md)
- 跨引:[`../module/index.md`](../module/index.md) ESM 模块规范与 barrel export
