---
name: sql-must-have-where
description: UPDATE / DELETE 必须带 WHERE 子句
parent: ./index.md
paths:
  - "py/**/*.py"
  - "backend/**/*.py"
  - "**/*.sql"
triggers:
  keywords: [UPDATE, DELETE, WHERE]
effort: medium
context: inline
version: "1.0"
---

# SQL · UPDATE/DELETE 必带 WHERE

## 规则

**`UPDATE` / `DELETE` 必须带 `WHERE` 子句**，无 WHERE 等于全表操作，几乎必然是事故。

## 反例 → 正例

```sql
-- ❌ 没 WHERE，全表清空
DELETE FROM sessions;

-- ✅ 限定条件
DELETE FROM sessions
WHERE expires_at < NOW() - INTERVAL 90 DAY;

-- ❌ 全表 UPDATE
UPDATE presentations SET theme_id = 'default';

-- ✅
UPDATE presentations SET theme_id = 'default'
WHERE theme_id IS NULL;
```

## Tortoise ORM 等价

```python
# ❌ 全表
await Presentation.all().delete()
await Presentation.all().update(theme_id="default")

# ✅
await Presentation.filter(expires_at__lt=cutoff).delete()
await Presentation.filter(theme_id=None).update(theme_id="default")
```

## 唯一例外：seed / data migration 全量重置

明确意图的"清空表"场景：

```python
# scripts/seed_textbooks.py
async def reset_and_seed():
    # 清空并重新插入: 仅在 seed 脚本允许, 注释必须说明
    await Textbook.all().delete()   # 注释说明意图（清空并重新插入）
    await Textbook.bulk_create(SEED_DATA)
```

## CI / hook 兜底

PostToolUse hook 可加正则检测 `\b(UPDATE|DELETE)\b` 后无 `\bWHERE\b`，命中则 stderr 警告。详见 `.claude/hooks/quill-post-tool.sh`。

## 事务保护

危险操作放入显式事务，便于回滚：

```python
async with in_transaction():
    deleted = await Session.filter(expires_at__lt=cutoff).delete()
    logger.info(f"清理过期 session: {deleted} 行")
    if deleted > 10000:
        raise ApiException(msg="清理异常，回滚")  # 触发回滚
```

## 自检

- [ ] 仓库内所有 `UPDATE` / `DELETE` 都带 `WHERE`？
- [ ] seed / migration 的全量操作有注释说明？
- [ ] 大批量危险操作在事务里？

## 相关

- 父：[`./index.md`](./index.md)

