---
name: framework-element-plus-index
description: "Element Plus 组件使用约定索引：表单校验 / 表格服务端分页 / 全局配置主题 / 消息反馈。Use when 用 Element Plus 写表单 / 写表格分页 / 配 locale 与主题变量 / 做消息反馈时。"
parent: ../index.md
children:
  - { name: form-validation, path: form-validation.md, tag: skill, note: "ElForm rules / validator 自定义校验 / validate 提交" }
  - { name: table-pagination, path: table-pagination.md, tag: skill, note: "ElTable 列定义 / ElPagination 服务端分页" }
  - { name: setup-and-theme, path: setup-and-theme.md, tag: skill, note: "安装 / locale 国际化 / 主题 CSS 变量定制" }
  - { name: message-feedback, path: message-feedback.md, tag: skill, note: "ElMessage / Notification / MessageBox 反馈" }
when_to_descend: |
  用 Element Plus 写表单(校验) / 写表格(服务端分页) / 配置 locale 与主题变量 / 做消息·通知·确认框反馈。
---

# element-plus · Element Plus 使用约定

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| form-validation | skill | ElForm rules / validator 自定义校验 / validate 提交 |
| table-pagination | skill | ElTable 列定义 + ElPagination 服务端分页 |
| setup-and-theme | skill | 安装 / locale 国际化 / 主题 CSS 变量定制 |
| message-feedback | skill | ElMessage / Notification / MessageBox 反馈 |

## 何时下钻

- 写表单并做校验 → `form-validation.md`
- 写表格 + 分页(服务端) → `table-pagination.md`
- 第一次安装 / 配 locale / 改主题色 → `setup-and-theme.md`
- 弹提示 / 通知 / 确认框 → `message-feedback.md`

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../vue/index.md`](../vue/index.md)
- 对照(React 生态等价)：[`../antd/index.md`](../antd/index.md)
