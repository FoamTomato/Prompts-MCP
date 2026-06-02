---
name: collection-internals-hashmap-sizing
description: HashMap 为何要预设初始容量 — 默认 16 装大量元素会反复扩容 rehash，已知大小时 new HashMap(expectedSize/0.75f+1)。Use when new 大 HashMap / 已知元素数 / 关心扩容 rehash 开销时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - HashMap 初始容量
  - 扩容 rehash
  - initialCapacity
  - 预设容量
  - resize
  - load factor
effort: medium
context: inline
version: '1.0'
---
# Java · HashMap 初始容量预设

> 本条只回答「new HashMap 时该不该、该怎么传初始容量」。链表/红黑树阈值与负载因子取舍见 [`treeify-and-loadfactor.md`](./treeify-and-loadfactor.md)；并发下用哪个 Map 见 [`concurrent-map-choice.md`](./concurrent-map-choice.md)。

## 原理 → 为什么要预设

HashMap 默认容量 16、负载因子 0.75，即放到第 13 个元素就触发扩容。扩容把底层数组翻倍并**逐个 rehash 重新分桶**——这是 O(n) 操作。从 16 装到 1 万个元素，会经历约 10 次扩容（16→32→…→16384），rehash 反复搬运，既慢又制造 GC 垃圾。已知大小却不预设 = 白白付这笔扩容税。

## 规则

| 情况 | 怎么做 |
|------|--------|
| 已知会放约 `n` 个元素 | `new HashMap<>((int)(n / 0.75f) + 1)`，让目标容量一次到位 |
| 来源是另一个集合 | `new HashMap<>(src.size() ... )` 或 `new HashMap<>(srcMap)`（构造器内部已按 size 算容量） |
| 大小未知 / 很小（几个） | 用默认 `new HashMap<>()`，预设无意义 |

注意：传进去的是 **expectedSize/0.75**，不是直接传 expectedSize——直接传 n 会在 0.75n 处就扩容，等于没省。HashMap 会把传入值向上取到最近的 2 的幂作为真实容量。

## 正例

```java
// ✅ 已知约 1000 条，容量一次到位，零扩容
Map<Long, User> cache = new HashMap<>((int) (1000 / 0.75f) + 1);

// ✅ 从已有集合构建，直接用拷贝构造器，内部已算好容量
Map<Long, User> copy = new HashMap<>(source);

// ✅ JDK19+ 工具方法，语义更清晰（等价于上面的公式）
Map<Long, User> cache2 = HashMap.newHashMap(1000);
```

## 反例

```java
// ❌ 默认 16 装 1 万条 —— 约 10 次扩容，每次全量 rehash
Map<Long, User> cache = new HashMap<>();
for (User u : tenThousandUsers) cache.put(u.getId(), u);

// ❌ 直接把 expectedSize 当容量传 —— 到 0.75*1000=750 处仍会扩容一次
Map<Long, User> cache = new HashMap<>(1000);
```

理由：扩容是数组翻倍 + 全量 rehash 的 O(n) 操作，已知规模时一次性给够容量可彻底避免；漏除 0.75 等于少给四分之一，仍会触发一次扩容。

## 自检

- [ ] 已知大致元素数的 HashMap 预设了初始容量？
- [ ] 容量按 `n / 0.75f + 1` 算（或用 `HashMap.newHashMap(n)`），而非直接传 `n`？
- [ ] 从已有集合构建时优先用拷贝构造器，没手动 put 循环？
- [ ] 大小未知或极小的场景没有为预设而预设？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`treeify-and-loadfactor.md`](./treeify-and-loadfactor.md)（负载因子怎么影响这条公式）
- 兄弟：[`concurrent-map-choice.md`](./concurrent-map-choice.md)（并发场景换 ConcurrentHashMap）
- 选型用法：[`lang/java/collections/collection-choice.md`](../../lang/java/collections/collection-choice.md)
