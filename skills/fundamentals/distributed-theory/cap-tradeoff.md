---
name: distributed-cap-tradeoff
description: CAP 取舍决策 — 分布式系统 P（分区容忍）必选，真正的取舍是网络分区时选 C（一致性，如 ZK/etcd 拒绝服务保正确）还是 A（可用性，如 Eureka/Nacos AP 返回旧数据）。Use when 选注册中心/配置中心的一致性模型 / 评审 CP 还是 AP 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - CAP
  - 一致性
  - 可用性
  - CP
  - AP
  - 注册中心
effort: medium
context: inline
version: '1.0'
---
# 分布式理论 · CAP 取舍

> 本条只管「C 和 A 之间怎么选」。事务一致性方案见 [`transaction-solutions.md`](./transaction-solutions.md)；幂等见 [`idempotent-design.md`](./idempotent-design.md)。

## 核心：P 不是选项，C/A 才是

分布式系统**一定有网络分区**，所以 **P 必选**；CAP 真正的取舍是「发生分区时，要 C 还是 A」——三者**不可能同时满足**。

| 取舍 | 分区时行为 | 代表组件 | 适合 |
|------|-----------|---------|------|
| **CP**（保一致） | 拒绝服务/不可用，宁可不返回也不返回错的 | ZooKeeper、etcd、Consul、Nacos CP | 配置/选主/分布式锁，错了代价大 |
| **AP**（保可用） | 始终响应，可能返回旧数据，分区恢复再收敛 | Eureka、Nacos AP 模式 | 服务发现，拿到稍旧节点列表可接受 |

## 选型速判

| 场景 | 选 | 理由 |
|------|-----|------|
| 服务注册发现 | AP（Eureka / Nacos AP） | 注册表短暂不一致可容忍，可用性优先 |
| 分布式锁 / 选主 / 配置 | CP（ZK / etcd） | 读到错的配置/双主，后果严重 |
| 金融账务等强一致读 | CP | 一致性 > 可用性 |

注意：Nacos **同时支持** AP/CP，按上述场景切换；不要无脑跟风选某个组件，先定 C/A 取向。

## 反例

```text
❌ 把"高可用"当成"什么都要满足"，以为能同时拿到 CAP —— 分区下三选二是定理
❌ 用 CP 的 ZK 做服务发现：ZK 一抖动注册表整个不可用，拖垮全链路（应选 AP）
❌ 用 AP 的注册中心存关键配置/做选主：分区时读到旧值导致双主/脏配置
```

## 自检

- [ ] 先承认 P 必选，把决策聚焦在「分区时要 C 还是 A」？
- [ ] 服务发现这类容忍短暂不一致的场景选了 AP？
- [ ] 锁/选主/关键配置这类错了代价大的场景选了 CP？
- [ ] 用 Nacos 时按场景显式选了 AP / CP 模式，不是用默认凑合？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`transaction-solutions.md`](./transaction-solutions.md)（数据一致性靠事务方案落地）
- 兄弟：[`idempotent-design.md`](./idempotent-design.md) · [`distributed-id.md`](./distributed-id.md)
