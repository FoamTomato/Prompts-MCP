---
name: typescript-as-const-assertion
description: "用 as const 把字面量收成只读窄类型，避免数组被拓宽成 string[]、对象字段退化为 string。Use when 路由表或配置常量想保留字面量 / 数组拓宽成 string[] 丢了三选一约束 / 元组要锁长度与下标 / 纠结 as const 还是 satisfies。"
parent: ./index.md
paths:
- frontend/src/**/*.ts
- frontend/src/**/*.tsx
triggers:
  keywords:
  - as const
  - const assertion
  - readonly tuple
  - literal type widening
  - 字面量收窄
  - 只读元组
  - 类型拓宽
effort: low
context: inline
version: '1.0'
---
# TypeScript · as const 字面量收窄

## 规则

决策点：**需要保字面量（路由表 / 配置常量 / 元组）就加 `as const`**。不加，数组拓宽成 `string[]`、布尔拓宽成 `boolean`，字面量信息全丢。

| 场景 | 选择 | 效果 |
|------|------|------|
| 配置 / 路由表 / 字面量数组要保真 | `as const` | `['a','b'] as const` → `readonly ['a','b']`，元组长度 + 下标字面量全保留 |
| 只想约束形状、不收窄字面量 | `satisfies`（见 [`../modern-syntax/ts-operators.md`](../modern-syntax/ts-operators.md)） | 校验合法性同时保留宽推断，与 `as const` 用途相反 |

`as const` **收窄并冻结成只读字面量**，`satisfies` **校验形状但保留宽推断**——要保字面量选前者。

## 反例 · 正例

```ts
// ❌ config 不加 as const：routes 被拓宽成 string[]，Route 退化为 string
const routes = ["/home", "/order", "/me"];
type Route = (typeof routes)[number];            // = string，失去三选一约束
```

```ts
// ✅ 路由表 + as const：字面量保真，Route 收成精确联合
const ROUTES = ["/home", "/order", "/me"] as const;   // readonly ['/home','/order','/me']
type Route = (typeof ROUTES)[number];                 // = '/home' | '/order' | '/me'

// ✅ 配置对象 + as const：每个值都是字面量类型而非 string/number
const THEME = {
  primary: "#1677ff",
  size: "middle",
  retry: 3,
} as const;                                           // 全字段 readonly + 字面量
type ThemeSize = (typeof THEME)["size"];              // = 'middle'

// 列表场景：as const 元组配合 map 推导映射，无手写 for
const STATUS = ["draft", "active", "done"] as const;
const STATUS_LABEL: Record<(typeof STATUS)[number], string> = {
  draft: "草稿",
  active: "进行中",
  done: "已完成",
};
const options = STATUS.map((value) => ({ value, label: STATUS_LABEL[value] }));
```

## 自检

- [ ] 路由表 / 字面量常量 / 元组加了 `as const`，没被拓宽成 `string[]` / `boolean`？
- [ ] 只想校验形状不收窄字面量的场景用 `satisfies` 而非 `as const`？
- [ ] 从 `as const` 常量派生联合类型用 `(typeof X)[number]`，新增项类型自动跟随？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`./enum-vs-const.md`](./enum-vs-const.md)（const 对象 + 联合替代 enum，同族）
- 跨引：[`../modern-syntax/ts-operators.md`](../modern-syntax/ts-operators.md)（`satisfies` 与 `as const` 的区别）
- 接不可信外部输入用 `unknown`：[`../typing/no-any.md`](../typing/no-any.md) + 收窄见 [`./type-guard.md`](./type-guard.md)
