---
name: java-concurrent-collections
description: 并发集合选型 — ConcurrentHashMap vs synchronizedMap、CopyOnWriteArrayList 适用场景，禁并发下用普通 HashMap。Use when 集合在多线程间共享读写 / 选并发容器时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 并发集合
  - concurrent collection
  - ConcurrentHashMap
  - synchronizedMap
  - CopyOnWriteArrayList
  - 线程安全集合
  - thread-safe collection
effort: high
context: inline
version: '1.0'
---
# Java · 并发集合

> 本条只管「多线程共享集合用哪个」。单线程选型见 [`collection-choice.md`](./collection-choice.md)；只读暴露见 [`immutable-collections.md`](./immutable-collections.md)。

## 规则

| 场景 | 用 |
|------|-----|
| 多线程读写的 Map | `ConcurrentHashMap`（分段/CAS，并发吞吐远高于 synchronizedMap） |
| 读多写极少的 List（如监听器列表、配置快照） | `CopyOnWriteArrayList` |
| 老代码 / 极简场景，全程整锁可接受 | `Collections.synchronizedMap`（遍历仍需手动 synchronized） |
| 单线程或确认无共享 | 普通 `HashMap` / `ArrayList` |

**铁律**：多线程并发写普通 `HashMap` 是禁止的——JDK7 下扩容可能成环导致 CPU 100% 死循环，JDK8 下也会丢数据 / 读到脏值。

## 正例

```java
// ✅ 多线程计数 / 缓存：ConcurrentHashMap + 原子复合操作
ConcurrentHashMap<String, Integer> counter = new ConcurrentHashMap<>();
counter.merge(key, 1, Integer::sum);          // 原子累加
counter.computeIfAbsent(key, k -> load(k));   // 原子初始化

// ✅ 读多写少：监听器列表用 CopyOnWriteArrayList，读无锁
private final List<Listener> listeners = new CopyOnWriteArrayList<>();
```

## 反例

```java
// ❌ 多线程共享普通 HashMap 并发 put —— 丢数据，JDK7 还可能死循环
static Map<String, Integer> counter = new HashMap<>();
executor.submit(() -> counter.put(k, v));  // 数据竞争

// ❌ ConcurrentHashMap 上“先 get 再 put”不是原子的，仍有竞态
if (!map.containsKey(k)) {
    map.put(k, init());   // 两线程可能都进来 → 用 computeIfAbsent 代替
}

// ❌ 写频繁却用 CopyOnWriteArrayList —— 每次写全量复制数组，性能崩
```

理由：`ConcurrentHashMap` 单个方法原子，但 check-then-act 复合操作不原子，要用 `merge`/`computeIfAbsent`；`CopyOnWriteArrayList` 每次写都复制整个底层数组，只适合写极少的场景。

## 自检

- [ ] 多线程共享的 Map 用了 `ConcurrentHashMap`，没有裸 `HashMap` 并发写？
- [ ] 复合操作（先查后写）用 `computeIfAbsent`/`merge`，没拆成两步？
- [ ] `CopyOnWriteArrayList` 只用在读多写极少的场景？
- [ ] 没有把单线程才安全的普通集合跨线程共享？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`collection-choice.md`](./collection-choice.md)（单线程下的实现选型）
- 兄弟：[`immutable-collections.md`](./immutable-collections.md)（用不可变集合规避共享可变状态）
- 兄弟：[`stream-api.md`](./stream-api.md)（parallelStream 的共享状态风险）
