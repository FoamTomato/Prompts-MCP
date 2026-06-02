---
name: ai-agent-function-calling
description: agent 执行底座是 tool use 循环（模型选工具→调用→看结果→再循环），必须给循环设最大步数与 token 上限防失控烧钱，并校验工具结果。Use when 写 agent 循环 / 接 function calling / 评审 agent 失控风险时。
parent: ./index.md
paths:
- '*.java'
- '*.py'
- '*.md'
triggers:
  keywords:
  - tool use
  - function calling
  - agent 循环
  - 最大步数
  - 失控防护
  - 工具调用
effort: high
context: inline
version: '1.0'
---
# Agent · function calling / tool use 循环

> 本条只管「工具调用循环与防护」。工具如何被标准化暴露见 [`mcp-protocol.md`](./mcp-protocol.md)；输出 schema 校验见 [`../llm-engineering/structured-output.md`](../llm-engineering/structured-output.md)。

## 规则

| 维度 | 要求 |
|------|------|
| 循环本质 | tool use = 模型**决定调哪个工具 → 执行 → 把结果喂回 → 再决定**，循环至产出终态。这是 agent 的执行底座 |
| 必设步数上限 | agent 自主循环必须设**最大步数(max steps)**，到顶强制停，防死循环反复调工具 |
| 必设 token 上限 | 必须设**单次任务 token / 成本上限**，超限即中断，防自主循环无声烧钱 |
| 工具结果校验 | 工具返回当作不可信输入校验（类型/范围/越权），不直接回灌模型或执行 |
| 权限隔离 | 工具按租户/partition 隔离，agent 只能访问授权范围，越权直接拒绝 |
| 错误可终止 | 工具连续失败要能熔断/上抛，不能让循环空转到耗尽预算 |

## 正例：带上限的 tool 循环

```java
// ✅ 步数 + 成本双上限，工具结果校验后才回灌
int step = 0;
while (step++ < MAX_STEPS && budget.remaining() > 0) {
    final var resp = llm.call(ctx);                 // 模型决定下一步
    if (resp.isFinal()) return resp.answer();       // 产出终态，退出
    final ToolResult r = tools.invoke(resp.toolCall(), tenantId);  // 带权限隔离
    ToolResultValidator.assertSafe(r);              // 结果校验，不盲目回灌
    budget.charge(resp.usage());                    // 计入 token 成本
    ctx = ctx.append(r);
}
return degrade();                                   // 触顶降级，不无限循环
```

## 反例：无上限的 while(true)

```java
// ❌ 没有步数/成本上限：模型反复调工具就能把账单和时间烧穿
while (true) {
    var resp = llm.call(ctx);
    if (resp.isFinal()) return resp.answer();
    ctx = ctx.append(tools.invoke(resp.toolCall()));  // 结果不校验、无权限隔离
}
```

## 自检

- [ ] 循环有最大步数上限，触顶强制停？
- [ ] 有单任务 token/成本上限，超限中断？
- [ ] 工具结果当不可信输入做了校验，没直接回灌/执行？
- [ ] 工具按租户/partition 权限隔离，越权拒绝？
- [ ] 工具连续失败能熔断，不空转烧预算？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`mcp-protocol.md`](./mcp-protocol.md)（工具如何被标准化发现与描述）
- 相关：[`../llm-engineering/structured-output.md`](../llm-engineering/structured-output.md)（工具调用是结构化输出）
- 相关：[`../llm-engineering/retry-degradation.md`](../llm-engineering/retry-degradation.md)（循环里的熔断降级）
