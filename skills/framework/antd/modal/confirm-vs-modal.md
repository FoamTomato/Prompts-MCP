---
name: antd-confirm-vs-modal
description: Modal.confirm 用于一次性确认 / <Modal> 用于复杂内容
parent: ./index.md
paths:
- frontend/src/**/*.tsx
triggers:
  keywords:
  - Modal
  - Modal.confirm
  - Drawer
  - 用于一次
  - 于一次性
  - 一次性确
effort: medium
context: inline
version: '1.0'
---
# antd · Modal.confirm vs <Modal>

## 规则

| 场景 | 用 |
|------|-----|
| 一次性确认对话（删除 / 退出 / 重置） | `modal.confirm()` |
| 含表单 / 复杂内容 / 多步骤 | `<Modal>` 受控组件 |
| 异步等待用户操作返回 boolean | `modal.confirm()`（返回 Promise） |

## Modal.confirm（推荐用于简单确认）

```tsx
import { App } from "antd";

function DeleteButton({ id }: { id: string }) {
  const { modal } = App.useApp();   // 必须在 <App> 内才能用

  const handleDelete = () => {
    modal.confirm({
      title: "确认删除？",
      content: "删除后不可恢复",
      okText: "删除",
      okType: "danger",
      cancelText: "取消",
      onOk: async () => {
        await presentationsApi.delete(id);
        message.success("已删除");
      },
    });
  };

  return <Button danger onClick={handleDelete}>删除</Button>;
}
```

**返回 Promise**：`onOk` 可 `async`，按"确定"会等待 Promise，期间按钮 loading。

## `<Modal>` 受控（复杂场景）

```tsx
const [open, setOpen] = useState(false);

<Modal
  title="编辑课件"
  open={open}
  onCancel={() => setOpen(false)}
  onOk={handleSave}
  okText="保存"
  cancelText="取消"
  width={680}
  destroyOnClose          // 关闭时卸载（释放内存）
  maskClosable={false}    // 不允许点遮罩关
>
  <Form>...</Form>
</Modal>
```

## 反例

```tsx
// ❌ 直接用 import 的 Modal.confirm（脱离 ConfigProvider context）
import { Modal } from "antd";
Modal.confirm({ ... });   // 主题可能丢失，控制台警告

// ✅ 用 App.useApp() 拿
const { modal } = App.useApp();
modal.confirm({ ... });
```

## destroyOnClose 何时用

```tsx
<Modal destroyOnClose>...</Modal>
```

| 何时开 | 何时关 |
|--------|--------|
| 内容含表单（重新打开应重置） | 内容是纯展示（保留状态） |
| 内容含大量数据 / 图片 | 同上 |
| 内容含 useEffect 订阅 | — |

详见 [`lazy-mount.md`](./lazy-mount.md)。

## 自检

- [ ] 简单确认用 modal.confirm()？
- [ ] 复杂内容用 <Modal>？
- [ ] confirm 的 onOk 用 async（按钮自动 loading）？
- [ ] 通过 App.useApp() 拿 modal，不直接 import Modal.confirm？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`lazy-mount.md`](./lazy-mount.md)

