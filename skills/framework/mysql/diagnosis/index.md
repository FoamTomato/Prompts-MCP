---
name: framework-mysql-diagnosis-index
description: MySQL 性能诊断 3 个独立决策点 — 读懂 EXPLAIN 执行计划、慢查询定位流程、count 与深分页优化。Use when 查询慢 / 看 EXPLAIN / 定位慢 SQL / 优化 count 或深分页时。
parent: ../index.md
children:
  - { name: mysql-explain-reading, path: explain-reading.md, tag: skill, note: "读 EXPLAIN：type/key/rows/Extra 警报项" }
  - { name: mysql-slow-query-triage, path: slow-query-triage.md, tag: skill, note: "慢查询定位流程：慢日志→EXPLAIN→改索引/改写" }
  - { name: mysql-count-and-deep-paging, path: count-and-deep-paging.md, tag: skill, note: "count(*) 真相 + 深分页 keyset 优化" }
when_to_descend: 查询慢、看 EXPLAIN、从慢日志定位问题 SQL、优化 count 统计或大 offset 深分页。
---

# MySQL · 性能诊断索引

性能诊断拆成 3 个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 看一条 SQL 的 EXPLAIN，想读懂各列 | [explain-reading](explain-reading.md) |
| 系统慢，要从慢日志定位是哪条 SQL | [slow-query-triage](slow-query-triage.md) |
| count(*) 慢、深分页（大 offset）慢 | [count-and-deep-paging](count-and-deep-paging.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 兄弟维度：[`../index/index.md`](../index/index.md)（改索引）
- 框架分页（互补）：[`../../mybatis/pagination.md`](../../mybatis/pagination.md)
