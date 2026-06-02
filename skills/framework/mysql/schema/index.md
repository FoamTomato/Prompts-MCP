---
name: framework-mysql-schema-index
description: MySQL Schema 与字段设计 4 个独立决策点 — 数值/时间/金额类型选型、字符串类型选型、NOT NULL 与默认值、字符集统一 utf8mb4。Use when 建表选字段类型 / 评审 DDL 字段定义 / 排查字符集乱码或 JOIN 隐式转换时。
parent: ../index.md
children:
  - { name: mysql-column-type-choice, path: column-type-choice.md, tag: skill, note: "数值/时间/金额：能小不大，钱用 DECIMAL，时间取舍" }
  - { name: mysql-string-type-choice, path: string-type-choice.md, tag: skill, note: "CHAR/VARCHAR/TEXT 取舍，TEXT 不进主表" }
  - { name: mysql-not-null-and-default, path: not-null-and-default.md, tag: skill, note: "列尽量 NOT NULL + 合理默认，NULL 伤索引/聚合" }
  - { name: mysql-charset-utf8mb4, path: charset-utf8mb4.md, tag: skill, note: "统一 utf8mb4 + collation 一致防 JOIN 隐式转换" }
when_to_descend: 建表 / 改字段类型 / 评审 DDL 字段定义 / 排查字符集乱码或跨表 JOIN 隐式转换。
---

# MySQL · Schema 与字段设计索引

字段设计拆成 4 个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 选数值/时间/金额字段类型 | [column-type-choice](column-type-choice.md) |
| 选字符串字段类型（CHAR/VARCHAR/TEXT） | [string-type-choice](string-type-choice.md) |
| 纠结某列要不要 NOT NULL、给什么默认值 | [not-null-and-default](not-null-and-default.md) |
| 定字符集/排序规则、排查乱码或 JOIN 隐式转换 | [charset-utf8mb4](charset-utf8mb4.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 兄弟维度：[`../index/index.md`](../index/index.md)
- 语句层（建表/迁移模板）：[`../../../lang/sql/ddl/index.md`](../../../lang/sql/ddl/index.md)
