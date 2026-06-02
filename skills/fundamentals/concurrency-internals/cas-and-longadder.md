---
name: concurrency-cas-and-longadder
description: CAS 原理与原子类选型 — 低/中并发计数用 AtomicLong，高并发热点计数用 LongAdder（分段累加减少 CAS 失败重试）；并理解 CAS 的 ABA 问题与解法。Use when 写并发计数器 / 选 AtomicLong 还是 LongAdder / 评审 CAS 自旋时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - CAS
  - LongAdder
  - AtomicLong
  - ABA 问题
  - 并发计数
  - 原子类
effort: medium
context: inline
version: '1.0'
---
# Java · CAS 原理与 AtomicLong/LongAdder 选型

> 本条只回答「并发计数/累加该用哪个原子类」。仅需可见性的标志位见 [`volatile-boundary.md`](./volatile-boundary.md)。

## 原理：CAS 是乐观锁，竞争越激烈越亏

`compareAndSet(expect, update)`：值仍是 expect 才更新，否则失败重试。无锁，但**高竞争下大量线程 CAS 失败空转自旋**，CPU 浪费随并发上升。

- `AtomicLong`：所有线程 CAS **同一个** value → 高并发时争抢同一缓存行，失败重试激增。
- `LongAdder`：内部分成多个 Cell，线程**分散**到不同 Cell 各自累加，读时求和 → 把竞争摊薄，写吞吐远高于 AtomicLong。

## 规则：按并发度和读写比选

| 场景 | 选 | 理由 |
|------|-----|------|
| 低/中并发计数 | `AtomicLong` | 简单，单值，读即最新 |
| 高并发热点累加（QPS 计数、限流统计） | `LongAdder` | 分段减少 CAS 冲突，写吞吐高 |
| 需要"读到精确瞬时值"且高频读 | `AtomicLong` | LongAdder 的 `sum()` 非原子快照，读有成本 |
| 累加 + 偶尔取近似总量 | `LongAdder` | 写多读少最划算 |

## ABA 问题

CAS 只比"值"不比"是否被改过"：值 A→B→A，CAS 仍认为没变。计数场景通常无害；若值是**带状态的引用**（如栈顶节点复用），用 `AtomicStampedReference`(加版本号) 或 `AtomicMarkableReference`(加标记) 区分。

## 正例：高并发计数用 LongAdder

```java
// ✅ 接口 QPS 统计：成千上万线程并发自增，LongAdder 分段累加避免 CAS 风暴
private final LongAdder qps = new LongAdder();
public void onRequest() { qps.increment(); }
public long snapshot() { return qps.sum(); }   // 求和是近似快照，统计场景足够
```

## 反例：高并发热点仍用 AtomicLong

```java
// ❌ 万级并发都 CAS 同一个 value，失败重试自旋打满 CPU，吞吐反而下降
private final AtomicLong counter = new AtomicLong();
public void onRequest() { counter.incrementAndGet(); }   // 高并发热点应换 LongAdder
```

## 自检

- [ ] 高并发热点计数用了 LongAdder，而非默认 AtomicLong？
- [ ] 需要精确瞬时值/高频读的场景才保留 AtomicLong（没误用 LongAdder.sum 当强一致）？
- [ ] CAS 的目标是带状态的引用时，评估了 ABA 并用 AtomicStampedReference 兜底？
- [ ] 没有在超高竞争下手写 CAS 自旋（应退化为锁）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`volatile-boundary.md`](./volatile-boundary.md)（仅需可见性的标志位用 volatile，不用原子类）
- 兄弟：[`synchronized-vs-lock.md`](./synchronized-vs-lock.md)（复杂临界区无法用单个原子类时改用锁）
- 兄弟：[`happens-before.md`](./happens-before.md)（原子类操作的内存语义）
