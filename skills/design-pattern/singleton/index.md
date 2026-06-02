---
name: design-pattern-singleton-index
description: 单例模式 — 线程安全的几种 Java 实现及取舍（枚举 / 静态内部类 / 双重检查锁）。Use when 需要全局唯一实例 / 纠结单例怎么写才线程安全时。
parent: ../index.md
children:
  - { name: singleton-thread-safe, path: thread-safe-singleton.md, tag: skill, note: 枚举/静态内部类/DCL 三种实现对比 }
when_to_descend: 写全局唯一实例、纠结线程安全单例实现时
---

# Singleton · 子项索引

| 你在做什么 | 进哪个 |
|-----------|-------|
| 要写一个线程安全的单例，纠结用枚举还是静态内部类还是双重检查锁 | [thread-safe-singleton](thread-safe-singleton.md) |
