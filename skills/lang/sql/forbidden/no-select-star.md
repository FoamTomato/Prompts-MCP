---
name: sql-no-select-star
description: 禁 SELECT *（已在 docs/Creative_Ideation/harness/skills/ 详写）。Use when 写 Python
  后端代码 / 评审涉及 `no-select-star` 的 PR。
parent: ./index.md
paths:
- py/**/*.py
- backend/**/*.py
- '**/*.sql'
triggers:
  keywords:
  - SELECT *
  - '*.sql'
  - 已在
  - 详写
effort: medium
context: inline
version: '1.0'
---
# SQL · 禁 SELECT *（同规则汇集）

## 规则与依据

同 [`../select/explicit-column-list.md`](../select/explicit-column-list.md)。本文件作为 forbidden/ 维度下的并列条目存在，便于"列禁项清单"时一并被检索到。

## 速记

| 检查项 | 状态 |
|--------|------|
| 生产 .sql 不出现 `SELECT *` | 必须 |
| Tortoise raw query 不用 `SELECT *` | 必须 |
| `.first()` / `.all()` 默认查全列 → 性能敏感场景改 `.only()` / `.values()` | 必须 |
| 交互式排查 SELECT * | 允许（不提交） |

## CI

```bash
grep -RIn "SELECT \*\|select \*" --include="*.py" --include="*.sql" backend/ py/
```

## 相关

- 父：[`./index.md`](./index.md)
- 详细版本：[`../select/explicit-column-list.md`](../select/explicit-column-list.md)

