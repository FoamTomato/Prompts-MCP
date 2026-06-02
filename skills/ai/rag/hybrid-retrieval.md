---
name: ai-rag-hybrid-retrieval
description: RAG 混合检索规约 — 向量+BM25 用 RRF 融合，再用 cross-encoder/ColBERT 重排并强制 top-k 限制。Use when 设计 RAG 检索召回 / 加 rerank / 排查召回不准时。
parent: ./index.md
paths:
- '*.java'
- '*.py'
- '*.md'
triggers:
  keywords:
  - 混合检索
  - 重排
  - RRF 融合
  - hybrid retrieval
  - BM25
  - cross-encoder rerank
effort: medium
context: inline
version: '1.0'
---
# RAG · 混合检索与重排

> 本条只管「召回+融合+重排」。chunk 怎么切见 [`chunking.md`](./chunking.md)；用什么 embedding 见 [`embedding-selection.md`](./embedding-selection.md)；回答约束见 [`anti-hallucination.md`](./anti-hallucination.md)。

## 规则

| 环节 | 推荐 | 规约级别 |
|---|---|---|
| 默认检索 | **向量 + BM25 混合**，不要只走纯向量 | 应成规约 |
| 融合 | 两路结果用 **RRF（Reciprocal Rank Fusion）** 融合 | 应成规约 |
| 重排 | cross-encoder / ColBERT 重排，**强制 top-k 限制**（神经重排延迟高） | 应成规约 |
| 上下文组装 | 回传 parent chunk + 元数据，控总 token，按相关度裁剪 | 应成规约 |

## 标准流水线

1. **向量召回** top-N（语义相似）。
2. **BM25 召回** top-N（关键词/精确匹配，补向量漏的术语/专名）。
3. **RRF 融合**两路排名，按融合分取候选集。
4. **rerank**：cross-encoder 对候选集重排，**只取 top-k**（如 top-5）进上下文。
5. **组装**：回传 parent chunk + 元数据，控总 token。

混合 + 重排相比纯向量可显著降幻觉（第三方基准 >40%，须自测）。

## 反例

- ❌ 只用纯向量召回 → 专有名词/编号类查询漏召回，BM25 本可补上。
- ❌ rerank 不限 top-k、把几百条都重排 → 延迟爆炸（神经重排逐对打分很慢）。
- ❌ 召回多少就喂多少给模型 → 上下文超长、噪声多、成本高，应按相关度裁剪。

## 自检

- [ ] 默认走向量 + BM25 混合，而非纯向量？
- [ ] 两路用 RRF 融合？
- [ ] rerank 强制了 top-k 限制（控延迟）？
- [ ] 上下文回传 parent chunk + 元数据并按相关度裁剪、控总 token？
- [ ] 引用的「降幻觉 >40%」标注为量级参考、需自测？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`embedding-selection.md`](./embedding-selection.md)（向量来自哪个模型）
- 兄弟：[`anti-hallucination.md`](./anti-hallucination.md)（检索到的上下文怎么约束回答）
