---
name: element-plus-form-validation
description: "ElForm 校验：:model + :rules + ref，字段 el-form-item prop 必填才生效。Use when 写 .vue 表单 / 改 .ts 校验逻辑 / 评审涉及 ElForm validate 的 PR / 字段联动或异步校验"
parent: ./index.md
paths:
- frontend/src/**/*.vue
- frontend/src/**/*.ts
triggers:
  keywords:
  - ElForm
  - el-form-item
  - validate
  - rules
  - validator
  - 表单校验
  - resetFields
effort: medium
context: inline
version: '1.0'
---
# element-plus · ElForm 校验

## 规则

| 场景 | 写法 |
|------|------|
| 简单必填 | `rules` 里 `{ required: true, message, trigger }` |
| 字段联动 / 异步 | 自定义 `validator(rule, value, callback)` |
| 提交前整体校验 | `formRef.value.validate()` 返回 Promise，早返回 |
| 重置 | `formRef.value.resetFields()` |

三件套缺一不可：`<el-form :model :rules ref>`；每个待校验字段 `<el-form-item prop="x">`。
**prop 必填**——不写 prop 该字段校验静默失效。

## 反例（手写 if 校验，绕过 ElForm）

```vue
<script setup lang="ts">
const onSubmit = () => {
  if (!form.name) return ElMessage.error("姓名必填");      // 手写校验，与 rules 脱节
  if (form.age < 0) return ElMessage.error("年龄非法");     // trigger/红框提示全丢
  api.submit(form);
};
</script>
```

## 正例（rules + validate 早返回，流水线编排）

```vue
<script setup lang="ts">
import { reactive, ref } from "vue";
import type { FormInstance, FormRules } from "element-plus";
import { checkNameUnique } from "@/api/user";

interface UserForm { name: string; confirm: string; pwd: string }

const formRef = ref<FormInstance>();
const form = reactive<UserForm>({ name: "", confirm: "", pwd: "" });

// 异步校验:用户名查重(validator 调 callback 回传错误)
const validateName = async (_r: unknown, v: string, cb: (e?: Error) => void) => {
  if (!v) return cb(new Error("姓名必填"));
  const taken = await checkNameUnique(v);
  return taken ? cb(new Error("姓名已被占用")) : cb();
};
// 字段联动:确认密码需与 pwd 一致
const validateConfirm = (_r: unknown, v: string, cb: (e?: Error) => void) =>
  v === form.pwd ? cb() : cb(new Error("两次密码不一致"));

const rules = reactive<FormRules<UserForm>>({
  name: [{ validator: validateName, trigger: "blur" }],
  pwd: [{ required: true, message: "密码必填", trigger: "blur" }],
  confirm: [{ validator: validateConfirm, trigger: "blur" }],
});

const onSubmit = async () => {
  if (!formRef.value) return;                                  // 前置:实例未挂载
  const ok = await formRef.value.validate().catch(() => false); // validate 异步
  if (!ok) return;                                             // 校验失败早返回
  await api.submit({ ...form });                               // 通过后提交
};
const onReset = () => formRef.value?.resetFields();            // 重置:清值+清校验态
</script>
```

模板见 [`form-validation.examples.md`](./form-validation.examples.md)（`<el-form ref :model :rules>` + 各 `el-form-item prop`）。

## 自检

- [ ] 每个待校验字段都写了 `prop`(否则校验不生效)？
- [ ] 提交前 `await formRef.value.validate()` 且失败早返回？
- [ ] 字段联动 / 异步查重用 `validator`，简单必填用 `required + message`？
- [ ] 重置用 `resetFields()` 而非手动清空对象？

## 相关

- 父：[`./index.md`](./index.md)
- 对照(antd)：[`../antd/form/validator-pattern.md`](../antd/form/validator-pattern.md)
