---
name: framework-react-i18n-index
description: React 国际化文案约定索引：禁字符串拼接、复数走 ICU、locale 化数字与日期、禁硬编码、RTL 布局。Use when 写需多语言的界面文案 / 把数字日期按 locale 本地化展示 / 处理复数与 RTL。
parent: ../index.md
children:
  - { name: message-formatting, path: message-formatting.md, tag: skill, note: 占位符模板 + 复数 ICU + Intl 数字日期 + RTL }
when_to_descend: |
  写需多语言的文案、把日期 / 数字按 locale 本地化展示、处理复数或 RTL 布局时下钻。
---

# React · 国际化(i18n)约定

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| message-formatting | skill | 占位符模板 + 复数 ICU + Intl 数字日期 + RTL |

## 何时下钻

- 文案含变量,想拼接字符串 → 改用占位符模板,见 `message-formatting.md`
- 出现 "1 项 / N 项" 复数分支 → 用 ICU plural,见 `message-formatting.md`
- 数字 / 货币 / 日期需按 locale 展示 → 用 `Intl.*` / dayjs locale,见 `message-formatting.md`
- 组件里出现中文硬编码字面量 → 抽 message key,见 `message-formatting.md`
- 支持阿拉伯语 / 希伯来语等 RTL 语言 → 布局方向处理,见 `message-formatting.md`

## 链接

- 上层:[`../index.md`](../index.md)
- 平行:[`../theming/index.md`](../theming/index.md) · [`../component/index.md`](../component/index.md)
