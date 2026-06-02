---
name: lang-sql-index
description: SQL 语句硬约束索引（DDL 模板 / SELECT 规则 / JOIN 规则 / 禁项清单）
parent: ../index.md
children:
  - { name: ddl, path: ddl/index.md, tag: folder, note: 建表 / 索引 / 迁移模板 }
  - { name: select, path: select/index.md, tag: folder, note: SELECT 必须显式列名等硬约束 }
  - { name: dml, path: dml/index.md, tag: folder, note: UPDATE / DELETE 必带 WHERE }
  - { name: join, path: join/index.md, tag: folder, note: ON 条件必填 / 显式 JOIN 类型 }
  - { name: forbidden, path: forbidden/index.md, tag: folder, note: 全表更新 / SELECT * 等禁项 }
when_to_descend: |
  写 / 改任何 SQL 语句、迁移脚本、ORM 中的原生 SQL fragment。
---

# SQL · 语句硬约束

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| ddl | 文件夹 | 建表 / 改表 / 索引迁移 |
| select | 文件夹 | SELECT 列名 / 分页 / 排序 |
| dml | 文件夹 | UPDATE / DELETE 必带 WHERE |
| join | 文件夹 | ON 条件强制 + 类型显式 |
| forbidden | 文件夹 | 全表 UPDATE / SELECT * 等禁项 |

## 何时下钻

- 写新迁移 / 加索引 → `ddl/index.md`
- 普通查询 → `select/index.md`
- 改数据（UPDATE/DELETE）→ `dml/index.md`
- 多表关联 → `join/index.md`
- 评审 SQL 风险 → `forbidden/index.md`

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../python/index.md`](../python/index.md) · [`../typescript/index.md`](../typescript/index.md)
