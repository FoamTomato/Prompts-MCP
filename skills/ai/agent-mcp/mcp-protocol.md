---
name: ai-agent-mcp-protocol
description: MCP 是 Anthropic 开放标准，标准化工具如何被发现描述（调用仍走 tool use），传输分 stdio 与 Streamable HTTP，Java 用 Spring AI 暴露、LangChain4j 消费。Use when 接入或暴露 MCP 工具 / 选传输 / 评审工具集成时。
parent: ./index.md
paths:
- '*.java'
- '*.py'
- '*.md'
triggers:
  keywords:
  - MCP
  - Model Context Protocol
  - stdio 传输
  - Streamable HTTP
  - MCP Server
  - 工具暴露
effort: high
context: inline
version: '1.0'
---
# Agent · MCP 协议与工程实践

> 本条只管「MCP 是什么 + 怎么接」。工具调用循环与防护见 [`function-calling.md`](./function-calling.md)。

## 是什么 · 与 function calling 的关系

| 点 | 说明 |
|----|------|
| MCP | **Model Context Protocol**，Anthropic 2024-11 开放标准；统一 AI 与外部工具/数据源的接入方式（2025-12 捐 Linux 基金会 Agentic AI Foundation） |
| 与 function calling 不冲突 | MCP 标准化的是"工具**如何被发现、描述、连接**"；模型实际**调用**仍走 tool use。MCP = 工具的"USB-C 接口"，function calling = 插上后怎么用 |
| 解决什么 | 没有 MCP 时每个工具各写各的对接（N×M 适配）；MCP 让一次按标准暴露的能力被任意 MCP 客户端复用 |

## 传输选型

| 传输 | 用于 | 说明 |
|------|------|------|
| **stdio** | 本地子进程 / CLI 工具 | 同机进程间，最简单，无网络；本仓这类 MCP server 即走 stdio |
| **Streamable HTTP** | 远程 / 生产 | 跨网络、可水平扩展、配合鉴权与网关；**生产远程接入推荐** |

## Java 角色

| 你要做 | 选 |
|--------|----|
| 把企业能力（查库/调 API/读文件）**暴露**为工具 | **Spring AI MCP Server** Boot Starter |
| **消费**外部 MCP 工具 | **LangChain4j MCP Client**（Streamable HTTP + stdio）或 Spring AI MCP Client |
| 多 agent / 工具**编排** | LangGraph4j / langchain4j-agentic |

## 工程实践（规约）

| 维度 | 要求 |
|------|------|
| 工具即能力，不硬编码 | 企业能力经 MCP 暴露为工具，别把外部调用硬编码进 agent 代码 |
| server 即 harness | MCP server 是模型外的"约束架"：精心设计**暴露哪些工具、工具描述怎么写**（描述就是路由信号），别一股脑全暴露撑爆上下文 |
| 工具描述要精准 | 工具 name + description 直接决定模型选不选它，写法等同 skill 的 description 路由——完整且仅覆盖该工具能力 |
| 权限与租户隔离 | server 侧按租户/partition 校验，客户端身份不可信；远程传输必上鉴权 |
| 结果校验 | server 返回与客户端接收都做结构校验，不互相盲信 |
| 最小暴露面 | 只暴露必要工具，敏感操作加二次确认或审批，降越权与误操作面 |

## 反例

```text
❌ 远程 MCP server 走 Streamable HTTP 却不加鉴权 → 任意客户端可调企业工具
❌ 一个 server 暴露 50 个工具、描述含糊 → 模型选错工具、上下文被工具清单撑爆
❌ 把"查订单"直接硬编码进 agent 代码而非作 MCP 工具 → 无法被其他 agent 复用、难治理
```

## 自检

- [ ] 工具经 MCP 暴露，没硬编码进 agent？
- [ ] 传输选对了（本地 stdio / 远程生产 Streamable HTTP）且远程上了鉴权？
- [ ] Java 角色选对（暴露用 Spring AI MCP Server / 消费用 LangChain4j MCP Client）？
- [ ] 工具描述精准（作路由信号），且只暴露必要工具不撑爆上下文？
- [ ] server 侧做了租户隔离 + 结果校验，不盲信客户端身份？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`function-calling.md`](./function-calling.md)（暴露后模型怎么循环调用）
- 相关：[`../llm-engineering/structured-output.md`](../llm-engineering/structured-output.md)（工具结果的 schema 校验）
