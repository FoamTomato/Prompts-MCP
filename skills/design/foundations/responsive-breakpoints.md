---
name: design-responsive-breakpoints
description: 响应式断点降列策略(≤1024 二列 / ≤768 单列)、移动优先、降列保持层级不重排、移动端守触控目标底线。Use when 设响应式断点 / 适配移动端 / 处理多列网格降列 / 评审小屏布局时。
parent: ./index.md
paths:
  - "**/*.tsx"
  - "**/*.vue"
  - "**/*.css"
  - "**/*.scss"
  - "**/*.html"
triggers:
  keywords:
    - 响应式
    - 断点
    - responsive
    - breakpoint
    - 移动端适配
    - 降列
    - media query
effort: low
version: "1.0"
---

# Responsive · 断点与降列

> 移动优先：先写单列基础样式，再用 `min-width` 往上叠多列。

## 断点档位

| 断点 | 典型布局 |
|------|---------|
| `< 768px` | 单列；隐藏装饰元素 |
| `768 - 1024px` | 二列 |
| `> 1024px` | 完整多列布局 |

按需再加 `1280` / `1440` 处理大屏最大宽度，但不要无脑铺一堆断点。

## 降列规则

- 多列 → 单列时，**保持从上到下的层级顺序，不重排内容**。
- 用 `grid-template-columns` + `auto-fit/minmax` 让网格自然降列，少写硬 media query：

```css
.grid {
  display: grid;
  gap: 24px;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
}
```

## 移动端要点

- 触控目标 **≥44×44px**（见 [`accessibility.md`](accessibility.md)）。
- 容器左右留 16px 安全边距，正文行长降到 30-40 字符。
- 装饰性元素（虚线框、角标、浮动小组件）在 `<768px` 隐藏，避免干扰。
- 正文字号不缩到 14px 以下。

## 自检

- [ ] 移动优先（基础单列 + `min-width` 往上叠）？
- [ ] 断点档位克制（核心三档，按需加大屏）？
- [ ] 降列后层级顺序不变、内容不重排？
- [ ] 移动端触控 ≥44px、留 16px 边距、装饰元素隐藏？

## 相关

- 父：[`./index.md`](./index.md)
- 触控目标：[`accessibility.md`](accessibility.md)
- 间距档位：[`spacing-grid.md`](spacing-grid.md)
