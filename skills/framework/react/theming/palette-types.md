---
name: react-palette-types
description: '框架约定 · react: 配色方案类型 — 单色/邻近/互补/分散'
parent: ./index.md
paths:
- frontend/src/styles/**/*.css
triggers:
  keywords:
  - palette
  - monochromatic
  - analogous
  - complementary
  - 配色方案类型
  - 单色
  - 邻近
effort: medium
context: inline
version: '1.0'
---
# React · 配色方案类型

## 4 种基本方案

### 1. 单色调（Monochromatic）

同一色相 + 明度变化。适合极简、企业、内容密集。

```css
--hue: 210;   /* 蓝色相 */
--bg-page:     hsl(var(--hue), 20%, 100%);
--bg-content:  hsl(var(--hue), 15%, 97%);
--bg-hover:    hsl(var(--hue), 12%, 94%);
--border:      hsl(var(--hue), 10%, 90%);
--accent:      hsl(var(--hue), 70%, 50%);
```

特点：高度和谐；缺点：可能单调。

### 2. 邻近色（Analogous）

色相环相邻 30°-60°（蓝 + 青 + 紫）。柔和过渡，营造氛围。

```css
--primary:   #3b82f6;   /* blue */
--secondary: #6366f1;   /* indigo */
--tertiary:  #06b6d4;   /* cyan */
```

适合：教育、阅读、设计工具类产品。

### 3. 互补色（Complementary）

180° 对位（蓝 + 橙、紫 + 黄）。强烈对比，吸睛。

```css
--primary: #3b82f6;     /* blue */
--accent:  #f59e0b;     /* amber，互补 */
```

适合：CTA、营销页、需要视觉张力的场景。**小面积使用**，大面积刺眼。

### 4. 分散色（Triadic / Split）

色相环 120° 三等分。活泼、富有节奏。

```css
--primary: #3b82f6;   /* blue */
--accent1: #f59e0b;   /* amber */
--accent2: #10b981;   /* green */
```

适合：儿童 / 游戏 / 数据看板。Quill 不用。

## Quill 选定方案

**邻近色（蓝 + 紫）+ 中性灰**：

- 主色：蓝 `#3b82f6` (accent)
- 副色：紫 `#6366f1`（用于品牌 CTA 渐变 `linear-gradient(135deg, #3b82f6, #6366f1)`）
- 中性：slate 色阶

学科色为辅助配色（不参与品牌识别）：

```css
--subject-math:    #6366f1;
--subject-chinese: #f59e0b;
--subject-english: #10b981;
--subject-physics: #ef4444;
```

## 选择决策

| 项目类型 | 推荐 |
|---------|------|
| 教育 / 阅读 / SaaS | 邻近色 + 中性 |
| 营销页 / 落地页 | 互补色（小面积） |
| 数据可视化 | 单色 + 序列色 |
| 儿童 / 创意 | 分散色 |

## 自检

- [ ] 主副色色相距离合理？
- [ ] 大面积不用互补色高饱和？
- [ ] 学科色 / 辅助色与品牌色独立？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`palette-principles.md`](./palette-principles.md)

