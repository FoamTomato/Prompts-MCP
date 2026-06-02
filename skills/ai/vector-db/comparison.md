---
name: ai-vector-db-comparison
description: 六款向量库横向对比 — Milvus/Qdrant/Weaviate/pgvector/Pinecone/Chroma 的部署/量级/索引/过滤/混合检索/运维差异。Use when 横向比较向量库 / 评估候选向量库能力 / 写选型调研时。
parent: ./index.md
paths:
- '*.java'
- '*.py'
- '*.md'
triggers:
  keywords:
  - 向量数据库对比
  - 向量库选型
  - Milvus
  - Qdrant
  - pgvector
  - Pinecone
  - vector database
effort: medium
context: inline
version: '1.0'
---
# 向量库 · 六款横向对比

> 本条只管「六款各维度差异」。**该选哪一款**走决策树见 [`decision-tree.md`](./decision-tree.md)；选定后索引怎么建见 [`index-and-filter.md`](./index-and-filter.md)。

## 对比表

| 维度 | Milvus | Qdrant | Weaviate | pgvector | Pinecone | Chroma |
|---|---|---|---|---|---|---|
| 语言 | C++/Go | Rust | Go | C(PG扩展) | 闭源SaaS | Python/JS |
| 部署 | 自托管/Zilliz | 自托管/Cloud | 自托管/Cloud | 任意PG | 仅全托管 | 内嵌/server |
| 推荐量级 | 十亿级 | 亿级 | 亿级 | 百万级(≤~5M) | 十亿级 | 十万级(原型) |
| 索引 | IVF/HNSW/DiskANN/GPU | HNSW+量化 | HNSW | HNSW/IVFFlat | 托管 | HNSW简化 |
| 标量过滤 | 强(强类型+partition) | 强(payload索引) | 支持 | 最强(原生SQL join/事务) | 支持 | 简单 |
| 混合检索 | 稀疏+稠密 | 稀疏+稠密+RRF | 内置BM25+向量 | 需配PG tsvector自拼 | sparse-dense | 不内置 |
| 运维 | 高(etcd/MinIO/MQ) | 中(单二进制) | 中 | 低(复用PG) | 极低(全托管) | 极低 |

## 怎么读这张表

| 你最看重 | 看哪几列 |
|---|---|
| 不想运维 | 部署 + 运维（Pinecone 全托管 / Chroma 内嵌最省） |
| 复杂标量过滤是核心 | 标量过滤（pgvector 原生 SQL 最强，Qdrant payload 索引次之） |
| 要原生混合检索 | 混合检索（Weaviate 内置 BM25，Qdrant 带 RRF，pgvector 需自拼） |
| 数据量未来会到十亿级 | 推荐量级 + 索引（Milvus 支持 DiskANN/GPU） |

## 量级参考（须自测）

| 库 | 场景 | 中位延迟 |
|---|---|---|
| pgvector | 百万级、建议 ≤500 万 | 5-50ms |
| Chroma | 10 万 / 384 维 | ~20ms |
| 专用库(Qdrant/Milvus) | 1M-10M | 10-100ms |

> 以上为第三方基准的**量级参考**，受维度/索引参数/硬件影响极大，必须自测后定参。

## 自检

- [ ] 是否按「部署 + 运维」评估了团队能承担的运维成本？
- [ ] 标量过滤 / 混合检索是不是核心需求，对应列是否满足？
- [ ] 推荐量级是否覆盖未来 1-2 年数据增长？
- [ ] 引用的延迟数字是否标注为「量级参考、需自测」？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`decision-tree.md`](./decision-tree.md)（到底选哪一款）
- 兄弟：[`index-and-filter.md`](./index-and-filter.md)（索引与过滤怎么建）
