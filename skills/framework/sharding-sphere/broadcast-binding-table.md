---
name: sharding-sphere-broadcast-binding-table
description: ShardingSphere 广播表与绑定表 — 广播表(字典/配置)全库同份避免跨片 join，绑定表(主从表同分片键)让 JOIN 落同片避免笛卡尔积全片乘积。Use when 配广播表绑定表 / 分片表 JOIN 数据翻倍或变慢 / 评审关联表分片时。
parent: ./index.md
paths:
- '*.java'
- '*.yml'
triggers:
  keywords:
  - 广播表
  - 绑定表
  - 笛卡尔积
  - 分片 JOIN
  - bindingTables
  - broadcastTables
effort: high
context: inline
version: '1.0'
---
# ShardingSphere · 广播表与绑定表

> 本条只管「哪类表配广播/绑定来避免坏 JOIN」。彻底做不了的跨库 JOIN 见 [`distributed-limitations.md`](./distributed-limitations.md)。

## 两种特殊表

| 类型 | 是什么 | 解决的问题 |
|------|--------|-----------|
| **广播表** | 数据量小、各分库各存**一份全量**（字典、地区、配置表） | 与任何分片表 join 都在本库完成，无需跨片 |
| **绑定表** | 一组分片键相同、分片规则一致的主从表（`t_order` + `t_order_item`） | 同 user_id 的主从行落**同一片**，JOIN 只在片内一对一 |

## 笛卡尔积问题

分片表之间若**未声明绑定**，中间件不知道它们同片，会把每个 t_order 分片 × 每个 t_order_item 分片做**全片两两 join**（笛卡尔积），结果行数翻倍且大量重复。声明 bindingTables 后只 join 对应分片，结果正确且快。

## 正例

```yaml
# ✅ 广播表 + 绑定表
rules:
  - !SHARDING
    broadcastTables: [t_dict, t_region]        # 字典/地区表全库各一份
    bindingTables:
      - t_order,t_order_item                   # 主从表声明绑定 → 同片 join
    tables:
      t_order:      { actualDataNodes: ds_${0..1}.t_order_${0..1}, ... }
      t_order_item: { actualDataNodes: ds_${0..1}.t_order_item_${0..1}, ... }
```

```sql
-- ✅ 绑定表 JOIN：t_order 与 t_order_item 按 user_id 同片，片内一对一
SELECT o.*, i.* FROM t_order o
JOIN t_order_item i ON o.order_id = i.order_id
WHERE o.user_id = 1001;
```

## 反例

```yaml
# ❌ t_order 与 t_order_item 都分片但没进 bindingTables
#    JOIN 时变成 2×2=4 个分片两两笛卡尔积，行数翻倍 + 结果错
rules:
  - !SHARDING
    tables: { t_order: {...}, t_order_item: {...} }   # 缺 bindingTables
```

理由：未绑定的分片表，中间件按「任意片可能匹配任意片」展开成笛卡尔积；同分片键的主从表声明绑定后才会只 join 同片，结果既对又快。字典类小表则用广播表，省掉跨片 join。

## 自检

- [ ] 字典/配置/地区这类小表配成 `broadcastTables`，不参与分片 join？
- [ ] 同分片键的主从表（订单/明细）声明进 `bindingTables`？
- [ ] 绑定表的分片键、分片规则、分片数完全一致（否则绑定无效）？
- [ ] JOIN 结果没出现行数翻倍/重复（笛卡尔积征兆）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`distributed-limitations.md`](./distributed-limitations.md)（无法绑定时的跨库 JOIN 规避）
- 兄弟：[`sharding-key-choice.md`](./sharding-key-choice.md)（绑定表要求分片键一致）
