---
name: typescript-utility-types
description: "TS 内置工具类型派生新类型,禁手抄字段重复 interface。Use when 定义表单草稿可选类型 / API 入参去掉 id / 枚举键值映射 / 从函数取返回值或参数类型"
parent: ./index.md
paths:
- frontend/src/**/*.ts
- frontend/src/**/*.tsx
triggers:
  keywords:
  - utility types
  - Partial
  - Omit
  - Record
  - ReturnType
  - 工具类型
  - 派生类型
effort: medium
context: inline
version: '1.0'
---
# TypeScript · 内置工具类型

## 规则

**决策点:有了源类型就派生,绝不手抄字段。** 改一处源类型,派生类型自动跟随。

| 工具类型 | 作用 | 典型场景 |
|---------|------|---------|
| `Partial<T>` | 全部字段变可选 | 表单草稿 / patch 更新 |
| `Required<T>` | 全部字段变必填 | 收窄可选配置 |
| `Pick<T, K>` | 取指定字段 | 列表只展示部分字段 |
| `Omit<T, K>` | 去掉指定字段 | API 入参去掉 `id` |
| `Record<K, V>` | 键值映射 | 枚举 → 文案/颜色映射 |
| `Readonly<T>` | 全部字段只读 | 不可变 props / 常量 |
| `ReturnType<typeof fn>` | 取函数返回类型 | 复用 service 返回 |
| `Parameters<typeof fn>` | 取函数参数元组 | 复用入参签名 |
| `Awaited<T>` | 拆 Promise 包装 | 取 async 返回的真实类型 |
| `NonNullable<T>` | 去掉 `null` / `undefined` | 收窄可空字段 |

组合:`Pick<T, K> & Partial<...>` 取子集再放宽必填。

## 反例 · 正例

```ts
// 源实体:唯一真相
interface Textbook {
  id: string;
  title: string;
  grade: number;
  publishedAt: string;
}

// ❌ 反例:手抄字段,源类型改了这里不跟随,极易漏改
interface CreateTextbookDTO {
  title: string;
  grade: number;
  publishedAt: string;
}

// ✅ API 入参:从实体去掉后端生成的 id
type CreateTextbookDTO = Omit<Textbook, "id">;

// ✅ 表单草稿:全字段可选,允许逐步填写
type TextbookDraft = Partial<Textbook>;

// ✅ 子集再放宽:列表项仅取标题+年级,且年级可选
type TextbookListItem = Pick<Textbook, "title"> & Partial<Pick<Textbook, "grade">>;

// ✅ 枚举键值映射:状态 → 中文文案,漏写某 key 会编译报错
type TextbookStatus = "draft" | "published" | "archived";
const STATUS_LABEL: Record<TextbookStatus, string> = {
  draft: "草稿",
  published: "已发布",
  archived: "已归档",
};
```

```ts
// 从已有函数派生类型,避免重复声明返回/入参形状
async function fetchTextbook(id: string): Promise<Textbook> {
  // 校验 id 非空,早返回交由上层处理
  return request.get(`/textbooks/${id}`);
}

// ✅ 取返回类型并拆 Promise:得到 Textbook
type FetchResult = Awaited<ReturnType<typeof fetchTextbook>>;

// ✅ 取参数元组:复用入参签名做包装函数
type FetchArgs = Parameters<typeof fetchTextbook>;

// ✅ 去 null:对可空字段收窄
type RequiredTitle = NonNullable<Textbook["title"]>;
```

## 自检

- [ ] 新类型是否从源实体/函数派生,而非手抄字段?
- [ ] API 入参用 `Omit<Entity, "id">` 去掉服务端生成字段?
- [ ] 表单草稿用 `Partial<T>` 而非另写一个全可选 interface?
- [ ] 枚举映射用 `Record<K, V>`,漏 key 会编译报错?
- [ ] 函数返回/参数类型用 `ReturnType` / `Parameters` 复用,未重复声明?

## 相关

- 父:[`./index.md`](./index.md)
- 兄弟:[`./generics.md`](./generics.md) 泛型约束派生条件类型
- 跨引:[`../naming/interface-type-alias.md`](../naming/interface-type-alias.md) interface vs type 选型
