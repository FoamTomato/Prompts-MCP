---
name: seata-saga-mode
description: Seata Saga 模式 — 长事务用状态机编排多个服务，每步配补偿动作，失败时反向逐步补偿，适合流程长、参与方多的业务。Use when 编排长流程审批/履约 / 参与方多到 TCC 难写 / 设计状态机与补偿时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 长事务
  - 状态机
  - 补偿动作
  - Saga 模式
  - 流程编排
  - StateMachine
effort: medium
context: inline
version: '1.0'
---
# Seata · Saga 模式（状态机长事务）

> 本条只管「Saga 状态机与补偿怎么设计」。无侵入默认见 [`at-mode.md`](./at-mode.md)；核心高性能见 [`tcc-mode.md`](./tcc-mode.md)；选哪种见 [`mode-selection.md`](./mode-selection.md)。

## 规则

| 项 | 约定 |
|----|------|
| 适用 | 流程长、步骤多、参与方多（审批、履约、跨多系统编排），TCC 三段难维护时 |
| 模型 | 用状态机 JSON 定义节点（服务调用）+ 流转，由状态机引擎驱动顺序执行 |
| 补偿 | **每个正向节点配一个补偿节点**，某步失败则按反向顺序逐个补偿已执行步骤 |
| 一致性 | 最终一致（非强一致），中间态对外可见，需业务能接受 |
| 幂等/空补偿 | 正向与补偿服务都要**幂等**，并处理空补偿（正向未成功就被补偿） |
| 防悬挂 | 补偿先到、正向后到时，正向须感知已补偿并放弃 |

## 正例

```java
// 启动状态机实例（流程在 JSON 状态机定义里编排，引擎按节点驱动）
@GlobalTransactional
public void startFulfillment(FulfillReq req) {
    final Map<String, Object> params = FulfillConvert.toParams(req);
    // 步骤1：启动履约状态机，引擎按节点顺序调各服务，失败自动反向补偿
    stateMachineEngine.startWithBusinessKey(
            "fulfillStateMachine", null, req.getOrderId(), params);
}
```

状态机 JSON 中每个 `ServiceTask` 节点声明正向方法与 `compensate` 补偿方法；引擎记录执行轨迹，异常时按轨迹反向调用补偿。

## 反例

❌ 某正向节点没配补偿节点：该步执行后无法回滚，流程中断即数据残留。

❌ 补偿动作非幂等：引擎重试补偿时重复操作，状态错乱。

❌ 把短流程（两三步）硬塞 Saga：状态机定义与补偿成本远高于直接用 AT/TCC。

❌ 业务要求强一致却用 Saga：Saga 是最终一致，中间态可见，不满足强一致诉求。

## 自检

- [ ] 每个正向节点都配了对应补偿节点？
- [ ] 正向与补偿服务都做了幂等，处理了空补偿/防悬挂？
- [ ] 业务能接受最终一致与中间态可见？
- [ ] 确实是长流程/多参与方才用 Saga，短流程没误用？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`at-mode.md`](./at-mode.md)（无侵入默认）
- 兄弟：[`tcc-mode.md`](./tcc-mode.md)（核心交易高性能）
- 兄弟：[`mode-selection.md`](./mode-selection.md)（三模式怎么选）
- 编排方法体写法：[`../../lang/java/pipeline-style/orchestration-method.md`](../../lang/java/pipeline-style/orchestration-method.md)
