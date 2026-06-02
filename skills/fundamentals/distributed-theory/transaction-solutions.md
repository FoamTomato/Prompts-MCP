---
name: distributed-transaction-solutions
description: 分布式事务方案选型 — 2PC 强一致但慢、TCC 高性能但侵入、Saga 适合长流程、本地消息表/MQ 最终一致、最大努力通知兜底，按一致性强度与侵入成本选。Use when 跨服务/跨库要保证数据一致 / 在多个事务方案间权衡 / 评审分布式事务设计时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 分布式事务
  - 最终一致
  - 2PC
  - TCC
  - Saga
  - 本地消息表
effort: high
context: inline
version: '1.0'
---
# 分布式理论 · 分布式事务方案选型

> 本条只管「选哪种分布式事务方案（理论维度）」。Seata 三模式（AT/TCC/Saga）的**落地实现与注解**见 [`../../framework/seata/index.md`](../../framework/seata/index.md)——本条给方案全景与取舍，那里给框架怎么用。幂等是事务重试的前提，见 [`idempotent-design.md`](./idempotent-design.md)。

## 方案全景（强一致 → 最终一致）

| 方案 | 一致性 | 侵入/成本 | 适合 |
|------|--------|----------|------|
| **2PC / XA** | 强一致 | 同步阻塞、慢、协调者单点 | 传统 DB/中间件，并发不高 |
| **TCC** | 强一致 | 业务侵入大（写 Try/Confirm/Cancel） | 核心交易，要高性能可接受改造 |
| **Saga** | 最终一致 | 每步配补偿动作，状态机编排 | 流程长、参与方多（履约/审批） |
| **本地消息表 / MQ** | 最终一致 | 中等，靠 MQ 可靠投递 + 消费幂等 | 异步解耦、可容忍短延迟 |
| **最大努力通知** | 最终一致（弱） | 低，定时重试 + 对账兜底 | 通知类（支付回调、对账） |

## 选型速判

```text
能不能不分布式？—— 单库内优先用本地 @Transactional，别为单库上分布式事务。
要强一致 + 并发不高      → 2PC/XA（或 Seata AT，无侵入近似强一致）
要强一致 + 高性能核心交易 → TCC
流程长、步骤多、要可编排  → Saga
能接受最终一致、想解耦    → 本地消息表 / MQ 事务消息
纯通知、可重试可对账      → 最大努力通知
```

最终一致方案**都依赖消费端幂等**（MQ 至少投递一次会重复）——见 idempotent-design。

## 反例

```text
❌ 单库操作也套分布式事务：本地 @Transactional 就够，过度设计还慢
❌ 高并发核心链路用 2PC：同步阻塞 + 协调者单点，吞吐压不上去
❌ 上了最终一致方案却不做消费幂等：MQ 重投 → 重复扣款/重复发货
❌ Saga 只写正向不写补偿：中途失败无法回滚，数据悬挂
```

## 自检

- [ ] 先确认「真的跨服务/跨库」才上分布式事务，单库用本地事务？
- [ ] 按「一致性强度 × 侵入成本」选方案，不是一律 2PC 或一律最终一致？
- [ ] 用最终一致（MQ/消息表）时消费端做了幂等？
- [ ] 用 TCC/Saga 时补偿（Cancel/补偿动作）都实现了？

## 相关

- 父：[`./index.md`](./index.md)
- 框架落地（Seata AT/TCC/Saga 实现与注解）：[`../../framework/seata/index.md`](../../framework/seata/index.md)
- 兄弟：[`idempotent-design.md`](./idempotent-design.md)（最终一致的前提）
- 兄弟：[`cap-tradeoff.md`](./cap-tradeoff.md)（一致性 vs 可用性的上层取舍）
