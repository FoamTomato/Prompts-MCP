---
name: antd-form-item-name
description: Form.Item 必带 name 字段（受控）。Use when 写 React 组件 / 改 .tsx 文件 / 评审涉及 `form-item-name`
  的 PR。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
triggers:
  keywords:
  - Form
  - Form.Item
  - name
  - 必带
  - 字段
  - 受控
effort: medium
context: inline
version: '1.0'
---
# antd · Form.Item 必带 name

## 规则

antd Form 用受控字段时，`Form.Item` 必须有 `name` 属性。否则字段值无法被 Form 收集。

## 反例 → 正例

```tsx
// ❌ 没 name —— values 里没这个字段
<Form.Item label="标题">
  <Input />
</Form.Item>

// ✅
<Form.Item name="title" label="标题" rules={[{ required: true }]}>
  <Input />
</Form.Item>
```

## 完整表单模板

```tsx
import { Form, Input, InputNumber, Select, Button } from "antd";

function GenerateForm() {
  const [form] = Form.useForm();

  const onFinish = (values: { title: string; pages: number; level: "easy" | "hard" }) => {
    console.log(values);
  };

  return (
    <Form
      form={form}
      layout="vertical"
      onFinish={onFinish}
      initialValues={{ pages: 10, level: "easy" }}
    >
      <Form.Item
        name="title"
        label="标题"
        rules={[
          { required: true, message: "标题必填" },
          { max: 200, message: "标题不超过 200 字" },
        ]}
      >
        <Input />
      </Form.Item>

      <Form.Item
        name="pages"
        label="页数"
        rules={[{ type: "integer", min: 5, max: 30 }]}
      >
        <InputNumber min={5} max={30} style={{ width: "100%" }} />
      </Form.Item>

      <Form.Item name="level" label="难度">
        <Select options={[
          { value: "easy", label: "简单" },
          { value: "hard", label: "困难" },
        ]} />
      </Form.Item>

      <Form.Item>
        <Button type="primary" htmlType="submit">提交</Button>
      </Form.Item>
    </Form>
  );
}
```

## 嵌套字段（nested）

```tsx
<Form.Item name={["author", "name"]} label="作者姓名">
  <Input />
</Form.Item>

<Form.Item name={["author", "email"]} label="邮箱">
  <Input />
</Form.Item>

// values: { author: { name: "...", email: "..." } }
```

## 与 react-hook-form 集成

详见 [`../../react/state/server-state-tanstack.md`](../../react/state/server-state-tanstack.md) 和 react_patterns 的"表单"段。
推荐 antd Form（视觉/无障碍）+ react-hook-form（状态/性能）+ zod（校验）三层。

## 自检

- [ ] 每个 Form.Item 都有 name？
- [ ] rules 有 required / 长度 / 范围约束？
- [ ] 初始值通过 `initialValues` 或 `form.setFieldsValue` 注入？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`validator-pattern.md`](./validator-pattern.md)

