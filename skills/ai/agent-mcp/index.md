---
name: ai-agent-mcp-index
description: Agent 与 MCP 三件事 — function calling/tool use 循环与失控防护 / MCP 协议与传输与 Java 角色 / 多轮记忆分层与隐私。Use when 构建 agent / 接入 MCP 工具 / 评审 agent 循环与记忆方案时。
parent: ../index.md
children:
  - { name: function-calling, path: function-calling.md, tag: skill, note: "tool use 循环 + agent 必设最大步数/token 上限防失控" }
  - { name: mcp-protocol, path: mcp-protocol.md, tag: skill, note: "MCP 是什么 + 与 function calling 关系 + stdio/Streamable HTTP + Java 角色" }
  - { name: memory, path: memory.md, tag: skill, note: "短期会话 + 长期持久化记忆分层 + 清理/隐私" }
when_to_descend: 在构建 agent、接入或暴露 MCP 工具、设计多轮记忆
---

# Agent & MCP · 子项索引

Agent 与 MCP 拆成三个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 让模型调工具、写 agent 执行循环、防它失控烧钱 | [function-calling](function-calling.md) |
| 接入或暴露 MCP 工具、选传输、定 Java 角色 | [mcp-protocol](mcp-protocol.md) |
| 给多轮对话设计短期/长期记忆与清理策略 | [memory](memory.md) |

> agent 自主循环天然有失控风险，**最大步数 / token 上限 / 权限隔离**是硬约束，不是可选项。
