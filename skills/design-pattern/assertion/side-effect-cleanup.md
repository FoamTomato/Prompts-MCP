---
name: assertion-side-effect-cleanup
description: 与 ApiException 三件套配合的边界 try/except — 何时需要捕获 ApiException 做副作用清理。Use when
  写 Python 后端代码 / 评审涉及 `side-effect-cleanup` 的 PR。
parent: ./index.md
paths:
- py/services/**/*.py
- backend/services/**/*.py
triggers:
  keywords:
  - try
  - except
  - ApiException
  - 副作用
  - 清理
  - finally
  - 状态更新
effort: medium
context: inline
version: '1.0'
---
# Assertion · 边界处理模式

## 默认：不捕获 ApiException

业务断言抛出 ApiException 后，**默认让其向上冒泡到 FastAPI exception_handler**。
业务层**不要**写：

```python
# ❌ 业务层不需要捕获自己抛的 ApiException
try:
    OutlineAsserts.title_not_blank(req.title)
except ApiException:
    raise  # 多此一举
```

## 例外：有副作用需要清理时

当断言失败前已经做了**有持久化副作用的操作**（如创建 DB 记录、扣减积分），失败时需要**先清理再透传**。

### 典型场景：pipeline 已建 doc 记录

```python
# py/services/knowledge/pipeline.py
async def process_local_file(knowledge_base_id, file_name):
    # 1. 入口断言（失败时 doc 尚未建，无需清理）
    file_path = _resolve_file_path(file_name)
    KnowledgeAsserts.source_file_exists(file_path)

    # 2. 已有副作用：建 doc 记录 status=processing
    doc = await KnowledgeDocument.create(
        knowledge_base_id=knowledge_base_id,
        file_name=file_name,
        status="processing",
    )

    try:
        # 3. 后续断言失败 → 需要把 doc 标 failed 再透传
        lc_docs = load_pdf(file_path)
        KnowledgeAsserts.pdf_text_extracted(lc_docs)

        chunked = process_documents(lc_docs)
        KnowledgeAsserts.chunks_non_empty(chunked)

        # ... 正常流程
        return result

    except ApiException as e:
        # 业务断言失败：先清理副作用再透传（不二次包装）
        await KnowledgeDocument.filter(id=doc.id).update(
            status="failed",
            error_message=e.error_message,
        )
        raise

    except Exception as e:
        # 未知异常：标记 failed 后让 global handler 兜底 X009
        logger.error(f"[Pipeline] 处理失败: {e}", exc_info=True)
        await KnowledgeDocument.filter(id=doc.id).update(
            status="failed",
            error_message=str(e),
        )
        raise
```

## 关键设计

| 段 | 行为 |
|----|------|
| 入口断言（无副作用前） | 直接断言，失败让其向上冒泡 |
| 副作用之后的断言 | `except ApiException` 清理副作用 + `raise` 透传（不二次包装） |
| 未知异常 | `except Exception` 清理副作用 + `logger.exception` + `raise` 让 X009 兜底 |

## 反模式

```python
# ❌ 反例 1：二次包装 ApiException
except ApiException as e:
    raise ApiException("X009", e.error_message)  # 丢失原始 code

# ❌ 反例 2：catch ApiException 后吞掉
except ApiException:
    return None  # 调用方以为成功

# ❌ 反例 3：catch 后转 ValueError
except ApiException as e:
    raise ValueError(e.error_message)  # 类型降级

# ❌ 反例 4：用 finally 做清理（清理逻辑会在正常路径也执行）
try:
    KnowledgeAsserts.pdf_text_extracted(lc_docs)
    return success(...)
finally:
    await KnowledgeDocument.filter(id=doc.id).update(status="failed")
    # 正常成功路径也会被标记 failed
```

## 配合积分扣减场景

```python
async def deduct_and_generate(uid, cost):
    # 1. 业务前置：先扣积分（持久化副作用）
    await deduct_credits(uid, cost)

    try:
        # 2. 调用 LLM（业务断言可能失败）
        result = await call_llm(req)
        OutlineAsserts.slides_min_count(result.slides)
        return result

    except ApiException:
        # 退还积分后透传
        await refund_credits(uid, cost)
        raise

    except Exception as e:
        # 退还积分 + 让 X009 兜底
        await refund_credits(uid, cost)
        logger.exception(f"LLM 失败 uid={uid}: {e}")
        raise
```

## 自检

- [ ] 默认不捕获自己抛的 ApiException？
- [ ] 有副作用清理时：先清理再 `raise`，不二次包装？
- [ ] `except Exception` 必带 `exc_info=True` 或 `logger.exception`？
- [ ] 没有用 `finally` 做"仅失败时执行"的清理？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`principle.md`](./principle.md) · [`asserts-class.md`](./asserts-class.md)
- 配套：[`../../lang/python/error-handling/api-exception.md`](../../lang/python/error-handling/api-exception.md) · [`../../lang/python/error-handling/no-bare-except.md`](../../lang/python/error-handling/no-bare-except.md)
- 实战代码：`py/services/knowledge/pipeline.py`
