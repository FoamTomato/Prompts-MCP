---
name: sql-dml-must-have-where
description: UPDATE / DELETE 必须带 WHERE 子句。Use when 写 Python 后端代码 / 评审涉及 `must-have-where`
  的 PR。
parent: ./index.md
paths:
- backend/**/*.py
- '**/*.py'
- '**/*.sql'
triggers:
  keywords:
  - UPDATE
  - DELETE
  - WHERE
  - 必须带
  - 子句
effort: medium
context: inline
version: '1.0'
---
# SQL · UPDATE/DELETE 必带 WHERE

## 规则

**`UPDATE` / `DELETE` 必须带 `WHERE` 子句**，无 WHERE 等于全表操作，几乎必然是事故。

## 反例 → 正例

```sql
-- ❌ 没 WHERE，全表清空
DELETE FROM orders;

-- ✅ 限定条件
DELETE FROM orders
WHERE expires_at < NOW() - INTERVAL 90 DAY;

-- ❌ 全表 UPDATE
UPDATE documents SET theme_id = 'default';

-- ✅
UPDATE documents SET theme_id = 'default'
WHERE theme_id IS NULL;
```

## Tortoise ORM 等价

```python
# ❌ 全表
await Document.all().delete()
await Document.all().update(theme_id="default")

# ✅
await Document.filter(expires_at__lt=cutoff).delete()
await Document.filter(theme_id=None).update(theme_id="default")
```

## 唯一例外：seed / data migration 全量重置

明确意图的"清空表"场景：

```python
# scripts/seed_articles.py
async def reset_and_seed():
    # 清空并重新插入: 仅在 seed 脚本允许, 注释必须说明
    await Article.all().delete()   # 注释说明意图（清空并重新插入）
    await Article.bulk_create(SEED_DATA)
```

## CI / hook 兜底

PostToolUse hook 可加正则检测 `\b(UPDATE|DELETE)\b` 后无 `\bWHERE\b`，命中则 stderr 警告。可在 `.claude/hooks/` 下实现对应脚本。

## 事务保护

危险操作放入显式事务，便于回滚：

```python
async with in_transaction():
    deleted = await Order.filter(expires_at__lt=cutoff).delete()
    logger.info(f"清理过期 order: {deleted} 行")
    if deleted > 10000:
        raise ApiException(msg="清理异常，回滚")  # 触发回滚
```

## 自检

- [ ] 仓库内所有 `UPDATE` / `DELETE` 都带 `WHERE`？
- [ ] seed / migration 的全量操作有注释说明？
- [ ] 大批量危险操作在事务里？

## 相关

- 父：[`./index.md`](./index.md)

