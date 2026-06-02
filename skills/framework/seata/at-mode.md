---
name: seata-at-mode
description: Seata AT 模式 — 业务无侵入，由代理数据源记录数据前后镜像、自动生成反向 SQL 回滚，需每库建 undo_log 表，是默认首选模式。Use when 给跨服务调用加分布式事务 / 想自动回滚不改业务 / 配 undo_log 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 自动回滚
  - 数据源代理
  - undo_log
  - AT 模式
  - 反向 SQL
  - DataSourceProxy
effort: medium
context: inline
version: '1.0'
---
# Seata · AT 模式（自动补偿）

> 本条只管「AT 模式怎么用与边界」。改不动业务/要高性能见 [`tcc-mode.md`](./tcc-mode.md)；长流程见 [`saga-mode.md`](./saga-mode.md)；选哪种见 [`mode-selection.md`](./mode-selection.md)。

## 规则

| 项 | 约定 |
|----|------|
| 适用 | 业务无侵入、绝大多数关系库跨服务场景，**默认首选** |
| 原理 | 代理数据源拦截 SQL，提交前存 before/after 镜像，回滚时按镜像生成反向 SQL 自动恢复 |
| undo_log | **每个参与库**必须建 `undo_log` 表，缺表则回滚失败 |
| 数据源 | 业务数据源需被 Seata 代理（Spring Boot starter 自动代理，勿手动绕过） |
| 隔离 | 写隔离靠全局锁，**默认读未提交**；要读已提交需 `@GlobalLock` + `SELECT ... FOR UPDATE` |
| 前提 | 表必须有**主键**，否则无法定位行做反向 SQL |

## 正例

```java
// 全局事务发起方：标注后内部跨服务调用纳入同一全局事务
@GlobalTransactional(rollbackFor = Exception.class)
public void placeOrder(OrderReq req) {
    // 步骤1：本服务扣库存（本地事务，AT 自动记录 undo_log）
    storageService.deduct(req.getSku(), req.getCount());
    // 步骤2：远程调用账户服务扣款（同一全局事务，失败则一并回滚）
    accountFacade.debit(req.getUserId(), req.getAmount());
    // 步骤3：写订单
    orderMapper.insert(OrderConvert.INSTANCE.toDO(req));
}
```

```sql
-- 每个参与库必建（字段以官方版本为准）
CREATE TABLE undo_log ( /* id, branch_id, xid, rollback_info, log_status ... */ );
```

## 反例

❌ 参与库没建 `undo_log` 表：分支注册成功但回滚时找不到镜像，全局事务无法补偿。

❌ 业务表无主键：AT 无法精确定位被改的行，反向 SQL 失效。

❌ 绕过代理数据源直接拿原始 `DataSource` 写库：该写操作不被 Seata 接管，回滚漏掉它，数据不一致。

❌ 给单库内操作套 `@GlobalTransactional`：单库用本地 `@Transactional` 即可，AT 是跨服务/跨库才需要。

## 自检

- [ ] 每个参与库都建了 `undo_log` 表？
- [ ] 业务表都有主键？
- [ ] 数据源走的是 Seata 代理（未手动绕过）？
- [ ] 发起方标了 `@GlobalTransactional`，单库场景没误用全局事务？
- [ ] 需要读已提交的地方用了 `@GlobalLock` + `FOR UPDATE`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`tcc-mode.md`](./tcc-mode.md)（改不动业务/要高性能时换 TCC）
- 兄弟：[`saga-mode.md`](./saga-mode.md)（流程长用 Saga）
- 兄弟：[`mode-selection.md`](./mode-selection.md)（三模式怎么选、注解标哪）
- 单库事务边界：[`../mysql/transaction/transaction-scope.md`](../mysql/transaction/transaction-scope.md)
