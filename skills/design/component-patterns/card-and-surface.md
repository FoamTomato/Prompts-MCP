---
name: design-card-and-surface
description: 卡片/面板/阴影层级约定 + inline sections over cards 原则(内容平铺用分区标题，不层层堆白卡)。Use when 写卡片面板 / 纠结要不要包卡片 / 评审页面是否卡片过载时。
parent: ./index.md
paths:
  - "**/*.tsx"
  - "**/*.vue"
  - "**/*.css"
  - "**/*.html"
triggers:
  keywords:
    - 卡片
    - card
    - 面板
    - surface
    - 阴影层级
    - 卡片过载
    - inline sections
effort: low
version: "1.0"
---

# Card & Surface · 卡片与面板

> 卡片不是默认容器。先问「这块内容真需要浮起来吗」，多数时候答案是否。

## inline sections over cards（默认平铺）

页面内容**默认平铺**在背景上，用「分区标题 + 下划线」分隔，而非层层堆叠白卡：

- ✅ 内容直接坐在页面背景，分区用标题 + `1px` 下划线分隔。
- ❌ 把每个子区块都包进 `.card{ bg+border+radius+shadow }` —— 造成「卡片过载」的廉价感。
- ❌ 彩色页底让一堆白卡「浮」着。

```css
.section-header { padding:20px 0 14px; border-bottom:1px solid var(--border); }
.section-title  { font-size:18px; font-weight:600; color:var(--text-primary); }
/* 标题下内容（表格/列表/表单）直接平铺，不再包面板 */
```

## 何时卡片才合理

| 场景 | 为何 |
|------|------|
| 网格里**可独立点击**的项（功能瓦片、套餐卡） | 每张是独立可点单元 |
| 弹窗 / 对话框 | 本就浮于内容之上 |
| 仪表盘 widget | dashboard 的本职就是并列独立指标 |
| 侧栏里的筛选分组 | 低对比软背景分组 |

## 阴影层级（仅在卡片确实合理时）

| 层级 | 阴影 | 用 |
|------|------|----|
| 默认 | 无 | 卡片静止态 |
| hover | `0 4px 16px rgba(0,0,0,.06)` | 可点卡片浮起 |
| 弹层 | `0 8px 24px rgba(0,0,0,.10)` | 弹窗/下拉 |

边框用 hairline（`1px solid var(--border)`）；hover 只动 `transform`/`box-shadow`。

## 自检

- [ ] 内容默认平铺（分区标题+下划线），没把每块都包卡片？
- [ ] 用卡片的地方是「可独立点击项/弹窗/widget/筛选组」之一？
- [ ] 卡片默认无阴影，仅 hover/弹层才有？
- [ ] 边框 hairline，hover 不触发重排？

## 相关

- 父：[`./index.md`](./index.md)
- bento 网格里的卡片：[`../theme/bento.md`](../theme/bento.md)
- 间距与留白：[`../foundations/spacing-grid.md`](../foundations/spacing-grid.md)
