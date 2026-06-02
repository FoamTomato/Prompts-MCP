---
name: mysql-count-and-deep-paging
description: MySQL count 与深分页优化 — count(*) 用最小索引勿用 count(列)，大 offset 的 LIMIT 改 keyset 游标分页或延迟关联。Use when count 统计慢 / 翻页到很后面变慢 / 评审 LIMIT 大偏移时。
parent: ./index.md
paths:
- '*.sql'
- '*.xml'
- '*.java'
triggers:
  keywords:
  - count(*)
  - 深分页
  - deep paging
  - LIMIT offset
  - 游标分页
  - keyset pagination
  - 键集分页
effort: high
context: inline
version: '1.0'
---
# MySQL · count 与深分页优化

> 本条只管「count 怎么写不慢、深翻页怎么救」。框架物理分页（PageHelper/IPage）怎么配见 [`../../mybatis/pagination.md`](../../mybatis/pagination.md)（本条是 SQL/索引层的优化原理）。

## count 真相

| 写法 | 说明 |
|------|------|
| `COUNT(*)` | **推荐**，优化器选最小的可用索引扫，不读具体列值 |
| `COUNT(1)` | 与 `COUNT(*)` 等价，无性能差别 |
| `COUNT(列)` | **不计该列为 NULL 的行**，语义不同且可能更慢 |
| 海量表精确 count | InnoDB 无缓存行数，必须扫描；可接受估算时用 `EXPLAIN` 的 `rows` 或单独维护计数表 |

> 别为「总数」纠结精确：列表页常可用近似总数或「下一页有无」替代精确 count，省一次全表级扫描。

## 深分页问题

```sql
-- ❌ offset 很大：MySQL 要扫 100020 行再丢弃前 100000 行
SELECT * FROM orders ORDER BY id LIMIT 100000, 20;
```

offset 越大越慢，因为前面的行也要读出来再扔掉。

## keyset（游标）分页

记住上一页最后一行的有序键，下页用 `WHERE 键 > 上次值` 直接定位，**不扫前面的行**：

```sql
-- ✅ 首页
SELECT * FROM orders ORDER BY id LIMIT 20;
-- ✅ 下一页：上次最后 id = 100000
SELECT * FROM orders WHERE id > 100000 ORDER BY id LIMIT 20;
```

| 方案 | 适用 | 限制 |
|------|------|------|
| keyset 游标 | 无限下拉、顺序翻页 | 不能跳到任意页码 |
| 延迟关联 | 必须支持跳页 | 先用覆盖索引取主键再 join 回表，减少回表行 |

延迟关联写法：

```sql
-- ✅ 子查询只在索引上算出本页 20 个 id（覆盖、轻），再 join 取整行
SELECT o.* FROM orders o
JOIN (SELECT id FROM orders ORDER BY id LIMIT 100000, 20) t ON o.id = t.id;
```

## 自检

- [ ] 计数用 `COUNT(*)`/`COUNT(1)`，没误用 `COUNT(列)` 改变语义？
- [ ] 海量表是否接受近似总数 / 用「有无下一页」替代精确 count？
- [ ] 顺序翻页是否用 keyset 游标（`WHERE id > 上次值`）而非大 offset？
- [ ] 必须跳页时是否用延迟关联减少回表？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`explain-reading.md`](./explain-reading.md)
- 框架分页：[`../../mybatis/pagination.md`](../../mybatis/pagination.md)
- 覆盖索引：[`../index/covering-index.md`](../index/covering-index.md)
