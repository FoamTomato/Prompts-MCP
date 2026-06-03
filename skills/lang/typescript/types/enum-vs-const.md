---
name: typescript-enum-vs-const
description: "定义一组常量时优先 as const 对象 + 联合类型,少用 enum。Use when 定义前端状态/类型常量集 / 纠结 enum 还是对象 / 需运行时遍历常量键值 / 对接跨语言固定数字协议"
parent: ./index.md
paths:
- frontend/src/**/*.ts
- frontend/src/**/*.tsx
triggers:
  keywords:
  - enum
  - as const
  - const 对象
  - 联合类型
  - 常量集
  - Object.values
  - 反向映射
effort: low
context: inline
version: '1.0'
---
# TypeScript · enum vs const 对象

## 规则

**决策点:定义常量集默认用 `as const` 对象 + 联合类型,`enum` 仅留给跨语言固定数字协议。** 数字 `enum` 会生成反向映射(运行时多余对象、类型不严:任意 `number` 可赋值);`const enum` 虽内联无运行时代码,但 `isolatedModules`(Vite/esbuild/babel-transpile)下不被支持会报错,且无法跨模块导出值。

| 场景 | 选 | 写法要点 |
|------|----|---------|
| 纯前端常量集(状态/角色/类型) | `as const` 对象 + 联合类型 | `const X={A:'a'} as const; type X=typeof X[keyof typeof X]` |
| 需运行时遍历键/值 | `as const` 对象 + `Object.values` | `Object.values(Status)` 得字面量联合数组 |
| 跨语言协议固定数字(后端/protobuf 约定枚举值) | 可用 `enum`(数字) | 仅当数值本身是契约的一部分 |
| 想要内联零运行时 | 不推荐 `const enum` | `isolatedModules` 下报错,改用 `as const` 对象 |

## 反例 · 正例

```ts
// ❌ 反例:用数字 enum 当字符串常量。生成反向映射,Status[0]==='Active',
// 任意 number 可赋给 Status 参数,类型不严且产物臃肿
enum BadStatus {
  Active,
  Closed,
}

// ❌ 反例:const enum 想省运行时,但 Vite/esbuild 开 isolatedModules 直接报错
const enum BadColor {
  Red = "red",
}
```

```ts
// ✅ 正例:as const 对象冻结字面量,推导出严格联合类型
const TaskStatus = {
  Active: "active",
  Paused: "paused",
  Closed: "closed",
} as const;

// 从对象值反推联合类型,新增一项类型自动跟随
type TaskStatus = (typeof TaskStatus)[keyof typeof TaskStatus];
// type TaskStatus = "active" | "paused" | "closed"

// ✅ 运行时遍历:Object.values 得到字面量数组,可直接做下拉选项
const STATUS_OPTIONS = Object.values(TaskStatus);
// readonly ["active", "paused", "closed"]
```

```ts
// 业务用法:函数入参收窄为联合,传错字符串编译即报错
function isTerminal(status: TaskStatus): boolean {
  // 终态判定:仅 Closed 为终态
  return status === TaskStatus.Closed;
}

// ✅ 跨语言固定数字协议:数值是契约,才用数字 enum
enum PriorityCode {
  Low = 0,
  High = 1,
}
```

## 自检

- [ ] 前端常量集是否用 `as const` 对象 + `typeof X[keyof typeof X]` 联合,而非 `enum`?
- [ ] 是否避免把数字 `enum` 当字符串常量用(反向映射 + 类型不严)?
- [ ] 需遍历时是否用 `Object.values` 取字面量数组,而非手抄数组?
- [ ] 是否避免 `const enum`(`isolatedModules` 兼容坑)?
- [ ] 仅当数值本身是跨语言契约时才保留数字 `enum`?

## 相关

- 父:[`./index.md`](./index.md)
- 兄弟:[`./as-const-assertion.md`](./as-const-assertion.md) as const 字面量收窄
- 兄弟:[`./discriminated-union.md`](./discriminated-union.md) 用联合 + tag 建模状态机
