---
name: mysql-explain-reading
description: 读懂 MySQL EXPLAIN 执行计划 — 重点看 type/key/rows/Extra，Extra 出现 Using filesort/Using temporary 即排序分组没走索引。Use when 看 SQL 的 EXPLAIN / 判断有没有走索引 / 评审查询计划时。
parent: ./index.md
paths:
- '*.sql'
- '*.xml'
- '*.java'
triggers:
  keywords:
  - EXPLAIN
  - 执行计划
  - type 访问类型
  - Using filesort
  - Using temporary
  - rows 扫描行
  - key 索引
effort: high
context: inline
version: '1.0'
---
# MySQL · 读懂 EXPLAIN

> 本条只管「单条 SQL 的 EXPLAIN 各列怎么读」。从慢日志找出该看哪条 SQL 见 [`slow-query-triage.md`](./slow-query-triage.md)；读完发现没走索引怎么改见 [`../index/index-fail-cases.md`](../index/index-fail-cases.md)。

## 关键列

| 列 | 看什么 |
|----|--------|
| `type` | 访问类型，好→坏：`const > eq_ref > ref > range > index > ALL`。**出现 `ALL`（全表扫）要警惕** |
| `key` | 实际用的索引；`NULL` = 没走索引 |
| `key_len` | 用到索引的字节数，判断联合索引用了几列 |
| `rows` | 优化器估算要扫的行数，越小越好 |
| `filtered` | 估算过滤后剩余行百分比 |
| `Extra` | 最信息量的列，见下 |

## Extra 常见信号

| Extra | 含义 | 是否警报 |
|-------|------|---------|
| `Using index` | 覆盖索引，免回表 | ✅ 好 |
| `Using index condition` | 索引下推 ICP 生效 | ✅ 好 |
| `Using where` | 在 server 层过滤（配 ALL 时常意味着没用好索引） | ⚠️ 看搭配 |
| `Using filesort` | **额外排序**（没用索引完成 ORDER BY） | ⚠️ 优化点 |
| `Using temporary` | **用了临时表**（常见于 GROUP BY/DISTINCT/复杂 ORDER BY） | ⚠️ 优化点 |

## 用法

```sql
-- 看计划
EXPLAIN SELECT id FROM orders WHERE user_id = 100 ORDER BY created_at;

-- 看真实执行的耗时分布（实际跑一遍）
EXPLAIN ANALYZE SELECT ...;
```

## 读法流程

1. 看 `type` 有没有 `ALL` / `key` 是不是 `NULL` → 有就是没走索引，去 [index-fail-cases](../index/index-fail-cases.md)。
2. 看 `rows` 估算值是否远大于结果集 → 扫太多，索引选择性差或没命中。
3. 看 `Extra` 有没有 `Using filesort` / `Using temporary` → 排序/分组没走索引，调整索引列顺序覆盖 ORDER BY/GROUP BY。
4. 联表查询逐行看每张表的 `type`/`key`，定位是哪张表全表扫。

## 自检

- [ ] 每张表的 `type` 都优于 `ALL`（理想 `ref`/`range`/`const`）？
- [ ] `key` 命中了预期索引，不是 `NULL`？
- [ ] `rows` 估算与实际结果集量级接近，没扫海量行？
- [ ] `Extra` 没有非预期的 `Using filesort` / `Using temporary`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`slow-query-triage.md`](./slow-query-triage.md) · [`count-and-deep-paging.md`](./count-and-deep-paging.md)
- 改索引：[`../index/index-fail-cases.md`](../index/index-fail-cases.md) · [`../index/leftmost-prefix.md`](../index/leftmost-prefix.md)
