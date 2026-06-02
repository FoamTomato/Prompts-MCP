---
name: ai-rag-anti-hallucination
description: RAG 防幻觉规约 — prompt 强制仅依据上下文回答、无依据就拒答说不知道、答案必须附引用来源。Use when 写 RAG 回答 prompt / 评审回答可信度 / 排查模型编造时。
parent: ./index.md
paths:
- '*.java'
- '*.py'
- '*.md'
triggers:
  keywords:
  - 防幻觉
  - 拒答
  - 引用来源
  - anti-hallucination
  - grounded answer
  - citation
effort: medium
context: inline
version: '1.0'
---
# RAG · 防幻觉与引用

> 本条只管「检索到上下文后，怎么约束模型回答」。怎么检索到上下文见 [`hybrid-retrieval.md`](./hybrid-retrieval.md)。

## 规则

| 规则 | 要求 |
|---|---|
| 仅据上下文 | prompt **强制**「只依据给定上下文回答，不得用上下文之外的知识」 |
| 缺据拒答 | 上下文无法支撑答案时，**明确说"不知道/资料中未找到"**，不许编 |
| 附引用 | 每条结论附来源引用（chunk id / title / page），可回溯 |
| 控注入风险 | 上下文来自外部文档时，做基本指令隔离，防 prompt 注入篡改约束 |

混合检索 + 重排是前置条件：上下文越准，仅据上下文回答的幻觉越低（第三方基准降 >40%，须自测）。

## prompt 骨架

```text
你是问答助手。只依据下面【上下文】回答问题。
若【上下文】不足以回答，直接说「资料中未找到相关信息」，不要编造。
每条结论后用 [来源:<title/page>] 标注引用。

【上下文】
{retrieved_chunks_with_metadata}

【问题】
{question}
```

## 反例

- ❌ prompt 没写「仅据上下文」→ 模型用训练知识补全，给出看似合理实则编造的答案。
- ❌ 没要求拒答 → 上下文缺失时强行回答，幻觉率飙升。
- ❌ 不附引用 → 用户无法核实，错误答案无法回溯定位。

## 自检

- [ ] prompt 明确「仅依据上下文回答」？
- [ ] 上下文不足时强制「拒答/说不知道」？
- [ ] 每条结论附可回溯引用（chunk id / title / page）？
- [ ] 外部文档上下文做了基本注入隔离？
- [ ] 「降幻觉 >40%」标注为量级参考、需自测？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`hybrid-retrieval.md`](./hybrid-retrieval.md)（上下文怎么检索出来）
