---
name: ai-rag-embedding
description: RAG embedding 选型规约 — 自托管首选 BGE-M3/BGE-large、API 用 OpenAI/Cohere，两条路线二选一并锁定版本，变更必须全量重建索引。Use when 选 embedding 模型 / 升级嵌入版本 / 评审检索一致性时。
parent: ./index.md
paths:
- '*.java'
- '*.py'
- '*.md'
triggers:
  keywords:
  - 嵌入模型选型
  - 版本锁定
  - 全量重建
  - embedding
  - BGE-M3
  - Cohere
effort: medium
context: inline
version: '1.0'
---
# RAG · Embedding 选型

> 本条只管「选哪个 embedding + 版本怎么管」。文档怎么切见 [`chunking.md`](./chunking.md)；embed 后怎么检索见 [`hybrid-retrieval.md`](./hybrid-retrieval.md)。

## 两条路线（二选一）

| 路线 | 推荐 | 适用 |
|---|---|---|
| **自托管** | BGE-M3（dense+sparse+多向量 / 100+ 语言 / 8192 token）或 BGE-large | 数据不出域、量大要控成本、要 sparse 做混合 |
| **API** | OpenAI / Cohere embedding | 起步快、不想运维、量级可控 |
| 中文场景 | 可评估 BCE 等中文优化模型 | 中文为主、需复测召回 |

选型规约：在「自托管 vs API」**先二选一**，依据是数据合规 + 成本 + 是否需要 sparse 向量，而非单看榜单分数。

## 版本管理（强约束）

| 规则 | 要求 |
|---|---|
| 版本锁定 | embedding 模型 + 版本写进配置并锁定，记录维度 |
| 变更全量重建 | **换模型/换版本/换维度 → 必须全量重建整个索引**，新旧向量不可混存 |
| 查询侧一致 | 查询用的 embedding 必须与入库时**同模型同版本**，否则向量空间不一致 |

## 反例

- ❌ 升级 embedding 版本只重建新文档、旧向量不动 → 新旧向量空间不一致，召回错乱。
- ❌ 入库用 BGE-M3、查询临时换成 OpenAI → 两套向量空间，相似度毫无意义。
- ❌ 选型只看「谁榜分高」不看数据合规 → 敏感数据被迫走外部 API。

## 自检

- [ ] 在「自托管 vs API」两条路线里明确选定了一条（依据合规+成本+sparse 需求）？
- [ ] embedding 模型+版本+维度已写进配置并锁定？
- [ ] 升级版本时是否触发了**全量重建**而非增量？
- [ ] 查询侧与入库侧用的是同模型同版本？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`chunking.md`](./chunking.md)（embed 前怎么切块）
- 兄弟：[`hybrid-retrieval.md`](./hybrid-retrieval.md)（embed 后怎么检索）
