---
name: coercion-equality-and-coercion
description: JS 相等判断与隐式类型转换的踩坑规约（=== / Number.isNaN / typeof null / sort 比较器 / parseInt radix / falsy）。Use when 纠结 == 还是 === / 判 NaN 或 null / 数组排序乱序 / parseInt 解析
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - 相等判断
  - 类型转换
  - strict equality
  - Number.isNaN
  - typeof null
  - sort 比较器
  - parseInt radix
  - falsy
  - "==="
  - "[].sort()"
effort: medium
context: inline
version: '1.0'
---
# TypeScript · 相等与类型转换

## 规则

决策点：能用 `===` 就别用 `==`；判 NaN/null/排序/解析各有专用写法，别靠隐式转换。

| 场景 | 用 | 禁 | 坑 |
|------|-----|-----|-----|
| 相等比较 | `===` / `!==` | `==` / `!=` | `"0" == false`、`[] == false` 都为 `true`，但 `Boolean([])` 也为 `true` |
| 判 NaN | `Number.isNaN(x)` | 全局 `isNaN(x)` | 全局版先 `Number(x)` 强转，`isNaN("abc")` 误判为 `true` |
| 判 null | `x === null` / `x?.` | `typeof x === "object"` | 历史 bug：`typeof null === "object"` |
| 数组排序 | `arr.sort((a,b)=>a-b)` | `arr.sort()` | 默认按 UTF-16 字典序，`[5,3,10].sort()` → `[10,3,5]` |
| 字符串转整数 | `parseInt(s, 10)` | `parseInt(s)` | 不带 radix 解析有歧义，`parseInt("08")` 取决于环境 |

falsy 清单（仅这 8 个，其余皆 truthy，含 `[]` / `{}` / `"0"`）：`false` / `0` / `-0` / `0n` / `""` / `null` / `undefined` / `NaN`。

## 反例 · 正例

```ts
// ❌ == 触发隐式转换，结果反直觉
"0" == false;        // true（两侧都转成数字 0）
[] == false;         // true（[] 转成 ""，再转成 0）
Boolean([]);         // true（空数组是 truthy，与上面的 == 结论冲突）

// ✅ === 不做类型转换，所见即所得
const isZero = value === 0;
const isEmpty = list.length === 0;     // 判空用 length，不要靠 [] 的真值
```

```ts
// ❌ 全局 isNaN 先 Number() 强转，把非数字误判成 NaN
isNaN("abc");                          // true —— "abc" 根本不是 NaN
// ❌ typeof 判 null 永远落空（历史遗留 bug）
typeof null === "object";              // true，挡不住 null

// ✅ Number.isNaN 不强转，只认真正的 NaN；判 null 用 === 或可选链
const isInvalidNum = Number.isNaN(input);
const hasUser = user === null ? false : true;
const cityName = order?.address?.city ?? "未知";
```

```ts
// ❌ 默认 sort 按字典序，数字会被排乱
const wrong = [5, 3, 10].sort();       // [10, 3, 5]

// ✅ 数字排序必传比较器；用数组方法链编排，不手写 for
const scores = [5, 3, 10];
// 升序：a-b；过滤无效值再排序，链式表达流程
const sorted = scores
  .filter((n) => Number.isFinite(n))   // 剔除 NaN/Infinity，避免比较器产出 NaN
  .sort((a, b) => a - b);              // [3, 5, 10]
```

```ts
// ❌ parseInt 不带 radix，解析有歧义
const wrongAge = parseInt("08");       // 依赖环境，可能解析异常

// ✅ parseInt 必带 radix=10；空值早返回，下沉到纯函数复用
const toInt = (raw: string | undefined): number => {
  // 前置校验：空串/undefined 直接给 0，不进解析
  if (!raw) return 0;
  // 显式十进制解析，杜绝前导 0 / 0x 歧义
  const parsed = parseInt(raw, 10);
  // 解析失败兜底为 0
  return Number.isNaN(parsed) ? 0 : parsed;
};
```

## 自检

- [ ] 全部相等比较用 `===` / `!==`，没有裸 `==` / `!=`？
- [ ] 判 NaN 用 `Number.isNaN`，没有用会强转的全局 `isNaN`？
- [ ] 判 null 用 `x === null` 或 `?.`，没有用 `typeof x === "object"`？
- [ ] 数字数组 `sort` 都传了 `(a,b)=>a-b` 比较器，没有裸 `sort()`？
- [ ] `parseInt` 都带了第二参 `10`，没有省略 radix？
- [ ] 记得 `[]` / `{}` / `"0"` 是 truthy，判空靠 `.length` 而非真值？

## 相关

- 父：[`./index.md`](./index.md)
- 跨引：[`../null-safety/optional-chaining-nullish.md`](../null-safety/optional-chaining-nullish.md)（`?.` 判 null / `??` 兜底，避开 `||` 吞 falsy）
- 跨引：[`../number/index.md`](../number/index.md)（数值精度 / 解析 / 格式化）
