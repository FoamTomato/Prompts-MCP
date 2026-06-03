---
name: optional-chaining-nullish
description: 用可选链 ?. 安全取值、用空值合并 ?? 设默认值，避开 || 吞假值的陷阱。Use when 取可空属性 user?.profile?.name / 设默认值 count ?? 10 / 处理后端 null vs undefined 字段
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - optional chaining
  - nullish coalescing
  - 可选链
  - 空值合并
  - "?."
  - "??"
  - count ?? 10
  - null vs undefined
effort: medium
context: inline
version: '1.0'
---
# TypeScript · 可选链与空值合并

## 规则

| 决策点 | 选 | 不选 |
|--------|-----|-------|
| 链式取可空属性 | `a?.b?.c` | `a && a.b && a.b.c` |
| 取可空数组/索引 | `arr?.[i]` | `arr && arr[i]` |
| 调可空方法 | `fn?.()` | `fn && fn()` |
| 设默认值 | `?.`（只兜 null/undefined） | `\|\|`（连 0/''/false 一起吞） |
| `??` 与 `\|\|`/`&&` 混用 | 必加括号 | 裸混用（TS 语法报错） |
| 缺省值语义 | 缺省/可选用 undefined，显式无用 null，与后端对齐 | 两者混用 |

核心陷阱：`count || 10` 会把 `count===0` 当假值替换成 10；`count ?? 10` 只在 `null/undefined` 时兜底，保住 0。

## 反例 · 正例

```ts
// ❌ &&链冗长、且 0/'' 会提前短路返回假值
const name1 = user && user.profile && user.profile.name;
const port1 = config.port || 8080;     // port=0 被吞成 8080
const label1 = item.text || "默认";    // text='' 被吞成 默认

// ✅ ?. 链式 + arr?.[i] + fn?.() + ?? 精确兜底
const name = user?.profile?.name ?? "匿名";
const first = list?.[0]?.id ?? "none";
onChange?.(value);
const port = config.port ?? 8080;      // port=0 保留
```

混用必须加括号（否则 `TS5076` 编译报错）：

```ts
// ❌ 语法报错：?? 不能和 || / && 裸混用
const v1 = a ?? b || c;

// ✅ 用括号显式优先级
const v2 = (a ?? b) || c;
const v3 = a ?? (b || c);
```

JSON.stringify 会丢 `undefined` 键，`null` 会保留——传后端前先归一：

```ts
// 入参组装：用纯函数把 undefined 归一成 null，避免序列化丢字段
const buildPayload = (form: FormValues): ApiPayload => ({
  title: form.title,
  // ❌ remark: form.remark        // remark=undefined 时 JSON.stringify 直接丢掉这个键
  remark: form.remark ?? null,     // ✅ 显式 null，后端能收到「清空」语义
});

const res = await api.save(JSON.stringify(buildPayload(form)));
```

React 组件里编排取值（嵌套 ≤1 层，每步一注释）：

```tsx
function UserCard({ user }: { user?: User }): React.ReactElement {
  // 取可空昵称，?? 兜底而非 ||（保留空串以外的真实值由上游处理）
  const nickname = user?.profile?.nickname ?? "未命名用户";
  // 安全索引访问：noUncheckedIndexedAccess 下 tags[0] 已是 T | undefined
  const primaryTag = user?.tags?.[0]?.label ?? "无标签";

  return <Card title={nickname}>{primaryTag}</Card>;
}
```

数组安全访问与索引类型收窄归 [`../typing/strict-mode.md`](../typing/strict-mode.md)（`noUncheckedIndexedAccess` 让 `arr[i]` 变 `T | undefined`，逼你 `?.` 或守卫）。

## 自检

- [ ] 链式取值用 `a?.b?.c` / `arr?.[i]` / `fn?.()`，没有 `a && a.b` 长链？
- [ ] 默认值用 `??` 而非 `||`，确认 0 / '' / false 不会被误吞？
- [ ] `??` 与 `||` / `&&` 混用处都加了括号（`tsc` 不报 TS5076）？
- [ ] 传后端的字段：缺省用 `undefined`、显式清空用 `?? null`，与后端契约一致？
- [ ] 知道 `JSON.stringify` 丢 `undefined` 键、保留 `null`，序列化前已归一？

## 相关

- 父：[`./index.md`](./index.md)
- 跨引：[`../typing/strict-mode.md`](../typing/strict-mode.md)（noUncheckedIndexedAccess / 安全索引访问）
