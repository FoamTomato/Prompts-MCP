---
name: typescript-no-any
description: 禁 any — 用 unknown + 类型守卫
parent: ./index.md
paths:
  - "frontend/**/*.ts"
  - "frontend/**/*.tsx"
triggers:
  keywords: [any, unknown, type guard, 类型守卫]
effort: medium
context: inline
version: "1.0"
---

# TypeScript · 禁 any

## 规则

**禁 `any`**。必要时用 `unknown` + 类型守卫缩窄。

## 反例 → 正例

```ts
// ❌ any 是逃逸口
function parse(data: any) {
  return data.user.name;   // 运行时炸
}

// ✅ unknown + 守卫
function parse(data: unknown) {
  if (typeof data === "object" && data !== null && "user" in data) {
    const user = (data as { user: unknown }).user;
    if (typeof user === "object" && user !== null && "name" in user) {
      const name = (user as { name: unknown }).name;
      if (typeof name === "string") return name;
    }
  }
  throw new Error("invalid data");
}
```

实用上用 `zod` 解析：

```ts
import { z } from "zod";

const Schema = z.object({ user: z.object({ name: z.string() }) });

function parse(data: unknown) {
  return Schema.parse(data).user.name;
}
```

## 其他禁用

| 禁用 | 替代 |
|------|------|
| `any` | `unknown` + 守卫 / zod |
| `Function` | 写具体签名 `(x: number) => string` |
| `{}` 对象类型 | `Record<string, unknown>` |
| `as` 强制断言 | 类型守卫 / zod；必须用 as 时加注释解释 |
| `enum` | `as const` 对象 + union 类型 |

```ts
// ❌ enum
enum Status { Pending = "pending", Done = "done" }

// ✅ as const + union
const Status = { Pending: "pending", Done: "done" } as const;
type Status = (typeof Status)[keyof typeof Status];
```

## API 返回类型

```ts
// ✅ 每个 api 模块的返回类型显式声明
import type { Textbook } from "@/types/textbook";

export const textbooksApi = {
  list: (params?: ListParams): Promise<Textbook[]> =>
    client.get<{ data: Textbook[] }>("/textbooks", { params }).then(r => r.data.data),
};
```

## 自检

- [ ] 业务代码无 `any`？
- [ ] 外部数据用 `unknown` 接，zod 校验后才使用？
- [ ] 无 `enum`（用 as const + union 替代）？
- [ ] `as` 断言加了说明注释？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`strict-mode.md`](./strict-mode.md)

