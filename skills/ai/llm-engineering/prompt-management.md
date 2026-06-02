---
name: ai-llm-prompt-management
description: prompt 工程化 — 模板外置不硬编码、每版打版本号且 trace 关联版本、模板内显式写格式/范围/语气/长度约束。Use when 写 LLM prompt / 调 prompt 又怕回归 / 评审硬编码 prompt 字符串时。
parent: ./index.md
paths:
- '*.java'
- '*.py'
- '*.md'
triggers:
  keywords:
  - prompt 版本化
  - 模板外置
  - prompt 约束
  - prompt template
  - prompt versioning
  - 输出约束
effort: medium
context: inline
version: '1.0'
---
# LLM · prompt 管理（版本化 + 外置 + 约束）

> 本条只管「prompt 怎么管」。追踪/归集见 [`observability.md`](./observability.md)；强制结构化结果见 [`structured-output.md`](./structured-output.md)。

## 规则

| 维度 | 要求 |
|------|------|
| 模板外置 | prompt 一律放配置/模板文件（如 `.md` / `prompt-store`），**禁止硬编码在 Java 字符串里拼接** |
| 版本化 | 每次改 prompt 都升版本号（`order-summary@v3`）；每条调用 trace 记录所用版本，便于回滚与 A/B |
| 显式约束 | 模板内写清四类约束：**格式**（JSON/Markdown）、**范围**（仅依据上下文）、**语气**、**长度**（字数/条数上限） |
| 变量占位 | 业务数据用占位符注入，不与指令文本混排，防注入与漏填 |
| 变更即复测 | prompt 改动视同代码变更，过评测集再发版（schema 校验失败率是回归先行指标） |

## 正例：模板外置 + 显式约束（模板文件）

```text
# order-summary@v3
你是订单客服助手。仅依据【上下文】回答，无依据时回复"暂无相关信息"。
输出格式：JSON，字段 {summary:string, items:string[]}。
长度约束：summary 不超过 50 字，items 不超过 5 条。语气：简洁中性。
【上下文】
{{context}}
【问题】
{{question}}
```

## 反例：硬编码 + 无约束

```java
// ❌ prompt 拼在代码里，改一版要发布；没版本号无法回滚；没格式/长度约束，输出发散
String prompt = "帮我总结这个订单：" + order.toString();
chatClient.call(prompt);
```

## 自检

- [ ] prompt 在模板文件里，代码只做变量注入，没有字符串拼接指令？
- [ ] 模板有版本号，且每条 trace 关联了所用版本？
- [ ] 模板写清了格式 / 范围 / 语气 / 长度四类约束？
- [ ] 业务数据走占位符，未与指令混排？
- [ ] prompt 改动过了评测集才发版？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`structured-output.md`](./structured-output.md)（格式约束怎么强制校验）
- 兄弟：[`observability.md`](./observability.md)（trace 关联 prompt 版本）
