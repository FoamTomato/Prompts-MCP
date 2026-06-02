---
name: ai-rag-index
description: RAG 工程规范四件事 — 切分策略 / embedding 选型 / 混合检索与重排 / 防幻觉。Use when 设计 RAG 流水线 / 评审检索质量 / 排查回答幻觉时。
parent: ../index.md
children:
  - { name: chunking, path: chunking.md, tag: skill, note: "recursive 512 默认 / 父子块 / chunk 带元数据" }
  - { name: embedding-selection, path: embedding-selection.md, tag: skill, note: "BGE 自托管 vs API；版本锁定，变更全量重建" }
  - { name: hybrid-retrieval, path: hybrid-retrieval.md, tag: skill, note: "向量+BM25 用 RRF 融合 + cross-encoder rerank 限 top-k" }
  - { name: anti-hallucination, path: anti-hallucination.md, tag: skill, note: "仅据上下文回答 / 缺据拒答 / 附引用" }
when_to_descend: 在设计或评审 RAG 切分、嵌入、检索、防幻觉
---

# RAG · 子项索引

RAG 工程拆成四个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 决定文档怎么切块、chunk 带什么元数据 | [chunking](chunking.md) |
| 选 embedding 模型、定版本与重建策略 | [embedding-selection](embedding-selection.md) |
| 设计向量+BM25 融合与 rerank | [hybrid-retrieval](hybrid-retrieval.md) |
| 约束模型仅据上下文回答、附引用 | [anti-hallucination](anti-hallucination.md) |

> 检索质量数字（如「混合+重排降幻觉 >40%」）为第三方量级参考，须自有数据集复测。
