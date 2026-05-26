---
name: framework-tortoise-index
description: Tortoise ORM 使用约定索引（model 类模板 / 事务上下文管理）
parent: ../index.md
children:
  - { name: model-class-pattern, path: model-class-pattern.md, tag: leaf, note: Model 类骨架 + Meta + 关系字段写法 }
  - { name: transaction-context, path: transaction-context.md, tag: leaf, note: in_transaction async with 上下文 + 嵌套规则 }
when_to_descend: |
  写 / 改 `backend/**/*.py` 中涉及 Tortoise Model 子类、事务包裹、关系字段（FK / M2M）的代码。
---

# Tortoise ORM · 使用约定

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| model-class-pattern | 叶子 | Model 子类骨架，Meta 表名 / 关系字段 / 默认值 |
| transaction-context | 叶子 | `in_transaction()` 上下文管理 + 嵌套行为 |

## 何时下钻

- 新建 Model 子类 → `model-class-pattern.md`
- 涉及多表写入 / 需要回滚保证 → `transaction-context.md`

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../fastapi/index.md`](../fastapi/index.md)
