---
name: mysql-slow-query-triage
description: MySQL 慢查询定位流程 — 开慢查询日志抓慢 SQL，用 pt-query-digest 聚合排序找 TopN，再逐条 EXPLAIN 定位。Use when 系统变慢要找慢 SQL / 配慢查询日志 / 不知从哪入手优化时。
parent: ./index.md
paths:
- '*.sql'
- '*.yml'
- '*.cnf'
- '*.properties'
triggers:
  keywords:
  - 慢查询日志
  - slow query log
  - long_query_time
  - pt-query-digest
  - mysqldumpslow
  - 慢 SQL 定位
effort: medium
context: inline
version: '1.0'
---
# MySQL · 慢查询定位流程

> 本条只管「怎么找出是哪条 SQL 慢」的流程。找到后单条 EXPLAIN 怎么读见 [`explain-reading.md`](./explain-reading.md)；定位是索引问题后怎么改见 [`../index/index.md`](../index/index.md)。

## 定位流程（按顺序）

1. **开慢查询日志**，设阈值：

```ini
# my.cnf
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 1          # 超过 1s 记录（按业务调，可先 0.5）
log_queries_not_using_indexes = 1   # 未走索引的也记
```

2. **聚合排序找 TopN**（不要手翻日志）：

```bash
# 自带工具，按平均耗时排序前 10
mysqldumpslow -s at -t 10 /var/log/mysql/slow.log
# 或 Percona 工具，按总耗时聚合（推荐，能合并参数不同的同型 SQL）
pt-query-digest /var/log/mysql/slow.log
```

3. **逐条 EXPLAIN** Top 慢 SQL → 见 [explain-reading](explain-reading.md)。
4. **对症下药**：没走索引→建/改索引；扫太多行→加过滤条件；filesort/临时表→调索引覆盖排序分组；SQL 写法问题→改写（见 index-fail-cases）。
5. **复测**：改完再 EXPLAIN + 实跑确认 `rows`/耗时下降。

## 优先级判断

- **按「总耗时 = 单次耗时 × 调用次数」排序**，不是只看单次最慢。一条 50ms 但每秒调 1000 次的，比一条 2s 但每天跑 1 次的更值得优化。
- `pt-query-digest` 的 grand total / Response time 占比直接给出这个排序。

## 临时排查（不便开日志时）

```sql
-- 看当前正在执行的长查询
SELECT * FROM information_schema.PROCESSLIST WHERE TIME > 5 AND COMMAND='Query';
-- 性能 schema 里的语句汇总（按平均耗时）
SELECT * FROM performance_schema.events_statements_summary_by_digest
ORDER BY AVG_TIMER_WAIT DESC LIMIT 10;
```

## 自检

- [ ] 慢查询日志已开、`long_query_time` 设了合理阈值？
- [ ] 用 `pt-query-digest`/`mysqldumpslow` **聚合**排序，而非肉眼翻日志？
- [ ] 按「总耗时（含调用频次）」而非单次耗时定优先级？
- [ ] 每条优化后都复测确认 `rows`/耗时确实下降？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`explain-reading.md`](./explain-reading.md)
- 改索引：[`../index/index.md`](../index/index.md)
