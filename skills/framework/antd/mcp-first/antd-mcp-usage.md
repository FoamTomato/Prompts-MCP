---
name: antd-mcp-usage
description: 写真实 antd 组件代码前必查 MCP — antd_info / antd_demo / antd_token / antd_semantic
parent: ./index.md
paths:
  - "frontend/src/**/*.tsx"
triggers:
  keywords: [antd, MCP, antd_info, antd_demo]
effort: medium
context: inline
version: "1.0"
---

# antd · MCP 工具（写代码前必查）

## 规则

**写任何真实 antd 组件代码之前，必须通过 antd MCP 查 props/example**。禁止凭记忆写。

## 4 个 MCP 工具

| 工具 | 用途 | 何时用 |
|------|------|--------|
| `antd_info` | 查组件元信息（导出名、所在包） | 不确定组件叫什么 |
| `antd_demo` | 查官方 demo 源码 | 学习用法 |
| `antd_token` | 查组件级 token | 自定义主题 |
| `antd_semantic` | 查组件 semantic class | 精确覆盖样式 |

## 为什么硬约束

1. antd API 在大版本之间会变（4→5 / 5.0→5.20 props 命名变化）
2. 凭记忆易出错（Modal 的 `visible` / `open` / `maskClosable` / `closable` 易混）
3. 凭记忆易遗漏新 props（如 `destroyOnClose`、`afterClose`）
4. MCP 比官方文档快（不用切换浏览器）

## 典型工作流

```
用户："实现 D11 MediaCard，悬停弹出操作菜单"
  ↓
Agent 调 antd_demo(name="Card") → 看悬停交互范式
  ↓
Agent 调 antd_demo(name="Dropdown") → 学操作菜单
  ↓
Agent 调 antd_token(component="Card") → 看可自定义 token
  ↓
开写代码
```

## 反例

```tsx
// ❌ 凭记忆（antd 4 的 visible）
<Modal visible={open} onCancel={close}>...</Modal>

// ✅ 查 MCP 后用 antd 5 的 open
<Modal open={open} onCancel={close}>...</Modal>
```

```tsx
// ❌ 凭记忆 Drawer props
<Drawer visible={open} placement="right" width={400}>

// ✅ 查 MCP 后
<Drawer open={open} placement="right" width={400} destroyOnClose>
```

## CLAUDE.md 加载提示

CLAUDE.md「指针」段最后一条：

> antd 组件 API → antd MCP（antd_info / antd_demo / antd_token）— 写真实组件代码前先查，禁止凭记忆写 props

## 自检

- [ ] 写 antd 组件前查过 MCP？
- [ ] props 命名与 MCP 返回一致？
- [ ] 不依赖记忆中的旧版 API？

## 相关

- 父：[`./index.md`](./index.md)

