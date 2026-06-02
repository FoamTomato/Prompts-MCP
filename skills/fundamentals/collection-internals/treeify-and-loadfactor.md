---
name: collection-internals-treeify-and-loadfactor
description: HashMap 链表何时转红黑树（链表>8 且数组容量≥64，否则先扩容）与负载因子 0.75 的时间/空间取舍。Use when 调负载因子 / 排查桶内退化 / 理解 treeify 触发条件时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 红黑树转换
  - treeify
  - 负载因子
  - load factor
  - 链表转树
  - TREEIFY_THRESHOLD
effort: medium
context: inline
version: '1.0'
---
# Java · 链表转红黑树与负载因子取舍

> 本条只回答「treeify 触发条件 + 负载因子怎么取舍」。容量预设公式见 [`hashmap-sizing.md`](./hashmap-sizing.md)；并发 Map 选型见 [`concurrent-map-choice.md`](./concurrent-map-choice.md)。

## 原理 → treeify 的两个阈值

JDK8 起 HashMap 桶内冲突的元素超过阈值会从链表转红黑树，把单桶查找从 O(n) 降到 O(log n)。但**链表长度超 8 不一定转树**，要同时满足两个条件：

| 常量 | 值 | 含义 |
|------|----|------|
| `TREEIFY_THRESHOLD` | 8 | 单桶链表长度 > 8 才考虑转树 |
| `MIN_TREEIFY_CAPACITY` | 64 | 数组容量 ≥ 64 才真转树 |
| `UNTREEIFY_THRESHOLD` | 6 | 树节点 ≤ 6 时退回链表 |

关键决策点：链表 > 8 **但容量 < 64** 时，HashMap **选择扩容而非转树**——因为容量小时冲突往往是桶太少导致，扩容重新分桶比建红黑树更划算。所以小表里看到长链表，先想到的是「容量不够」（回到 [`hashmap-sizing.md`](./hashmap-sizing.md)），而非「该转树了」。

## 负载因子 0.75 的取舍

负载因子 = 元素数 / 容量，达到它就扩容。默认 0.75 是**时间与空间的折中**：

| 负载因子 | 后果 | 适合 |
|---------|------|------|
| 调高（如 1.0） | 省内存，但冲突变多、链表变长、查找变慢 | 内存极紧、查询少 |
| 调低（如 0.5） | 冲突少查得快，但浪费近一半空间、扩容更频繁 | 查询极频、内存富裕 |
| **默认 0.75** | 泊松分布下单桶冲突概率低，时空均衡 | 绝大多数场景，**不要乱改** |

## 正例

```java
// ✅ 绝大多数场景：用默认负载因子，只调初始容量
Map<Long, User> cache = new HashMap<>((int) (1000 / 0.75f) + 1);
```

## 反例

```java
// ❌ 为"省内存"把负载因子拉到 1.0 —— 冲突剧增，桶内退化成长链表
Map<Long, User> m = new HashMap<>(16, 1.0f);

// ❌ 以为"插到第 9 个就有红黑树" —— 容量没到 64，其实是先扩容
//    小表里出现长链表，根因是初始容量不足，不是缺红黑树
```

理由：负载因子直接决定冲突率与扩容频率，0.75 已是经统计验证的折中，盲目调高会让查找退化、调低会浪费空间和加剧扩容；treeify 需容量≥64，小表的长链表应通过预设容量解决而非依赖转树。

## 自检

- [ ] 没有无依据地修改默认负载因子 0.75？
- [ ] 理解链表 > 8 但容量 < 64 时是**扩容**而非转树？
- [ ] 小表里发现长链表，先排查初始容量是否过小（而非纠结红黑树）？
- [ ] 内存/性能确有极端需求才调负载因子，且配套压测？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`hashmap-sizing.md`](./hashmap-sizing.md)（容量不足才是小表长链表的根因）
- 兄弟：[`concurrent-map-choice.md`](./concurrent-map-choice.md)（ConcurrentHashMap 同样用这套 treeify 机制）
