---
name: design-theme-index
description: 主题风格库索引 — 默认 bento，指定则切 flat-design / wes-anderson / glass·新拟物·极简等冷门风格速查。Use when 选视觉风格 / 切换主题 / 要某风格的配色圆角阴影细则时。
parent: ../index.md
children:
  - { name: theme-selection, path: theme-selection.md, tag: leaf, note: 选哪套风格的决策 + 「未指定则默认 bento」规则 }
  - { name: bento, path: bento.md, tag: leaf, note: 默认风格 — 模块化卡片网格 / 统一 gap / 圆角 + soft hover }
  - { name: flat-design, path: flat-design.md, tag: leaf, note: 扁平化 2.0 — 纯色填充 / 单层 soft shadow / 小圆角 }
  - { name: wes-anderson, path: wes-anderson.md, tag: leaf, note: 韦斯·安德森 — 对称 / 粉彩 / 复古排版 / 克制动效 }
  - { name: other-styles, path: other-styles.md, tag: leaf, note: glassmorphism/neumorphism/brutalism/minimalism/claymorphism 一行速查 + 何时用 }
when_to_descend: |
  任务需要确定「界面长什么观感」。先进 theme-selection 决定用哪套，再进对应风格叶子拿细则。
  风格只叠加观感，不得突破 foundations 的对比度/间距/字阶/响应式底线。
---

# Theme · 主题风格库

> **默认 bento；用户指定主题则用对应风格。** 拿不准用哪套先看 [theme-selection](theme-selection.md)。

## 路由

| 你在做什么 | 进哪个 |
|-----------|-------|
| 不知道该用哪套风格 | [theme-selection](theme-selection.md) |
| 默认 / 仪表盘 / 产品展示 / 作品集 | [bento](bento.md) |
| SaaS / 内容站 / 移动端，要简洁高性能 | [flat-design](flat-design.md) |
| 精品 / 编辑 / 叙事 / 品牌官网，要艺术气质 | [wes-anderson](wes-anderson.md) |
| 想用 glass / neumorphism / brutalism / 极简 / clay | [other-styles](other-styles.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 风格之下的硬底线：[`../foundations/index.md`](../foundations/index.md)
- 风格落到 token / 换肤：[`../design-language/tokens-and-theming.md`](../design-language/tokens-and-theming.md)
- 更大的风格检索库：外部 `ui-ux-pro-max`
