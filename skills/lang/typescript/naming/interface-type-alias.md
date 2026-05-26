---
name: typescript-interface-type-alias
description: interface PascalCase / type alias 仅用于联合/工具。Use when 写 TS 业务代码 / 评审涉及
  `interface-type-alias` 的 PR。
parent: ./index.md
paths:
- frontend/**/*.ts
- frontend/**/*.tsx
triggers:
  keywords:
  - interface
  - type alias
  - PascalCase
  - 仅用于联合
  - 工具
effort: medium
context: inline
version: '1.0'
---
# TypeScript · interface vs type alias

## 规则

| 场景 | 用 |
|------|-----|
| 对象形状（最常见） | `interface` |
| 联合类型 | `type` |
| 元组 | `type` |
| 工具类型组合 | `type` |
| Props / Public API | `interface`（可被合并、被实现） |
| 简单别名 | `type`（更轻） |

## 命名

- **`PascalCase`**：所有类型 / 接口名
- **不加前缀**：禁用 `I`（如 `IUser`）和 `T`（如 `TUser`）
- **明确语义**：`TextbookCardProps` 而非 `Props` / `Data` / `Item`

## 示例

```ts
// ✅ Props 用 interface
export interface TextbookCardProps {
  textbook: Textbook;
  selected?: boolean;
  onSelect: (id: string) => void;
}

// ✅ 联合用 type
type LoadingState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: Textbook[] }
  | { status: "error"; error: string };

// ✅ 工具类型用 type
type PartialBy<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

// ❌ I 前缀
interface IUser { id: string }

// ❌ Data 太泛
type Data = { ... };
```

## interface 合并 vs type 不合并

```ts
// interface 可在多处声明合并（用于 d.ts 扩展第三方）
interface Window {
  myGlobal: string;
}
interface Window {
  another: number;
}   // 两个声明合并

// type 不可合并 — 重复声明报错
type Foo = { a: 1 };
type Foo = { b: 2 };   // ❌
```

## 自检

- [ ] Props 类型用 `interface` 并 export？
- [ ] 联合类型用 `type`？
- [ ] 命名 PascalCase 不带 `I`/`T` 前缀？
- [ ] 命名表达业务语义（不是 Data/Item/Info）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`file-naming.md`](./file-naming.md)

