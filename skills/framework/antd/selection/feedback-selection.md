---
name: antd-feedback-selection
description: antd 反馈组件按持久度选型:瞬时 message / 富文本 notification / 内联 Alert / 整页 Result。Use when 给操作结果做反馈 / message 与 notification 纠结 / 表单校验错该用哪个 / 渲染 404 落地页。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
triggers:
  keywords:
  - message
  - notification
  - Alert
  - Result
  - App.useApp
  - 反馈选型
  - 瞬时提示
  - 表单校验错
effort: low
context: inline
version: '1.0'
---
# antd · 反馈组件选型

## 规则

决策点：**反馈要持续多久、绑定多大范围？** 先按持久度+范围定组件。

| 持久度 / 范围 | 形态 | 用 |
|------|------|-----|
| 瞬时、自动消失、单行 ack（已保存 / 已删除 / 已复制） | 顶部居中轻提示 | `message` |
| 瞬时但更丰富（标题+描述、可堆叠、需手动关、带操作按钮） | 右上角卡片 | `notification` |
| 持久内联、绑定某区域或表单、直到条件改变才消失 | 块级横幅 / inline | `Alert`（`banner` 或内联） |
| 整页结果落地（404 / 403 / 操作成功页 / 空操作结果） | 整页态 | `Result` |

二选一细则：

- **message vs notification**：一行就能说清→`message`；多行、需标题+描述或可操作→`notification`。
- **Alert vs message**：反馈需**持续到某条件变化**（校验未过、配额超限、降级提示）→`Alert`；**短暂** ack→`message`。

> `message` / `notification` 必须经 `App.useApp()` 取，直接 `import { message }` 静态调用会脱离 ConfigProvider context（主题丢失、控制台告警），同 [`../modal/confirm-vs-modal.md`](../modal/confirm-vs-modal.md) 的坑。

## 反例

```tsx
import { message } from "antd"; // ❌ 静态导入，脱离 context

function SaveForm() {
  const onSave = async () => {
    const errors = await form.validateFields().catch((e) => e.errorFields);
    // ❌ 用瞬时 message 显示需持久存在的表单校验错——一闪而过，用户来不及读、无法对照字段修正
    if (errors?.length) message.error("表单有误");
  };
}
```

## 正例

```tsx
import { App, Alert, Form } from "antd";

function SaveForm() {
  // 经 App.useApp() 取实例，挂在 ConfigProvider context 上
  const { message } = App.useApp();
  const [form] = Form.useForm();
  // 持久校验错文案下沉到 validator 纯函数,组件体只编排
  const errorText = collectFormErrorText(form);

  const handleSave = async () => {
    // 步骤 1:校验,失败则早返回(错误由下方持久 Alert 承载,不用瞬时 message)
    const ok = await validateOrFalse(form);
    if (!ok) return;
    // 步骤 2:提交并用瞬时 message 做一行成功 ack
    await draftApi.save(form.getFieldsValue());
    message.success("已保存");
  };

  // 持久反馈:校验错绑定表单区域,Alert 内联展示直到改正才消失
  return (
    <Form form={form} onFinish={handleSave}>
      {errorText && <Alert type="error" showIcon message={errorText} />}
      {/* fields... */}
    </Form>
  );
}
```

## 自检

- [ ] 单行自动消失 ack 用 `message`，富文本/可堆叠/可操作用 `notification`？
- [ ] 需持续到条件变化的反馈(表单校验错/配额/降级)用 `Alert`，没用瞬时 `message`？
- [ ] 整页 404/403/成功落地/空结果用 `Result`？
- [ ] `message` / `notification` 经 `App.useApp()` 取，未静态 `import`？
- [ ] >3 行的文案拼装/校验下沉到 validator 纯函数？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`overlay-selection.md`](./overlay-selection.md)
- 跨引：[`../modal/confirm-vs-modal.md`](../modal/confirm-vs-modal.md)（同样必须经 App.useApp() 取实例）
