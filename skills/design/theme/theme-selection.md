---
name: design-theme-selection
description: 选视觉风格的决策 — 用户指定则用对应风格，未指定默认 bento，按产品类型/目标情绪映射到 bento/flat/wes-anderson。Use when 开新页面没定风格 / 用户报了主题词 / 纠结用哪套观感时。
parent: ./index.md
paths:
  - "**/*.tsx"
  - "**/*.vue"
  - "**/*.css"
  - "**/*.html"
triggers:
  keywords:
    - 风格选择
    - 主题选择
    - theme selection
    - style selection
    - 默认风格
    - 视觉风格
    - 选哪个风格
    - 写页面
    - 做首页
    - 落地页
    - 没指定风格
    - new page
effort: low
version: "1.0"
---

# Theme Selection · 选哪套风格

> 这条只回答「这次用哪套风格」。具体风格细则进对应风格叶子。

## 决策顺序

```text
// 步骤1: 用户是否指定了主题词？
//        指定 → 用对应风格（bento / flat / wes-anderson / 冷门风格）
// 步骤2: 未指定 → 默认 bento
// 步骤3: 指定的是冷门风格（glass/neumorphism/brutalism/极简/clay）
//        → 进 other-styles 速查，或转外部 ui-ux-pro-max 取大全
```

**核心规则：未指定一律默认 bento。**

## 产品 / 情绪 → 风格映射

| 产品类型 / 目标情绪 | 推荐风格 |
|--------------------|---------|
| 仪表盘 / 产品功能展示 / 作品集 / 混合重要度首页 | **bento**（默认） |
| SaaS / 内容站 / 移动端 / 性能与无障碍优先 | [flat-design](flat-design.md) |
| 精品·生活方式·酒店 / 编辑·叙事 / 美术馆 / 独立品牌官网 | [wes-anderson](wes-anderson.md) |
| 想要 frost 玻璃 / 软 UI / 粗野 / 极简 / 黏土质感 | [other-styles](other-styles.md) |

## 用户报了主题词怎么对

| 用户说 | 对到 |
|--------|------|
| bento / 便当 / 卡片网格 / Apple 风 | [bento](bento.md) |
| 扁平 / flat / 简洁 / 无阴影 | [flat-design](flat-design.md) |
| 韦斯·安德森 / 对称 / 粉彩 / 复古 / 电影感 | [wes-anderson](wes-anderson.md) |
| 玻璃拟态 / 新拟物 / 粗野 / 极简 / 黏土 | [other-styles](other-styles.md) |

## 自检

- [ ] 确认过用户是否指定主题，未指定才走默认 bento？
- [ ] 按产品类型/情绪而非个人喜好选风格？
- [ ] 一个项目只用一套主风格，没混搭多套？
- [ ] 选定风格后仍守 foundations 的对比度/间距/字阶底线？

## 相关

- 父：[`./index.md`](./index.md)
- 默认风格：[`bento.md`](bento.md)
- 通用底线：[`../foundations/index.md`](../foundations/index.md)
