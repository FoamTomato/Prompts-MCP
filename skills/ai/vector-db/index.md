---
name: ai-vector-db-index
description: 向量库三件事 — 六款选型对比 / 选哪一款的决策树规约 / 索引与元数据过滤怎么建。Use when 选型向量数据库 / 设计向量检索索引 / 评审 RAG 存储方案时。
parent: ../index.md
children:
  - { name: comparison, path: comparison.md, tag: skill, note: "Milvus/Qdrant/Weaviate/pgvector/Pinecone/Chroma 六维对比表" }
  - { name: decision-tree, path: decision-tree.md, tag: skill, note: "按量级/运维/已有栈选库的决策树 + 规约条款" }
  - { name: index-and-filter, path: index-and-filter.md, tag: skill, note: "HNSW/IVF/DiskANN 索引选型 + 过滤字段必建索引" }
when_to_descend: 在做向量库选型、索引设计或 RAG 存储评审
---

# Vector DB · 子项索引

向量库拆成三个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 横向了解六款向量库各维度差异 | [comparison](comparison.md) |
| 不知道该选哪一款（原型 / 已有 PG / 零运维 / 自托管亿级） | [decision-tree](decision-tree.md) |
| 已选定库，要决定用哪种索引、过滤字段怎么建 | [index-and-filter](index-and-filter.md) |

> 性能/量级数字均为第三方基准的**量级参考**，必须用自有数据集复测后定参。
