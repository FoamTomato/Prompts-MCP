---
name: python-logger-discipline
description: 日志规范 — 入口出口必打 + 禁 print + 禁敏感信息
parent: ./index.md
paths:
  - "backend/**/*.py"
  - "py/**/*.py"
triggers:
  keywords: [logger, print, 敏感信息, API Key]
effort: medium
context: inline
version: "1.0"
---

# Python · 日志规范

## 规则

| 规则 | 说明 |
|------|------|
| 一个模块一个 logger | `logger = logging.getLogger(__name__)` |
| 关键路径入口/出口必打 | INFO 级，含关键参数 |
| 失败用 `logger.exception` | 等价 `error(..., exc_info=True)` |
| 禁 `print()` | 全部走 logger |
| 禁敏感信息 | 密码 / API Key / Token / 完整 PII |
| 大对象选关键字段 | 不 dump 整个 dict |

## 模板

```python
import logging

logger = logging.getLogger(__name__)

async def service_create_presentation(req, user_id):
    logger.info(
        f"创建课件开始 - user_id={user_id}, title={req.title}, "
        f"slide_count={req.slide_count}"
    )

    try:
        result = await build_presentation(req, user_id)
        logger.info(
            f"创建课件完成 - user_id={user_id}, presentation_id={result.id}, "
            f"duration={result.elapsed:.2f}s"
        )
        return result

    except ApiException as e:
        logger.warning(f"创建课件失败（业务）- user_id={user_id}, msg={e.msg}")
        raise

    except Exception as e:
        logger.exception(f"创建课件失败（未知）- user_id={user_id}: {e}")
        raise ApiException(msg="创建失败，请重试")
```

## 级别使用决策

| 级别 | 用途 |
|------|------|
| `DEBUG` | 仅开发，CI 关闭 |
| `INFO` | 业务入口/出口、关键决策点 |
| `WARNING` | 降级 / 重试 / 业务异常 |
| `ERROR` | 未知异常（必带 exc_info） |
| `CRITICAL` | 系统级故障（DB 挂、Redis 挂） |

## 反例

```python
# ❌ print
print(f"user logged in: {user.id}")

# ❌ 敏感信息
logger.info(f"login attempt: email={email}, password={pwd}")

# ❌ 大对象
logger.info(f"created: {full_object_dict}")   # → 关键字段只 log id/title

# ❌ 不可定位
logger.error("failed")   # → 没有 user_id / request_id 等上下文，无法排查

# ❌ ERROR 不带 exc_info
logger.error(f"failed: {e}")
```

## 配置

`core/logger.py`：

```python
import logging
import sys

FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] [%(request_id)s] %(message)s"

def setup_logging(level: str = "INFO"):
    logging.basicConfig(
        level=level,
        format=FORMAT,
        stream=sys.stdout,
    )
    # 过滤第三方 noisy logger
    logging.getLogger("tortoise.db_client").setLevel(logging.WARNING)
```

## 自检

- [ ] 模块顶部有 `logger = logging.getLogger(__name__)`？
- [ ] 业务入口/出口有 INFO 日志？
- [ ] 失败用 `logger.exception` 或 `logger.error(..., exc_info=True)`？
- [ ] 无 `print()`？
- [ ] 无敏感信息泄漏？
- [ ] 关键日志包含 user_id / resource_id 等上下文？

## 相关

- 父：[`./index.md`](./index.md)
- 配套：[`../error-handling/logger-exc-info.md`](../error-handling/logger-exc-info.md)

