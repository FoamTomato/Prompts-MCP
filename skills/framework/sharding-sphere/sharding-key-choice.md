---
name: sharding-sphere-sharding-key-choice
description: ShardingSphere 分片键选择 — 用绝大多数查询的 WHERE 条件做分片键命中单片，非分片键查询会广播全片变慢，跨片需建索引表映射。Use when 选 ShardingSphere 分片键 / 排查查询广播全片 / 评审分片维度时。
parent: ./index.md
paths:
- '*.java'
- '*.yml'
triggers:
  keywords:
  - 分片键选择
  - 高频查询条件
  - 跨片查询
  - 广播全片
  - 索引表
  - shardingColumn
effort: high
context: inline
version: '1.0'
---
# ShardingSphere · 分片键选择

> 本条只管「中间件配置层选哪列做 `shardingColumn`」。算法怎么配见 [`sharding-strategy.md`](./sharding-strategy.md)。
> **分工**：数据库视角的拆分键原理（要不要分、热点、分布均匀的 DB 道理）见 [`../mysql/ops/sharding-key-choice.md`](../mysql/ops/sharding-key-choice.md)，不重复；本条聚焦 ShardingSphere 选键后**查询命中单片**的落地与 SQL 写法。

## 规则

| 原则 | 说明 |
|------|------|
| **高频查询条件做分片键** | 分片键应是 90% 查询的 WHERE 列，SQL 带上它才能路由到单片 |
| **WHERE 必带分片键** | 查询条件里没有分片键 → 中间件无法定位 → 广播到**所有**分片再归并 |
| **业务维度对齐** | 用户类查询用 `user_id`；订单按 `user_id` 分（用户查自己订单命中单片）而非 `order_id` |
| **次要查询走索引表** | 偶尔按非分片键查（如按 order_id）→ 建 `order_id → user_id` 索引表先查映射再带分片键查 |

## 正例

```sql
-- ✅ 分片键 user_id 在 WHERE，路由到单片
SELECT * FROM t_order WHERE user_id = 1001 AND status = 'PAID';
```

```java
// ✅ 按非分片键(order_id)查：先查索引表拿 user_id，再带分片键查 → 仍命中单片
final Long userId = orderIndexMapper.findUserIdByOrderId(orderId);
final OrderDO order = orderMapper.selectByUserAndOrder(userId, orderId);
```

## 反例

```sql
-- ❌ WHERE 不含分片键 user_id —— 中间件广播到全部分片，扫全库
SELECT * FROM t_order WHERE order_no = 'NO123';
```

理由：ShardingSphere 靠 SQL 中的分片键值算路由；缺了分片键就只能广播全片再合并，分片数越多越慢，等于自废分片。高频非分片键查询必须靠索引表把它转回分片键。

## 自检

- [ ] 分片键是绝大多数查询的 WHERE 列？
- [ ] 主流程 SQL 都带上了分片键，没有触发全片广播？
- [ ] 高频的非分片键查询有索引表/冗余分片键，不靠广播？
- [ ] 选键的 DB 层原理（热点、分布均匀）已对照 [`../mysql/ops/sharding-key-choice.md`](../mysql/ops/sharding-key-choice.md)？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`sharding-strategy.md`](./sharding-strategy.md)（选好键后配分片算法）
- 兄弟：[`distributed-limitations.md`](./distributed-limitations.md)（广播查询带来的分页/聚合限制）
- DB 视角拆分键：[`../mysql/ops/sharding-key-choice.md`](../mysql/ops/sharding-key-choice.md)
