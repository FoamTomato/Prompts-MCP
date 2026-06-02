---
name: mysql-transaction-scope
description: 事务边界控制 — 事务要短，@Transactional 方法内禁裹 RPC/HTTP/MQ 等远程调用和大循环，长事务撑大 undo、占连接、加锁久。Use when 写 @Transactional 方法 / 事务里夹了远程调用或批处理 / 排查长事务与连接耗尽时。
parent: ./index.md
paths:
- '*.java'
- '*.py'
triggers:
  keywords:
  - 长事务
  - 事务范围
  - long transaction
  - transaction scope
  - '@Transactional'
  - 事务里远程调用
  - undo log 膨胀
effort: high
context: inline
version: '1.0'
---
# MySQL · 事务边界控制

> 本条只管「事务该包多大、@Transactional 不该裹什么」。@Transactional 的传播/回滚等基础用法见 [`../../spring-boot/index.md`](../../spring-boot/index.md)；加锁久导致的死锁见 [`gap-lock-deadlock.md`](./gap-lock-deadlock.md)。

## 长事务的危害

| 危害 | 机制 |
|------|------|
| undo log 膨胀 | RR 下长事务的一致性视图阻止旧版本回收，undo 暴涨 |
| 连接被长期占用 | 事务持有连接直到提交，长事务拖垮连接池 |
| 锁持有时间长 | 行锁/间隙锁直到提交才释放，放大死锁与锁等待 |
| 主从延迟 | 大事务 binlog 一次性同步，从库追不上 |

## 规则

| 项 | 约定 |
|----|------|
| 事务尽量短 | 只把「必须原子」的几条 DB 写包进事务 |
| **禁裹远程调用** | 事务方法内不调 RPC/HTTP/MQ/发邮件 —— 网络阻塞会把事务拖到几秒甚至超时 |
| 禁裹大循环 | 别在事务里 for 循环逐条写 N 千行；改批量或分批提交 |
| 查询移出事务 | 纯读、参数校验、调外部接口放到 `@Transactional` 方法**之外** |
| 大批量分批 | 批处理按每 N 行一个小事务提交，避免单个巨型事务 |

## 反例

```java
// ❌ 事务里夹了 HTTP 调用：远程慢 → 事务长 → 锁久占、连接耗尽
@Transactional
public void pay(Long orderId) {
    orderMapper.updateStatus(orderId, "PAID");
    paymentClient.notifyThirdParty(orderId);   // 网络调用，可能几秒
    orderMapper.insertLog(orderId);
}
```

## 正例

```java
// ✅ 远程调用移出事务；事务只包必须原子的 DB 写
public void pay(Long orderId) {
    boolean ok = paymentClient.notifyThirdParty(orderId);   // 事务外
    if (ok) doPay(orderId);                                  // 事务内
}

@Transactional
public void doPay(Long orderId) {
    orderMapper.updateStatus(orderId, "PAID");
    orderMapper.insertLog(orderId);
}
```

## 自检

- [ ] `@Transactional` 方法内是否**没有**任何 RPC/HTTP/MQ/IO 远程调用？
- [ ] 事务是否只包必须原子的那几条写，纯读和校验已移出？
- [ ] 大批量写是否分批提交，没有单个超大事务？
- [ ] 自调用（同类内 this.xxx 调 @Transactional 方法）失效问题已规避（走代理）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`gap-lock-deadlock.md`](./gap-lock-deadlock.md)
- 基础用法：[`../../spring-boot/index.md`](../../spring-boot/index.md)（@Transactional 传播/回滚）
