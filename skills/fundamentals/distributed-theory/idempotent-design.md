---
name: distributed-idempotent-design
description: 幂等设计 — 同一请求/消息重复执行结果一致，手段按场景选：唯一索引/去重表（插入类）、Token 令牌（防重复提交）、状态机（流转类）、乐观锁（更新类），接口幂等 + 消息幂等。Use when 接口可能被重试 / MQ 至少投递一次会重复 / 设计防重复提交时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 幂等
  - idempotent
  - 防重复提交
  - 去重表
  - 唯一索引
  - 状态机
  - 乐观锁
effort: high
context: inline
version: '1.0'
---
# 分布式理论 · 幂等设计

> 本条只管「怎么保证重复执行只生效一次」。它是最终一致事务的前提，方案选型见 [`transaction-solutions.md`](./transaction-solutions.md)；乐观锁的 ID/version 落地不在这。

## 为什么要幂等

网络重试、MQ「至少投递一次」、用户重复点击——同一操作会**重复到达**。幂等 = 重复执行 N 次与执行 1 次**效果相同**。

## 手段按场景选

| 操作类型 | 手段 | 怎么做 |
|---------|------|--------|
| 插入（创建订单/支付单） | **唯一索引 / 去重表** | 业务唯一键建唯一约束，重复插入直接被 DB 挡 |
| 防重复提交（表单/下单） | **Token 令牌** | 进页面发 token，提交校验并删除，重复提交 token 已失效 |
| 状态流转（待支付→已支付） | **状态机** | 只允许合法前置态流转，重复请求落在错误前置态被拒 |
| 更新（扣库存/改余额） | **乐观锁** | `update ... set v=v+1 where id=? and v=?`，影响行数为 0 即重复 |
| 通用消息消费 | **去重表 + 唯一 msgId** | 消费前查/插 msgId，已存在则跳过 |

## 正例

```java
// ✅ 唯一键去重：靠 DB 唯一索引兜底，捕获重复键即视为幂等命中
try {
    orderMapper.insert(order);            // uk: (user_id, biz_no)
} catch (DuplicateKeyException e) {
    return queryExisting(order.getBizNo()); // 重复请求返回已有结果，不报错
}
```

```java
// ✅ 乐观锁更新，影响行数=0 说明已被处理过（重复）
int rows = accountMapper.deduct(id, amount, version);
if (rows == 0) { /* 已处理或并发，按业务幂等返回 */ }
```

## 反例

```text
❌ 只在应用层 if (exists) 判重不加 DB 唯一约束：并发下两条同时过检查双插入
❌ 消费 MQ 不做去重：至少投递一次 → 同条消息消费两次 → 重复扣款
❌ 用「查到再插」两步且无唯一索引兜底：典型 check-then-act 竞态
❌ 把幂等键设成业务无关的随机值：重试时键变了，根本判不出是同一请求
```

## 自检

- [ ] 幂等键是**业务唯一**的（订单号/msgId），重试时保持不变？
- [ ] 插入类有 **DB 唯一索引**兜底，不只靠应用层判断？
- [ ] 更新类用乐观锁/状态机，靠影响行数/前置态判重复？
- [ ] MQ 消费端做了去重（至少投递一次必然重复）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`transaction-solutions.md`](./transaction-solutions.md)（最终一致方案依赖消费幂等）
- 兄弟：[`cap-tradeoff.md`](./cap-tradeoff.md) · [`distributed-id.md`](./distributed-id.md)
- MQ 落地：[`../../framework/kafka/idempotent-consumer.md`](../../framework/kafka/idempotent-consumer.md) · [`../../framework/rocketmq/idempotent.md`](../../framework/rocketmq/idempotent.md)（消费端按本条通用方案做去重）
