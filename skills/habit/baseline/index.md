---
name: habit-baseline-index
description: 基础写法宪法 — 语言无关的硬底线，任何 dev 任务写第一行代码前必读。Use when 写/改任意源码（不限语言）、dev/dev-lite 启动、code review 兜底。
parent: ../index.md
children:
  - { name: code-baseline, path: code-baseline.md, tag: skill, note: 七条语言无关硬底线，写码时按序自检（命名→魔法值→错误→最小改动→无残留→边界→依赖） }
triggers:
  keywords:
  - baseline
  - 基础
  - 写法
  - 规约
  - 底线
  - code-baseline
when_to_descend: |
  任何 dev / dev-lite 任务的第一步（--ensure-style 会无条件钉入）。
  与具体语言/框架无关，是 lang/*、framework/*、design-pattern/* 之上的统一底座。
  语言级细则（命名表、空安全、并发…）下钻到 lang/<lang>/。
---

# Baseline · 基础写法宪法

> dev 写代码的底座。`--ensure-style` 无条件把它钉进必读池——
> 无论用什么语言、命中哪些 framework/style skill，这七条先成立。
> 语言级细则下钻到 [`../../lang/`](../../lang/index.md)；本层只管语言无关的硬底线。

## 子项

| 子项 | 一句话 |
|------|-------|
| [code-baseline](code-baseline.md) | 七条语言无关硬底线，写码时按序自检 |

## 与其它维度的边界

- 不替代 `lang/*`：命名底线在 Python 下细化为 [`../../lang/python/naming/`](../../lang/python/index.md)，Java 下为 [`../../lang/java/naming/`](../../lang/java/index.md)。
- 与 [`../code-quality/`](../code-quality/index.md)：code-quality 写带语言示例的可读性规则；baseline 写语言无关的元规则，是其上位。

## 链接

- 父：[`../index.md`](../index.md)
- 兄弟：[`../code-quality/index.md`](../code-quality/index.md)
