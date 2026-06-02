---
name: ai-agent-memory
description: 多轮对话记忆分层 — 短期(会话内 ChatMemory，控窗口)与长期(跨会话持久化，如 Spring AI AutoMemoryTools)分开管，并配清理与隐私脱敏策略。Use when 设计 agent 多轮记忆 / 做跨会话记忆 / 评审记忆留存与隐私时。
parent: ./index.md
paths:
- '*.java'
- '*.py'
- '*.md'
triggers:
  keywords:
  - 多轮记忆
  - 记忆分层
  - ChatMemory
  - 长期记忆
  - 记忆隐私
  - conversation memory
effort: medium
context: inline
version: '1.0'
---
# Agent · 多轮记忆分层

> 本条只管「记忆怎么分层与治理」。工具调用循环见 [`function-calling.md`](./function-calling.md)。

## 规则

| 层 | 是什么 | 载体 / 例 |
|----|--------|----------|
| 短期记忆 | 单次会话内的上下文，会话结束即可丢 | ChatMemory / 会话窗口缓冲 |
| 长期记忆 | 跨会话持久化的用户偏好/事实/历史结论 | 持久存储（如 Spring AI **AutoMemoryTools** 跨会话） |

附加规约：

| 维度 | 要求 |
|------|------|
| 短期控窗口 | 短期记忆按 token/轮数滚动裁剪或摘要，**别无限拼接**进 prompt（否则撑爆上下文 + 烧 token） |
| 长期要召回 | 长期记忆按相关度检索后注入，不整库灌入；写入要去重 |
| 清理策略 | 两层都设 TTL / 容量上限 / 失效规则，到期清理 |
| 隐私脱敏 | 落库的记忆对 PII 脱敏；提供按用户**删除/导出**能力，遵守留存合规 |
| 隔离 | 记忆按用户/租户隔离，绝不跨用户串记忆 |

## 正例：短期滚动 + 长期检索注入

```java
// ✅ 短期：限轮数滚动；长期：按相关度召回再注入
final ChatMemory shortTerm = MessageWindowChatMemory.builder()
    .maxMessages(20).build();                         // 控窗口，超出滚动
final List<Memory> recalled = longTermStore
    .search(userId, query, TOP_K);                    // 长期按相关度召回，非整库灌
ctx.system(MemoryFormatter.format(recalled));         // 注入精选记忆
ctx.history(shortTerm.get(sessionId));
```

## 反例：单层无限拼接 + 不隔离

```java
// ❌ 把整段历史无限拼进 prompt：上下文越滚越大，token 成本飙升、还触模型上限
String prompt = allHistory.stream().collect(joining("\n")) + "\n" + question;
// ❌ 记忆不按用户隔离 → A 的偏好串到 B，且 PII 未脱敏落库
memoryStore.put("global", question);
```

## 自检

- [ ] 短期与长期记忆分开管理，职责清晰？
- [ ] 短期记忆按窗口/轮数滚动裁剪或摘要，没无限拼接？
- [ ] 长期记忆按相关度召回注入，不整库灌入？
- [ ] 两层都有 TTL/容量上限与清理策略？
- [ ] 记忆按用户/租户隔离，PII 脱敏并支持删除/导出？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`function-calling.md`](./function-calling.md)（记忆作为循环上下文的一部分）
- 相关：[`../llm-engineering/rate-limit-token.md`](../llm-engineering/rate-limit-token.md)（记忆拼接影响 token 成本）
