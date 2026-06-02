---
name: fundamentals-concurrency-internals-index
description: Java 并发内功四件事（原理服务于选型）— 锁升级指导 synchronized/Lock 选型、volatile 适用边界、CAS 与 LongAdder 计数选型、用 happens-before 判线程安全。Use when 选并发原语 / 判断线程安全 / 评审同步代码时。
parent: ../index.md
children:
  - { name: concurrency-synchronized-vs-lock, path: synchronized-vs-lock.md, tag: skill, note: 锁升级原理指导 synchronized vs ReentrantLock 选型 }
  - { name: concurrency-volatile-boundary, path: volatile-boundary.md, tag: skill, note: volatile 边界（仅可见性+禁重排非原子），适合标志位 }
  - { name: concurrency-cas-and-longadder, path: cas-and-longadder.md, tag: skill, note: 高并发计数用 LongAdder 不用 AtomicLong，ABA 问题 }
  - { name: concurrency-happens-before, path: happens-before.md, tag: skill, note: 用 happens-before 规则判断这段代码线程安全吗 }
when_to_descend: 选并发原语 / 判断某共享变量是否线程安全 / 评审同步代码时
---
# Concurrency Internals · 子项索引

并发内功拆成四个**独立决策点**，原理用来指导"该用哪个"，不背八股。按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 纠结同步用 synchronized 还是 ReentrantLock（凭锁升级原理选） | [synchronized-vs-lock](synchronized-vs-lock.md) |
| 某变量想加 volatile，不确定够不够（如 i++ 行不行） | [volatile-boundary](volatile-boundary.md) |
| 写并发计数器，选 AtomicLong 还是 LongAdder / 遇到 ABA | [cas-and-longadder](cas-and-longadder.md) |
| 判断"这段并发代码到底线程安全吗"，找可见性依据 | [happens-before](happens-before.md) |

> 这里讲**原理→选型**。线程池/异步编排等**用法**在 [`../../lang/java/concurrency/index.md`](../../lang/java/concurrency/index.md)。
