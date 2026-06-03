# element-plus · ElForm 校验 · 模板示例

配合 `form-validation.md` 的 `<script setup>` 使用。要点：`<el-form>` 上挂 `ref` / `:model` / `:rules`，每个待校验字段的 `<el-form-item>` 必须写 `prop`，否则该字段校验静默失效。

```vue
<template>
  <el-form ref="formRef" :model="form" :rules="rules" label-width="90">
    <!-- prop 必填:与 rules 的 key 对应才会触发校验 -->
    <el-form-item label="姓名" prop="name">
      <el-input v-model="form.name" />
    </el-form-item>
    <el-form-item label="密码" prop="pwd">
      <el-input v-model="form.pwd" type="password" />
    </el-form-item>
    <el-form-item label="确认密码" prop="confirm">
      <el-input v-model="form.confirm" type="password" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="onSubmit">提交</el-button>
      <el-button @click="onReset">重置</el-button>
    </el-form-item>
  </el-form>
</template>
```

## 触发时机 trigger

- `trigger: "blur"`：失焦校验，适合输入框、异步查重。
- `trigger: "change"`：值变即校验，适合 select / radio / checkbox。
- 数组可叠加：`trigger: ["blur", "change"]`。

## 单字段校验 / 滚动到错误

```ts
// 只校验部分字段(传 prop 数组)
await formRef.value?.validateField(["name", "pwd"]);
// 清除指定字段校验态(不重置值)
formRef.value?.clearValidate(["name"]);
// 提交失败滚动到首个错误字段
formRef.value?.validate((_ok, fields) => {
  const first = fields && Object.keys(fields)[0];
  if (first) formRef.value?.scrollToField(first);
});
```
