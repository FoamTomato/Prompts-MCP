---
name: typescript-strict-mode
description: tsconfig strict + noUncheckedIndexedAccess 全启用
parent: ./index.md
paths:
- frontend/**/*.ts
- frontend/**/*.tsx
- frontend/tsconfig.json
triggers:
  keywords:
  - TypeScript
  - strict
  - tsconfig
  - noUncheckedIndexedAccess
  - 全启用
effort: medium
context: inline
version: '1.0'
---
# TypeScript · strict mode

## 规则

`tsconfig.json` 必须开 **strict + noUncheckedIndexedAccess + exactOptionalPropertyTypes**：

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true,
    "noFallthroughCasesInSwitch": true,
    "paths": { "@/*": ["./src/*"] }
  }
}
```

## 各项含义

| 选项 | 作用 | 典型修复 |
|------|------|---------|
| `strict` | 总开关（含 strictNullChecks 等 6 项） | 必须开 |
| `noUncheckedIndexedAccess` | `arr[i]` 类型变 `T \| undefined` | 加 if 守卫或非空断言（仅在确认安全时） |
| `noImplicitOverride` | 子类覆盖必须显式 `override` 关键字 | 加 `override` |
| `exactOptionalPropertyTypes` | `foo?: string` ≠ `foo: string \| undefined` | 不要给 optional 字段显式赋 undefined |

## 索引访问示例

```ts
const items = ["a", "b", "c"];

// ❌ items[10] 看似 string，运行时是 undefined
const x: string = items[10];        // 编译期通过，运行时崩

// ✅ noUncheckedIndexedAccess 强制类型变成 string | undefined
const x = items[10];                // x: string | undefined
if (x) doSomething(x);
```

## 编辑器集成

VSCode：自动启用项目 tsconfig。
CI:
```bash
pnpm tsc --noEmit
```

## 自检

- [ ] tsconfig 包含上述 5 个选项？
- [ ] CI 跑 `tsc --noEmit` 全绿？
- [ ] 没有 `// @ts-ignore` / `// @ts-expect-error`（必要时带说明注释）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`no-any.md`](./no-any.md)

