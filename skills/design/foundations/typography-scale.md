---
name: design-typography-scale
description: 正文 16px 基准、单一模块化字阶比例(默认 1.25)、行长 45-75 字符、行高 1.5、靠字重造层级。Use when 定字号阶梯 / 设正文行高行长 / 选字体配对 / 评审排版层级时。
parent: ./index.md
paths:
  - "**/*.tsx"
  - "**/*.vue"
  - "**/*.css"
  - "**/*.scss"
  - "**/*.html"
triggers:
  keywords:
    - 字阶
    - 模块化字阶
    - type scale
    - typography
    - 行高
    - 行长
    - 字体配对
    - font pairing
effort: low
version: "1.0"
---

# Typography · 模块化字阶

> 字号不是随手定，而是从一个基准 × 一个比例推导出整套阶梯。

## 基准与比例

- 正文基准 **16px = 1rem**（不要更小当正文）。
- 整套字号由**单一比例**逐级相乘得出：

| 比例 | 名称 | 适用 |
|------|------|------|
| **1.250** | Major Third | **默认**，通用 |
| 1.200 | Minor Third | 密集 / 数据型 |
| 1.333 | Perfect Fourth | 编辑 / 内容站 |
| 1.5 / 1.618 | — | hero 大标题张力 |

示例（16px × 1.25）：`16 → 20 → 25 → 31 → 39 → 49`px。

## 行长与行高

| 项 | 值 |
|----|----|
| 正文行长 | **45-75 字符**（理想 66；移动端 30-40）→ `max-width: 60-75ch`（约 600-700px） |
| 正文行高 | **1.5** 无单位（区间 1.4-1.6） |
| 标题行高 | 1.1 - 1.3（越大越紧） |

## 层级靠字重，不靠堆字号

- 同一字号用 **字重**（400/500/600/700）拉开主次，而非无限加字号档。
- 字体族**最多 2 套**（硬上限 3）：标题管个性、正文管易读；优先单一可变字体（如 Inter 100-900）用字重造层级。
- 配对原则：分类有对比（衬线+无衬线）但共享特征（x-height 相近）。

> 常用字体配对清单见 [`../design-language/design-language.reference.md`](../design-language/design-language.reference.md)。

## 自检

- [ ] 正文 16px 基准，整套字号由单一比例推导（默认 1.25）？
- [ ] 正文 `max-width` 控制行长在 45-75 字符？
- [ ] 正文行高 ~1.5、标题 1.1-1.3？
- [ ] 字体族 ≤2，层级主要靠字重而非堆字号？

## 相关

- 父：[`./index.md`](./index.md)
- 间距同属节奏体系：[`spacing-grid.md`](spacing-grid.md)
- 字体配对与字阶 token 化：[`../design-language/design-language.md`](../design-language/design-language.md)
