---
name: fundamentals-collection-internals-index
description: 集合源码原理服务于实践决策 — HashMap 初始容量、并发 Map 选型、红黑树与负载因子。Use when 预估 HashMap 容量 / 选并发 Map / 调负载因子或纠结链表转树时。
parent: ../index.md
children:
  - { name: collection-internals-hashmap-sizing, path: hashmap-sizing.md, tag: skill, note: "已知大小时 new HashMap(n/0.75f+1) 省扩容 rehash" }
  - { name: collection-internals-concurrent-map-choice, path: concurrent-map-choice.md, tag: skill, note: "并发 Map 选 ConcurrentHashMap，不用 Hashtable/synchronizedMap" }
  - { name: collection-internals-treeify-and-loadfactor, path: treeify-and-loadfactor.md, tag: skill, note: "链表>8 且容量>64 转红黑树、负载因子 0.75 取舍" }
when_to_descend: 写 / 调 / 评审用到 HashMap、ConcurrentHashMap 的 Java 代码，需要从源码原理做决策时
---

# Collection Internals · 子项索引

> 内功定位：**原理 → 实践决策**，不是八股背诵。每条都用「源码机制」回答一个「该怎么写代码」的问题。
> 这里讲**为什么这样写**；具体**用哪个集合实现**的选型见 [`lang/java/collections/`](../../lang/java/collections/index.md)，不重复。

按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| new 一个已知大致元素数的 HashMap，想避免它反复扩容 rehash | [hashmap-sizing](hashmap-sizing.md) |
| Map 要在多线程间共享读写，在 ConcurrentHashMap / synchronizedMap / Hashtable 之间选 | [concurrent-map-choice](concurrent-map-choice.md) |
| 纠结负载因子怎么设、链表什么时候转红黑树、为什么有时扩容而不转树 | [treeify-and-loadfactor](treeify-and-loadfactor.md) |
