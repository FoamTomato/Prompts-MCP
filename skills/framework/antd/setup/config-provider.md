---
name: antd-config-provider
description: antd ConfigProvider 注入主题 token（颜色/圆角/字体/动画）。Use when 写 React 组件 / 改 .tsx
  文件 / 评审涉及 `config-provider` 的 PR。
parent: ./index.md
paths:
- frontend/src/main.tsx
- frontend/src/App.tsx
- frontend/src/**/*.tsx
triggers:
  keywords:
  - ConfigProvider
  - theme
  - token
  - colorPrimary
  - 注入主题
  - 字体
  - 动画
effort: medium
context: inline
version: '1.0'
---
# antd · ConfigProvider

## 全局配置模板

```tsx
// src/main.tsx
import { ConfigProvider, App as AntdApp } from "antd";
import zhCN from "antd/locale/zh_CN";
import "antd/dist/reset.css";
import "@/styles/tokens.css";
import "@/styles/global.css";

const antdTheme = {
  token: {
    colorPrimary:  "#3b82f6",
    colorSuccess:  "#10b981",
    colorWarning:  "#f59e0b",
    colorError:    "#ef4444",
    colorInfo:     "#3b82f6",

    colorText:           "#0f172a",
    colorTextSecondary:  "#334155",
    colorTextTertiary:   "#64748b",
    colorTextQuaternary: "#94a3b8",

    colorBgBase:      "#ffffff",
    colorBgContainer: "#ffffff",
    colorBgLayout:    "#f8fafc",
    colorBgElevated:  "#ffffff",

    colorBorder:          "#e5e7eb",
    colorBorderSecondary: "#f1f5f9",

    borderRadius:    8,
    borderRadiusLG:  12,
    borderRadiusSM:  6,
    borderRadiusXS:  4,

    fontFamily: '-apple-system, "PingFang SC", system-ui, sans-serif',
    fontSize:   13,
    fontSizeLG: 14,
    fontSizeSM: 12,
    fontSizeXL: 16,

    controlHeight:   36,
    controlHeightLG: 40,
    controlHeightSM: 30,

    boxShadow:          "0 4px 12px rgba(15, 23, 42, 0.06)",
    boxShadowSecondary: "0 1px 2px rgba(15, 23, 42, 0.04)",

    motionDurationFast: "0.15s",
    motionDurationMid:  "0.24s",
    motionDurationSlow: "0.4s",
  },
  components: {
    Button: { fontWeight: 600 },
    Input:  { paddingBlock: 6, paddingInline: 10 },
    Modal:  { borderRadiusLG: 12, padding: 24 },
    Drawer: { paddingLG: 24 },
    Form:   { labelFontSize: 13, verticalLabelPadding: "0 0 6px" },
    Table:  { headerBg: "#f8fafc", rowHoverBg: "#f8fafc" },
    Select: { optionSelectedBg: "#dbeafe" },
  },
};

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ConfigProvider locale={zhCN} theme={antdTheme}>
      <AntdApp>
        <QueryClientProvider client={queryClient}>
          <RouterProvider router={router} />
        </QueryClientProvider>
      </AntdApp>
    </ConfigProvider>
  </StrictMode>
);
```

## 为什么用 `<App>` 包装

antd 5 的 `<App>` 提供静态方法（`message.success` / `notification.open` / `Modal.confirm`）的 context，避免脱离 ConfigProvider 上下文导致主题丢失。

```tsx
// ✅ 在组件内
const { message, modal, notification } = App.useApp();
message.success("保存成功");
modal.confirm({ title: "确认删除？", onOk: ... });
```

## tokens.css ↔ antdTheme 对齐表

详见 [`../../react/theming/css-token-system.md`](../../react/theming/css-token-system.md)。**单一可信源**。

## 修改主题

新增 token 必须同步三处：
1. `tokens.css` `:root` 加变量
2. `main.tsx` `antdTheme.token` 加镜像
3. `framework/react/theming/css-token-system.md` 更新对齐表

## 自检

- [ ] ConfigProvider 在最外层包了 App + Router + QueryClient？
- [ ] locale 注入了 zhCN？
- [ ] 颜色 / 圆角 / 字号与 tokens.css 完全对齐？
- [ ] 用 `App.useApp()` 调静态方法？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`install-and-locale.md`](./install-and-locale.md)
- 配套：[`../../react/theming/css-token-system.md`](../../react/theming/css-token-system.md)

