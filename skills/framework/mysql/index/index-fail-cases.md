---
name: mysql-index-fail-cases
description: 索引失效场景全集 — 函数/运算包裹索引列、隐式类型转换、前导 % 的 LIKE、!= 与 NOT IN、OR 一侧无索引，都会退化为全表扫。Use when 查询慢且 EXPLAIN 没走索引 / 评审 WHERE 写法 / 排查全表扫时。
parent: ./index.md
paths:
- '*.sql'
- '*.xml'
- '*.java'
triggers:
  keywords:
  - 索引失效
  - 全表扫描
  - index not used
  - full table scan
  - 函数包裹列
  - LIKE 前导百分号
  - OR 索引
effort: high
context: inline
version: '1.0'
---
# MySQL · 索引失效场景

> 本条只管「为什么 WHERE 没走索引」。最左前缀那一类失效见 [`leftmost-prefix.md`](./leftmost-prefix.md)；隐式类型转换的语法红线见 [`../../../lang/sql/forbidden/no-implicit-conversion.md`](../../../lang/sql/forbidden/no-implicit-conversion.md)（本条把它纳入失效场景做统一排查）。

## 失效场景速查

| 场景 | 失效写法 | 改法 |
|------|---------|------|
| 函数/运算包列 | `WHERE DATE(created_at)='2026-01-01'` | 改区间 `created_at >= '...' AND < '...'` |
| 列参与计算 | `WHERE amount + 1 > 100` | 移到右侧 `amount > 99` |
| 隐式类型转换 | 字符串列 `WHERE phone = 138...`（传 int） | 类型对齐 `phone = '138...'` |
| 前导 % | `WHERE name LIKE '%foo'` | 去前导 %，或用全文/搜索引擎 |
| 否定条件 | `!=` / `<>` / `NOT IN` / `NOT LIKE` | 改正向枚举 `IN (...)` |
| OR 跨列 | `WHERE a=1 OR b=2`（b 无索引） | 拆 `UNION` 或给 b 建索引 |
| 区分度太低 | `WHERE is_deleted=0`（值只有 0/1） | 优化器主动放弃，见 cardinality 条 |

## 正例对比

```sql
-- ❌ 函数包裹 created_at → 索引失效，全表扫
SELECT id FROM orders WHERE DATE(created_at) = '2026-01-01';
-- ✅ 改成区间，走索引
SELECT id FROM orders WHERE created_at >= '2026-01-01' AND created_at < '2026-01-02';

-- ❌ OR 一侧 mobile 无索引 → 整条退化全表扫
SELECT id FROM users WHERE user_id = 1 OR mobile = '138';
-- ✅ 两列各有索引时用 UNION 各走各的索引
SELECT id FROM users WHERE user_id = 1
UNION SELECT id FROM users WHERE mobile = '138';
```

## 注意点

- **不是绝对**：优化器基于成本估算，当索引扫描成本反而高于全表（如要回表的行占比很大）时，会**主动放弃索引**，这是正确行为，别强行 `FORCE INDEX`。
- 失效与否**以 `EXPLAIN` 为准**，不要凭记忆断言；读法见诊断条。
- `IN (...)` 通常能走索引；`NOT IN` 通常不能 —— 这是为什么用正向枚举替代否定。

## 自检

- [ ] WHERE 里索引列是否「裸用」、没被函数/运算包裹？
- [ ] 比较两侧类型一致、无隐式转换？
- [ ] LIKE 没有前导 `%`？
- [ ] 用正向 `IN` 而非 `!=`/`NOT IN`？
- [ ] OR 的每一侧都有可用索引，否则改 UNION？
- [ ] 已用 `EXPLAIN` 确认而非凭感觉？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`leftmost-prefix.md`](./leftmost-prefix.md) · [`cardinality-and-prefix.md`](./cardinality-and-prefix.md)
- 语法红线：[`../../../lang/sql/forbidden/no-implicit-conversion.md`](../../../lang/sql/forbidden/no-implicit-conversion.md)
- 诊断：[`../diagnosis/explain-reading.md`](../diagnosis/explain-reading.md)
