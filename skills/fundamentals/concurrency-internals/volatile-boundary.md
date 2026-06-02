---
name: concurrency-volatile-boundary
description: volatile 适用边界 — 它只保证可见性 + 禁重排，不保证复合操作原子性；适合状态标志位，i++/check-then-act 这类非原子操作必须改用原子类或锁。Use when 用 volatile / 判断某变量该不该 volatile / 评审标志位时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - volatile
  - 可见性
  - 指令重排
  - 内存可见性
  - 状态标志位
  - 原子性
effort: medium
context: inline
version: '1.0'
---
# Java · volatile 适用边界

> 本条只回答「这个变量该不该用 volatile」。需要原子自增/计数见 [`cas-and-longadder.md`](./cas-and-longadder.md)，需要互斥见 [`synchronized-vs-lock.md`](./synchronized-vs-lock.md)。

## 原理：volatile 给两个保证，不给第三个

| 保证 | 含义 |
|------|------|
| 可见性 | 一个线程写，其他线程立刻读到最新值（不走线程本地缓存） |
| 禁重排 | 写前的指令不会重排到写之后（屏障），读后的不会重排到读之前 |
| ❌ 不保证原子性 | 复合操作（读-改-写）整体**不是**原子的 |

判据一句话：**只有"一写多读、且写入不依赖旧值"的变量才适合 volatile**。

## 规则：能/不能用 volatile

| 场景 | 能否 volatile | 替代 |
|------|--------------|------|
| 布尔/状态标志位（一处 set，多处读） | ✅ 能 | —— |
| 双重检查锁的单例引用 | ✅ 必须（禁半初始化对象重排逸出） | —— |
| 计数器 `count++` | ❌ 不能（读-改-写非原子） | `AtomicLong` / `LongAdder` |
| `if (x == null) x = ...`（check-then-act） | ❌ 不能（两步非原子） | `synchronized` / 原子类 CAS |
| 依赖旧值的更新（`x = x * 2`） | ❌ 不能 | 锁 / 原子类 |

## 正例：状态标志位 —— volatile 的标准用法

```java
// ✅ 一个线程置 false 停止，工作线程循环读：只需可见性，写不依赖旧值
private volatile boolean running = true;

public void run() {
    while (running) { doTask(); }   // 没有 volatile，可能永远读到本地缓存的 true 死循环
}
public void stop() { running = false; }
```

## 反例：拿 volatile 当原子计数器

```java
// ❌ count++ 是「读 → +1 → 写」三步，volatile 只保证每步可见，不保证三步整体原子
//    并发下必然丢更新
private volatile int count;
public void incr() { count++; }      // 错

// ✅ 计数改用原子类（高并发用 LongAdder，见 cas-and-longadder.md）
private final LongAdder count = new LongAdder();
public void incr() { count.increment(); }
```

## 自检

- [ ] 这个变量是"一写多读、写入不依赖旧值"才用 volatile？
- [ ] 没有把 `i++` / check-then-act 这类复合操作交给 volatile？
- [ ] 双重检查锁单例的引用字段加了 volatile（防半初始化逸出）？
- [ ] 需要原子自增/累加的，已改用原子类而非 volatile？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`cas-and-longadder.md`](./cas-and-longadder.md)（非原子操作改用原子类/LongAdder）
- 兄弟：[`synchronized-vs-lock.md`](./synchronized-vs-lock.md)（需要互斥而非仅可见性时）
- 兄弟：[`happens-before.md`](./happens-before.md)（volatile 写-读构成 happens-before）
