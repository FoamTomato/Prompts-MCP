---
name: react-button-naming
description: 三类按钮：antd Button / 品牌 CTA / 业务包装。Use when 写 React 组件 / 改 .tsx 文件 / 评审涉及
  `button-naming` 的 PR。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/components/**/*
- frontend/src/features/**/*
triggers:
  keywords:
  - Button
  - CTA
  - BrandButton
  - 按钮
effort: medium
context: inline
version: '1.0'
---
# React · 按钮三类命名

## 三类硬性区分

| 类别 | 命名 | 何时用 | 实现 |
|------|------|--------|------|
| **antd Button** | 直接 `<Button>` 不包装 | 表单提交 / Modal 底部 / 表格行操作 / 普通触发 | antd `<Button>` |
| **品牌 CTA** | `<Action>CTA` 或 `<Feature>BrandButton` | 主页 H7、Hero 主按钮、付费转化按钮 | 自研（蓝紫渐变） |
| **业务包装** | `<Verb><Noun>Button` | 含 confirm / 复杂业务逻辑的特定按钮 | 内部用 antd Button + 业务 hook |

## 命名规则

1. **品牌 CTA**：`<Action>CTA` 或 `<Feature>BrandButton`
   - 例：`GenerateCTA` / `UpgradeBrandButton`
   - 文件：`features/<page>/<Action>CTA.tsx`

2. **业务包装**：`<Verb><Noun>Button`（动词在前）
   - 例：`DeletePresentationButton` / `DuplicateSlideButton`
   - 文件：`features/<page>/<Verb><Noun>Button.tsx`

3. **不允许的命名**：
   - `MyButton` / `CustomButton` / `PrimaryButton`（语义空洞）
   - `Btn` / `BtnDelete`（缩写）

## H7 GenerateButton 历史案例

`home_page.md` 的 H7 命名 `GenerateButton`——这是历史遗留。新代码遵循三类规则；老组件不强制改名，但**需在文件顶部注释指明类别**：

```tsx
// frontend/src/features/home/GenerateButton.tsx
// 品牌 CTA：蓝紫渐变 + ✨ icon；按 home_page.md「H7 GenerateButton」实现。
// 命名约定见 .claude/skills/framework/react/component/button-naming.md
export function GenerateButton() { ... }
```

## 何时复用 antd Button（三条件全满足）

- 不需要品牌渐变
- 不需要独立的业务封装逻辑
- 文字内容是"确定 / 取消 / 提交 / 重置"等通用动作

满足即 `<Button type="primary">`，**不要再包装一层**。

## 自检

- [ ] 按钮是 3 类中哪一类？
- [ ] 命名符合该类规范？
- [ ] 不用语义空洞名（MyButton / Btn）？
- [ ] 品牌 CTA 文件顶部有类别注释？

## 相关

- 父：[`./index.md`](./index.md)
- 配套：antd MCP（写 antd Button 前必查）：[`../../antd/antd-mcp-usage.md`](../../antd/antd-mcp-usage.md)

