---
name: ai-llm-structured-output
description: 需要可解析结果时强制用 JSON schema / function calling 约束模型输出，并对每次响应做 schema 校验（校验失败率是模型回归的先行指标）。Use when 让 LLM 返回结构化数据 / 解析模型 JSON 老报错 / 评审输出校验时。
parent: ./index.md
paths:
- '*.java'
- '*.py'
- '*.md'
triggers:
  keywords:
  - 结构化输出
  - JSON schema
  - schema 校验
  - function calling
  - 输出解析
  - structured output
effort: medium
context: inline
version: '1.0'
---
# LLM · 结构化输出与 schema 校验

> 本条只管「输出怎么结构化 + 校验」。prompt 里的格式约束见 [`prompt-management.md`](./prompt-management.md)；工具调用循环见 [`../agent-mcp/function-calling.md`](../agent-mcp/function-calling.md)。

## 规则

| 维度 | 要求 |
|------|------|
| 强约束输出 | 要可解析结果时，用供应商的 **JSON schema / structured output / function calling**，而非只在 prompt 里"请返回 JSON"靠运气 |
| 每次必校验 | 对**每条响应**按 schema 校验（字段、类型、枚举、必填）；不要 `JSON.parse` 后直接信任 |
| 校验失败处理 | 失败时按需修复重试一次或走降级，**绝不**把不合法结构透传给下游 |
| 失败率即指标 | schema 校验失败率上升是**模型/prompt 回归的先行指标**，纳入监控与告警 |
| schema 收窄 | schema 尽量收窄（枚举代替自由字符串、限定长度），收窄越多模型越难跑偏 |

## 正例：function calling + 强校验（Java）

```java
// ✅ 用 schema 约束 + 反序列化即校验，失败不透传
final ChatResponse resp = chatClient.prompt().user(q)
    .options(toolSchema)            // 声明 JSON schema / tool
    .call().chatResponse();
final OrderResult result = jsonMapper.readValue(resp.content(), OrderResult.class);
SchemaValidator.assertValid(result);          // 字段/枚举/必填校验
metrics.recordSchemaCheck(true);
```

## 反例：prompt 求 JSON + 裸 parse

```java
// ❌ 只在 prompt 写"返回 JSON"，模型偶发夹带解释文字 → parse 抛错或脏数据透传
String text = chatClient.prompt().user("返回 JSON：" + q).call().content();
OrderResult r = jsonMapper.readValue(text, OrderResult.class);  // 无 schema 校验
return r;   // 不合法结构直接流向下游
```

## 自检

- [ ] 用了 JSON schema / function calling 强约束，而非只靠 prompt 文字？
- [ ] 每条响应都按 schema 校验了字段/类型/枚举/必填？
- [ ] 校验失败走修复重试或降级，没把脏结构透传下游？
- [ ] schema 校验失败率进了监控（作回归先行指标）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`prompt-management.md`](./prompt-management.md)（prompt 里的格式约束）
- 相关：[`../agent-mcp/function-calling.md`](../agent-mcp/function-calling.md)（工具调用即结构化输出的一种）
