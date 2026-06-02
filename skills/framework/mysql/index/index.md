---
name: framework-mysql-index-index
description: InnoDB 索引设计 5 个独立决策点 — 聚簇主键选型 / 联合索引最左前缀 / 覆盖索引免回表 / 索引失效场景 / 区分度与前缀索引。Use when 建索引 / 排查没走索引或慢查询 / 评审索引列顺序时。
parent: ../index.md
children:
  - { name: mysql-clustered-pk-design, path: clustered-pk-design.md, tag: skill, note: "聚簇索引：主键宜自增 BIGINT，忌 UUID/业务键" }
  - { name: mysql-leftmost-prefix, path: leftmost-prefix.md, tag: skill, note: "联合索引最左前缀 + 索引下推 ICP" }
  - { name: mysql-covering-index, path: covering-index.md, tag: skill, note: "覆盖索引免回表，SELECT 列收敛进索引" }
  - { name: mysql-index-fail-cases, path: index-fail-cases.md, tag: skill, note: "索引失效：函数包列 / != / OR / 前缀 like / 类型不匹配" }
  - { name: mysql-cardinality-and-prefix, path: cardinality-and-prefix.md, tag: skill, note: "低区分度列不建索引，长字符串用前缀索引" }
when_to_descend: 设计 / 评审 InnoDB 索引：定主键、排联合索引列顺序、排查没走索引、做覆盖索引或前缀索引。
---

# MySQL · 索引设计索引

InnoDB 索引拆成 5 个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 定主键类型（自增 / UUID / 业务键） | [clustered-pk-design](clustered-pk-design.md) |
| 排联合索引列顺序、排查没命中联合索引 | [leftmost-prefix](leftmost-prefix.md) |
| 想免回表、把查询列收进索引 | [covering-index](covering-index.md) |
| 查询走了全表扫、怀疑索引失效 | [index-fail-cases](index-fail-cases.md) |
| 纠结某列该不该建索引、字符串太长 | [cardinality-and-prefix](cardinality-and-prefix.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 兄弟维度：[`../transaction/index.md`](../transaction/index.md) · [`../diagnosis/index.md`](../diagnosis/index.md)
- 语句层（互补）：[`../../../lang/sql/forbidden/index.md`](../../../lang/sql/forbidden/index.md)
