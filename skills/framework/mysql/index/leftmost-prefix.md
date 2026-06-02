---
name: mysql-leftmost-prefix
description: 联合索引最左前缀法则 + 索引下推 ICP — 索引 (a,b,c) 只能从 a 起连续命中，跳列或范围后断列即失效。Use when 设计联合索引列顺序 / 排查 WHERE 没走联合索引 / 评审 ORDER BY 用不上索引时。
parent: ./index.md
paths:
- '*.sql'
- '*.xml'
- '*.java'
triggers:
  keywords:
  - 最左前缀
  - 联合索引
  - leftmost prefix
  - composite index
  - 索引下推
  - index condition pushdown
  - ICP
effort: high
context: inline
version: '1.0'
---
# MySQL · 联合索引最左前缀

> 本条只管「联合索引列怎么排、为什么没命中」。索引选不选、区分度见 [`cardinality-and-prefix.md`](./cardinality-and-prefix.md)；命中后还回表见 [`covering-index.md`](./covering-index.md)；其它失效场景见 [`index-fail-cases.md`](./index-fail-cases.md)。

## 规则

联合索引 `(a, b, c)` 的 B+Tree 按 `a→b→c` 顺序排列，**只能从最左列开始、连续使用**：

| WHERE 条件 | 用到几列 | 原因 |
|-----------|---------|------|
| `a=? AND b=? AND c=?` | a,b,c | 全前缀命中 |
| `a=? AND b=?` | a,b | 前缀命中，c 不用也行 |
| `a=? AND c=?` | 仅 a | **跳过 b**，c 用不上 |
| `b=? AND c=?` | 无 | **缺最左列 a**，整索引失效 |
| `a=? AND b>10 AND c=?` | a,b | **b 是范围**，范围后的 c 断列 |

## 列顺序设计原则

1. **等值列在前，范围列在后**：`WHERE a=? AND b BETWEEN`→建 `(a,b)`，范围列放最后。
2. **高频等值 + 区分度高的列靠左**：让更多查询能复用同一索引。
3. **覆盖 ORDER BY**：排序列接在等值列后，可省 filesort（见下例）。

## 正例

```sql
-- 索引 idx_uid_status_ctime (user_id, status, created_at)

-- ✅ 全部走索引：等值 user_id + status，再按 created_at 有序扫
SELECT id FROM orders
WHERE user_id = 100 AND status = 'PAID'
ORDER BY created_at DESC;

-- ✅ 范围列放最后，前缀 user_id 仍命中
SELECT id FROM orders WHERE user_id = 100 AND created_at > '2026-01-01';
```

## 反例

```sql
-- ❌ 缺最左列 user_id：idx_uid_status_ctime 整体用不上 → 全表扫
SELECT id FROM orders WHERE status = 'PAID';

-- ❌ status 用了范围，后面的 created_at 无法再走索引排序 → filesort
SELECT id FROM orders WHERE user_id = 100 AND status > 'A' ORDER BY created_at;
```

## 索引下推（ICP，5.6+）

最左前缀断列后，**未断的索引列仍可在引擎层先过滤再回表**，减少回表行数：

```sql
-- 索引 (name, age)，name 用了 like 'foo%'（前缀），age=10 本来无法走索引
-- ICP 让 age=10 在索引层就过滤掉不匹配行，EXPLAIN Extra 显示 Using index condition
SELECT * FROM staff WHERE name LIKE 'foo%' AND age = 10;
```

ICP 默认开启，无需手动配置；`EXPLAIN` 的 `Extra` 出现 `Using index condition` 即生效。

## 自检

- [ ] WHERE 是否从联合索引最左列开始、中间无跳列？
- [ ] 范围条件（`>`/`<`/`BETWEEN`/`LIKE 前缀`）的列是否排在索引最后？
- [ ] ORDER BY 列是否紧接等值列，避免额外 filesort？
- [ ] EXPLAIN 的 `key` 是否命中预期索引，`Extra` 无 `Using filesort`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`covering-index.md`](./covering-index.md) · [`index-fail-cases.md`](./index-fail-cases.md) · [`cardinality-and-prefix.md`](./cardinality-and-prefix.md)
- 诊断：[`../diagnosis/explain-reading.md`](../diagnosis/explain-reading.md)
