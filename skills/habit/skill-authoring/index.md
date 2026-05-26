---
name: habit-skill-authoring-index
description: 写一条好 skill 的规约索引 — description 写法 / 长度边界 / progressive disclosure / 触发词。Use when 新建 skill 文件、review skill PR、或被问 "怎么把约定写成 skill" 时进入此索引。
parent: ../index.md
children:
  - { name: description-format, path: description-format.md, tag: leaf, note: description 字段写法 — 两句结构 + Use when }
  - { name: body-length-budget, path: body-length-budget.md, tag: leaf, note: skill 正文 ≤100 行，超出拆 reference.md }
  - { name: progressive-disclosure, path: progressive-disclosure.md, tag: leaf, note: 主文件 + reference/examples 分层加载 }
  - { name: trigger-phrasing, path: trigger-phrasing.md, tag: leaf, note: keywords 中英双语 + 用户原话触发词 }
when_to_descend: |
  新建 skill / 改 skill 文件 frontmatter / 评审 PR 涉及 skill / 训练新人写 skill。本索引下钻是「写 skill」时的强制起点。
---

# Skill Authoring · 写 skill 的规约

> 灵感来自 Matt Pocock 的 [skills repo](https://github.com/mattpocock/skills)，结合本仓 MCP 检索语义化做的本地化。

## 核心理念

skill 是给 **agent** 看的，不是给人看的。所有规约都围绕一个问题：

> agent 看到这条 skill 时，能否 (1) 立刻判断要不要加载它，(2) 加载后知道该做什么？

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| description-format | 叶子 | description 字段两句结构：是什么 + Use when |
| body-length-budget | 叶子 | 正文 ≤100 行硬边界，超出拆引用 |
| progressive-disclosure | 叶子 | 渐进披露 — SKILL.md 主入口 + 外链深内容 |
| trigger-phrasing | 叶子 | triggers.keywords 必须含中英双语 + 用户原话 |

## 写新 skill 时的执行顺序

1. 先写 `description`（两句结构）—— 写不出来说明意图不清晰，回去想
2. 再写 frontmatter 其他字段（`paths` / `triggers.keywords` / `effort`）
3. 写正文 H1 + ≤100 行内容
4. 跑 `python scripts/lint_skills.py` 自检
5. 跑一遍假想 query：`search_skills(query="<相关任务原话>")` 能命中本条吗？不能就回头改 keywords

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../code-quality/index.md`](../code-quality/index.md) · [`../prd-sync/index.md`](../prd-sync/index.md)
- 参考：本仓 [`CONTRIBUTING.md`](../../../CONTRIBUTING.md) 是这套规约的最终强制版（lint 工具按它跑）
