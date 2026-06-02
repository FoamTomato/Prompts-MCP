---
name: ai-vector-db-index-filter
description: 向量库索引与过滤规约 — HNSW 默认/IVF/DiskANN 怎么选 + 元数据过滤字段必须建索引避免全表暴力扫。Use when 配置向量索引参数 / 设计元数据过滤 / 排查向量检索慢时。
parent: ./index.md
paths:
- '*.java'
- '*.py'
- '*.md'
triggers:
  keywords:
  - 向量索引选型
  - 元数据过滤
  - HNSW
  - IVF
  - DiskANN
  - payload 索引
  - metadata filter
effort: medium
context: inline
version: '1.0'
---
# 向量库 · 索引选型与元数据过滤

> 本条只管「选定库后索引怎么建、过滤字段怎么配」。该选哪一款见 [`decision-tree.md`](./decision-tree.md)；六款能力对比见 [`comparison.md`](./comparison.md)。

## 索引选型

| 索引 | 何时用 | 取舍 |
|---|---|---|
| **HNSW**（默认） | 绝大多数场景、内存放得下 | 召回/延迟均衡，建图内存占用较高 |
| IVF / IVFFlat | 内存吃紧、可接受调 nprobe 换召回 | 省内存，召回需调 nlist/nprobe |
| DiskANN | 单机内存放不下、十亿级 | 走 SSD，延迟高于纯内存但能装下超大集 |
| GPU 索引 | 超大批量、有 GPU 预算 | 吞吐高，硬件成本高（仅 Milvus 等支持） |

规约：**默认 HNSW**，只有在内存/量级触顶时才换 IVF/DiskANN，且换索引必须自测召回率不是只看延迟。

## 元数据过滤

| 规则 | 要求 |
|---|---|
| 过滤字段必建索引 | 任何参与 `filter` 的元数据字段**必须建索引**（Qdrant payload index / pgvector B-tree / Milvus scalar index），否则退化为全表暴力扫 |
| 字段强类型 | 过滤字段定义明确类型（int/keyword/bool），别用大 JSON blob 兜 |
| 高基数谨慎 | 高基数字段过滤代价高，结合 partition / 分片减小扫描范围 |
| 先过滤后近邻 | 让引擎做「先标量过滤、再向量近邻」，而非取回大批向量后在应用层过滤 |

## 反例

- ❌ `tenant_id` 参与过滤却没建索引 → 每次查询全表扫元数据，量级一大就超时。
- ❌ 把一堆属性塞进一个 JSON 字段再 filter → 无法走索引，过滤变线性扫。
- ❌ 换 IVF 只对比延迟变快就上线 → 召回率掉了没发现，结果质量回归。

## 自检

- [ ] 默认用了 HNSW？换 IVF/DiskANN 是因为内存/量级触顶且自测过召回？
- [ ] **所有**参与过滤的元数据字段都建了索引？
- [ ] 过滤字段是强类型，不是大 JSON blob？
- [ ] 多租户/分区场景用 partition 缩小了扫描范围？
- [ ] 换索引时同时复测了召回率与延迟（量级参考须自测）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`decision-tree.md`](./decision-tree.md)（先选定哪一款库）
- 兄弟：[`comparison.md`](./comparison.md)（各库索引/过滤能力对比）
