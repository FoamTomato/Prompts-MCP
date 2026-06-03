---
name: py-structured-logging-config
description: structlog + pydantic-settings 结构化日志初始化与环境变量配置。Use when 初始化日志 / 配 structlog processor / 用 env 管理日志级别与 JSON 输出。
parent: ./index.md
paths:
- backend/**/*.py
- py/**/*.py
triggers:
  keywords:
  - 结构化日志
  - structlog
  - pydantic-settings
  - 日志配置
  - JSON 日志
effort: medium
context: inline
version: '1.0'
---
# Python · 结构化日志初始化与配置

> 这条只管**初始化与配置**（structlog processor 链、用 env 注入级别/格式）。
> 什么时候打、打哪一级、禁 print/禁敏感信息见 [`../style/logger-discipline.md`](../style/logger-discipline.md)。

## 规则

| 规则 | 说明 |
|------|------|
| 用 structlog 出结构化事件 | key=value / JSON，机器可解析，胜过裸字符串 |
| 配置集中一处初始化 | 进程启动时调一次 `configure()`，不分散各模块 |
| 级别/格式走环境变量 | 用 pydantic-settings 读 env，不硬编码 |
| 开发用 Console，生产用 JSON | 由 settings 切换 renderer |
| 绑上下文用 `bind_logger` | request_id / user_id 用 contextvars 绑定，自动带入每条 |
| 桥接标准库 logging | 第三方库走 stdlib，统一交给 structlog 渲染 |

## 正例

`config.py`（pydantic-settings 管配置）：

```python
from pydantic_settings import BaseSettings

class LogSettings(BaseSettings):
    log_level: str = "INFO"
    log_json: bool = False          # 生产置 True
    model_config = {"env_prefix": "APP_"}   # 读 APP_LOG_LEVEL 等

settings = LogSettings()
```

`logging_setup.py`（初始化一次）：

```python
import logging
import structlog
from config import settings

def configure_logging() -> None:
    renderer = (
        structlog.processors.JSONRenderer()
        if settings.log_json
        else structlog.dev.ConsoleRenderer()
    )
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,  # 带入 request_id 等
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.getLevelName(settings.log_level)
        ),
    )

log = structlog.get_logger()
log.info("server_started", port=8000)   # → 结构化事件
```

绑定请求级上下文：

```python
structlog.contextvars.bind_contextvars(request_id=rid, user_id=uid)
# 之后这个请求内所有 log 自动带 request_id / user_id
```

## 反例

```python
# ❌ 每个模块各自 configure，行为不一致
structlog.configure(...)   # 散落在多个文件 → 只在启动入口调一次

# ❌ 级别硬编码，无法按环境调
structlog.make_filtering_bound_logger(logging.DEBUG)  # 应读 settings

# ❌ 拼字符串，丢失结构化优势
log.info(f"user {uid} did {action}")  # → log.info("user_action", user_id=uid, action=action)
```

## 自检

- [ ] 进程启动入口只调一次 `configure_logging()`？
- [ ] 日志级别 / JSON 开关来自 pydantic-settings + env，没硬编码？
- [ ] 生产用 JSONRenderer，开发用 ConsoleRenderer？
- [ ] 用 `merge_contextvars` + `bind_contextvars` 带 request_id / user_id？
- [ ] 事件用 key=value（`log.info("event", k=v)`），没拼字符串？
- [ ] 打什么/打哪级的纪律另见 logger-discipline？

## 相关

- 父：[`./index.md`](./index.md)
- 互补（打什么/哪级/禁项）：[`../style/logger-discipline.md`](../style/logger-discipline.md)
- 兄弟：[`ci-pipeline.md`](./ci-pipeline.md) · [`pre-commit-hooks.md`](./pre-commit-hooks.md)
