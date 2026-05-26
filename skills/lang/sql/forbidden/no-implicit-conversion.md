---
name: sql-no-implicit-conversion
description: 禁隐式类型转换（VARCHAR ↔ INT），用 CAST 显式
parent: ./index.md
paths:
- '**/*.sql'
- py/**/*.py
- backend/**/*.py
triggers:
  keywords:
  - CAST
  - CONVERT
  - implicit
  - 禁隐式类
  - 隐式类型
  - 式类型转
effort: medium
context: inline
version: '1.0'
---
# SQL · 禁隐式类型转换

## 规则

WHERE / JOIN 条件中**禁止依赖 MySQL 隐式类型转换**。比较两侧必须类型一致，必要时显式 `CAST` 或 `CONVERT`。

## 反例

```sql
-- ❌ session_id 是 VARCHAR，传 INT
SELECT * FROM sessions WHERE session_id = 12345;
-- MySQL 隐式转换：可能使索引失效 + 结果不正确

-- ❌ JSON 字段比较
SELECT * FROM presentations WHERE data = '{"key": "value"}';
-- → 不会走 JSON_EXTRACT 索引
```

## 正例

```sql
-- ✅ 类型对齐
SELECT * FROM sessions WHERE session_id = '12345';

-- ✅ 显式转换
SELECT * FROM tasks WHERE CAST(payload->>'$.user_id' AS UNSIGNED) = 123;

-- ✅ JSON 用 JSON_EXTRACT + CAST
SELECT * FROM presentations
WHERE JSON_UNQUOTE(JSON_EXTRACT(data, '$.theme_id')) = 'theme_001';
```

## 为什么严重

1. **索引失效**：MySQL 决定如何执行 cast 时可能丢弃索引，全表扫描
2. **结果不确定**：精度丢失（`'01' = 1` 为真，`'01abc' = 1` 也为真）
3. **跨数据库不一致**：MySQL / PostgreSQL 隐式转换规则不同

## Tortoise 中的体现

```python
# ❌ session_id 是字符串字段，传入 int
sess = await Session.filter(session_id=12345).first()
# Tortoise 会自动 stringify，但日志里看不到，难以排查

# ✅ 调用方保持类型
sess = await Session.filter(session_id=str(12345)).first()
```

## CI 检测

人工 review 重点关注。无可靠的纯静态规则。

## 自检

- [ ] WHERE / JOIN 两侧类型一致？
- [ ] JSON 字段查询用 `JSON_EXTRACT` 并显式 CAST？
- [ ] 索引字段类型与查询参数完全匹配？

## 相关

- 父：[`./index.md`](./index.md)

