---
name: lang-python-index
description: Python 语言级规则索引 — 命名/数据模型/标准库/迭代器/装饰器/异步/类型/错误/上下文/OOP/测试/打包/工程化/性能/import/style。Use when 写改 .py 文件时。
parent: ../index.md
children:
  - { name: naming, path: naming/index.md, tag: folder, note: 命名规范（function/class/variable/module） }
  - { name: data-model, path: data-model/index.md, tag: folder, note: "数据模型：可变默认参数/is vs ==/拷贝语义/dunder/闭包/GIL-free-threading" }
  - { name: stdlib, path: stdlib/index.md, tag: folder, note: "标准库：collections/itertools/functools/pathlib/dataclasses/enum" }
  - { name: iterators, path: iterators/index.md, tag: folder, note: 迭代器与生成器：惰性求值/协议/yield from/推导式 }
  - { name: decorators, path: decorators/index.md, tag: folder, note: 装饰器：wraps/带参/横切关注点 }
  - { name: async, path: async/index.md, tag: folder, note: 异步规范（asyncio / TaskGroup / 取消 / no-blocking / SSE） }
  - { name: typing, path: typing/index.md, tag: folder, note: 类型注解 / PEP695 泛型 / Protocol / TypedDict / 延迟求值 }
  - { name: error-handling, path: error-handling/index.md, tag: folder, note: ApiException / ExceptionGroup / raise from / EAFP }
  - { name: context-managers, path: context-managers/index.md, tag: folder, note: with 协议 / ExitStack / async with }
  - { name: oop, path: oop/index.md, tag: folder, note: 方法类型/MRO/dataclass vs pydantic/描述符/元类 }
  - { name: testing, path: testing/index.md, tag: folder, note: pytest / fixture / 参数化 / mock / 覆盖率 }
  - { name: packaging, path: packaging/index.md, tag: folder, note: uv / pyproject.toml / lockfile / build-publish }
  - { name: tooling, path: tooling/index.md, tag: folder, note: ruff / 类型检查 CI / pre-commit / 结构化日志 }
  - { name: performance, path: performance/index.md, tag: folder, note: profiling / 缓存 / 进程-线程-async 选型 / 子解释器-JIT }
  - { name: import, path: import/index.md, tag: folder, note: import 顺序 / 绝对导入 / 循环依赖 }
  - { name: style, path: style/index.md, tag: folder, note: 日志规范 / N+1 避免 / 命名清单 }
when_to_descend: |
  写 / 改 .py 文件：backend/ 主后端 / py/ 工作进程 / 任何 Python 模块。
---

# Python · 语言级规则

> 单一职责的叶子文件，由 CLAUDE.md Step 5 按需注入。

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| naming | 文件夹 | 函数 snake_case 动词 / 变量名词 / 模块小写 |
| data-model | 文件夹 | 可变默认参数 / is vs == / 拷贝 / dunder / 闭包 / GIL（6 子项） |
| stdlib | 文件夹 | collections / itertools / functools / pathlib / dataclasses / enum（6 子项） |
| iterators | 文件夹 | 生成器惰性 / 迭代器协议 / yield from / 推导式（4 子项） |
| decorators | 文件夹 | wraps / 带参装饰器 / 横切关注点（3 子项） |
| async | 文件夹 | 全 I/O await / TaskGroup / 取消 / 桥接同步 / SSE（7 子项） |
| typing | 文件夹 | 100% 注解 / PEP695 泛型 / Protocol / TypedDict / 延迟求值（8 子项） |
| error-handling | 文件夹 | ApiException / ExceptionGroup / raise from / EAFP（6 子项） |
| context-managers | 文件夹 | with 协议 / ExitStack / async with（3 子项） |
| oop | 文件夹 | 方法类型 / MRO / dataclass vs pydantic / 描述符 / 元类（5 子项） |
| testing | 文件夹 | pytest / fixture / 参数化 / mock / 异步测试 / 覆盖率（6 子项） |
| packaging | 文件夹 | uv / pyproject.toml / lockfile / build-publish（4 子项） |
| tooling | 文件夹 | ruff / 类型检查 CI / pre-commit / 结构化日志（5 子项） |
| performance | 文件夹 | profiling / 缓存 / 进程-线程-async 选型 / 子解释器-JIT（4 子项） |
| import | 文件夹 | 绝对导入 / 禁循环 / stdlib-third-party-local 三段顺序 |
| style | 文件夹 | 日志规范 / Redis Key 格式 / N+1 防御 |

## 下钻决策表

| 任务 | 选哪几个叶子 |
|------|----------|
| 新增 Service 函数 | naming + async + typing + error-handling/api-exception |
| 写 SSE 流式接口 | async/sse-streaming + error-handling/api-exception |
| 写 Tortoise 查询 | style/no-n-plus-one（→ 同时进 framework/tortoise） |
| 写 Pydantic schema | typing/pydantic-v2-field + oop/dataclass-vs-pydantic |
| 写单元测试 | testing（pytest-structure + fixture-usage + mock-patch） |
| 配 / 改项目依赖与构建 | packaging（uv-workflow + pyproject-toml） |
| 配 lint / 类型检查 / CI | tooling（ruff-lint-format + type-checker-ci + ci-pipeline） |
| 写资源管理（文件/连接/事务） | context-managers + error-handling |
| 处理大数据流 / 省内存 | iterators/generator-lazy + performance |
| 排查性能 / 选并发模型 | performance（profiling + process-vs-thread-vs-async） |
| 用标准库（别造轮子） | stdlib |
| 写装饰器（重试/缓存/计时） | decorators |
| Review 后端代码 | 按改动涉及的子目录下钻 |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行语言：[`../typescript/index.md`](../typescript/index.md) · [`../sql/index.md`](../sql/index.md)
- 关联框架：[`../../framework/fastapi/index.md`](../../framework/fastapi/index.md) · [`../../framework/tortoise/index.md`](../../framework/tortoise/index.md)
