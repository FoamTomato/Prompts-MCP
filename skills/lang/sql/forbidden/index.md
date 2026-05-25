---
name: lang-sql-forbidden-index
description: SQL 禁项清单
parent: ../index.md
children:
  - { name: no-select-star, path: no-select-star.md, tag: skill, note: 禁 SELECT * }
  - { name: no-implicit-conversion, path: no-implicit-conversion.md, tag: skill, note: 禁隐式类型转换 }
  - { name: no-cross-join, path: no-cross-join.md, tag: skill, note: 禁 CROSS JOIN / 笛卡尔积 }
when_to_descend: Code Review / DBA 上线前检查 / 写 SQL 时
---

# Forbidden · 子项索引

| 子项 | 一句话 |
|------|-------|
| no-select-star | 禁 SELECT * |
| no-implicit-conversion | 禁隐式类型转换 |
| no-cross-join | 禁 CROSS JOIN / 笛卡尔积 |
