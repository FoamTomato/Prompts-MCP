---
name: lang-java-naming-index
description: Java 命名五件事 — 类 / 方法 / 变量字段 / 常量 / 包，各自的大小写与措辞约定。Use when 写 Java 代码 / 起名 / 评审命名风格的 PR 时。
parent: ../index.md
children:
  - { name: class-naming, path: class-naming.md, tag: skill, note: PascalCase + 后缀 Service/Repository/Controller }
  - { name: method-naming, path: method-naming.md, tag: skill, note: 动词开头，boolean 用 is/has/can，禁缩写 }
  - { name: variable-naming, path: variable-naming.md, tag: skill, note: camelCase，集合用复数，单字母仅限循环 }
  - { name: constant-naming, path: constant-naming.md, tag: skill, note: UPPER_SNAKE_CASE + static final，组值优先 enum }
  - { name: package-naming, path: package-naming.md, tag: skill, note: 全小写反域名，按业务分包优先于按技术 }
when_to_descend: 写 / 评审 Java 代码涉及任何标识符命名
---

# Naming · 子项索引

命名拆成五个**独立决策点**，按你正在给什么起名下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 给类 / 接口 / 异常 / 枚举起名（PascalCase + 后缀） | [class-naming](class-naming.md) |
| 给方法起名（动词开头 / boolean 前缀 / getter setter） | [method-naming](method-naming.md) |
| 给局部变量或字段起名（camelCase / 集合复数 / 单字母） | [variable-naming](variable-naming.md) |
| 给常量起名，或纠结一组 int 常量该不该改枚举 | [constant-naming](constant-naming.md) |
| 给 package 起名，或纠结按业务还是按技术分包 | [package-naming](package-naming.md) |
