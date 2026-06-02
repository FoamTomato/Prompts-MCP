---
name: lang-java-error-handling-index
description: Java 异常处理三件事 — 抛哪一类（checked vs runtime）/ catch 到怎么办 / 资源怎么释放。Use when 写 Java try-catch / 设计异常类型 / 评审异常与资源处理的 PR 时。
parent: ../index.md
children:
  - { name: checked-vs-runtime, path: checked-vs-runtime.md, tag: skill, note: 该抛 Checked 还是 Runtime 的选型边界 }
  - { name: catch-block-rules, path: catch-block-rules.md, tag: skill, note: catch 到之后：禁吞、log+重抛、包装保留 cause }
  - { name: resource-management, path: resource-management.md, tag: skill, note: AutoCloseable 资源必用 try-with-resources }
when_to_descend: Spring 服务里写 / 评审异常处理与资源释放
---

# Exception · 子项索引

异常处理拆成三个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 决定一个失败该抛 Checked 还是 RuntimeException | [checked-vs-runtime](checked-vs-runtime.md) |
| 已经 catch 到异常，纠结怎么处理（能不能 return null / 怎么重抛） | [catch-block-rules](catch-block-rules.md) |
| 用到流 / 连接 / 锁等需要关闭的资源 | [resource-management](resource-management.md) |
