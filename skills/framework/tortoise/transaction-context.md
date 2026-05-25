---
name: tortoise-transaction-context
description: in_transaction() 事务上下文 — 跨表写入必用
parent: ./index.md
paths:
  - "backend/services/**/*.py"
  - "py/services/**/*.py"
triggers:
  keywords: [in_transaction, 事务, atomic]
effort: medium
context: inline
version: "1.0"
---

# Tortoise · in_transaction 事务

## 规则

**跨表写入必须包在 `in_transaction()` 上下文内**，确保原子性。

## 标准用法

```python
from tortoise.transactions import in_transaction

async def create_presentation_with_slides(req: PresentationCreateReq, uid: int) -> Presentation:
    async with in_transaction():
        # 1. 创建课件
        presentation = await Presentation.create(
            owner_id=uid,
            title=req.title,
            theme_id=req.theme_id,
        )

        # 2. 批量创建幻灯片
        slides = [
            Slide(presentation_id=presentation.id, order=i, content=c)
            for i, c in enumerate(req.slides)
        ]
        await Slide.bulk_create(slides)

        # 3. 扣减积分
        await Credits.filter(user_id=uid).update(
            base_credits=F("base_credits") - 1,
        )

        return presentation
    # 任何步骤抛异常 → 整个事务回滚
```

## 嵌套事务（Savepoint）

```python
async with in_transaction():
    await create_main()
    try:
        async with in_transaction():     # 子事务用 savepoint
            await create_optional()
    except OptionalError:
        pass     # 子事务回滚，主事务继续
```

## 跨数据库连接

```python
async with in_transaction("readonly_replica"):
    # 在指定连接上的事务
    ...
```

## 何时**不**需要事务

- 单表单条 INSERT / UPDATE / DELETE（自动事务）
- 只读查询
- 跨进程协调（用 Redis 锁，不用 DB 事务）

## 反例

```python
# ❌ 跨表写无事务
await Presentation.create(...)
await Slide.bulk_create(...)   # 如果这里挂，Presentation 已存在但没 Slide，数据不一致

# ❌ 在事务内做长时间 I/O
async with in_transaction():
    p = await Presentation.create(...)
    result = await llm_call(p)     # LLM 调用可能 30s → 长时间持锁
    await Slide.bulk_create(...)

# ✅ 长 I/O 在事务外
result = await llm_call(req)
async with in_transaction():
    p = await Presentation.create(...)
    await Slide.bulk_create(...)
```

## 错误回滚 + 业务异常

```python
async with in_transaction():
    try:
        await deduct_credits(uid, 1)
        result = await call_llm(req)
        await save_result(result)
    except ApiException:
        # ApiException 被 raise → 触发自动回滚
        raise
```

## 自检

- [ ] 跨表写都在 `in_transaction()` 内？
- [ ] 事务内没有长时间 I/O（LLM 调用 / HTTP / 文件 IO）？
- [ ] 事务外的失败有补偿逻辑？
- [ ] 不在事务里做分布式锁（用 Redis）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`model-class-pattern.md`](./model-class-pattern.md)

