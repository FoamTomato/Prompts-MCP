---
name: typescript-assert-helpers
description: Asserts 工具集 + asserts value is T 谓词收窄类型 + 11 个常用断言方法
parent: ./index.md
paths:
  - "frontend/app/lib/assertion.ts"
  - "frontend/app/**/*.ts"
  - "frontend/app/**/*.tsx"
triggers:
  keywords: [Asserts, assert, "asserts value is", type narrowing, 类型收窄]
effort: medium
context: inline
version: "1.0"
---

# TypeScript · Asserts 工具

## 11 个静态方法

```typescript
export const Asserts = {
  notNull<T>(value: T | null | undefined, opts: AssertOpts): asserts value is T,
  notBlank(value: string | null | undefined, opts: AssertOpts): asserts value is string,
  notEmpty<T>(arr: readonly T[] | null | undefined, opts: AssertOpts): asserts arr is readonly T[],
  inRange(value: number, min: number, max: number, opts: AssertOpts): void,
  maxLength(value: string | readonly unknown[], maxLen: number, opts: AssertOpts): void,
  minLength(value: string | readonly unknown[], minLen: number, opts: AssertOpts): void,
  matches(value: string, pattern: RegExp, opts: AssertOpts): void,
  equals<T>(actual: T, expected: T, opts: AssertOpts): void,
  contains<T>(haystack: readonly T[], needle: T, opts: AssertOpts): void,
  isTrue(condition: boolean, opts: AssertOpts): asserts condition,
  isFalse(condition: boolean, opts: AssertOpts): asserts condition is false,
};
```

每个失败 → 抛 `ApiError({code, message, httpStatus?})`。

## TS 断言谓词的威力

`asserts value is T` 返回类型让 TypeScript **自动收窄**调用方的类型：

```typescript
function loadUserDoc(user: User | null) {
  // 此处 user 是 User | null
  Asserts.notNull(user, { code: "A002", message: "Session 已过期" });
  // ↓ Asserts 通过后，TS 把 user 收窄为 User
  console.log(user.id);  // 不需要 user!.id 或 if (user) {...}
}
```

```typescript
function checkTitle(title: string | undefined) {
  // title: string | undefined
  Asserts.notBlank(title, { code: "D003", message: "标题不能为空" });
  // ↓ TS 知道 title 现在是 string
  return title.trim();  // 不需要 title?.trim()
}
```

```typescript
function processEnabled(enabled: boolean) {
  Asserts.isTrue(enabled, { code: "R005", message: "邀请功能已关闭" });
  // TS 知道 enabled 现在是 true
}
```

## 典型用法：表单校验

```typescript
import { Asserts, ApiError } from "@/app/lib/assertion";

interface OutlineForm {
  title: string;
  slideCount: number;
  chapterIds: string[];
}

function validateForm(form: OutlineForm): void {
  Asserts.notBlank(form.title, { code: "D003", message: "大纲标题不能为空", httpStatus: 422 });
  Asserts.maxLength(form.title, 200, { code: "D003", message: "标题不能超过 200 字符", httpStatus: 422 });
  Asserts.inRange(form.slideCount, 3, 20, { code: "D002", message: "幻灯片数 3-20", httpStatus: 422 });
  Asserts.notEmpty(form.chapterIds, { code: "D005", message: "请选择至少一个章节", httpStatus: 422 });
}
```

调用方在 onSubmit 用 try/catch + `instanceof ApiError` 接住，见 [`form-error-handling.md`](./form-error-handling.md)。

## 反例

```typescript
// ❌ 自己写 if + throw
if (!form.title) throw new Error("标题不能为空");
// 没拿到 code / 没收窄类型

// ❌ Asserts 失败后再 if 检查
Asserts.notNull(user, { code: "A002", message: "..." });
if (user) {  // 多此一举，TS 已经知道 user is User
  ...
}

// ❌ 把 Asserts 当 return（它没返回值）
const valid = Asserts.notBlank(title, { ... });  // valid 是 undefined

// ❌ 在循环里用 Asserts（每行抛异常成本高）
for (const row of bigArray) {
  Asserts.notBlank(row.name, { ... });  // 改批量收集
}
```

## 自检

- [ ] 用 `Asserts.<方法>` 而非自己写 if + throw？
- [ ] 利用 `asserts value is T` 谓词省略后续 `!` / `?.`？
- [ ] 失败时拿到的是 ApiError 含 code，不是泛型 Error？
- [ ] 大数组循环改批量收集而不是逐项断言？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`api-error-class.md`](./api-error-class.md) · [`form-error-handling.md`](./form-error-handling.md)
- 配套：[`../typing/strict-mode.md`](../typing/strict-mode.md)
- 实战代码：`frontend/app/lib/assertion.ts`
