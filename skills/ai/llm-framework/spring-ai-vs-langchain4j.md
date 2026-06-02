---
name: ai-spring-ai-vs-langchain4j
description: Java LLM 框架 Spring AI 与 LangChain4j 选型 — 定位差异、各自适用栈、多模型对接与 MCP 支持，按贴合现有栈选。Use when 选 Java LLM 框架 / 评审 Spring AI 或 LangChain4j 选型时。
parent: ./index.md
paths:
- '*.java'
- '*.py'
- '*.md'
triggers:
  keywords:
  - LLM 框架选型
  - 框架贴合栈
  - Spring AI
  - LangChain4j
  - ChatClient
  - MCP 支持
effort: medium
context: inline
version: '1.0'
---
# Java LLM 框架 · Spring AI vs LangChain4j

> 两者均 2025-05 GA、均支持 MCP。本条只回答「该选哪个框架」。向量库选型见 [`../vector-db/index.md`](../vector-db/index.md)；RAG 工程规范见 [`../rag/index.md`](../rag/index.md)。

## 对比表

| 维度 | Spring AI | LangChain4j |
|---|---|---|
| 定位 | Spring 生态原生 | 框架无关的 Java 工具箱 |
| 最佳栈 | Spring Boot | Quarkus / 任意 Java / 要最大灵活 |
| 集成方式 | auto-config / DI / Actuator 开箱 | 轻量可插拔，供应商覆盖最广 |
| RAG | ETL + QuestionAnswerAdvisor | DocumentSplitter/EmbeddingStore/ContentRetriever 细粒度 |
| Agent | Advisor+Tool，AutoMemoryTools 持久记忆 | langchain4j-agentic / a2a |
| 多模型对接 | 各家 starter，统一 `ChatClient` | 各家 module，覆盖最广 |
| MCP | MCP Server/Client Boot Starter | MCP Client（Streamable HTTP + stdio） |

## 选型决策

| 你的现状 | 选 |
|---|---|
| 已是 Spring Boot 项目 | **Spring AI**（auto-config/DI 顺滑，统一 ChatClient） |
| Quarkus / 非 Spring / 要最广供应商覆盖 | **LangChain4j**（框架无关、模块化） |
| 要细粒度控制 RAG 各环节 | LangChain4j（splitter/store/retriever 可单独替换） |
| 要 Spring 风格 RAG 流水线 + Actuator 可观测 | Spring AI |

核心规约：按**「贴合现有栈」**选，不是「谁更强」。两者能力高度对齐，错配技术栈带来的胶水成本远大于框架本身差异。

## 正例：Spring AI 调用（流水线编排风格）

```java
// 业务方法写成编排器：前置校验早返回 / 每步一调用 / 中间变量 final
public AnswerVO ask(AskReq req) {
    // 前置校验
    if (req == null || !StringUtils.hasText(req.getQuestion())) {
        log.warn("ask req or question is blank");
        return null;
    }

    // 步骤1：检索上下文（向量库召回，逻辑下沉 retriever）
    final List<Document> context = retriever.retrieve(req.getQuestion());

    // 步骤2：调用模型，附上下文 advisor
    final String reply = chatClient.prompt()
            .user(req.getQuestion())
            .advisors(new QuestionAnswerAdvisor(vectorStore))
            .call().content();

    // 步骤3：组装返回
    return AnswerConvert.INSTANCE.toVO(reply, context);
}
```

## 反例

- ❌ Spring Boot 项目硬塞 LangChain4j 又手写一套 DI 胶水 → 放弃了 auto-config，徒增维护面。
- ❌ 以「谁基准跑分高」拍板 → 两者本质都封装同一批模型 API，跑分差异被错配栈的成本淹没。

## 自检

- [ ] 选型依据是「贴合现有栈」而非「谁更强」？
- [ ] Spring Boot 项目优先评估了 Spring AI？非 Spring 优先 LangChain4j？
- [ ] 确认目标框架支持你需要的模型供应商与 MCP 角色（Server/Client）？
- [ ] 给的业务方法遵循流水线编排（早返回 / 每步一调用 / final）？

## 相关

- 父：[`./index.md`](./index.md)
- 流水线编排风格：[`../../lang/java/pipeline-style/orchestration-method.md`](../../lang/java/pipeline-style/orchestration-method.md)
- 向量库选型：[`../vector-db/index.md`](../vector-db/index.md)
- RAG 工程规范：[`../rag/index.md`](../rag/index.md)
