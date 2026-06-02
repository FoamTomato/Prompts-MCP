---
name: sharding-sphere-read-write-split
description: ShardingSphere 读写分离 — 主库写从库读自动路由，主从复制延迟导致写后立即读取到旧数据，靠 HintManager 强制走主库或事务内自动走主库解决。Use when 配读写分离 / 写完立即查不到数据 / 评审主从延迟方案时。
parent: ./index.md
paths:
- '*.java'
- '*.yml'
triggers:
  keywords:
  - 读写分离
  - 主从延迟
  - 写后读
  - 强制主库
  - HintManager
  - readwrite-splitting
effort: high
context: inline
version: '1.0'
---
# ShardingSphere · 读写分离

> 本条只管「主写从读 + 主从延迟读不到数据」。分片算法见 [`sharding-strategy.md`](./sharding-strategy.md)。

## 规则

| 事项 | 约定 |
|------|------|
| 路由默认 | `INSERT/UPDATE/DELETE` 走主库，`SELECT` 走从库（多从可配负载均衡） |
| 事务内 | 同一事务内的 `SELECT` **自动走主库**，保证读到本事务刚写的数据 |
| 写后立即读 | 跨事务的「写完马上查」会命中**主从延迟**：从库还没同步到 → 读到旧值 |
| 强制主库 | 写后必须读到最新值的链路，用 `HintManager.setWriteRouteOnly()` 强制走主库 |
| 负载均衡 | 多从库配 `loadBalancerName`（ROUND_ROBIN / RANDOM / WEIGHT） |

## 正例

```yaml
# ✅ 读写分离规则：write 主库 + read 多从轮询
rules:
  - !READWRITE_SPLITTING
    dataSources:
      rw_ds:
        writeDataSourceName: ds_master
        readDataSourceNames: [ds_slave_0, ds_slave_1]
        loadBalancerName: round_robin
    loadBalancers:
      round_robin: { type: ROUND_ROBIN }
```

```java
// ✅ 写后立即读最新值：强制本次查询走主库，避开主从延迟
try (HintManager hint = HintManager.getInstance()) {
    hint.setWriteRouteOnly();              // 本线程后续 SQL 都走主库
    final Long id = orderMapper.insert(order);
    return orderMapper.selectById(id);     // 命中主库，读得到刚写的
}
```

## 反例

```java
// ❌ 写完跨事务立即从从库读 —— 主从还没同步，查到 null 或旧数据
orderService.create(order);               // 写主库，事务已提交
OrderDO got = orderMapper.selectById(order.getId());  // 走从库 → 可能读不到
```

理由：主库写完到从库可见有复制延迟（毫秒到秒级）。事务提交后跨事务的读会路由到从库，此刻从库未必同步完，于是读到旧数据；需要强一致读时用 `setWriteRouteOnly` 走主库，或把读放进同一事务。

## 自检

- [ ] 写操作走主库、普通读走从库（默认即可）？
- [ ] 「写后立即读且要求最新」的链路用了 `setWriteRouteOnly` 或同事务读主库？
- [ ] `HintManager` 用 try-with-resources / 显式 `close()`，避免线程复用串味？
- [ ] 能容忍延迟的读（如列表、报表）才放从库，不滥用强制主库压垮主库？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`sharding-strategy.md`](./sharding-strategy.md)（读写分离常与分片叠加配置）
- 兄弟：[`distributed-limitations.md`](./distributed-limitations.md)（分布式事务下的读一致性）
