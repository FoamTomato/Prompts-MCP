---
name: antd-validator-pattern
description: antd Form 自定义校验器（validator）模板 — 字段联动 / 异步校验
parent: ./index.md
paths:
- frontend/src/**/*.tsx
triggers:
  keywords:
  - Form
  - validator
  - rules
  - 自定义校
  - 定义校验
  - 义校验器
effort: medium
context: inline
version: '1.0'
---
# antd · Form 自定义校验

## 规则

复杂校验用 `rules` 数组传入自定义 validator。简单校验用 antd 内置类型。

## 内置校验

```tsx
<Form.Item
  name="email"
  rules={[
    { required: true, message: "邮箱必填" },
    { type: "email", message: "邮箱格式不正确" },
    { max: 100, message: "邮箱不超过 100 字" },
  ]}
>
  <Input />
</Form.Item>
```

## 自定义同步 validator

```tsx
<Form.Item
  name="password"
  rules={[
    { required: true, message: "密码必填" },
    {
      validator: (_, value: string) => {
        if (!value) return Promise.resolve();
        if (value.length < 8) return Promise.reject("密码至少 8 位");
        if (!/[A-Z]/.test(value)) return Promise.reject("需含大写字母");
        if (!/[0-9]/.test(value)) return Promise.reject("需含数字");
        return Promise.resolve();
      },
    },
  ]}
>
  <Input.Password />
</Form.Item>
```

## 自定义异步 validator（如查重）

```tsx
<Form.Item
  name="invite_code"
  rules={[
    {
      validator: async (_, value: string) => {
        if (!value) return;
        const exists = await referralsApi.checkCode(value);
        if (!exists) throw new Error("邀请码无效");
      },
    },
  ]}
>
  <Input />
</Form.Item>
```

## 跨字段校验

```tsx
<Form.Item
  name="password_confirm"
  dependencies={["password"]}
  rules={[
    { required: true, message: "请确认密码" },
    ({ getFieldValue }) => ({
      validator: async (_, value) => {
        if (!value || getFieldValue("password") === value) return;
        throw new Error("两次密码不一致");
      },
    }),
  ]}
>
  <Input.Password />
</Form.Item>
```

## 提交前整体校验

```tsx
const [form] = Form.useForm();

const onSubmit = async () => {
  try {
    const values = await form.validateFields();
    await api.submit(values);
  } catch (errInfo) {
    // 校验失败：errInfo.errorFields
  }
};
```

## 复杂表单 → zod

字段超过 5 个或有复杂跨字段逻辑：用 zod + react-hook-form：

```tsx
const Schema = z.object({
  password: z.string().min(8).regex(/[A-Z]/).regex(/[0-9]/),
  password_confirm: z.string(),
}).refine(d => d.password === d.password_confirm, {
  message: "两次密码不一致",
  path: ["password_confirm"],
});
```

## 自检

- [ ] 简单校验用内置类型？
- [ ] 异步 validator 返回 Promise？
- [ ] 跨字段用 `dependencies`？
- [ ] 复杂表单考虑 zod？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`form-item-name.md`](./form-item-name.md)

