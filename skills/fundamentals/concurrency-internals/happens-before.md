---
name: concurrency-happens-before
description: 用 happens-before 规则判断"这段并发代码线程安全吗" — 把 JMM 的可见性保证落成可逐条检查的判据（写是否对读可见）。Use when 判断共享变量是否需同步 / 评审线程安全 / 排查并发可见性 bug 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - happens-before
  - 内存可见性
  - JMM
  - 线程安全判断
  - 先行发生
  - 数据竞争
effort: medium
context: inline
version: '1.0'
---
# Java · 用 happens-before 判断线程安全

> 本条只回答「凭 happens-before 判断这段代码线程安全吗」。具体该上哪种同步手段见兄弟叶子（volatile / 锁 / 原子类）。

## 原理：happens-before 是"写对读可见"的判据

JMM 不保证一个线程的写对另一个线程立即可见，**除非两操作之间存在 happens-before 关系**。判线程安全 = 对每个"一写一读的共享变量"，检查写 hb 读是否成立；**不成立就是数据竞争**，必须加同步建立这条关系。

## 规则：能直接用的 6 条 happens-before

| 规则 | 内容 | 落地检查 |
|------|------|---------|
| 程序顺序 | 同一线程内，前面操作 hb 后面 | 单线程内天然成立，跨线程不算 |
| 锁 | unlock hb 后续对同一锁的 lock | 读写都进同一把锁的临界区即安全 |
| volatile | volatile 写 hb 后续对它的读 | 标志位写→读可见 |
| 线程启动 | `t.start()` hb 线程内所有操作 | start 前的写对新线程可见 |
| 线程终止 | 线程内所有操作 hb `t.join()` 返回 | join 后能读到该线程的写 |
| 传递性 | A hb B 且 B hb C ⇒ A hb C | 串起多条规则判可见 |

## 正例：靠规则建立可见性

```java
// ✅ volatile 写-读 + 传递性：写 ready 前对 data 的写，对读到 ready==true 的线程可见
int data;                       // 普通字段
volatile boolean ready;
// 线程A
data = 42;                      // 1
ready = true;                   // 2  (volatile 写)
// 线程B
if (ready) {                    // 3  (volatile 读，2 hb 3)
    use(data);                  // 4  程序顺序 1 hb 2、2 hb 3、3 hb 4 ⇒ 1 hb 4，读到 42
}
```

## 反例：无任何 happens-before，存在数据竞争

```java
// ❌ data 和 flag 都是普通字段，线程间无 hb 关系：
//    读线程可能看到 flag==true 但 data 仍是 0（重排 + 不可见）
boolean flag;
int data;
// 写: data = 42; flag = true;
// 读: if (flag) use(data);   // data 可能读到 0 —— 把 flag 改 volatile 才安全
```

## 自检

- [ ] 每个跨线程读写的共享变量，写与读之间能找到一条 happens-before 链？
- [ ] 找不到链 → 已加 volatile / 锁 / 原子类建立关系，而非"测着没事就行"？
- [ ] 读写进的是**同一把**锁 / 同一个 volatile 字段（不同锁不建立 hb）？
- [ ] 没有把"程序顺序"误用到跨线程（它只在单线程内成立）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`volatile-boundary.md`](./volatile-boundary.md)（volatile 写-读如何建立 hb）
- 兄弟：[`synchronized-vs-lock.md`](./synchronized-vs-lock.md)（锁的 hb 保证）
- 兄弟：[`cas-and-longadder.md`](./cas-and-longadder.md)（原子类的内存语义）
