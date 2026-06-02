---
name: mysql-cardinality-and-prefix
description: 索引区分度与前缀索引 — 低区分度列（状态/性别/软删标记）单独建索引收益低，长字符串列用前缀索引控制索引体积。Use when 纠结某列该不该建索引 / 给长字符串列建索引 / 评审冗余索引时。
parent: ./index.md
paths:
- '*.sql'
- '*.xml'
- '*.java'
triggers:
  keywords:
  - 区分度
  - 选择性
  - cardinality
  - selectivity
  - 前缀索引
  - prefix index
  - 冗余索引
effort: medium
context: inline
version: '1.0'
---
# MySQL · 区分度与前缀索引

> 本条只管「这列该不该建索引、字符串太长怎么建」。建了为什么没走见 [`index-fail-cases.md`](./index-fail-cases.md)；联合索引列顺序见 [`leftmost-prefix.md`](./leftmost-prefix.md)。

## 区分度（选择性）

选择性 = 不重复值数 / 总行数，越接近 1 越值得建索引。

```sql
-- 估算某列选择性，> 0.1 才考虑单独建索引
SELECT COUNT(DISTINCT status) / COUNT(*) FROM orders;
```

| 列类型 | 选择性 | 建索引建议 |
|--------|--------|-----------|
| 主键 / 唯一键 | =1 | 必建（天然唯一） |
| user_id / order_no | 高 | 适合 |
| status / type（少量枚举） | 低 | **不单独建**，放联合索引靠前的等值列里才有意义 |
| is_deleted / 性别（值仅 2-3 种） | 极低 | 不建，优化器多半放弃；用联合索引覆盖 |

> 低区分度列的正确用法：作为**联合索引最左等值列**与高区分度列组合，而非单列索引。

## 前缀索引

长字符串列（URL、邮箱、长 token）整列建索引太占空间，可只索引前 N 个字符：

```sql
-- 取能保住足够区分度的最短前缀长度
SELECT COUNT(DISTINCT LEFT(email, 8)) / COUNT(*) FROM users;   -- 试不同长度
ALTER TABLE users ADD INDEX idx_email_prefix (email(12));      -- 选区分度够的长度
```

| 项 | 说明 |
|----|------|
| 长度选取 | 取使选择性接近全列的最短前缀，平衡区分度与体积 |
| 代价 | 前缀索引**无法用于覆盖索引和 ORDER BY**（只有前缀信息） |
| 不适用 | 区分度集中在尾部的字符串（如同域名邮箱），前缀几乎不区分 |

## 反例

```sql
-- ❌ 给只有 0/1 的 is_deleted 单独建索引：优化器基本不用，白占空间拖写入
ALTER TABLE orders ADD INDEX idx_deleted (is_deleted);

-- ❌ 已有 (a,b) 联合索引又单独建 (a)：(a) 冗余，删掉
ALTER TABLE t ADD INDEX idx_a (a);   -- 被 idx_ab 的最左前缀覆盖
```

## 自检

- [ ] 这列选择性是否够高（粗判 > 0.1）才单独建索引？
- [ ] 低区分度列是否改为放进联合索引最左等值位，而非单列索引？
- [ ] 长字符串列是否用前缀索引、并验证过前缀长度的区分度？
- [ ] 是否存在被联合索引最左前缀覆盖的冗余单列索引？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`leftmost-prefix.md`](./leftmost-prefix.md) · [`index-fail-cases.md`](./index-fail-cases.md)
