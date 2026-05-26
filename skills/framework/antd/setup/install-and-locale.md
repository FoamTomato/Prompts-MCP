---
name: antd-install-and-locale
description: '框架约定 · antd: antd 安装 + zhCN locale + 按需引入'
parent: ./index.md
paths:
- frontend/package.json
- frontend/src/main.tsx
triggers:
  keywords:
  - antd
  - zhCN
  - locale
  - ConfigProvider
  - 按需引入
effort: medium
context: inline
version: '1.0'
---
# antd · 安装与本地化

## 安装

```bash
pnpm add antd @ant-design/icons
```

`antd@5.x` 自带 dayjs，不需要 moment。

## 不需要的

```bash
# ❌ 不需要（antd 5 原生支持 tree-shaking）
pnpm add babel-plugin-import

# ❌ 不需要（antd 5 用 dayjs）
pnpm add moment
```

## CSS 引入

```ts
// src/main.tsx — 顺序很重要
import "antd/dist/reset.css";    // 1. antd reset
import "@/styles/tokens.css";    // 2. tokens 变量
import "@/styles/global.css";    // 3. 全局补充
```

## Locale

```tsx
import { ConfigProvider } from "antd";
import zhCN from "antd/locale/zh_CN";

<ConfigProvider locale={zhCN}>{children}</ConfigProvider>
```

zhCN 影响：
- DatePicker 中文
- Pagination 中文（"上一页" / "下一页"）
- Empty 中文（"暂无数据"）
- Modal 按钮中文（"确定" / "取消"）

## dayjs 本地化

```ts
// src/main.tsx
import dayjs from "dayjs";
import "dayjs/locale/zh-cn";
dayjs.locale("zh-cn");
```

DatePicker 才能显示中文星期。

## 图标按需引入

```tsx
// ✅ named import — Vite 自动 tree-shake
import { SearchOutlined, EditOutlined } from "@ant-design/icons";

// ❌ default import 全包（增加 bundle）
import Icons from "@ant-design/icons";
```

## 自检

- [ ] `antd` + `@ant-design/icons` 已安装？
- [ ] 没装 babel-plugin-import / moment？
- [ ] CSS 引入顺序：reset → tokens → global？
- [ ] ConfigProvider 注入 zhCN？
- [ ] dayjs 设置 zh-cn locale？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`config-provider.md`](./config-provider.md)

