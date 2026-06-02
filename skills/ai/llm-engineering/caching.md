---
name: ai-llm-caching
description: LLM 三层缓存 — 精确匹配普通缓存（FAQ 可省 80%+ 调用）、按语义命中跳过模型的语义缓存、供应商 prompt caching 降长前缀成本。Use when 给 LLM 调用省 token/降延迟 / 设计缓存层 / 评审重复调用时。
parent: ./index.md
paths:
- '*.java'
- '*.py'
- '*.md'
triggers:
  keywords:
  - LLM 缓存
  - 语义缓存
  - prompt caching
  - 精确缓存
  - semantic cache
  - 缓存命中
effort: medium
context: inline
version: '1.0'
---
# LLM · 缓存（普通 + 语义 + prompt caching）

> 本条只管「怎么缓存省成本」。成本核算见 [`rate-limit-token.md`](./rate-limit-token.md)；缓存作降级兜底见 [`retry-degradation.md`](./retry-degradation.md)。

## 规则

| 层 | 机制 | 适用 |
|----|------|------|
| 普通缓存 | key = 规范化输入精确哈希，命中直接返回，**不调模型** | 高频重复问法（FAQ 可省 **80%+** 调用） |
| 语义缓存 | 对输入向量化，与历史问题**语义相似**即返回缓存答案 | 问法多变但语义重复（"怎么退款"≈"如何申请退货"） |
| prompt caching | 用**供应商**的 prompt 缓存，复用长系统提示/上下文前缀，降 input token 成本 | 长且固定的 system prompt、RAG 大上下文 |

附加约束：缓存必须设 TTL 与失效策略（prompt 版本变更即失效）；语义缓存要设相似度阈值并防"近似但答案不同"误命中；含个性化/时效性的请求不缓存。

## 正例：先精确、再语义、最后才调模型

```java
// ✅ 三级穿透：精确缓存 → 语义缓存 → 模型；命中即省整次调用
final String key = normalize(req.question());
return exactCache.get(key)
    .or(() -> semanticCache.find(req.embedding(), THRESHOLD))   // 语义相似命中
    .orElseGet(() -> {
        final String ans = llm.call(req);                        // 都没命中才调模型
        exactCache.put(key, ans, TTL);
        return ans;
    });
```

## 反例：每次都打模型 / 语义缓存无阈值

```java
// ❌ FAQ 也每次打模型，80% 成本本可省掉
return llm.call(req);
// ❌ 语义缓存不设相似度阈值，"退款" 命中 "退货" 答案，给错答案
return semanticCache.nearest(req.embedding());
```

## 自检

- [ ] 高频精确重复走普通缓存，没每次打模型？
- [ ] 语义缓存设了相似度阈值，防近似误命中？
- [ ] 长固定前缀用了供应商 prompt caching？
- [ ] 缓存有 TTL，prompt 版本变更即失效？个性化/时效请求不缓存？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`rate-limit-token.md`](./rate-limit-token.md)（cached token 单独计价）
- 兄弟：[`prompt-management.md`](./prompt-management.md)（prompt 版本变更要失效缓存）
