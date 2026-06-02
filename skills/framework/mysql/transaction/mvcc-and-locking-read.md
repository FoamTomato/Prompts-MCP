---
name: mysql-mvcc-and-locking-read
description: MVCC 一致性视图与当前读加锁 — 普通 SELECT 走 undo 多版本不加锁，需读最新并锁定时用 SELECT FOR UPDATE（写锁）或 LOCK IN SHARE MODE（读锁）。Use when 防超卖/防并发改 / 纠结要不要 FOR UPDATE / 排查读到旧值时。
parent: ./index.md
paths:
- '*.sql'
- '*.java'
- '*.xml'
triggers:
  keywords:
  - MVCC
  - 多版本并发控制
  - FOR UPDATE
  - LOCK IN SHARE MODE
  - 当前读
  - 一致性视图
  - undo log
  - 防超卖
effort: high
context: inline
version: '1.0'
---
# MySQL · MVCC 与当前读加锁

> 本条只管「何时该用加锁读、MVCC 为什么让你读到旧值」。RR/RC 级别本身怎么选见 [`isolation-level.md`](./isolation-level.md)；加锁带来的间隙锁/死锁见 [`gap-lock-deadlock.md`](./gap-lock-deadlock.md)。

## MVCC 机制（为什么普通读看不到最新值）

每行有隐藏的事务版本号 + 回滚指针，旧版本存在 undo log。普通 `SELECT` 按事务的**一致性视图**沿 undo 找到「对本事务可见」的版本 → 不加锁、不阻塞写，但**读到的可能不是最新已提交值**。

这是高并发读的基石，但意味着：**靠普通 SELECT 读出来再做判断、再 UPDATE，存在并发覆盖风险（如超卖）。**

## 当前读：读最新 + 加锁

| 写法 | 锁类型 | 用途 |
|------|--------|------|
| `SELECT ... FOR UPDATE` | 排他锁（X） | 读出最新值并锁定，准备改它（防超卖、防并发改） |
| `SELECT ... LOCK IN SHARE MODE` | 共享锁（S） | 读出最新值并保证读期间别人不能改（弱于上者） |
| `UPDATE` / `DELETE` | X 锁 | 本身就是当前读 |

## 正例：防超卖

```sql
-- ✅ 当前读锁定库存行，串行化扣减
START TRANSACTION;
SELECT stock FROM goods WHERE id = 1 FOR UPDATE;   -- 锁住，别的事务在此等待
-- 应用层判断 stock > 0
UPDATE goods SET stock = stock - 1 WHERE id = 1;
COMMIT;
```

```sql
-- ✅ 或直接用原子 UPDATE + WHERE 条件，连 SELECT 都省（更轻）
UPDATE goods SET stock = stock - 1 WHERE id = 1 AND stock > 0;
-- 看 affected rows 是否为 1 判断是否扣成功
```

## 反例

```sql
-- ❌ 快照读判断 + 后续更新：两步之间别人已扣，导致超卖
SELECT stock FROM goods WHERE id = 1;     -- 普通读，可能是旧值
if (stock > 0) UPDATE goods SET stock = stock - 1 WHERE id = 1;
```

## 选用原则

- **能用原子 `UPDATE ... WHERE 条件`** 解决就别加 `FOR UPDATE`（锁范围更小、更快）。
- 必须「读出值→应用层复杂判断→再写」才用 `FOR UPDATE`。
- 跨进程/跨服务的互斥不归行锁管，见 [`../../redis/distributed-lock.md`](../../redis/distributed-lock.md)。

## 自检

- [ ] 需要基于「读到的值」做判断再更新时，是否用了当前读（FOR UPDATE）或原子 UPDATE，而非快照读？
- [ ] 能用原子 `UPDATE...WHERE` 就没多加一道 `FOR UPDATE`？
- [ ] 加锁读是否在事务内、且事务尽快提交（见 transaction-scope）？
- [ ] 没把行锁误当跨进程分布式锁用？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`isolation-level.md`](./isolation-level.md) · [`gap-lock-deadlock.md`](./gap-lock-deadlock.md) · [`transaction-scope.md`](./transaction-scope.md)
- 跨进程锁：[`../../redis/distributed-lock.md`](../../redis/distributed-lock.md)
