---
name: modern-array-object-methods
description: ES2022+ 标准库新方法采用 — at 取负索引 / findLast 反向查找 / Object.groupBy 分组 / structuredClone 深拷贝 / allSettled 容错。Use when 取末尾元素 / 倒序查找 / 按 key 分组 / 深拷贝对象 / 并发部分失败
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - at
  - findLast
  - findLastIndex
  - Object.groupBy
  - structuredClone
  - allSettled
  - replaceAll
  - top-level await
  - 深拷贝
  - 分组
effort: low
context: inline
version: '1.0'
---
# TypeScript · ES2022+ 数组对象新方法

## 规则

决策点：能用标准库新方法的，别再手写老惯用法。逐条按下表替换，前提是 `tsconfig` 的 `target` / `lib` 覆盖到对应版本（不够则升 `lib` 或保留旧写法）。

| 场景 | 旧写法 | 新写法 | 注意 |
|------|--------|--------|------|
| 取末位元素 | `arr[arr.length - 1]` | `arr.at(-1)` | 负索引从尾倒数 |
| 反向查找 | 倒序 for / `[...arr].reverse().find` | `arr.findLast(fn)` / `arr.findLastIndex(fn)` | 从尾向头找 |
| 按 key 分组 | `arr.reduce` 累加对象 | `Object.groupBy(arr, fn)` / `Map.groupBy(arr, fn)` | 需较新 `lib`(ES2024)；key 非字符串用 `Map.groupBy` |
| 全量替换 | `str.replace(/x/g, y)` | `str.replaceAll('x', y)` | 字面量直接传，无需正则 `g` |
| 深拷贝 | `JSON.parse(JSON.stringify(o))` | `structuredClone(o)` | 保留 Date/Map/Set，但丢函数与原型 |
| 并发容错 | `Promise.all`(一败全败) | `Promise.allSettled` | 要全部跑完、逐个看成败时用 |

顶层 `await`（top-level await）仅在 ESM module 可用，受 `module: esnext` 限制——见兄弟模块 esm-only。`?.` / `??` 不在本层，属 null-safety 维度。

## 反例 → 正例

```ts
// ❌ 老惯用法散落各处
function summarize(orders: Order[]): Summary {
  const latest = orders[orders.length - 1];
  let lastPaid: Order | undefined;
  for (let i = orders.length - 1; i >= 0; i--) {
    if (orders[i].status === "paid") { lastPaid = orders[i]; break; }
  }
  const byBuyer = orders.reduce<Record<string, Order[]>>((acc, o) => {
    (acc[o.buyerId] ??= []).push(o);
    return acc;
  }, {});
  return { latest, lastPaid, byBuyer };
}
```

```ts
// ✅ 标准库新方法 — 注释驱动编排，体内只调用
function summarize(orders: Order[]): Summary {
  // 取最近一笔：负索引从尾倒数
  const latest = orders.at(-1);
  // 反向查找最后一笔已支付订单
  const lastPaid = orders.findLast((o) => o.status === "paid");
  // 按买家分组：key 是字符串故用 Object.groupBy
  const byBuyer = Object.groupBy(orders, (o) => o.buyerId);
  return { latest, lastPaid, byBuyer };
}
```

```ts
// ❌ JSON 深拷贝丢失 Date / Map，且静默把它们变成字符串/空对象
const snapshot = JSON.parse(JSON.stringify(state));

// ✅ structuredClone 保留 Date / Map / Set（注意：含函数的对象会抛错）
const snapshot = structuredClone(state);
```

```ts
// ❌ all 一个失败整批 reject，已成功的结果也拿不到
const pages = await Promise.all(ids.map(fetchPage));

// ✅ allSettled 全部跑完，逐个分拣成败
async function loadPages(ids: string[]): Promise<Page[]> {
  // 并发拉取，允许部分失败
  const results = await Promise.allSettled(ids.map(fetchPage));
  // 过滤出成功项，失败项落日志
  const ok = results.filter((r) => r.status === "fulfilled").map((r) => r.value);
  results
    .filter((r) => r.status === "rejected")
    .forEach((r) => logger.warn("page load failed", r.reason));
  return ok;
}
```

## 自检

- [ ] 取末位 / 倒序查找已换成 `at(-1)` / `findLast` / `findLastIndex`？
- [ ] reduce 手写分组已换成 `Object.groupBy`（字符串 key）或 `Map.groupBy`（任意 key）？
- [ ] 深拷贝用 `structuredClone`，且确认对象不含函数？需要 Date/Map 保真时尤其用它？
- [ ] 并发需要"全部跑完看成败"时用 `Promise.allSettled` 而非 `Promise.all`？
- [ ] 已确认 `tsconfig` 的 `target` / `lib` 覆盖到这些方法（如 groupBy 需 ES2024）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`ts-operators.md`](./ts-operators.md)
- 跨引：顶层 await → [`../module/esm-only.md`](../module/esm-only.md)；`?.` / `??` → [`../null-safety/index.md`](../null-safety/index.md)
