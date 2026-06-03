---
name: design-theme-wes-anderson
description: 韦斯·安德森风格 — 中轴对称、5 色粉彩(中性70/粉彩25/强调5)、复古全大写宽字距标题 + 衬线正文、克制叙事动效。Use when 做品牌官网·落地页·作品集 / 要艺术怀旧调性 / 用户指定韦斯·安德森风时。
parent: ./index.md
paths:
  - "**/*.tsx"
  - "**/*.vue"
  - "**/*.css"
  - "**/*.html"
triggers:
  keywords:
    - 韦斯安德森
    - 韦斯·安德森
    - wes anderson
    - 粉彩
    - pastel
    - 对称构图
    - 复古排版
    - 电影感
effort: medium
version: "1.0"
---

# Wes Anderson · 对称粉彩复古

> 电影故事书般的怀旧美学：对称、粉彩、复古排版、克制叙事感。
> 6 套调色板全色值、排版层级、组件库、纹理、Tailwind 配置见 [`wes-anderson.reference.md`](wes-anderson.reference.md)。

## 5 条核心原则

1. **对称至上** —— 中轴线对称、正面平视，奇数列内容居中、两侧等宽留白。
2. **精选粉彩** —— 一个项目只用**一套 5 色调色板**；中性占 70%、粉彩 25%、强调仅 5%。
3. **复古排版** —— 标题几何无衬线**全大写 + 宽字距**（电影海报感），正文优雅衬线、行高 1.7。
4. **精致细节** —— 双线边框、装饰分隔符（`✦ ─── TITLE ─── ✦`）、章节编号（CHAPTER I）。
5. **克制叙事动效** —— 优雅升起 / 幕布展开 / 淡入淡出；禁弹跳、粒子、3D、霓虹。

## 何时用 / 不用

| 适合 | 不适合 |
|------|--------|
| 精品·生活方式·酒店、编辑·叙事、美术馆、独立品牌官网、作品集 | 企业仪表盘、数据密集后台 |
| 需要「高级感 + 艺术气质」的展示页 | 高转化漏斗、需要中性现代权威感的品牌 |

## 调色板速查（6 套，详见 reference）

布达佩斯大饭店（温暖粉红）· 月升王国（自然绿）· 天才一族（暖棕）· 了不起的狐狸爸爸（秋橘）· 海海人生（冷蓝绿）· 法兰西特派（淡紫）。

中性深色用暖深色替代纯黑、浅色用奶白替代纯白。

## 关键 CSS 线索

```css
.wa-hero { text-align: center; place-items: center; }   /* 对称居中 */
.wa-title {
  font-family: 'Josefin Sans', system-ui;   /* 几何无衬线，Futura 替代 */
  text-transform: uppercase;
  letter-spacing: .12em;
}
.wa-body { font-family: 'Playfair Display', Georgia, serif; line-height: 1.7; }
.wa-card { border: 1px solid var(--wa-border); border-radius: 2px; }   /* 近直角 */
```

## 自检

- [ ] 布局中轴对称，奇数列居中？
- [ ] 只用一套 5 色调色板，强调色 <5%，无纯黑纯白？
- [ ] 标题全大写宽字距、正文衬线行高 1.7？
- [ ] 动效克制（无弹跳/粒子/3D），并守 `prefers-reduced-motion`？

## 详细参考

- 6 套调色板全色值 / 排版层级 / 组件库 / 纹理 / Tailwind 配置：[`wes-anderson.reference.md`](wes-anderson.reference.md)

## 相关

- 父：[`./index.md`](./index.md)
- 通用底线：[`../foundations/index.md`](../foundations/index.md)
- 动效兜底：[`../component-patterns/motion-and-animation.md`](../component-patterns/motion-and-animation.md)
