---
name: typescript-generics
description: "TS 泛型做\"类型随入参变化\"的复用（函数 / 组件 / hook / 工具类型），禁用 any 顶替。Use when 返回类型依赖入参类型 / 写可复用工具函数 / 组件或 hook 要保留调用方类型 / 纠结要不要引入泛型"
parent: ./index.md
paths:
- frontend/src/**/*.ts
- frontend/src/**/*.tsx
triggers:
  keywords:
  - generics
  - 泛型
  - extends 约束
  - 默认泛型参数
  - 类型推断
  - useState<T>
effort: medium
context: inline
version: '1.0'
---
# TypeScript · 泛型

## 规则

**决策点：返回/输出类型由入参类型决定时引入泛型；否则写死，别过度泛型。**

| 场景 | 用泛型？ | 写法 |
|------|---------|------|
| 返回类型 = 入参类型派生（取元素/包装/透传） | ✅ | `<T>(arr: T[]): T \| undefined` |
| 入参形状固定、返回写死 | ❌ 写死 | `(id: string): User` |
| 想用 `any` 让它“随便传” | ❌ 改泛型 | `<T>` 而非 `any` |
| 泛型只出现一次、不参与推断 | ❌ 多余 | 直接用具体类型 |

约束用 `extends` 限定形状：`<T extends { id: string }>`；默认参数 `<T = Foo>`；多泛型让 TS 从入参推断，调用方不手写。

## 反例 → 正例

```ts
// ❌ any 抹掉类型：返回值丢失，调用方拿到 any
function first(arr: any[]): any {
  return arr[0];
}

// ✅ 泛型：返回类型随入参元素类型走，可能为空显式 T | undefined
function first<T>(arr: T[]): T | undefined {
  // 空数组早返回，避免下游误判
  if (arr.length === 0) return undefined;
  return arr[0];
}

const n = first([1, 2, 3]); // number | undefined
```

```ts
// ✅ extends 约束形状 + 多泛型推断：按 key 建索引
function indexBy<T extends { id: string }, K extends keyof T>(
  list: T[],
  key: K,
): Record<string, T> {
  // reduce 累积成字典，禁手写 for
  return list.reduce<Record<string, T>>((acc, item) => {
    // 以 item[key] 作为索引键写入
    acc[String(item[key])] = item;
    return acc;
  }, {});
}
```

```tsx
// ✅ React: useState 泛型 + 组件 props 泛型,保留调用方元素类型
type SelectProps<T> = {
  options: T[];
  labelOf: (item: T) => string;
  onPick: (item: T) => void;
};

function Select<T>({ options, labelOf, onPick }: SelectProps<T>) {
  // 选中项类型随 options 推断为 T,初始无选中用 null
  const [active, setActive] = useState<T | null>(null);

  return (
    <ul>
      {options.map((item, i) => (
        <li key={i} aria-selected={item === active} onClick={() => { setActive(item); onPick(item); }}>
          {labelOf(item)}
        </li>
      ))}
    </ul>
  );
}
```

```ts
// ✅ 自定义 hook 泛型返回:取值与 setter 都带 T,禁用 any
function useLocalState<T>(key: string, initial: T) {
  // 惰性读 localStorage,解析下沉 readJson 纯函数,失败回退 initial
  const [value, setValue] = useState<T>(() => readJson<T>(key) ?? initial);
  return [value, setValue] as const; // 元组类型固化,调用方解构带类型
}
```

## 自检

- [ ] 返回/输出类型确实依赖入参，才引入泛型？(否则写死)
- [ ] 用泛型 `<T>` 而非 `any` 表达“随入参变化”？
- [ ] 类型参数有形状要求时用 `extends` 约束(`<T extends {...}>`)？
- [ ] 多泛型靠推断,调用方未手写类型实参？
- [ ] hook 元组返回加了 `as const` 固化位置类型？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`./utility-types.md`](./utility-types.md)（从已有类型派生新类型）
- 跨引：[`../typing/no-any.md`](../typing/no-any.md)（禁 any，泛型/unknown 替代）
