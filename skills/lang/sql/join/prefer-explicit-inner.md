---
name: sql-prefer-explicit-inner
description: 显式 INNER JOIN vs LEFT JOIN — 不省 JOIN 类型
parent: ./index.md
paths:
  - "**/*.sql"
  - "py/**/*.py"
  - "backend/**/*.py"
triggers:
  keywords: [INNER JOIN, LEFT JOIN]
effort: medium
context: inline
version: "1.0"
---

# SQL · 显式 INNER JOIN

## 规则

**默认用 `INNER JOIN`，而非裸 `JOIN`**。代码清晰度优先。

```sql
-- ⚠️ 含义同 INNER JOIN，但不显式
SELECT * FROM a JOIN b ON ...;

-- ✅ 显式
SELECT * FROM a INNER JOIN b ON ...;
SELECT * FROM a LEFT JOIN b ON ...;
SELECT * FROM a RIGHT JOIN b ON ...;
```

## JOIN 类型选择

| 用 | 何时 |
|----|------|
| `INNER JOIN` | 两边都必须存在的关联（订单 + 用户） |
| `LEFT JOIN` | 左表为主，右表可空（用户 + 可选的偏好） |
| `RIGHT JOIN` | 极少用，通常改写成 LEFT 更易读 |
| `FULL OUTER JOIN` | MySQL 不支持，用 LEFT UNION RIGHT 模拟 |

## 性能考虑

```sql
-- ❌ 大表 LEFT JOIN 小表（顺序反了）
SELECT * FROM presentations p
LEFT JOIN users u ON u.id = p.owner_id;
-- 优化器一般能纠正，但显式更好

-- ✅ 小表 LEFT JOIN 大表
SELECT u.name, p.title
FROM users u
LEFT JOIN presentations p ON p.owner_id = u.id;
```

## 多表 JOIN 编排

```sql
-- ✅ 缩进风格
SELECT
  p.id, p.title,
  u.name AS owner,
  t.name AS theme
FROM presentations p
INNER JOIN users u  ON u.id = p.owner_id
LEFT JOIN  themes t ON t.id = p.theme_id
WHERE p.created_at > '2026-01-01';
```

## 自检

- [ ] 用 `INNER JOIN` 而非裸 `JOIN`？
- [ ] LEFT JOIN 用在确实可空的右表？
- [ ] 多表 JOIN 缩进对齐，便于阅读？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`on-clause-required.md`](./on-clause-required.md)

