---
name: lang-python-context-managers-index
description: Python 上下文管理与资源规范（with 协议 / ExitStack 动态多资源 / async with 异步资源）。Use when 写或评审 with / 资源释放 / 上下文管理器。
parent: ../index.md
children:
  - { name: py-ctx-contextmanager-protocol, path: contextmanager-protocol.md, tag: skill, note: "__enter__/__exit__ + @contextmanager 生成器写法" }
  - { name: py-ctx-exitstack-suppress, path: exitstack-suppress.md, tag: skill, note: "ExitStack 动态多资源 / suppress / nullcontext / redirect_stdout" }
  - { name: py-ctx-async-context-manager, path: async-context-manager.md, tag: skill, note: "async with / __aenter__/__aexit__ / AsyncExitStack" }
when_to_descend: 写 with / async with / 自定义资源释放 / 评审上下文管理器实现
---

# Python · 上下文管理子项索引

| 你在做什么 | 进哪个 |
|-----------|-------|
| 自己写一个上下文管理器（类实现或 `@contextmanager` 生成器写法），关心异常传播 | [`contextmanager-protocol.md`](./contextmanager-protocol.md) |
| 资源数量运行时才知道、要批量进栈，或要 `suppress` 忽略异常、`nullcontext` 占位、重定向输出 | [`exitstack-suppress.md`](./exitstack-suppress.md) |
| 异步资源用 `async with`，自定义 `__aenter__/__aexit__`，或动态管理多个异步资源 | [`async-context-manager.md`](./async-context-manager.md) |
