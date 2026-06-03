---
name: typescript-type-guard
description: "用类型守卫在分支前收窄联合类型：typeof / instanceof / in / 字面量比较 / 自定义谓词 x is T。Use when 收窄联合类型分支 / 校验 API 响应或 unknown / 写 isFoo 谓词函数 / 想用 as 强转跳过校验时"
parent: ./index.md
paths:
- frontend/src/**/*.ts
- frontend/src/**/*.tsx
triggers:
  keywords:
  - type guard
  - type narrowing
  - typeof
  - instanceof
  - in operator
  - user-defined type guard
  - x is T
  - 类型守卫
  - 类型收窄
  - 谓词函数
effort: medium
context: inline
version: '1.0'
---
# TypeScript · 类型守卫与收窄

## 规则

联合类型 / `unknown` 取值前，**先用守卫收窄到具体分支再访问字段**——别 `as` 强转跳过运行时校验。

| 要判别的是 | 用守卫 | 收窄结果 |
|-----------|--------|---------|
| 原始类型（string/number/boolean） | `typeof x === 'string'` | `x: string` |
| 是否某个类实例（Error/Date/自定义类） | `x instanceof ApiError` | `x: ApiError` |
| 对象有无某属性 | `'id' in obj` | 含 `id` 的那一支 |
| 字面量 / 带 tag 的联合 | `x.kind === 'success'` | 对应判别联合分支 |
| 跨边界数据（API 响应 / unknown） | 自定义谓词 `function isUser(x): x is User` | `x: User` |

决策：**跨边界数据集中校验**——把 `unknown` / API 响应交给一个谓词函数（或 [`../error-handling/assert-helpers.md`](../error-handling/assert-helpers.md) 的 `asserts value is T`）逐字段校验后再收窄，校验逻辑只写一处。**模型内部状态**用带 tag 的[判别联合](./discriminated-union.md)，比手写 `in` / `typeof` 更稳。

## 反例 · 正例

```ts
// ❌ as 强转：跳过运行时校验，res 字段缺失/类型错时运行期才炸，类型系统帮不了你
const user = (await api.get("/me")).data as User;
console.log(user.profile.name);   // data 实为 {error:'401'} 时这里 TypeError

// ❌ 联合不收窄直接访问：TS 报「属性不存在于某分支」
function area(s: Circle | Square) {
  return Math.PI * s.radius ** 2;  // Square 没有 radius
}
```

```ts
// ✅ 自定义谓词：跨边界数据集中逐字段校验，返回 x is User 供调用方收窄
const isUser = (x: unknown): x is User =>
  typeof x === "object" && x !== null
  && "id" in x && typeof (x as Record<string, unknown>).id === "string"
  && "name" in x && typeof (x as Record<string, unknown>).name === "string";

async function fetchUser(): Promise<User> {
  // 拿到 unknown 响应
  const raw: unknown = (await api.get("/me")).data;
  // 谓词收窄前先校验，失败抛错而非裸 as
  if (!isUser(raw)) throw new ApiError({ code: "U001", message: "用户响应格式非法" });
  // 此处 raw 已收窄为 User，安全访问
  return raw;
}
```

```ts
// ✅ typeof / in / instanceof / 字面量 四种内置守卫
function describe(v: string | number): string {
  // 原始类型用 typeof 收窄
  if (typeof v === "string") return v.trim();
  return v.toFixed(2);            // 此支 v 收窄为 number
}

function getId(obj: { id: string } | { code: string }): string {
  // 属性存在用 in 收窄到对应分支
  return "id" in obj ? obj.id : obj.code;
}

function toMessage(err: unknown): string {
  // 类实例用 instanceof 收窄
  if (err instanceof ApiError) return `[${err.code}] ${err.message}`;
  if (err instanceof Error) return err.message;
  return String(err);
}

function render(state: Loading | Success): string {
  // 字面量/tag 比较收窄判别联合（建模见 discriminated-union）
  return state.kind === "success" ? state.data.title : "加载中…";
}
```

谓词函数体内 `>3 行的逐字段校验`下沉为独立纯函数复用；列表筛选用 `arr.filter(isUser)`——`filter` 接受谓词后返回的数组已被收窄为 `User[]`，无需再 `as`。

## 自检

- [ ] 联合 / `unknown` 取字段前已用守卫收窄，没有裸 `as T` 跳过校验？
- [ ] 跨边界数据（API 响应 / unknown）由谓词函数或 `asserts` 集中校验，校验只一处？
- [ ] 原始类型用 `typeof`、类实例用 `instanceof`、属性用 `in`、tag 用字面量比较——选对工具？
- [ ] 模型内部状态优先用带 tag 的判别联合，而非手写多个 `in` / `typeof`？
- [ ] `arr.filter(isFoo)` 直接拿到收窄后的 `Foo[]`，没有额外 `as`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`./discriminated-union.md`](./discriminated-union.md)（带 tag 的联合建模 + switch 穷尽 never）
- 跨引：[`../error-handling/assert-helpers.md`](../error-handling/assert-helpers.md)（`asserts value is T` 集中校验后收窄）
