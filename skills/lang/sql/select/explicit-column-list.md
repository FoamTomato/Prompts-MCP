---
name: sql-explicit-column-list
description: '语言规则 · sql: SELECT 必须显式列出列名 — 禁 SELECT *'
parent: ./index.md
paths:
- py/**/*.py
- backend/**/*.py
- '**/*.sql'
triggers:
  keywords:
  - SELECT
  - query
  - raw_query
  - fetch
  - 必须显式
  - 须显式列
  - 显式列出
effort: medium
context: inline
version: '1.0'
---
# SQL · SELECT 显式列出列名

## 规则

任何生产 SQL（含 ORM raw、Alembic data migration、seed 脚本）**必须显式列出查询的列**，禁 `SELECT *`。

## 反例 → 正例

```python
# ❌
rows = await conn.execute_query_dict("SELECT * FROM presentations WHERE owner_id = %s", [uid])

# ✅
rows = await conn.execute_query_dict(
    "SELECT id, title, theme_id, created_at FROM presentations WHERE owner_id = %s",
    [uid],
)
```

## Tortoise ORM 等价

```python
# ❌ 默认查全列
items = await Presentation.filter(owner_id=uid)

# ✅ 性能敏感场景用 only / values
items = await Presentation.filter(owner_id=uid).only("id", "title", "theme_id", "created_at")

# ✅ 只要 dict 不要 ORM 对象
data = await Presentation.filter(owner_id=uid).values("id", "title", "theme_id")
```

## 为什么

1. Schema 变更（加列）后行为静默改变
2. ORM 反序列化遇到未声明列抛 / 忽略（Tortoise 抛 `FieldError`）
3. 索引覆盖优化失效——强迫回表
4. 网络/磁盘 IO 浪费

## CI 检测

```bash
grep -RIn "SELECT \*\|select \*" --include="*.py" --include="*.sql" backend/ py/
```

命中即 fail。

## 例外（仅一种）

DBA 交互式排查（DBeaver / mysql CLI）的临时查询。**不得提交到仓库**。

## 自检

- [ ] 仓库内无 `SELECT *`？
- [ ] Tortoise 性能敏感场景用 `.only()` / `.values()` ？
- [ ] 列变更前确认所有引用方？

## 相关

- 父：[`./index.md`](./index.md)
- 配套：[`../forbidden/no-select-star.md`](../forbidden/no-select-star.md)（同规则的另一切入点）

