---
name: python-logger-exc-info
description: logger.error(..., exc_info=True) 必带 traceback。Use when 写 Python 后端代码
  / 评审涉及 `logger-exc-info` 的 PR。
parent: ./index.md
paths:
- backend/**/*.py
- py/**/*.py
triggers:
  keywords:
  - logger
  - logging
  - exc_info
  - traceback
  - 必带
effort: medium
context: inline
version: '1.0'
---
# Python · logger.error 必带 exc_info

## 规则

记录 ERROR 级别日志时**必须传 `exc_info=True`** 才会带上完整 traceback。否则只看到一行错误描述，排查时 grep 不到调用栈。

```python
import logging

logger = logging.getLogger(__name__)

try:
    result = await call_external_api(params)
except Exception as e:
    logger.error(
        f"外部 API 失败 - service=textbook, params={params}: {e}",
        exc_info=True,   # ← 必须
    )
    raise ApiException(msg="服务繁忙")
```

## 日志层级对照

| 级别 | 用法 | 是否带 exc_info |
|------|------|---------------|
| `logger.info(...)` | 入口 / 出口 / 关键决策 | 否 |
| `logger.warning(...)` | 降级 / 重试 / 非致命异常 | 视情况 |
| `logger.error(...)` | 异常 / 失败 | **总是 True** |
| `logger.exception(...)` | == `error(..., exc_info=True)` 的简写 | 自动 |

推荐用 `logger.exception(msg)`：

```python
except Exception as e:
    logger.exception(f"外部 API 失败 - service=textbook: {e}")
    raise ApiException(msg="服务繁忙")
```

## 日志格式约定

```
[<时间>] [<level>] [<module>:<line>] [<request_id>] <message>
```

`<request_id>` 由 `middleware/request_id.py` 注入到 logging context。

## 不要记录的

```python
# ❌ 敏感信息
logger.info(f"login: pwd={password}")
logger.error(f"api key: {settings.openai_api_key}")

# ❌ 大对象全量
logger.info(f"data: {large_dict}")  # 截断或选关键字段
```

## 自检

- [ ] `logger.error` 全部带 `exc_info=True`（或改用 `logger.exception`）？
- [ ] 不记录密码 / API Key / Token？
- [ ] 大对象只 log 关键字段？
- [ ] 错误日志含可定位的上下文（user_id、resource_id 等）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`api-exception.md`](./api-exception.md)
- 配套：[`../style/logger-discipline.md`](../style/logger-discipline.md)

