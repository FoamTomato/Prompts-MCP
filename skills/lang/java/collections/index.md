---
name: lang-java-collections-index
description: Java 集合四件事 — 容器选型 / Stream 用法 / 不可变集合 / 并发集合。Use when 选 List、Set、Map 实现 / 写 Stream 链 / 暴露只读集合 / 在多线程下共享集合时。
parent: ../index.md
children:
  - { name: collection-choice, path: collection-choice.md, tag: skill, note: ArrayList/HashMap/TreeMap 等实现选型与初始容量 }
  - { name: stream-api, path: stream-api.md, tag: skill, note: Stream collect/map/filter 用法、并行流与 toMap 重复 key }
  - { name: immutable-collections, path: immutable-collections.md, tag: skill, note: List.of/unmodifiableList、防御性拷贝、Arrays.asList 坑 }
  - { name: concurrent-collections, path: concurrent-collections.md, tag: skill, note: ConcurrentHashMap/CopyOnWriteArrayList 适用场景 }
when_to_descend: 写 / 改 / 评审任何用到 List、Set、Map、Stream 的 Java 代码
---

# Collections · 子项索引

集合拆成四个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 决定该用 ArrayList/LinkedList、HashMap/TreeMap、HashSet/TreeSet 哪个实现，怎么预估初始容量 | [collection-choice](collection-choice.md) |
| 写 Stream 链（map/filter/collect），纠结 peek、并行流、toMap 重复 key 怎么办 | [stream-api](stream-api.md) |
| 要返回 / 暴露一个不让外部改的集合，或防御外部传入的集合 | [immutable-collections](immutable-collections.md) |
| 集合要在多个线程间共享读写 | [concurrent-collections](concurrent-collections.md) |
