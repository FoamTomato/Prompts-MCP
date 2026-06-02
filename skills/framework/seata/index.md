---
name: framework-seata-index
description: Seata 分布式事务 4 项 — AT 自动回滚 / TCC 业务侵入 / Saga 长事务状态机 / 三模式选型与全局事务注解。Use when 跨服务保证数据一致 / 选 Seata 事务模式 / 写全局事务注解 / 评审分布式事务 PR 时。
parent: ../index.md
children:
  - { name: seata-at-mode, path: at-mode.md, tag: skill, note: "AT 模式：无侵入、自动反向 SQL 回滚、需 undo_log 表，默认首选" }
  - { name: seata-tcc-mode, path: tcc-mode.md, tag: skill, note: "TCC：Try-Confirm-Cancel 业务侵入、高性能，适合核心交易" }
  - { name: seata-saga-mode, path: saga-mode.md, tag: skill, note: "Saga：长事务状态机，适合流程长、参与方多的业务" }
  - { name: seata-mode-selection, path: mode-selection.md, tag: skill, note: "@GlobalTransactional 与三模式选型：一般 AT / 高性能核心 TCC / 长流程 Saga" }
when_to_descend: 跨服务/跨库要保证数据一致、选 Seata 事务模式、写全局事务边界或评审分布式事务实现时。
---

# Seata · 分布式事务索引

> 性能/侵入性描述是**量级与定性参考**，落地需结合自身业务压测。
> 单库内事务用本地 `@Transactional` 即可，**不要**为单库引入 Seata。

Seata 三种事务模式 + 选型拆成 4 个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 跨服务一致性，业务无侵入、想自动回滚（绝大多数场景） | [at-mode](at-mode.md) |
| 核心交易（下单扣款），要高性能、可接受写 Try/Confirm/Cancel | [tcc-mode](tcc-mode.md) |
| 流程长、参与方多（如审批、履约编排），按状态机串联 | [saga-mode](saga-mode.md) |
| 不确定选哪种模式、要在哪标 `@GlobalTransactional` | [mode-selection](mode-selection.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 单库事务边界（不跨服务时优先看）：[`../mysql/transaction/transaction-scope.md`](../mysql/transaction/transaction-scope.md)
- 分布式 MQ 最终一致方案对比：[`../../tech-selection/message-queue/index.md`](../../tech-selection/message-queue/index.md)
