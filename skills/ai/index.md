---
name: ai-index
description: AI 应用开发维度 — 向量库选型 / LLM 框架 / RAG 工程 / LLM 调用规范 / Agent 与 MCP。Use when 做 RAG / 调 LLM API / 写 Agent / 选向量库或 AI 框架时。
parent: ../index.md
children:
  - { name: vector-db, path: vector-db/index.md, tag: folder, note: "向量库选型(Milvus/Qdrant/pgvector/Pinecone...) / 索引与过滤" }
  - { name: llm-framework, path: llm-framework/index.md, tag: folder, note: "Spring AI vs LangChain4j 选型" }
  - { name: rag, path: rag/index.md, tag: folder, note: "切分 / embedding 选型 / 混合检索 / 防幻觉" }
  - { name: llm-engineering, path: llm-engineering/index.md, tag: folder, note: "prompt 管理 / 流式 SSE / 限流 / 重试降级 / 结构化输出 / 缓存 / 可观测" }
  - { name: agent-mcp, path: agent-mcp/index.md, tag: folder, note: "function calling / MCP 协议 / 多轮记忆" }
when_to_descend: |
  任务涉及 AI 应用集成：选向量库 / 选 Spring AI 或 LangChain4j / 做 RAG（切分/embedding/检索）/ 调 LLM（流式/限流/重试/结构化输出）/ 写 Agent / 用 MCP。
---

# AI · 应用开发维度

> Java/Spring 后端做 AI 应用集成（RAG / Agent / LLM 调用）的选型与工程规范。
> 性能/量级数字为业界基准参考，落地前需用自有数据集复测。

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| vector-db | 文件夹 | 向量库选型 + 索引/过滤（3 子项） |
| llm-framework | 文件夹 | Spring AI vs LangChain4j（1 子项） |
| rag | 文件夹 | 切分 / embedding / 混合检索 / 防幻觉（4 子项） |
| llm-engineering | 文件夹 | prompt / SSE / 限流 / 重试 / 结构化 / 缓存 / 可观测（7 子项） |
| agent-mcp | 文件夹 | function calling / MCP / 记忆（3 子项） |

## 下钻决策表

| 你在做什么 | 进哪个 |
|-----------|-------|
| 给 RAG 选向量库 / 定索引与过滤 | vector-db |
| 选 Java 侧 LLM 框架 | llm-framework |
| 搭 RAG：切分、选 embedding、混合检索、防幻觉 | rag |
| 调 LLM API：流式、限流、重试、结构化输出、缓存、监控 | llm-engineering |
| 写 Agent / 用工具调用 / 接 MCP / 做记忆 | agent-mcp |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行维度：[`../lang/index.md`](../lang/index.md) · [`../framework/index.md`](../framework/index.md) · [`../tech-selection/index.md`](../tech-selection/index.md) · [`../design-pattern/index.md`](../design-pattern/index.md) · [`../habit/index.md`](../habit/index.md) · [`../fundamentals/index.md`](../fundamentals/index.md)
- 向量库选型也可对照：[`../tech-selection/database/index.md`](../tech-selection/database/index.md)（pgvector 复用 PostgreSQL）
