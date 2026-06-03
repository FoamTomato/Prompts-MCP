---
name: lang-python-decorators-index
description: Python 装饰器规范（functools.wraps 包裹 / 带参三层嵌套 / 横切关注点实战）。Use when 写或评审 Python 装饰器。
parent: ../index.md
children:
  - { name: py-decorator-basics, path: decorator-basics.md, tag: skill, note: "闭包包裹 + 必加 functools.wraps" }
  - { name: py-decorator-parametrized, path: parametrized-decorator.md, tag: skill, note: "带参三层嵌套 / 类装饰器 / 叠加顺序" }
  - { name: py-decorator-cross-cutting, path: cross-cutting-patterns.md, tag: skill, note: "重试 / 限流 / 计时 / 缓存横切关注点" }
when_to_descend: 写 @decorator / 给函数加横切逻辑（重试/限流/计时/缓存）/ 评审装饰器实现
---

# Python · 装饰器子项索引

| 你在做什么 | 进哪个 |
|-----------|-------|
| 第一次写装饰器，函数 `__name__` / 文档串丢了 | [`decorator-basics.md`](./decorator-basics.md) |
| 装饰器要接收参数（`@retry(times=3)`），或用类实现，或多个叠加 | [`parametrized-decorator.md`](./parametrized-decorator.md) |
| 给函数加重试 / 限流 / 计时 / 缓存等横切逻辑 | [`cross-cutting-patterns.md`](./cross-cutting-patterns.md) |
