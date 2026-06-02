---
name: distributed-id
description: 分布式 ID 算法选型（理论视角）— 雪花算法本地生成但有时钟回拨、号段模式趋势递增依赖 DB、Redis incr 简单、UUID 无序不宜做主键，按是否要有序/是否依赖中心组件取舍。Use when 给分布式系统选全局唯一 ID 算法 / 在雪花/号段/Redis/UUID 间权衡时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 分布式 ID
  - ID 选型
  - 雪花算法
  - 时钟回拨
  - 号段模式
  - UUID
effort: medium
context: inline
version: '1.0'
---
# 分布式理论 · 分布式 ID 选型（算法视角）

> 本条是**理论/算法选型视角**：在雪花/号段/Redis/UUID 之间按特性取舍。
> 若你的问题是「分库分表后主键怎么选、为什么不能用 UUID 伤聚簇索引」，那是 **DB 主键视角**，去 [`../../framework/mysql/ops/distributed-id.md`](../../framework/mysql/ops/distributed-id.md)（含号段/雪花的 DB 落地细节）。
> 分工：**本条管"选哪种算法及其取舍"，那条管"作为 MySQL 主键时的约束与发号器实现"**，避免重复。

## 四种算法对比

| 算法 | 有序性 | 依赖 | 关键问题 |
|------|--------|------|---------|
| **雪花算法 Snowflake** | 趋势递增 | 无中心，本地生成 | **时钟回拨**会重号，须处理 |
| **号段模式 segment** | 趋势递增、连续 | DB 发号 | 中心 DB，宕机丢一段（可接受） |
| **Redis incr** | 单调递增 | Redis | Redis 单点/持久化丢号风险 |
| **UUID** | **无序** | 无 | 36 位随机串，不宜做有序主键 |

## 选型速判

```text
要本地高并发生成、无中心依赖   → 雪花（务必处理时钟回拨）
要 ID 连续/可读、能接受中心发号 → 号段模式
量不大、已有 Redis、想简单      → Redis incr
只需全局唯一、不要求有序        → UUID（如 traceId、文件名；别拿来当 DB 主键）
```

## 时钟回拨：雪花的头号坑

雪花高位是时间戳，机器时钟**被 NTP 校准回拨**时会生成更小甚至重复的 ID。处理策略：

```text
回拨幅度小 → 等待时钟追上再发号（阻塞几毫秒）
回拨幅度大 → 直接拒绝发号并告警 / 切换备用 workerId
进阶       → 用百度 uid-generator / 美团 Leaf 等带回拨处理的成熟实现
```

## 反例

```text
❌ 拿 UUID 当 MySQL 主键：无序破坏聚簇索引（详见 mysql 那条），且占空间
❌ 自己撸雪花不处理时钟回拨：NTP 一校准就重号，唯一性直接破防
❌ workerId 多机重复（如硬编码/同镜像部署）：不同机器生成相同 ID
❌ 单库未分片就上分布式 ID 算法：过度设计，库自增 BIGINT 就够
```

## 自检

- [ ] 按「是否要有序 × 是否依赖中心组件」选算法，不是无脑雪花？
- [ ] 用雪花时**处理了时钟回拨**，且 workerId 多机唯一？
- [ ] UUID 只用在不要求有序的场景，没拿来当有序主键？
- [ ] 作为 DB 主键的约束已对照 [`mysql/ops/distributed-id`](../../framework/mysql/ops/distributed-id.md)，没在两处重复设计？

## 相关

- 父：[`./index.md`](./index.md)
- DB 主键视角（分片主键约束 + 发号器落地）：[`../../framework/mysql/ops/distributed-id.md`](../../framework/mysql/ops/distributed-id.md)
- 兄弟：[`idempotent-design.md`](./idempotent-design.md)（唯一 ID 常作幂等键）
- 兄弟：[`cap-tradeoff.md`](./cap-tradeoff.md) · [`transaction-solutions.md`](./transaction-solutions.md)
