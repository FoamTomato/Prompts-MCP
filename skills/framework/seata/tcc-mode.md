---
name: seata-tcc-mode
description: Seata TCC 模式 — 业务侵入式，每操作拆 Try 预留资源 / Confirm 提交 / Cancel 释放三段，无全局锁性能高，适合核心交易。Use when 写高性能扣款扣库存 / AT 锁竞争扛不住 / 设计 Try-Confirm-Cancel 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 业务侵入
  - 资源预留
  - 空回滚
  - TCC 模式
  - Try-Confirm-Cancel
  - TwoPhaseBusinessAction
effort: medium
context: inline
version: '1.0'
---
# Seata · TCC 模式（业务补偿）

> 本条只管「TCC 三段怎么写与三大坑」。无侵入默认见 [`at-mode.md`](./at-mode.md)；长流程见 [`saga-mode.md`](./saga-mode.md)；选哪种见 [`mode-selection.md`](./mode-selection.md)。

## 规则

| 项 | 约定 |
|----|------|
| 适用 | 核心交易（扣款/扣库存），要高性能、AT 全局锁竞争扛不住时 |
| 三段 | Try 预留资源（冻结而非直接扣）；Confirm 真正提交；Cancel 释放预留 |
| 接口 | 标 `@LocalTCC`，Try 方法用 `@TwoPhaseBusinessAction(name, commitMethod, rollbackMethod)` |
| 空回滚 | Try 未执行就收到 Cancel，须能识别并直接返回成功（不能误扣） |
| 幂等 | Confirm/Cancel 可能重试，必须**幂等**（按事务 ID 去重） |
| 防悬挂 | Cancel 先到、Try 后到时，Try 须检测到已回滚并放弃预留 |

## 正例

```java
@LocalTCC
public interface AccountTccService {
    // Try：冻结金额，不真正扣
    @TwoPhaseBusinessAction(name = "accountDebit",
            commitMethod = "confirm", rollbackMethod = "cancel")
    boolean tryDebit(BusinessActionContext ctx,
                     @BusinessActionContextParameter("userId") Long userId,
                     @BusinessActionContextParameter("amount") BigDecimal amount);

    boolean confirm(BusinessActionContext ctx);  // 把冻结转为已扣（幂等）
    boolean cancel(BusinessActionContext ctx);   // 解冻（幂等 + 处理空回滚）
}
```

## 反例

❌ Confirm/Cancel 未做幂等：重试时二次扣款 / 二次解冻，金额错乱。

❌ Cancel 不处理空回滚：Try 因网络未到、Cancel 先到，直接解冻一笔不存在的冻结。

❌ Try 阶段直接扣真实余额（而非冻结）：违背资源预留语义，Cancel 难以还原。

❌ 把 TCC 当默认模式给所有 CRUD 用：三段代码量大、维护成本高，非核心交易应走 AT。

## 自检

- [ ] Try 是「预留/冻结」而非直接扣减？
- [ ] Confirm、Cancel 都做了幂等（按事务 ID 去重）？
- [ ] 处理了空回滚（Cancel 先于 Try）与防悬挂（Try 晚于 Cancel）？
- [ ] 确实是高性能核心交易才用 TCC，普通业务没误用？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`at-mode.md`](./at-mode.md)（无侵入默认，先考虑它）
- 兄弟：[`saga-mode.md`](./saga-mode.md)（流程长用 Saga）
- 兄弟：[`mode-selection.md`](./mode-selection.md)（三模式怎么选）
- 幂等设计参考：[`../mysql/transaction/transaction-scope.md`](../mysql/transaction/transaction-scope.md)
