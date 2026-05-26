---
name: sql-no-cross-join
description: 禁 CROSS JOIN 与 JOIN 缺 ON 子句 — 都会产生笛卡尔积，是性能杀手
parent: ./index.md
paths:
  - "**/*.sql"
  - "py/**/*.py"
  - "backend/**/*.py"
triggers:
  keywords: [CROSS JOIN, 笛卡尔积, cartesian product, JOIN ON, 性能杀手]
effort: medium
context: inline
version: "1.0"
---

# SQL · 禁 CROSS JOIN / 笛卡尔积

## 规则

**禁** `CROSS JOIN`，**禁**多表 FROM 而无 JOIN ON 条件（隐式笛卡尔积）。

## 反例

```sql
-- ❌ 显式 CROSS JOIN
SELECT * FROM users CROSS JOIN presentations;

-- ❌ 隐式笛卡尔积（多表 FROM 无 WHERE 连接）
SELECT *
FROM users u, presentations p;
-- 100 用户 × 1000 课件 = 100K 行

-- ❌ JOIN 漏写 ON 条件（被 MySQL 当成 CROSS JOIN）
SELECT *
FROM users u
JOIN presentations p;
```

## 正例

```sql
-- ✅ 显式 INNER JOIN
SELECT u.name, p.title
FROM users u
INNER JOIN presentations p ON p.owner_id = u.id;

-- ✅ 唯一允许的"笛卡尔积"：与小常量表/CTE 交叉
WITH date_series AS (
  SELECT '20260501' AS dt UNION SELECT '20260502' UNION ...
)
SELECT u.id, ds.dt FROM users u CROSS JOIN date_series ds;
-- 用于生成补齐数据
```

## Tortoise 中的对应

Tortoise 不会无意产生 CROSS JOIN（API 强制 ON 条件）。但 raw query 时仍需注意。

## CI 检测

```bash
# 简单 grep
grep -RIn "CROSS JOIN" --include="*.sql" --include="*.py"

# 多表 FROM 无 JOIN 关键字
grep -RIn -P "FROM\s+\w+\s*,\s*\w+" --include="*.sql"
```

## 自检

- [ ] 无 `CROSS JOIN`（特殊场景必须加注释说明意图）？
- [ ] 无 `FROM a, b` 多表逗号语法？
- [ ] 所有 `JOIN` 都跟 `ON` 条件？

## 相关

- 父：[`./index.md`](./index.md)
- 配套：[`../join/on-clause-required.md`](../join/on-clause-required.md)

