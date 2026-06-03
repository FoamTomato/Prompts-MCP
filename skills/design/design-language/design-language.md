---
name: design-language-method
description: 为一个项目定一套设计语言的方法论 — 5 级灰阶/品牌色 scale/状态色/排版/间距/组件态/动效曲线七件套 + 字体配对清单。Use when 从零定项目设计系统 / 统一全站观感 / 查字体配对 / 评审设计语言完整性时。
parent: ./index.md
paths:
  - "**/*.css"
  - "**/*.scss"
  - "**/*.tsx"
  - "**/*.vue"
  - "**/*.md"
triggers:
  keywords:
    - 设计语言
    - design language
    - 设计系统
    - design system
    - 视觉规范
    - 灰阶
    - 品牌色
    - 组件状态
    - 字体配对
    - font pairing
effort: medium
version: "1.0"
---

# Design Language · 定一套设计语言的方法

> 「设计语言」= 让全站观感一致的一组明确决策。定齐下面七件套，落成 token，再让所有组件引用。

## 七件套（缺一不可）

| # | 要定什么 | 关键决策 |
|---|---------|---------|
| 1 | **文字灰阶** | 5 级：强(标题)/主(正文)/次(描述)/弱(占位)/禁用(分隔) |
| 2 | **品牌强调色 scale** | 一个品牌色拉 50→900 的梯度，配 hover/active/subtle-bg/subtle-border |
| 3 | **背景与边框** | 页面 bg / 内容区 bg / 卡片 hover / 主边框 / 浅边框 |
| 4 | **状态色** | 成功/警告/错误/信息，自成一组，不复用品牌色 |
| 5 | **排版层级** | 字体族 + 各级 size/weight/letter-spacing（接字阶规范） |
| 6 | **组件状态** | 按钮/输入/卡片的 default·hover·active·focus·disabled |
| 7 | **动效曲线** | 标准/弹性曲线 + 时长档 + 入场/hover 规则 |

## 流程

```text
// 步骤1: 选品牌强调色，拉出 50→900 scale
// 步骤2: 定 5 级文字灰阶（用暖灰而非纯黑链）
// 步骤3: 定背景/边框/状态色
// 步骤4: 接字阶 + 间距网格规范定排版与节奏
// 步骤5: 把以上全落成三层 token（见 tokens-and-theming）
// 步骤6: 定组件五态 + 动效曲线
// 步骤7: 全站组件只引用 token，逐页核一致性
```

## 两条反复出现的取舍

- **暖灰替纯黑/纯白**：灰阶链用带暖调的深浅色（如 `#1C1917 … #D6D3D1`），界面更高级、不刺眼。
- **inline sections over cards**：内容区默认用「分区标题 + 下划线」平铺，不要层层堆叠白卡（详见 [`../component-patterns/card-and-surface.md`](../component-patterns/card-and-surface.md)）。

## 自检

- [ ] 七件套都定了，没漏组件状态或动效曲线？
- [ ] 品牌色是一条 scale 而非单个 hex？
- [ ] 灰阶用暖灰链，不用纯黑纯白？
- [ ] 全部落成 token，组件只引用而不写字面值？

## 详细参考

- 完整设计语言范例（灰阶/品牌 scale/组件五态/动效）+ 字体配对清单 + 配色档案：[`design-language.reference.md`](design-language.reference.md)

## 相关

- 父：[`./index.md`](./index.md)
- token 落地与换肤：[`tokens-and-theming.md`](tokens-and-theming.md)
- 字阶规范：[`../foundations/typography-scale.md`](../foundations/typography-scale.md)
