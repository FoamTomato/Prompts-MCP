---
name: typescript-esm-only
description: TypeScript 项目纯 ESM 模块系统 — 禁 require / module.exports / CommonJS 混用
parent: ./index.md
paths:
  - "frontend/**/*.ts"
  - "frontend/**/*.tsx"
triggers:
  keywords: [ESM, CommonJS, import, export, 模块系统, ES Modules]
effort: medium
context: inline
version: "1.0"
---

# TypeScript · ESM only

## 规则

Quill 前端**纯 ESM**：

| 用 | 不用 |
|----|------|
| `import x from "y"` / `export ...` | `require` / `module.exports` |
| `import.meta.env` / `import.meta.url` | `__dirname` / `__filename` |
| `import.meta.glob`（Vite） | webpack-style `require.context` |

## tsconfig

```json
{
  "compilerOptions": {
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "target": "ES2022",
    "esModuleInterop": true,
    "verbatimModuleSyntax": true
  }
}
```

`verbatimModuleSyntax: true` 强制类型 import 显式：

```ts
// ✅
import type { Textbook } from "@/types/textbook";
import { fetchTextbooks } from "@/api/textbooks";

// ❌
import { Textbook, fetchTextbooks } from "@/api/textbooks";  // 类型混在值 import 里
```

## 路径别名

`@/` → `src/`：

```ts
// ✅
import { Button } from "@/components/Button";
import { useSession } from "@/stores/session";

// ❌ 相对路径深嵌套
import { Button } from "../../../components/Button";
```

## 副作用 import

```ts
// 仅副作用，无 export — 用 bare specifier
import "antd/dist/reset.css";
import "@/styles/global.css";
```

## 反例

```ts
// ❌ CommonJS
const x = require("lib");
module.exports = { x };

// ❌ __dirname（Node 全局，Vite 下不存在）
const path = __dirname + "/data.json";

// ✅ ESM 等价
import { fileURLToPath } from "node:url";
const here = fileURLToPath(new URL(".", import.meta.url));
```

## 自检

- [ ] 无 `require` / `module.exports`？
- [ ] 类型 import 用 `import type`？
- [ ] 路径别名 `@/...` 不是相对深嵌套？
- [ ] CSS 副作用 import 顺序：reset → tokens → global？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`barrel-export.md`](./barrel-export.md)

