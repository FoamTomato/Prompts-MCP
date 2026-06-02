---
name: mysql-covering-index
description: 覆盖索引避免回表 — 查询所需列全在二级索引中时，直接从索引取数不回聚簇索引，EXPLAIN Extra 显示 Using index。Use when 热点查询想免回表 / SELECT 列收敛进索引 / 评审高频查询性能时。
parent: ./index.md
paths:
- '*.sql'
- '*.xml'
- '*.java'
triggers:
  keywords:
  - 覆盖索引
  - 回表
  - covering index
  - Using index
  - 免回表
  - 二级索引取数
effort: high
context: inline
version: '1.0'
---
# MySQL · 覆盖索引免回表

> 本条只管「让查询不回表」。列顺序与最左前缀见 [`leftmost-prefix.md`](./leftmost-prefix.md)；SELECT 禁星号的语法红线见 [`../../../lang/sql/select/explicit-column-list.md`](../../../lang/sql/select/explicit-column-list.md)（语法层，本条是性能层）。

## 机制

二级索引叶子只存「索引列 + 主键值」。普通查询命中二级索引后，要拿其它列得**用主键值回聚簇索引再查一次**（回表）。若查询要的列**全部已在该二级索引里**，就无需回表 —— 这叫覆盖索引。

`EXPLAIN` 的 `Extra` 出现 `Using index` = 命中覆盖索引（注意区别于 `Using index condition` = ICP）。

## 规则

| 做法 | 说明 |
|------|------|
| 收敛 SELECT 列 | 高频查询只取需要的列，让列集落进某个二级索引 |
| 把高频列纳入联合索引 | 在 `WHERE/ORDER BY` 列后追加被 SELECT 的少量列，组成覆盖索引 |
| 不滥用 | 覆盖索引会变宽、拖慢写入；只对**高频读**查询做，不对每个查询都堆 |

## 正例

```sql
-- 索引 idx_uid_status_amount (user_id, status, amount)

-- ✅ 取的 amount 已在索引中 → Using index，不回表
SELECT amount FROM orders WHERE user_id = 100 AND status = 'PAID';

-- ✅ 只需 id（主键，二级索引天然带）→ 也覆盖
SELECT id FROM orders WHERE user_id = 100;
```

## 反例

```sql
-- ❌ SELECT * 必然要 created_at/remark 等非索引列 → 每行回表
SELECT * FROM orders WHERE user_id = 100 AND status = 'PAID';

-- ❌ 为覆盖把 10 个列全塞进一个索引 → 索引比表还大，写入变慢
CREATE INDEX idx_fat ON orders (user_id, status, amount, remark, ...);
```

## 与最左前缀配合

覆盖索引必须同时满足最左前缀才生效。`idx (a,b,c)` 下 `SELECT c WHERE a=?` 是覆盖的（c 在索引里），但 `SELECT c WHERE b=?` 不命中索引（缺最左列 a），自然也谈不上覆盖。

## 自检

- [ ] 这是高频读查询，值得为它做覆盖？（写多读少别做）
- [ ] SELECT 列是否已收敛到最小、避免 `SELECT *`？
- [ ] 需要的列是否都在某个满足最左前缀的二级索引中？
- [ ] EXPLAIN `Extra` 是否出现 `Using index`？
- [ ] 索引是否没有为了覆盖而变得过宽、拖累写入？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`leftmost-prefix.md`](./leftmost-prefix.md) · [`index-fail-cases.md`](./index-fail-cases.md)
- 诊断：[`../diagnosis/explain-reading.md`](../diagnosis/explain-reading.md)
