---
name: seata-mode-selection
description: Seata 三模式选型与全局事务边界 — 一般业务选 AT、高性能核心交易选 TCC、长流程选 Saga，发起方标 @GlobalTransactional。Use when 不确定用哪种 Seata 模式 / 决定在哪标全局事务 / 评审分布式事务选型时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 事务模式选型
  - 全局事务
  - 分布式事务选型
  - '@GlobalTransactional'
  - rollbackFor
  - 事务发起方
effort: medium
context: inline
version: '1.0'
---
# Seata · 模式选型与全局事务边界

> 本条只管「选哪种模式 + 注解标哪」。各模式细节见 [`at-mode.md`](./at-mode.md) / [`tcc-mode.md`](./tcc-mode.md) / [`saga-mode.md`](./saga-mode.md)。

## 规则

| 你的场景 | 选哪个 | 原因 |
|---------|-------|------|
| 一般跨服务业务、不想改业务代码 | **AT**（默认首选） | 无侵入、自动反向 SQL 回滚 |
| 高性能核心交易（扣款、扣库存） | **TCC** | 无全局锁、性能高，可接受写 Try/Confirm/Cancel |
| 流程长、参与方多（审批/履约编排） | **Saga** | 状态机串联 + 逐步补偿 |
| 单库内部、不跨服务 | 都不用 | 本地 `@Transactional` 即可，勿引入 Seata |

| 注解约定 | 要求 |
|---------|------|
| 标在哪 | **只标全局事务发起方**（最外层入口方法），分支服务不标 |
| 注解 | 发起方用 `@GlobalTransactional`，**显式 `rollbackFor = Exception.class`** |
| 不嵌套 | 一个全局事务内不再开新的 `@GlobalTransactional`，分支自动纳入 |
| 超时 | 长流程显式调大 `timeoutMills`，避免全局事务过早超时回滚 |

## 正例

```java
// 发起方：一次只用一种模式，显式 rollbackFor，配合理超时
@GlobalTransactional(rollbackFor = Exception.class, timeoutMills = 60000)
public void placeOrder(OrderReq req) {
    // 步骤1：扣库存（分支，不再标 @GlobalTransactional）
    storageFacade.deduct(req.getSku(), req.getCount());
    // 步骤2：扣款
    accountFacade.debit(req.getUserId(), req.getAmount());
    // 步骤3：建订单
    orderService.create(req);
}
```

## 反例

❌ 不写 `rollbackFor`：默认只对 `RuntimeException` 回滚，受检异常抛出时全局事务**不回滚**，数据不一致。

❌ 给每个分支方法都标 `@GlobalTransactional`：重复开启全局事务，语义混乱；分支只需被发起方纳入。

❌ 普通单库 CRUD 也套全局事务：徒增 TC 交互开销，本地 `@Transactional` 足矣。

❌ 同一业务同时混用 AT 和 TCC 还指望强一致：模式应按场景明确选定，勿无脑混搭。

## 自检

- [ ] 按场景选定了唯一模式（一般 AT / 核心 TCC / 长流程 Saga）？
- [ ] `@GlobalTransactional` 只标在发起方，且写了 `rollbackFor = Exception.class`？
- [ ] 分支服务没有重复标全局事务？
- [ ] 单库场景没误用 Seata，改用了本地 `@Transactional`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`at-mode.md`](./at-mode.md)（AT 细节）
- 兄弟：[`tcc-mode.md`](./tcc-mode.md)（TCC 细节）
- 兄弟：[`saga-mode.md`](./saga-mode.md)（Saga 细节）
- 单库事务边界：[`../mysql/transaction/transaction-scope.md`](../mysql/transaction/transaction-scope.md)
