---
name: react-controlled-uncontrolled
description: 受控/非受控输入 — value 必始终 defined、value 与 defaultValue 二选一、数字输入解析下沉。Use when 写表单输入 / 改 .tsx 输入组件 / 修 uncontrolled-to-controlled 警告。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - 受控组件
  - 非受控组件
  - controlled
  - uncontrolled
  - defaultValue
  - InputNumber
  - value 警告
effort: medium
context: inline
version: '1.0'
---
# React · 受控/非受控输入

## 规则

决策点：**输入框的 value 是否始终 defined**。React 按首次渲染 `value` 是否 `undefined` 判定受控/非受控，初始 `undefined` 后变定值会触发 `uncontrolled→controlled` 警告并重置光标。

| 场景 | 写法 | 理由 |
|------|------|------|
| 受控文本 | `value={x ?? ''}` | 永远是 string，绝不 undefined |
| 受控数字(antd) | `<InputNumber value={n} onChange={v => set(v)} />`，`n: number \| null` | InputNumber 接受 null 表示空，不抛警告 |
| 受控数字(原生) | `value={n ?? ''}` + onChange 解析字符串 | `e.target.value` 是 string，解析下沉 utils |
| 非受控 | `defaultValue` 只读初值 + ref 取值 | 与 value 互斥，不混用 |

铁律：`value` 与 `defaultValue` 二选一，不混用;条件渲染不让 `value` 时有时无（要么始终给 `?? ''`，要么整个组件卸载）。

## 反例 · 正例

```tsx
// ❌ value 初始 undefined，输入后变定值 → uncontrolled→controlled 警告
const [name, setName] = useState<string>();
<Input value={name} onChange={e => setName(e.target.value)} />

// ❌ value 与 defaultValue 同时给 → React 忽略 defaultValue 且告警
<Input value={name} defaultValue="初始" onChange={...} />

// ❌ 原生数字输入直接把 string 当 number 存入 state
<input type="number" value={age} onChange={e => setAge(e.target.value)} />
```

```tsx
// ✅ 受控文本:value 用 nullish 兜底，永远 defined
const [name, setName] = useState<string | undefined>();
<Input value={name ?? ''} onChange={e => setName(e.target.value)} />

// ✅ 受控数字 — antd InputNumber 用 number | null
const [age, setAge] = useState<number | null>(null);
<InputNumber value={age} min={0} onChange={value => setAge(value)} />

// ✅ 受控数字 — 原生 input,解析下沉 utils 纯函数
const handleAgeChange = (e: ChangeEvent<HTMLInputElement>) => {
  // 字符串解析逻辑下沉 utils,组件体只编排
  setAge(parseNullableInt(e.target.value));
};
<input type="number" value={age ?? ''} onChange={handleAgeChange} />
```

```ts
// frontend/src/utils/parse.ts — >3 行的解析下沉纯函数
export function parseNullableInt(raw: string): number | null {
  // 空串视为"未填",返回 null 而非 NaN
  const trimmed = raw.trim();
  if (trimmed === '') return null;
  // 解析为整数,非法输入也归一为 null
  const parsed = Number.parseInt(trimmed, 10);
  return Number.isNaN(parsed) ? null : parsed;
}
```

## 自检

- [ ] 每个受控 `value` 都用 `?? ''`（文本）或 `number | null`（数字）兜底,绝不为 undefined?
- [ ] 同一输入未同时出现 `value` 与 `defaultValue`?
- [ ] 原生 `type=number` 的 `e.target.value`(string) 已交解析函数转 number,未直接存 state?
- [ ] 条件渲染下 `value` 不会时有时无（始终兜底或整体卸载）?

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`state-completeness.md`](./state-completeness.md)（输入也属交互状态完备）
- antd Form 字段绑定（受控交给 Form 托管）：[`../../antd/form/form-item-name.md`](../../antd/form/form-item-name.md)
- value 兜底用的 `??` / `?.`：[`../../../lang/typescript/null-safety/optional-chaining-nullish.md`](../../../lang/typescript/null-safety/optional-chaining-nullish.md)
