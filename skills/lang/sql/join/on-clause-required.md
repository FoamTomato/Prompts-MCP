---
name: sql-on-clause-required
description: SQL 多表 JOIN 必带 ON 子句 — 缺 ON 会退化为笛卡尔积 / CROSS JOIN。Use when 写 SQL / 迁移脚本
  / 评审涉及 `on-clause-required` 的 PR。
parent: ./index.md
paths:
- '**/*.sql'
- py/**/*.py
- backend/**/*.py
triggers:
  keywords:
  - JOIN
  - 'ON'
  - 多表
  - 条件
effort: medium
context: inline
version: '1.0'
---
# SQL · JOIN 必带 ON

## 规则

每个 `JOIN` 后**必须**跟 `ON <连接条件>`。

## 反例

```sql
-- ❌ JOIN 后无 ON（MySQL 会当成 CROSS JOIN）
SELECT *
FROM users u
JOIN presentations p
WHERE p.owner_id = u.id;   -- WHERE 不是 ON

-- ❌ 用 WHERE 替代 ON（旧式语法）
SELECT *
FROM users u, presentations p
WHERE p.owner_id = u.id;
```

## 正例

```sql
-- ✅
SELECT u.name, p.title
FROM users u
INNER JOIN presentations p ON p.owner_id = u.id;

-- ✅ 多条件
INNER JOIN slides s
  ON s.presentation_id = p.id
 AND s.is_active = TRUE;
```

## LEFT JOIN 注意点

```sql
-- ⚠️ LEFT JOIN 把过滤条件放 ON vs WHERE 含义不同
-- ON 上：保留左表全部行
SELECT u.name, p.title
FROM users u
LEFT JOIN presentations p ON p.owner_id = u.id AND p.is_active = TRUE;

-- WHERE 上：把 is_active=FALSE 的左表行也过滤掉，退化为 INNER JOIN
SELECT u.name, p.title
FROM users u
LEFT JOIN presentations p ON p.owner_id = u.id
WHERE p.is_active = TRUE;
```

按需选择，写 PR comment 说明意图。

## Tortoise 中的等价

```python
# Tortoise 自动生成正确的 ON
await Presentation.filter(owner__id=uid).prefetch_related("owner")
# 但 raw query 时仍要手写
```

## 自检

- [ ] 每个 JOIN 后跟 ON？
- [ ] LEFT JOIN 的过滤条件位置（ON vs WHERE）符合意图？
- [ ] 无逗号多表 FROM 写法？

## 相关

- 父：[`./index.md`](./index.md)
- 配套：[`prefer-explicit-inner.md`](./prefer-explicit-inner.md)

