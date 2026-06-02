---
name: mysql-distributed-id
description: 分布式有序主键生成 — 分库分表后不能用单库自增，选号段模式（DB 批量发号、趋势递增）或雪花算法（Snowflake、时间戳+机器+序列），保持单调避免退回 UUID 伤聚簇索引。Use when 分片后选主键生成 / 评审用 UUID 当分布式 ID / 设计发号器时。
parent: ./index.md
paths:
- '*.java'
- '*.sql'
- '*.py'
triggers:
  keywords:
  - 分布式 ID
  - 分布式主键
  - 雪花算法
  - Snowflake
  - 号段模式
  - segment
  - 发号器
  - 趋势递增
effort: high
context: inline
version: '1.0'
---
# MySQL · 分布式有序主键生成

> 本条只管「分片后主键怎么生成」。为什么主键要单调递增、不能用 UUID 见 [`../index/clustered-pk-design.md`](../index/clustered-pk-design.md)（本条给分布式场景的具体生成方案）；拆分键见 [`sharding-key-choice.md`](./sharding-key-choice.md)。

## 为什么不能用库自增 / 不能退回 UUID

- 分库分表后**单库自增会撞号**（各库各自从 1 涨）。
- 但也**不能退回 UUID**：随机分布破坏 InnoDB 聚簇索引顺序，页分裂 + 二级索引膨胀（见 clustered-pk-design）。
- 目标：全局唯一 + **趋势/单调递增**（保住聚簇索引顺序）+ `BIGINT` 宽度。

## 两种主流方案

### 号段模式（segment）

发号器从 DB 一次取一段（如 1000 个）缓存在内存，用完再取下一段。

| 优点 | 缺点 |
|------|------|
| 趋势递增、ID 连续、DB 压力小 | 依赖发号 DB；号段缓存，宕机丢一段（可接受） |

适合：对 ID 连续性/可读性有要求、能接受中心发号器（如美团 Leaf-segment）。

### 雪花算法（Snowflake）

64 位 `BIGINT` = 时间戳 + 机器/数据中心 ID + 同毫秒序列号。

| 优点 | 缺点 |
|------|------|
| 本地生成、无中心依赖、趋势递增 | **依赖机器时钟**，时钟回拨会重号，需处理回拨 |

适合：高并发、不想引入中心发号 DB；务必处理时钟回拨（拒绝/等待/借位）。

## 选型速判

| 场景 | 选 |
|------|-----|
| 能接受中心发号器、要 ID 连续 | 号段模式 |
| 要本地高并发生成、无中心依赖 | 雪花算法（处理回拨） |
| 单库未分片 | 直接库自增 BIGINT，**别提前上分布式 ID** |

## 反例

```text
❌ 分片后图省事用 UUID 当主键 → 解决了唯一性，却拖垮聚簇索引写入
✅ 用雪花/号段产出趋势递增的 BIGINT 主键，唯一且不伤聚簇索引
```

## 自检

- [ ] 产出的是趋势/单调递增的 `BIGINT`，没有退回 UUID/随机串？
- [ ] 选号段还是雪花，是基于「能否接受中心发号器」权衡的？
- [ ] 用雪花时是否处理了**时钟回拨**？
- [ ] 单库未分片时没有过度设计、直接用库自增？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`sharding-key-choice.md`](./sharding-key-choice.md)
- 主键设计：[`../index/clustered-pk-design.md`](../index/clustered-pk-design.md)
