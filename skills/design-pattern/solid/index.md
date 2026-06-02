---
name: design-pattern-solid-index
description: SOLID 五大面向对象设计原则 — 单一职责 / 开闭 / 里氏替换 / 接口隔离 / 依赖倒置。Use when 设计类与接口职责 / 评审面向对象结构 / 重构臃肿类时。
parent: ../index.md
children:
  - { name: solid-single-responsibility, path: single-responsibility.md, tag: skill, note: 一个类只有一个变化的理由 }
  - { name: solid-open-closed, path: open-closed.md, tag: skill, note: 对扩展开放对修改封闭 }
  - { name: solid-liskov-substitution, path: liskov-substitution.md, tag: skill, note: 子类可无声替换父类 }
  - { name: solid-interface-segregation, path: interface-segregation.md, tag: skill, note: 接口要小而专不要胖 }
  - { name: solid-dependency-inversion, path: dependency-inversion.md, tag: skill, note: 依赖抽象而非实现配合 Spring DI }
when_to_descend: 设计类/接口职责、重构臃肿类、评审面向对象结构时
---

# SOLID · 五大原则索引

按你正在纠结的设计问题下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 一个类越改越大、职责混杂 | [single-responsibility](single-responsibility.md) |
| 加新功能要改大量旧代码 | [open-closed](open-closed.md) |
| 子类继承父类后行为不一致、被迫加 if 判类型 | [liskov-substitution](liskov-substitution.md) |
| 接口太大，实现类被迫实现用不到的方法 | [interface-segregation](interface-segregation.md) |
| 高层模块直接 new 低层实现、难以替换/测试 | [dependency-inversion](dependency-inversion.md) |
