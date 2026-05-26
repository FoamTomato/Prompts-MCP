---
name: typescript-barrel-export
description: barrel export 仅在 features/<page>/index.ts 使用
parent: ./index.md
paths:
- frontend/src/features/**/index.ts
triggers:
  keywords:
  - barrel
  - index.ts
  - re-export
  - 仅在
  - 使用
effort: medium
context: inline
version: '1.0'
---
# TypeScript · barrel export 边界

## 规则

**barrel export（`index.ts` 汇总 re-export）只在 `features/<page>/` 用，其他地方禁用。**

## 为什么限制

barrel 优点：调用方写 `from "@/features/home"` 更简洁。
barrel 缺点：
1. 增加打包分析难度（tree-shaking 不稳）
2. 容易引入循环依赖
3. 跳转到定义时 IDE 多一跳

## 允许的场景

```ts
// features/home/index.ts
export { HomePage } from "./HomePage";
export { ContentTypeSelector } from "./ContentTypeSelector";
export { GenerateButton } from "./GenerateButton";
export type { HomePageProps } from "./HomePage";
```

调用方：

```ts
import { HomePage, GenerateButton } from "@/features/home";
```

## 不允许的场景

```ts
// ❌ components/ 不要 index.ts
components/index.ts
  export * from "./Button";
  export * from "./Input";
  ...

// ❌ utils/ 不要 index.ts
utils/index.ts
  export * from "./format-date";
  ...
```

`components/` 和 `utils/` 的调用方一律直接 import 具体文件：

```ts
// ✅
import { Button } from "@/components/Button";
import { formatDate } from "@/utils/format-date";
```

## 例外：types/ 可以适度 barrel

仅当一个领域的类型分散到多个文件时：

```ts
// types/textbook/index.ts
export type { Textbook } from "./textbook";
export type { Chapter } from "./chapter";
export type { Subject } from "./subject";
```

## 自检

- [ ] `features/<page>/index.ts` 只做 re-export 不写实现？
- [ ] `components/` / `utils/` 没有 `index.ts`？
- [ ] 调用方 import 简洁但能跳转到原始定义？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`esm-only.md`](./esm-only.md)

