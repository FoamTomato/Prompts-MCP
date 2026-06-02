---
name: ai-rag-chunking
description: RAG 文档切分规约 — 默认 recursive 512 token 并记录 size/overlap，复杂文档用父子块，切分前为 chunk 保留元数据。Use when 设计 RAG 切分策略 / 调 chunk 大小 / 处理长文档时。
parent: ./index.md
paths:
- '*.java'
- '*.py'
- '*.md'
triggers:
  keywords:
  - 文档切分
  - 父子块
  - 切分策略
  - chunking
  - recursive splitter
  - chunk overlap
effort: medium
context: inline
version: '1.0'
---
# RAG · 文档切分策略

> 本条只管「怎么切块」。chunk 用哪个模型 embed 见 [`embedding-selection.md`](./embedding-selection.md)；切完怎么检索见 [`hybrid-retrieval.md`](./hybrid-retrieval.md)。

## 规则

| 场景 | 推荐 | 规约级别 |
|---|---|---|
| 默认切分 | **recursive 512 token**，记录 size/overlap 进配置 | 应成规约 |
| 复杂/长文档 | **父子块**：child 128-256 token 用于检索 → 命中后回传 parent 512-1024 token | 应成规约 |
| chunk 元数据 | embed **前**为每块保留 title/section/page | 应成规约 |
| 语义切分 | 慎用（基准召回仅 ~54%、易碎片过短），除非专业领域 | 视场景 |

## 父子块怎么工作

1. 按小粒度（child 128-256 token）切块并 embed，**检索精度高**。
2. 命中 child 后，不直接喂 child，而是回传其所属 parent（512-1024 token），**上下文更完整**。
3. parent/child 用稳定 id 关联，元数据随块带。

## 反例

- ❌ 切分参数硬编码、不记录 size/overlap → 换参数后无法复现检索质量，回归无从定位。
- ❌ 直接上语义切分当默认 → 碎片过短、召回掉，违反「慎用语义切分」。
- ❌ embed 后才补元数据 → title/section 没进向量上下文，过滤与引用都缺字段。

## 自检

- [ ] 默认用 recursive 512 token，且 size/overlap 写进配置可复现？
- [ ] 长/复杂文档用了父子块（child 检索、parent 回传）？
- [ ] chunk 在 embed **前**就带了 title/section/page 元数据？
- [ ] 没有把语义切分当默认（仅专业领域且自测后才用）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`embedding-selection.md`](./embedding-selection.md)（chunk 用什么模型 embed）
- 兄弟：[`hybrid-retrieval.md`](./hybrid-retrieval.md)（切完怎么检索）
