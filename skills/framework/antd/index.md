---
name: framework-antd-index
description: Ant Design 组件使用约定索引（Form / Modal / Table / 边界 / 全局配置 / MCP）
parent: ../index.md
children:
  - { name: setup, path: setup/index.md, tag: folder, note: 安装 / ConfigProvider 全局配置 }
  - { name: boundary, path: boundary/index.md, tag: folder, note: 何时用 antd / 何时自研 }
  - { name: form, path: form/index.md, tag: folder, note: Form 表单与校验模式 }
  - { name: modal, path: modal/index.md, tag: folder, note: Modal / Drawer 用法与懒挂载 }
  - { name: table, path: table/index.md, tag: folder, note: Table 表格 / 分页 / 滚动 }
  - { name: mcp-first, path: mcp-first/index.md, tag: folder, note: 通过 antd MCP 工具查 API / 例子 / token }
when_to_descend: |
  写 / 改 React 组件中使用 antd 组件（Button / Form / Modal / Table 等）的代码，或调整全局主题 / ConfigProvider。
---

# antd · Ant Design 使用约定

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| setup | 文件夹 | ConfigProvider / locale / theme 全局配置 |
| boundary | 文件夹 | antd vs 自研组件边界 |
| form | 文件夹 | Form 表单与自定义校验 |
| modal | 文件夹 | Modal / Drawer 懒挂载与销毁 |
| table | 文件夹 | Table 列定义 / 分页 / 虚拟滚动 |
| mcp-first | 文件夹 | 优先用 antd MCP 工具查组件 API |

## 何时下钻

- 第一次配置 antd → `setup/index.md`
- 决定要不要用 antd 现成组件 → `boundary/index.md`
- 写表单 → `form/index.md`
- 写弹窗 → `modal/index.md`
- 写表格 → `table/index.md`
- 不确定 API 用法 → `mcp-first/index.md` 优先调 MCP

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../react/index.md`](../react/index.md)
