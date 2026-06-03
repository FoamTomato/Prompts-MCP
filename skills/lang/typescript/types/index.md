---
name: lang-typescript-types-index
description: "TypeScript 进阶类型能力索引（泛型 / 工具类型 / 类型守卫 / 判别联合 / 枚举 / 断言 / 声明文件与 paths 别名）。Use when 设计可复用泛型类型 / 收窄联合类型 / 用判别联合建模状态 / 为配置定义类型别名"
parent: ../index.md
children:
  - { name: generics, path: generics.md, tag: skill, note: "泛型约束 extends / 默认参数 / 条件类型 infer" }
  - { name: utility-types, path: utility-types.md, tag: skill, note: "Pick / Omit / Record / ReturnType / Partial 工具类型" }
  - { name: type-guard, path: type-guard.md, tag: skill, note: "类型守卫 is / in / typeof / 收窄 unknown" }
  - { name: discriminated-union, path: discriminated-union.md, tag: skill, note: "判别联合 tag 字段 / switch 穷尽 never" }
  - { name: enum-vs-const, path: enum-vs-const.md, tag: skill, note: "enum 坑 / const 对象 + as const 替代" }
  - { name: as-const-assertion, path: as-const-assertion.md, tag: skill, note: "as const 把字面量收成只读窄类型，防数组拓宽成 string[]" }
  - { name: declaration-and-paths, path: declaration-and-paths.md, tag: skill, note: ".d.ts 声明文件 / tsconfig paths 别名"}
when_to_descend: |
  设计可复用泛型类型 / 收窄联合类型 → generics / type-guard。
  建模状态机或 API 返回 → discriminated-union。
  为配置 / 常量定义类型别名 → utility-types / enum-vs-const / as-const-assertion。
  外部库无类型或配置路径别名 → declaration-and-paths。
  接不可信外部输入用 unknown 见 ../typing/no-any.md，收窄见 type-guard。
---

# TypeScript · 进阶类型

## 本层包含

| 子项 | 一句话 |
|------|-------|
| generics | 泛型约束 extends / 默认参数 / 条件类型 infer |
| utility-types | Pick / Omit / Record / ReturnType / Partial |
| type-guard | 类型守卫 is / in / typeof，收窄 unknown |
| discriminated-union | 判别联合 tag 字段 + switch 穷尽 never |
| enum-vs-const | enum 坑 vs const 对象 + as const |
| as-const-assertion | as const 字面量收窄，防数组拓宽成 string[] |
| declaration-and-paths | .d.ts 声明文件 / tsconfig paths 别名 |

## 何时下钻

- 写可复用泛型函数/类型，约束类型参数 → `generics.md`
- 从已有类型派生新类型（挑字段/改可选/取返回值）→ `utility-types.md`
- 运行时收窄 unknown / union，写 `x is T` 谓词 → `type-guard.md`
- 用带 tag 的联合建模状态机、API 响应、Result → `discriminated-union.md`
- 定义一组常量并要其类型，纠结 enum 还是对象 → `enum-vs-const.md`
- 需要字面量类型而非 string（路由表/配置/元组）→ `as-const-assertion.md`
- 给无类型 JS 库补声明、配置 `@/` 路径别名 → `declaration-and-paths.md`

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../typing/index.md`](../typing/index.md) · [`../naming/index.md`](../naming/index.md) · [`../modern-syntax/index.md`](../modern-syntax/index.md)
