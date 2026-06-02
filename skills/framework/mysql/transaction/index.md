---
name: framework-mysql-transaction-index
description: InnoDB 事务与锁 4 个独立决策点 — 隔离级别选 RR/RC、MVCC 与当前读加锁、间隙锁与死锁规避、事务范围控制。Use when 配隔离级别 / 写 FOR UPDATE / 排查死锁或锁等待 / 评审 @Transactional 范围时。
parent: ../index.md
children:
  - { name: mysql-isolation-level, path: isolation-level.md, tag: skill, note: "RR vs RC 选择，快照读 vs 当前读" }
  - { name: mysql-mvcc-and-locking-read, path: mvcc-and-locking-read.md, tag: skill, note: "MVCC 一致性视图，FOR UPDATE/共享锁何时用" }
  - { name: mysql-gap-lock-deadlock, path: gap-lock-deadlock.md, tag: skill, note: "间隙锁/Next-Key Lock 成因与死锁规避" }
  - { name: mysql-transaction-scope, path: transaction-scope.md, tag: skill, note: "事务要短，@Transactional 不裹远程调用/大循环" }
when_to_descend: 配隔离级别、写加锁读、排查死锁与锁等待超时、控制事务边界与 @Transactional 范围。
---

# MySQL · 事务与锁索引

InnoDB 事务/锁拆成 4 个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 选隔离级别、搞不清快照读和当前读 | [isolation-level](isolation-level.md) |
| 要加锁读数据（FOR UPDATE / 共享锁）、理解 MVCC 可见性 | [mvcc-and-locking-read](mvcc-and-locking-read.md) |
| 排查死锁、锁等待超时、间隙锁挡插入 | [gap-lock-deadlock](gap-lock-deadlock.md) |
| 事务太长、@Transactional 裹了 RPC/大循环 | [transaction-scope](transaction-scope.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 兄弟维度：[`../index/index.md`](../index/index.md) · [`../diagnosis/index.md`](../diagnosis/index.md)
- 相关：[`../../spring-boot/index.md`](../../spring-boot/index.md)（@Transactional 基础用法）· [`../../redis/distributed-lock.md`](../../redis/distributed-lock.md)（跨进程锁，不同于行锁）
