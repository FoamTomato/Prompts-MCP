---
name: lang-python-iterators-index
description: Python 迭代器与生成器规范（生成器惰性 / 迭代器协议 / yield from 委托 / 推导式风格）。Use when 写生成器 / 实现可迭代对象 / 选推导式还是生成器。
parent: ../index.md
children:
  - { name: py-generator-lazy, path: generator-lazy.md, tag: skill, note: 生成器惰性求值 / 流式降内存 }
  - { name: py-iterator-protocol, path: iterator-protocol.md, tag: skill, note: "__iter__ / __next__ / StopIteration" }
  - { name: py-yield-from-delegation, path: yield-from-delegation.md, tag: skill, note: yield from 委托子生成器 }
  - { name: py-comprehension-style, path: comprehension-style.md, tag: skill, note: 推导式 / 海象 / 推导 vs 生成器选型 }
when_to_descend: 写生成器函数 / 实现可迭代类 / 拆分大集合处理 / 选推导式还是生成器。
---

# Python · 迭代器与生成器 · 子项索引

| 你在做什么 | 进哪个 |
|------------|--------|
| 处理大数据流 / 想边产边消降内存 | [`generator-lazy.md`](./generator-lazy.md) |
| 让自定义类支持 `for` 循环 | [`iterator-protocol.md`](./iterator-protocol.md) |
| 一个生成器要转发另一个生成器 | [`yield-from-delegation.md`](./yield-from-delegation.md) |
| 写列表/字典/集合推导，纠结要不要用生成器 | [`comprehension-style.md`](./comprehension-style.md) |
