---
name: typescript-form-error-handling
description: 表单局部 catch ApiError + 字段映射 — 比 ErrorBoundary 更细粒度
parent: ./index.md
paths:
  - "frontend/app/**/*.tsx"
  - "frontend/app/views/**/*.tsx"
triggers:
  keywords: [Form, setError, onSubmit, ApiError, instanceof, 表单校验, antd Form]
effort: medium
context: inline
version: "1.0"
---

# Form · 局部错误处理

## 场景分类

| 错误类型 | 处理位置 |
|---------|---------|
| 路由级未捕获错误 | `app/error.tsx` ErrorBoundary |
| 表单提交业务失败 | **表单组件内 try/catch** + setError |
| 表单字段实时校验 | Pydantic schema 或 antd Form rules（不用 ApiError） |
| 全局 toast 错误 | App.message.error（API 失败兜底） |

本叶子专讲第 2 类：**表单提交后业务断言失败**的处理。

## 标准模式

```typescript
"use client";

import { Form, Input, InputNumber, Button } from "antd";
import { useState } from "react";

import { ApiError, Asserts } from "@/app/lib/assertion";

interface OutlineForm {
  title: string;
  slideCount: number;
}

// code → 字段映射（错误码字典约定）
const FIELD_BY_CODE: Record<string, keyof OutlineForm> = {
  D003: "title",       // 标题相关
  D002: "slideCount",  // 数量相关
};

export function OutlineFormView() {
  const [form] = Form.useForm<OutlineForm>();
  const [submitting, setSubmitting] = useState(false);

  async function onSubmit(values: OutlineForm) {
    setSubmitting(true);
    try {
      // 1. 客户端预校验（断言式）
      Asserts.notBlank(values.title, { code: "D003", message: "大纲标题不能为空" });
      Asserts.maxLength(values.title, 200, { code: "D003", message: "标题不能超过 200 字符" });
      Asserts.inRange(values.slideCount, 3, 20, { code: "D002", message: "幻灯片数 3-20" });

      // 2. 调用后端（fetcher 失败也抛 ApiError）
      const result = await api.createOutline(values);
      console.log("created:", result);

    } catch (e) {
      if (e instanceof ApiError) {
        const field = FIELD_BY_CODE[e.code];
        if (field) {
          // 字段相关错误 → 高亮对应输入框
          form.setFields([{ name: field, errors: [e.message] }]);
        } else {
          // 业务级错误 → 顶部 alert / toast
          form.setFields([{ name: ["_root"], errors: [`${e.code}: ${e.message}`] }]);
        }
        return;
      }
      throw e; // 未知错误透传给 ErrorBoundary
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <Form form={form} layout="vertical" onFinish={onSubmit}>
      <Form.Item name="title" label="大纲标题">
        <Input />
      </Form.Item>
      <Form.Item name="slideCount" label="幻灯片数">
        <InputNumber min={3} max={20} />
      </Form.Item>
      <Button type="primary" htmlType="submit" loading={submitting}>
        提交
      </Button>
    </Form>
  );
}
```

## FIELD_BY_CODE 字典维护

每个有表单的业务在自己模块下维护一个 code → field 映射：

```typescript
// frontend/app/outline/_internals/error-mapping.ts
export const OUTLINE_FIELD_BY_CODE: Record<string, string> = {
  D002: "slideCount",
  D003: "title",
  D005: "chapterIds",
};
```

避免在表单组件里硬编码。

## 与客户端 Asserts vs 后端断言

客户端断言**和**后端断言**用同一套错误码**：

```typescript
// 客户端预校验：避免无效请求打到后端
Asserts.notBlank(form.title, { code: "D003", message: "大纲标题不能为空" });

// 后端返回：同样抛 D003
// fetcher 把后端 D003 转为 ApiError
// catch 块用同一个 FIELD_BY_CODE 映射 → 同样的字段高亮
```

错误码字典是前后端共同契约。详见 `/.ai/skills/core/error_code_dict.md`。

## 何时**不**用 try/catch

```typescript
// ❌ 简单 antd Form 校验 — 用 rules 就够
<Form.Item
  name="title"
  rules={[{ required: true, message: "标题必填" }]}
>
  <Input />
</Form.Item>

// 仅在「需要打到后端 + 业务断言」时才用 try/catch
```

## 反例

```typescript
// ❌ catch 后吞掉
catch (e) {
  console.log(e);
  // 用户看不到任何反馈
}

// ❌ catch 后只 toast，不绑定字段
catch (e) {
  if (e instanceof ApiError) {
    message.error(e.message);  // 用户不知道哪个字段错
  }
}

// ❌ 在 try/catch 外又裸 await
await api.createOutline(form.getFieldsValue());  // 失败直接打到 ErrorBoundary

// ❌ catch 后直接 throw（这是 finally 才该做的）
catch (e) {
  setSubmitting(false);  // 应放 finally
  throw e;
}
```

## 自检

- [ ] try/catch 包住 await + 客户端预校验？
- [ ] catch 用 `e instanceof ApiError` 守卫？
- [ ] 字段相关错误用 `form.setFields` 绑定到具体 input？
- [ ] 业务级错误用 root 区域或 toast？
- [ ] 未知错误 `throw e` 透传给 ErrorBoundary？
- [ ] FIELD_BY_CODE 映射独立维护，不硬编码？
- [ ] `setSubmitting(false)` 在 finally？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`assert-helpers.md`](./assert-helpers.md) · [`error-boundary.md`](./error-boundary.md) · [`api-error-class.md`](./api-error-class.md)
- 配套：[`../../../framework/antd/form/index.md`](../../../framework/antd/form/index.md)
- 错误码字典：`/.ai/skills/core/error_code_dict.md`
