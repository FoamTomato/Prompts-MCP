---
name: typescript-discriminated-union
description: "判别联合用共同字面量字段(status/type)区分成员，switch 该字段自动收窄分支并配 never 穷尽检查。Use when 建模请求态 loading/success/error / 表单分步 / 多类型消息 / 替代全 optional 的 interface"
parent: ./index.md
paths:
- frontend/src/**/*.ts
- frontend/src/**/*.tsx
triggers:
  keywords:
  - discriminated union
  - tagged union
  - 判别联合
  - 穷尽检查
  - assertNever
  - status 字段
  - never 收窄
effort: medium
context: inline
version: '1.0'
---
# TypeScript · 判别联合

## 规则

**决策点：一个值存在"多形态"(每态字段不同)时，用共同字面量 tag 字段建联合，禁用全 optional 的单 interface。**

| 场景 | 建模 | tag 字段 |
|------|------|---------|
| 异步请求态 | `{status:'loading'}\|{status:'success',data:T}\|{status:'error',error:E}` | `status` |
| 表单分步 | `{step:'info',name}\|{step:'pay',cardNo}\|{step:'done'}` | `step` |
| 消息/事件类型 | `{type:'text',text}\|{type:'image',url}` | `type` |
| 单态可选字段堆叠 | ❌ 改判别联合 | — |

- tag 必须是**字面量类型**(`'loading'` 而非 `string`)，TS 才能按它收窄。
- `switch (x.tag)` 各 `case` 内自动收窄到对应成员，只能访问该态字段。
- `default` 分支调 `assertNever(x)` 做**穷尽检查**：新增成员未处理时编译报错。

## 反例 → 正例

```ts
// ❌ 全 optional 单 interface：分不清哪态有哪字段，data 与 error 可能同时缺失/共存
interface FetchState<T> {
  loading?: boolean;
  data?: T;     // success 才有，但类型不强制
  error?: Error; // error 才有，编译器拦不住误用
}
```

```ts
// ✅ status 判别 + 字面量 tag：每态字段精确，互斥不可越界
type FetchState<T> =
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

// 穷尽守卫：联合被穷尽后 x 收窄为 never，新增成员未处理则此处编译报错
function assertNever(x: never): never {
  throw new Error(`未处理的联合分支: ${JSON.stringify(x)}`);
}

// 渲染前按 status 收窄，switch 各分支只能访问该态字段
function renderState<T>(state: FetchState<T>, view: (data: T) => string): string {
  switch (state.status) {
    // loading 态无 data/error 可访问
    case 'loading':
      return '加载中…';
    // success 态收窄后 state.data 必存在
    case 'success':
      return view(state.data);
    // error 态收窄后 state.error 必存在
    case 'error':
      return `失败: ${state.error.message}`;
    // 穷尽兜底:漏掉任一 case 这里类型不为 never 即报错
    default:
      return assertNever(state);
  }
}
```

```tsx
// ✅ React: 用判别联合驱动 UI，每态渲染互斥，省去 if (loading) / if (error) 嵌套
type StepState =
  | { step: 'info'; name: string }
  | { step: 'pay'; cardNo: string }
  | { step: 'done' };

function StepView({ state }: { state: StepState }) {
  // tag 收窄后各分支拿到的字段精确，平坦顺序无嵌套
  switch (state.step) {
    case 'info':
      return <span>填写资料: {state.name}</span>;
    case 'pay':
      return <span>支付卡号: {state.cardNo}</span>;
    case 'done':
      return <span>完成</span>;
    default:
      return assertNever(state);
  }
}
```

> 构造各态的工厂/校验逻辑(>3 行)下沉 utils 纯函数，组件只消费收窄后的类型。

## 自检

- [ ] tag 字段是字面量类型(`'loading'`)而非 `string`/`boolean`？
- [ ] 各成员字段互斥，没退化成全 optional 的单 interface？
- [ ] `switch (x.tag)` 各 case 内只访问了该态独有字段？
- [ ] `default` 调 `assertNever(x)`，新增成员能在编译期报错？
- [ ] tag 命名统一(同一域用 `status`/`type`/`step` 之一，不混用)？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`./type-guard.md`](./type-guard.md)（运行时收窄 unknown / union，写 `x is T` 谓词）
- 跨引：[`../../../framework/react/component/state-completeness.md`](../../../framework/react/component/state-completeness.md)（状态字段完整性，避免布尔标志拼状态）
