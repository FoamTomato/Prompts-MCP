---
name: design-component-patterns-index
description: 跨风格组件落地约定索引 — 按钮层级、卡片与面板（含何时不用卡片）、动效曲线时长、每组件入场速查。Use when 写按钮·卡片·动效 / 定某组件入场方式 / 统一组件交互态 / 评审组件还原时。
parent: ../index.md
children:
  - { name: button-hierarchy, path: button-hierarchy.md, tag: leaf, note: 主/CTA/描边/幽灵四类层级 + default·hover·active·focus·disabled }
  - { name: card-and-surface, path: card-and-surface.md, tag: leaf, note: 卡片/面板/阴影层级 + inline sections over cards（何时不用卡片） }
  - { name: motion-and-animation, path: motion-and-animation.md, tag: leaf, note: 入场/hover/stagger 曲线时长 + 强制 prefers-reduced-motion 兜底 }
  - { name: entrance-patterns, path: entrance-patterns.md, tag: leaf, note: 每类组件入场速查 modal/drawer/toast/dropdown/accordion/list/tab/page }
when_to_descend: |
  写或评审具体组件（按钮、卡片、面板、过渡动效）时进这里。
  这些约定跨风格通用；风格层只决定它们的配色圆角，不改交互态结构。
---

# Component Patterns · 组件落地

> 跨风格通用的组件交互与结构约定。风格层（bento/flat/wes）只换观感，这里的状态与层级不变。

## 路由

| 你在做什么 | 进哪个 |
|-----------|-------|
| 写按钮 / 定主次 CTA 层级与交互态 | [button-hierarchy](button-hierarchy.md) |
| 写卡片面板 / 纠结要不要包卡片 | [card-and-surface](card-and-surface.md) |
| 定曲线时长档位 / 处理 reduced-motion 底线 | [motion-and-animation](motion-and-animation.md) |
| 某个组件（弹窗/抽屉/下拉/列表…）该用哪种入场 | [entrance-patterns](entrance-patterns.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 交互态对比度/焦点底线：[`../foundations/accessibility.md`](../foundations/accessibility.md)
- 组件态如何 token 化：[`../design-language/tokens-and-theming.md`](../design-language/tokens-and-theming.md)
