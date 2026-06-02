---
name: framework-mysql-index
description: MySQL/InnoDB 引擎特性规约 5 大类 — 索引设计 / 事务与锁 / Schema 字段设计 / 性能诊断(EXPLAIN/慢查询) / 上线与扩展(Online DDL/分库分表/分布式ID)。Use when 建索引或排查没走索引 / 处理事务隔离与死锁 / 选字段类型 / 调慢查询 / 大表改表或分片时。
parent: ../index.md
children:
  - { name: index, path: index/index.md, tag: folder, note: "索引设计：聚簇主键/最左前缀/覆盖索引/失效场景/区分度（5 子项）" }
  - { name: transaction, path: transaction/index.md, tag: folder, note: "事务与锁：隔离级别/MVCC 当前读/间隙锁死锁/事务范围（4 子项）" }
  - { name: schema, path: schema/index.md, tag: folder, note: "Schema 字段设计：数值时间金额/字符串/NOT NULL/字符集（4 子项）" }
  - { name: diagnosis, path: diagnosis/index.md, tag: folder, note: "性能诊断：EXPLAIN/慢查询定位/count 与深分页（3 子项）" }
  - { name: ops, path: ops/index.md, tag: folder, note: "上线与扩展：Online DDL/分库分表拆分键/分布式 ID（3 子项）" }
when_to_descend: |
  涉及 MySQL/InnoDB 引擎本身的设计与调优：建索引、排查没走索引、处理事务隔离级别与死锁、选字段类型与字符集、读 EXPLAIN 调慢查询、大表在线改表或分库分表。
  注意分工：SQL 语句语法红线（禁 SELECT * / 必带 WHERE 等）在 lang/sql/；MyBatis/Mapper 持久层用法在 framework/mybatis/；要不要用 MySQL（vs PG）的选型在 tech-selection/database/。本目录只管「MySQL 引擎特性与调优」。
---

# MySQL · 引擎特性规约索引

> 本目录管 **MySQL/InnoDB 引擎本身**的设计与调优，与三个邻居分工：
> - 语句语法红线（禁 `SELECT *`、必带 WHERE/ON、禁隐式转换）→ [`../../lang/sql/index.md`](../../lang/sql/index.md)
> - MyBatis Mapper / 动态 SQL / 分页框架用法 → [`../mybatis/index.md`](../mybatis/index.md)
> - 关系库选 MySQL 还是 PostgreSQL → [`../../tech-selection/database/index.md`](../../tech-selection/database/index.md)

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| index | 文件夹 | 索引设计：聚簇主键 / 最左前缀 / 覆盖索引 / 失效场景 / 区分度（5 子项）|
| transaction | 文件夹 | 事务与锁：隔离级别 / MVCC 当前读 / 间隙锁死锁 / 事务范围（4 子项）|
| schema | 文件夹 | Schema 字段设计：数值时间金额 / 字符串 / NOT NULL / 字符集（4 子项）|
| diagnosis | 文件夹 | 性能诊断：EXPLAIN / 慢查询定位 / count 与深分页（3 子项）|
| ops | 文件夹 | 上线与扩展：Online DDL / 分库分表拆分键 / 分布式 ID（3 子项）|

## 何时下钻

| 你在做什么 | 进哪个 |
|-----------|-------|
| 建索引、查询慢且没走索引、定主键 | [index/](index/index.md) |
| 配隔离级别、写 FOR UPDATE、排查死锁/锁等待 | [transaction/](transaction/index.md) |
| 建表选字段类型、字符集、NOT NULL | [schema/](schema/index.md) |
| 看 EXPLAIN、从慢日志定位、优化 count/深分页 | [diagnosis/](diagnosis/index.md) |
| 大表加字段/加索引、分库分表、选分布式主键 | [ops/](ops/index.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行框架：[`../mybatis/index.md`](../mybatis/index.md) · [`../redis/index.md`](../redis/index.md) · [`../spring-boot/index.md`](../spring-boot/index.md)
- 语句层：[`../../lang/sql/index.md`](../../lang/sql/index.md)
- 选型层：[`../../tech-selection/database/index.md`](../../tech-selection/database/index.md)
