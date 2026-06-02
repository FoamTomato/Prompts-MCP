---
name: mysql-isolation-level
description: InnoDB 隔离级别选型 — 默认 RR 用一致性快照防不可重复读/幻读，RC 锁范围小更适合高并发短事务，区分快照读与当前读。Use when 配 tx_isolation / 纠结 RR 还是 RC / 排查读到旧数据或幻读时。
parent: ./index.md
paths:
- '*.sql'
- '*.java'
- '*.yml'
- '*.properties'
triggers:
  keywords:
  - 隔离级别
  - 可重复读
  - 读已提交
  - isolation level
  - RR RC
  - 快照读
  - 当前读
  - 幻读
effort: high
context: inline
version: '1.0'
---
# MySQL · 隔离级别选型

> 本条只管「选哪个隔离级别、快照读 vs 当前读的区别」。当前读怎么加锁见 [`mvcc-and-locking-read.md`](./mvcc-and-locking-read.md)；间隙锁/幻读防护的代价见 [`gap-lock-deadlock.md`](./gap-lock-deadlock.md)。

## 四级别与现象

| 级别 | 脏读 | 不可重复读 | 幻读 | InnoDB 备注 |
|------|------|-----------|------|------------|
| READ UNCOMMITTED | 可能 | 可能 | 可能 | 基本不用 |
| READ COMMITTED (RC) | 否 | 可能 | 可能 | 每次快照读都取最新视图 |
| REPEATABLE READ (RR) | 否 | 否 | **InnoDB 用 Next-Key Lock 基本消除** | **MySQL 默认** |
| SERIALIZABLE | 否 | 否 | 否 | 读也加锁，并发最差 |

## RR vs RC 怎么选

| 倾向 RR（默认） | 倾向 RC |
|----------------|---------|
| 同一事务内多次读要一致（报表、对账） | 高并发短事务，想减小锁范围 |
| 依赖 InnoDB 间隙锁防幻读 | 频繁出现间隙锁导致的死锁/锁等待 |
| 不确定就保持默认 | 主从用 row 格式 binlog（RC 配 row 才安全） |

> 没有明确理由就**保持默认 RR**。改 RC 是为了换取更小的锁范围，代价是放弃可重复读，需团队达成共识。

## 快照读 vs 当前读（关键区别）

| 类型 | 语句 | 读到什么 |
|------|------|---------|
| 快照读 | 普通 `SELECT` | 事务启动时的一致性视图（MVCC，**不加锁**） |
| 当前读 | `SELECT ... FOR UPDATE` / `LOCK IN SHARE MODE` / `UPDATE` / `DELETE` | **最新已提交数据 + 加锁** |

```sql
-- RR 下：A 事务内两次普通 SELECT 结果一致（快照读）
START TRANSACTION;
SELECT balance FROM account WHERE id=1;   -- 快照，期间别人改了也看不见
SELECT balance FROM account WHERE id=1;   -- 仍是同一值
-- 但 UPDATE / FOR UPDATE 是当前读，看到的是最新值
UPDATE account SET balance = balance - 10 WHERE id=1;
```

## 自检

- [ ] 没有特殊理由时是否保持默认 RR？
- [ ] 改用 RC 是经过权衡（要小锁范围），且 binlog 为 row 格式？
- [ ] 清楚「业务里那条读是快照读还是当前读」，避免以为读到了最新值？
- [ ] 需要读最新值并锁住时，显式用了当前读（见 mvcc 条），而非普通 SELECT？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`mvcc-and-locking-read.md`](./mvcc-and-locking-read.md) · [`gap-lock-deadlock.md`](./gap-lock-deadlock.md)
