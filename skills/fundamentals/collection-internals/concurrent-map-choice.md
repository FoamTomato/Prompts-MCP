---
name: collection-internals-concurrent-map-choice
description: 并发 Map 三选一原理 — ConcurrentHashMap（CAS+桶级锁）吞吐远高于全表锁的 Collections.synchronizedMap 和已过时的 Hashtable。Use when 多线程共享 Map / 选并发容器 / 评审 Hashtable 遗留时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 并发 Map 选型
  - ConcurrentHashMap
  - synchronizedMap
  - Hashtable
  - 分段锁
  - CAS
effort: high
context: inline
version: '1.0'
---
# Java · 并发 Map 选型（原理指导）

> 本条只回答「多线程共享 Map 选哪个、为什么」。HashMap 容量预设见 [`hashmap-sizing.md`](./hashmap-sizing.md)；并发集合的整体用法（含 CopyOnWriteArrayList、复合操作原子性）见 [`lang/java/collections/concurrent-collections.md`](../../lang/java/collections/concurrent-collections.md)。

## 原理 → 为什么选 ConcurrentHashMap

三者都线程安全，差别在**锁的粒度**：

| 实现 | 锁机制 | 并发吞吐 | 结论 |
|------|--------|---------|------|
| `ConcurrentHashMap` | JDK8 起：CAS 写空桶 + 仅锁单个桶头（`synchronized`），读基本无锁 | 高，不同桶并发写互不阻塞 | **并发首选** |
| `Collections.synchronizedMap` | 一把全表锁包住每个方法 | 低，任意两操作都串行 | 仅极简/低并发遗留可接受 |
| `Hashtable` | 每个方法 `synchronized`，全表锁 | 低，且 API 老旧 | **已过时，新代码禁用** |

关键点：JDK8 的 ConcurrentHashMap 已抛弃 JDK7 的 Segment 分段锁，改为「CAS + 桶级 synchronized」，锁粒度细到单个桶，所以高并发下吞吐碾压另外两个全表锁方案。

## 规则

- 多线程共享读写的 Map → 直接 `ConcurrentHashMap`。
- 复合操作（先查后写）用原子方法 `computeIfAbsent` / `merge`，**不要**拆成 `get` + `put`（不原子）。
- key / value 均不可为 null（与 HashMap 不同），需要 null 语义时用哨兵值或 Optional。
- 不要用 `Hashtable`；`synchronizedMap` 仅在确认低并发、且能接受遍历时手动 `synchronized(map)` 的遗留场景保留。

## 正例

```java
// ✅ 并发计数 / 缓存：ConcurrentHashMap + 原子复合操作
ConcurrentHashMap<String, Long> counter = new ConcurrentHashMap<>();
counter.merge(key, 1L, Long::sum);              // 原子累加
counter.computeIfAbsent(key, this::loadOnce);   // 原子初始化，只 load 一次
```

## 反例

```java
// ❌ 新代码还用 Hashtable —— 全表锁、API 过时
Map<String, Long> m = new Hashtable<>();

// ❌ ConcurrentHashMap 上 check-then-act 不原子，两线程可能都进来
if (!map.containsKey(k)) {
    map.put(k, init());     // 用 computeIfAbsent 替代
}

// ❌ 高并发还用 synchronizedMap —— 一把大锁，操作全串行
Map<String, Long> m = Collections.synchronizedMap(new HashMap<>());
```

理由：ConcurrentHashMap 单方法原子但 check-then-act 复合操作不原子，必须用 `merge`/`computeIfAbsent`；Hashtable/synchronizedMap 的全表锁在并发下让所有操作排队，吞吐受单锁瓶颈。

## 自检

- [ ] 多线程共享的 Map 用了 `ConcurrentHashMap`，没有 `Hashtable`？
- [ ] 复合操作用 `computeIfAbsent` / `merge`，没拆成 `get` 再 `put`？
- [ ] 没有给 ConcurrentHashMap 存 null key / value？
- [ ] `synchronizedMap` 只出现在确认低并发的遗留代码里？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`hashmap-sizing.md`](./hashmap-sizing.md)（单线程下的容量预设）
- 兄弟：[`treeify-and-loadfactor.md`](./treeify-and-loadfactor.md)（桶内链表转树机制）
- 选型用法：[`lang/java/collections/concurrent-collections.md`](../../lang/java/collections/concurrent-collections.md)
