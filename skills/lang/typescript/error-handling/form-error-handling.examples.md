# Form 局部错误处理 — 完整代码示例

> 配套 [`form-error-handling.md`](./form-error-handling.md)。这里只放完整代码 + 反例集。

## 完整标准模式

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

## 简单 antd Form 校验（不该用 try/catch）

```typescript
// ✅ 简单的必填 / 长度 / 格式校验，用 rules 就够
<Form.Item
  name="title"
  rules={[{ required: true, message: "标题必填" }]}
>
  <Input />
</Form.Item>

// 仅在「需要打到后端 + 业务断言」时才用 try/catch
```

## 反例集

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

// ❌ catch 后直接 throw（应该 finally 才做 cleanup）
catch (e) {
  setSubmitting(false);  // 应放 finally
  throw e;
}
```
