---
name: tech-selection-mq-decision
description: 消息队列选型决策树 + 典型场景速查（日志大数据→Kafka，订单事务+定时关单→RocketMQ，低延迟任务队列→RabbitMQ，多租户→Pulsar）。Use when 已知场景要直接定一款 MQ / 评审 MQ 选型结论时。
parent: ./index.md
paths:
- '*.java'
- '*.yml'
- '*.xml'
triggers:
  keywords:
  - 消息队列决策树
  - 场景选型
  - 事务消息
  - 定时关单
  - Kafka
  - RocketMQ
effort: medium
context: inline
version: '1.0'
---
# 消息队列 · 决策树与场景速查

> 本条只管「已知场景直接选谁」。四款逐项能力差异见 [`comparison.md`](./comparison.md)。
> 前置：先确认真有异步解耦/削峰/重放需求再上 MQ，否则别引入。

## 决策树

| 你的硬需求 | 选谁 |
|-----------|------|
| 金融级事务消息 / 任意定时延迟消息 / 严格全局顺序 | RocketMQ |
| 百万级吞吐 + 日志重放 + 大数据流（Flink/Spark） | Kafka |
| 低延迟 + 灵活路由 + 传统任务队列/RPC，万级够用 | RabbitMQ |
| 多租户 / 跨地域 / 存算分离弹性 / 冷热分层 | Pulsar |

## 典型场景速查

| 场景 | 选谁 | 关键理由 |
|------|------|---------|
| 日志采集 / 大数据 ETL | Kafka | 百万级吞吐 + offset 重放 |
| 电商订单 + 定时关单 + 下单事务 | RocketMQ | 内置定时 + 两阶段事务回查 |
| 削峰任务队列 / 低延迟通知 / 广播 | RabbitMQ | 单数字 ms 延迟 + 灵活路由 |
| 多租户云平台 | Pulsar | 原生多租户 + 存算分离 |

## 反例：选错的常见踩坑

- ❌ 需要定时关单却选 Kafka —— Kafka 无原生定时/延迟消息，被迫自造轮子。
- ❌ 只要万级吞吐的任务队列却上 Kafka/Pulsar —— 运维成本远超收益，RabbitMQ 够用。
- ❌ 需要严格全局顺序却选 RabbitMQ —— 顺序保证弱，应选 RocketMQ。

## 自检

- [ ] 确认真有异步/削峰/重放硬需求，而非「别人都用所以上」？
- [ ] 场景的核心约束（事务 / 定时 / 顺序 / 吞吐）映射到了正确的那一款？
- [ ] 运维复杂度团队扛得住（尤其 Kafka/Pulsar）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`comparison.md`](./comparison.md)（四款逐项能力对比）
