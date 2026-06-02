---
name: ai-vector-db-decision
description: 向量库选哪一款的决策树 — 原型/已有PG/零运维/自托管亿级/十亿级各走哪款 + 不要一上来上 Milvus 等规约条款。Use when 决定用哪个向量库 / 评审向量库选型是否过度 / 定迁移阈值时。
parent: ./index.md
paths:
- '*.java'
- '*.py'
- '*.md'
triggers:
  keywords:
  - 向量库决策树
  - 选型规约
  - 向量库迁移阈值
  - Chroma
  - Qdrant
  - pgvector
  - decision tree
effort: medium
context: inline
version: '1.0'
---
# 向量库 · 选型决策树

> 本条只管「按场景选哪一款 + 选型规约」。六款各维度细节见 [`comparison.md`](./comparison.md)；选定后索引怎么建见 [`index-and-filter.md`](./index-and-filter.md)。

## 决策树

按从上到下第一个命中的条件选库（命中即停）：

| 你的场景 | 选 | 理由 |
|---|---|---|
| 原型 / 本地 demo | **Chroma** | 内嵌零部署，十万级足够 |
| 已有 PostgreSQL 且 <5M、要与业务数据强一致/join | **pgvector** | 复用 PG，原生 SQL 过滤+事务 |
| 零运维 / Serverless | **Pinecone** | 全托管，无需自己运维 |
| 自托管 + 亿级 + 复杂标量过滤是核心 | **Qdrant** | 单二进制、payload 索引，性价比高 |
| 自托管 + 想 DB 直接 embed / 原生 BM25 hybrid | **Weaviate** | 内置向量化与 BM25 混合 |
| 生产十亿级 / GPU 索引 / 企业多租户 | **Milvus** | 量级最高，但运维最重 |

## 规约条款

| 条款 | 要求 |
|---|---|
| 不过度选型 | 原型用 Chroma/pgvector，**不要一上来就上 Milvus**（etcd/MinIO/MQ 运维重） |
| pgvector 上限 | 数据冲到数千万级，评估 pgvectorscale 或迁专用库（Qdrant/Milvus） |
| 迁移阈值 | 超 **5000 万** 行 或 云账单超 **~$500/月**，触发迁专用库评估 |
| 按需选不按名气 | 选型依据是「贴合量级+运维能力+过滤需求」，不是「谁更强/谁更火」 |

## 反例

- ❌ 百万级原型直接上 Milvus → 三个中间件（etcd/MinIO/消息队列）拖垮迭代速度，违反「不过度选型」。
- ❌ 已有 PG、量级才几十万，却新引专用库 → 数据双写、一致性成本远高于 pgvector。
- ❌ 选 Pinecone 但没算账 → 量级一大账单失控，应先比对「迁移阈值」条款。

## 自检

- [ ] 是否按决策树「第一个命中即停」选定了唯一一款？
- [ ] 原型阶段是否避免了直接上 Milvus？
- [ ] 是否定义了迁移触发阈值（5000 万行 / ~$500 月）？
- [ ] 选型理由是「贴合场景」而非「名气/性能榜」？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`comparison.md`](./comparison.md)（六款各维度对比）
- 兄弟：[`index-and-filter.md`](./index-and-filter.md)（选定后索引与过滤怎么建）
