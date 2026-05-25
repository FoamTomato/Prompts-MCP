---
name: lang-python-index
description: Python 语言级规则索引（命名 / async / import / typing / error-handling / style）
parent: ../index.md
children:
  - { name: naming, path: naming/index.md, tag: folder, note: 命名规范（function/class/variable/module） }
  - { name: async, path: async/index.md, tag: folder, note: 异步规范（asyncio / no-blocking / SSE） }
  - { name: import, path: import/index.md, tag: folder, note: import 顺序 / 绝对导入 / 循环依赖 }
  - { name: typing, path: typing/index.md, tag: folder, note: 100% 类型注解 / 禁 Any / Pydantic v2 }
  - { name: error-handling, path: error-handling/index.md, tag: folder, note: ApiException / logger exc_info / 禁裸 except }
  - { name: style, path: style/index.md, tag: folder, note: 日志规范 / N+1 避免 / 命名清单 }
when_to_descend: |
  写 / 改 .py 文件：backend/ 主后端 / py/ 工作进程 / 任何 Python 模块。
---

# Python · 语言级规则

> 单一职责的叶子文件，由 CLAUDE.md Step 5 按需注入。
> 历史源（已迁移并删除）：原 py/python_async_service 单文件 676 行 → 拆分到本树各叶子。

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| naming | 文件夹 | 函数 snake_case 动词 / 变量名词 / 模块小写 |
| async | 文件夹 | 全 I/O await / 禁 time.sleep+requests / SSE 模板 |
| import | 文件夹 | 绝对导入 / 禁循环 / stdlib-third-party-local 三段顺序 |
| typing | 文件夹 | 函数签名 100% 注解 / Pydantic Field description 必填 |
| error-handling | 文件夹 | ApiException + logger.error(exc_info=True) 三件套 |
| style | 文件夹 | 日志规范 / Redis Key 格式 / N+1 防御 |

## 下钻决策表

| 任务 | 选哪几个叶子 |
|------|----------|
| 新增 Service 函数 | naming + async + typing + error-handling/api-exception |
| 写 SSE 流式接口 | async/sse-streaming + error-handling/api-exception |
| 写 Tortoise 查询 | style/no-n-plus-one（→ 同时进 framework/tortoise） |
| 写 Pydantic schema | typing/pydantic-v2-field |
| Review 后端代码 | 全部 6 个子目录都看一眼 |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行语言：[`../typescript/index.md`](../typescript/index.md) · [`../sql/index.md`](../sql/index.md)
- 关联框架：[`../../framework/fastapi/index.md`](../../framework/fastapi/index.md) · [`../../framework/tortoise/index.md`](../../framework/tortoise/index.md)
