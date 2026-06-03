---
name: antd-overlay-selection
description: antd 浮层选型，在 Modal / Drawer / Popover / Tooltip / Popconfirm 间按交互意图定夺。Use when 弹出层拿不准用哪个 / Modal 与 Drawer 纠结 / 确认用 Popconfirm 还是 Modal.confirm
parent: ./index.md
paths:
- frontend/src/**/*.tsx
triggers:
  keywords:
  - Modal
  - Drawer
  - Popover
  - Tooltip
  - Popconfirm
  - 浮层选型
  - 阻断式聚焦
  - 行内确认
effort: medium
context: inline
version: '1.0'
---
# antd · 浮层组件选型

## 规则

决策点:**先按交互意图定组件，再用 tie-breaker 处理近义边界**。

| 交互意图 | 用 |
|----------|-----|
| 阻断式全屏聚焦，必须先处理才能继续 | `<Modal>` |
| 侧滑、内容多含表单、需保留主页面上下文参照 | `<Drawer>` |
| 悬浮辅助富内容、可点（含链接 / 按钮） | `<Popover>` |
| 纯文字提示、不可交互 | `<Tooltip>` |
| 就地一次性确认删除 / 高危单项操作 | `<Popconfirm>` |
| 操作结果瞬时反馈（成功 / 失败 / 进行中） | `message` · `notification` |

**Modal vs Drawer tie-breaker**:表单字段 > 6,或需边填边引用背后页面 → `<Drawer>`;否则居中聚焦用 `<Modal>`。

**Popconfirm vs Modal.confirm**:锚定在行内某个按钮旁就地确认 → `<Popconfirm>`;全局居中、内容稍重 → `Modal.confirm`(见 [`../modal/confirm-vs-modal.md`](../modal/confirm-vs-modal.md))。

**Tooltip vs Popover**:内容不可交互纯说明 → `<Tooltip>`;内容可点 / 富结构 → `<Popover>`。

## 反例 · 正例

```tsx
// ❌ 反例:Tooltip 里塞按钮——浮层非焦点容器，键盘 Tab 不可达，鼠标移开即消失
<Tooltip title={<Button onClick={onEdit}>编辑</Button>}>
  <InfoCircleOutlined />
</Tooltip>

// ✅ 正例:可交互富内容改用 Popover,焦点可达、点击外部才关闭
function RowActionPopover({ record }: { record: PresentationRow }) {
  // 1. 富内容里的操作下沉为编排,Popover 只承载可聚焦节点
  const content = (
    <Space direction="vertical">
      <Button type="link" onClick={() => onEdit(record.id)}>编辑</Button>
      <Button type="link" danger onClick={() => onArchive(record.id)}>归档</Button>
    </Space>
  );
  return (
    <Popover content={content} trigger="click" placement="bottomRight">
      <Button type="text" icon={<MoreOutlined />} />
    </Popover>
  );
}
```

```tsx
// ✅ 正例:行内删除——锚定按钮旁就地确认,选 Popconfirm 而非全屏 Modal
function DeleteCell({ id }: { id: string }) {
  const { message } = App.useApp();

  // 1. 确认副作用下沉,组件体只编排浮层与回调
  const handleConfirm = async () => {
    await presentationsApi.delete(id);
    message.success("已删除");
  };

  return (
    <Popconfirm
      title="确认删除这条课件?"
      okText="删除"
      okButtonProps={{ danger: true }}
      cancelText="取消"
      onConfirm={handleConfirm}
    >
      <Button type="link" danger>删除</Button>
    </Popconfirm>
  );
}
```

## 自检

- [ ] 阻断必须先处理 → Modal;侧滑留上下文 / 表单字段 > 6 → Drawer?
- [ ] 内容可交互(含按钮 / 链接)用 Popover,纯文字提示才用 Tooltip?
- [ ] 没把按钮塞进 Tooltip(键盘不可达)?
- [ ] 行内就地确认用 Popconfirm,全局居中确认用 Modal.confirm?
- [ ] 瞬时结果反馈用 message / notification,而非弹 Modal 打断?

## 相关

- 父:[`./index.md`](./index.md)
- 跨引:[`../modal/confirm-vs-modal.md`](../modal/confirm-vs-modal.md)(Popconfirm 升级到 Modal.confirm 的边界)
- 跨引:[`./feedback-selection.md`](./feedback-selection.md)(message / notification 等反馈组件细分)
