---
name: sharding-sphere-sharding-strategy
description: ShardingSphere 分片策略 — 标准/复合/Hint 三种分片，简单 mod 用 inline 表达式，range 或复杂逻辑用自定义分片算法类。Use when 配分片算法 / 选 inline 还是自定义算法 / 评审分片 YAML 时。
parent: ./index.md
paths:
- '*.java'
- '*.yml'
triggers:
  keywords:
  - 分片策略
  - 标准分片
  - Hint 分片
  - inline 表达式
  - 自定义分片算法
  - StandardShardingAlgorithm
effort: high
context: inline
version: '1.0'
---
# ShardingSphere · 分片策略

> 本条只管「分片算法怎么配」。选哪个列做分片键见 [`sharding-key-choice.md`](./sharding-key-choice.md)。

## 三种分片策略

| 策略 | 适用 | 分片键 |
|------|------|--------|
| **STANDARD** 标准分片 | 单分片键，最常用；支持 `=` `IN` 与 `BETWEEN AND`（range） | 1 个 |
| **COMPLEX** 复合分片 | 需要**多个**分片键联合定位（如同时按 user_id + 时间） | 多个 |
| **HINT** 强制路由 | 分片键不在 SQL 里，靠代码 `HintManager` 显式指定落哪片 | 无（手动注入） |

## inline 表达式 vs 自定义算法

| 方式 | 用途 | 表达力 |
|------|------|--------|
| **inline** | 简单取模/拼接，配置里一行 Groovy 表达式即可 | 仅简单运算，**不支持 range** 查询路由 |
| **自定义算法类** | 一致性哈希、按时间分、range 路由等复杂逻辑 | 实现 `StandardShardingAlgorithm` 等接口，全可控 |

## 正例

```yaml
# ✅ inline：t_order 按 user_id 取模分 4 库 + 4 表（简单 mod）
rules:
  - !SHARDING
    tables:
      t_order:
        actualDataNodes: ds_${0..3}.t_order_${0..3}
        databaseStrategy:
          standard: { shardingColumn: user_id, shardingAlgorithmName: db_mod }
        tableStrategy:
          standard: { shardingColumn: user_id, shardingAlgorithmName: tbl_mod }
    shardingAlgorithms:
      db_mod:  { type: INLINE, props: { algorithm-expression: ds_${user_id % 4} } }
      tbl_mod: { type: INLINE, props: { algorithm-expression: t_order_${user_id % 4} } }
```

```java
// ✅ range 查询需自定义 STANDARD 算法：实现 doSharding 处理 BETWEEN
public class TimeRangeAlgorithm implements StandardShardingAlgorithm<Long> {
    // 精确路由（= / IN）
    public String doSharding(Collection<String> nodes, PreciseShardingValue<Long> v) { ... }
    // 范围路由（BETWEEN AND）—— inline 做不到，这里命中多片
    public Collection<String> doSharding(Collection<String> nodes, RangeShardingValue<Long> v) { ... }
}
```

## 反例

```yaml
# ❌ 业务要按时间范围查，却用 inline —— inline 不解析 BETWEEN，range 查询会广播全片
shardingAlgorithms:
  by_time: { type: INLINE, props: { algorithm-expression: t_log_${create_time...} } }
```

理由：inline 只算单值映射，`BETWEEN AND` 它无从展开，结果退化为广播所有分片；范围分片必须用实现 `RangeShardingValue` 的自定义 STANDARD 算法。

## 自检

- [ ] 单键且简单 mod → 用 inline；复杂/range/一致性哈希 → 自定义算法类？
- [ ] 需要多键联合定位时用了 COMPLEX，而非塞进单个 inline？
- [ ] 分片键不出现在 SQL（如后台按租户路由）才用 HINT，且用完 `HintManager.close()`？
- [ ] 有 range 查询的表没用 inline，而是实现了 `RangeShardingValue` 路由？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`sharding-key-choice.md`](./sharding-key-choice.md)（先定分片键再配算法）
- 兄弟：[`distributed-limitations.md`](./distributed-limitations.md)（路由到多片后的查询限制）
