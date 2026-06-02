---
name: lang-java-generics-index
description: Java 泛型两件事 — 通配符 PECS（? extends / ? super 怎么选）/ 类型擦除的坑（new T[]、instanceof、重载冲突）。Use when 写 Java 泛型方法 / 设计泛型 API / 排查擦除相关编译错误时。
parent: ../index.md
children:
  - { name: wildcard-pecs, path: wildcard-pecs.md, tag: skill, note: "PECS：生产者 ? extends、消费者 ? super、泛型方法" }
  - { name: type-erasure-pitfalls, path: type-erasure-pitfalls.md, tag: skill, note: "擦除导致 new T[]/instanceof 不能用，靠 Class<T>/TypeReference 传类型" }
when_to_descend: 写 / 评审带泛型的 Java API、容器、工具方法
---

# Generics · 子项索引

泛型拆成两个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 给方法参数 / 返回值选通配符边界（要读还是要写一个集合） | [wildcard-pecs](wildcard-pecs.md) |
| 想 `new T[]` / 对泛型 `instanceof` / 按泛型重载，编译报错或行为诡异 | [type-erasure-pitfalls](type-erasure-pitfalls.md) |
