---
name: mysql-gap-lock-deadlock
description: InnoDB 间隙锁/Next-Key Lock 与死锁规避 — RR 下范围当前读会锁间隙挡插入，多事务交叉加锁顺序不一致即死锁。Use when 排查 Deadlock found / Lock wait timeout / 范围更新挡住插入 / 设计加锁顺序时。
parent: ./index.md
paths:
- '*.sql'
- '*.java'
- '*.xml'
triggers:
  keywords:
  - 间隙锁
  - Next-Key Lock
  - 死锁
  - deadlock
  - 锁等待超时
  - lock wait timeout
  - gap lock
  - 加锁顺序
effort: high
context: inline
version: '1.0'
---
# MySQL · 间隙锁与死锁规避

> 本条只管「间隙锁为什么挡插入、死锁怎么避」。FOR UPDATE 何时用见 [`mvcc-and-locking-read.md`](./mvcc-and-locking-read.md)；级别（RR 才有间隙锁）见 [`isolation-level.md`](./isolation-level.md)。

## 间隙锁 / Next-Key Lock

RR 隔离级别下，范围当前读不仅锁命中行，还锁住它们之间的**间隙**（防幻读）。Next-Key Lock = 行锁 + 间隙锁。后果：**别的事务无法在被锁间隙内插入新行**。

```sql
-- RR 下：锁住 id 在 (10,20] 的间隙
SELECT * FROM t WHERE id BETWEEN 10 AND 20 FOR UPDATE;
-- 此时其它事务 INSERT id=15 会被阻塞，直到本事务提交
```

排查要点：「插入莫名被卡住」「Lock wait timeout」常是别处的范围当前读把间隙锁住了。RC 级别无间隙锁，是改 RC 的动机之一（见 isolation-level）。

## 死锁的根因与规避

死锁 = 两事务各持一把锁、又互相等对方的锁，形成环。InnoDB 会检测并回滚其中一个（报 `Deadlock found`）。

| 规避手段 | 做法 |
|----------|------|
| **统一加锁顺序** | 多行加锁时按固定顺序（如按主键升序）访问，杜绝交叉 |
| 缩小事务 | 事务越短，持锁时间越短，撞车概率越低（见 transaction-scope） |
| 一次锁定 | 把要锁的行用一条语句 / `IN` 一次锁完，别分多次 |
| 降级隔离 | 高频间隙锁死锁时评估改 RC |
| 控制并发 | 热点行用队列/分布式锁前置串行化 |

## 正例：统一加锁顺序

```java
// ✅ 转账：对两个账户按 id 升序加锁，A→B 和 B→A 的转账都按同序加锁，不成环
long first = Math.min(fromId, toId), second = Math.max(fromId, toId);
lockRow(first); lockRow(second);
```

## 反例

```java
// ❌ 各按自己的 from→to 顺序加锁：T1 锁1等2，T2 锁2等1 → 死锁
lockRow(fromId); lockRow(toId);
```

## 自检

- [ ] 多行加锁是否按统一顺序（如主键升序），不会成环？
- [ ] 事务是否足够短、持锁时间最小？
- [ ] 范围当前读是否意识到会锁间隙、可能挡住他人插入？
- [ ] 出现死锁时是否看了 `SHOW ENGINE INNODB STATUS` 的 LATEST DETECTED DEADLOCK 定位两条 SQL？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`isolation-level.md`](./isolation-level.md) · [`mvcc-and-locking-read.md`](./mvcc-and-locking-read.md) · [`transaction-scope.md`](./transaction-scope.md)
