---
name: mysql-string-type-choice
description: MySQL 字符串字段选型 — 定长用 CHAR、变长用 VARCHAR 并按实际估长度，大文本 TEXT/BLOB 拆出主表避免拖慢行扫描。Use when 建表选字符串字段 / 给 VARCHAR 定长度 / 评审主表塞 TEXT 大字段时。
parent: ./index.md
paths:
- '*.sql'
- '*.java'
- '*.py'
triggers:
  keywords:
  - 字符串类型
  - CHAR VARCHAR
  - TEXT BLOB
  - VARCHAR 长度
  - 大字段拆表
  - string type
effort: medium
context: inline
version: '1.0'
---
# MySQL · 字符串字段选型

> 本条只管「字符串列选 CHAR/VARCHAR/TEXT、长度怎么定」。数值/时间见 [`column-type-choice.md`](./column-type-choice.md)；字符集见 [`charset-utf8mb4.md`](./charset-utf8mb4.md)；长字符串建索引见 [`../index/cardinality-and-prefix.md`](../index/cardinality-and-prefix.md)。

## 选型表

| 类型 | 适用 | 注意 |
|------|------|------|
| `CHAR(n)` | **定长**：MD5(32)、状态码、国家码、性别 | 不足补空格，长度固定才用 |
| `VARCHAR(n)` | **变长**：名称、标题、备注 | n 按业务实际估，别动辄 255/无脑大 |
| `TEXT` / `LONGTEXT` | 大段文本：富文本、JSON、日志 | **不进高频主表**，见下 |
| `BLOB` | 二进制 | 同 TEXT，通常应存对象存储只留 URL |

## VARCHAR 长度怎么定

- 按**业务实际最大值 + 余量**估，不要无脑 `VARCHAR(255)`。
- 长度本身不占额外存储（按实际内容存），但**影响内存临时表/排序的预分配**，过大有代价。
- 超出长度会**截断**（严格模式报错），宁可略留余量。

## TEXT/BLOB 为什么拆表

InnoDB 中大字段超过阈值会**行外存储**，但仍可能拖慢全表/范围扫描与 `SELECT *`。原则：

```sql
-- ❌ 主表混入大富文本，每次扫描都背着它
CREATE TABLE article (
  id BIGINT PRIMARY KEY,
  title VARCHAR(200),
  content LONGTEXT          -- 几十 KB，拖慢列表查询
);

-- ✅ 大字段拆到从表，主表只留摘要字段
CREATE TABLE article (id BIGINT PRIMARY KEY, title VARCHAR(200), summary VARCHAR(500));
CREATE TABLE article_content (article_id BIGINT PRIMARY KEY, content LONGTEXT);
```

> 配合 [覆盖索引](../index/covering-index.md)：主表不含大字段，列表查询更容易覆盖/免回表。

## 自检

- [ ] 真定长才用 CHAR，变长用 VARCHAR？
- [ ] VARCHAR 长度按业务实际估，没有无脑 255 / 超大？
- [ ] 大文本/二进制用 TEXT/BLOB，且**没有**塞进高频查询的主表？
- [ ] 二进制大对象是否考虑存对象存储、库里只留 URL？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`column-type-choice.md`](./column-type-choice.md) · [`charset-utf8mb4.md`](./charset-utf8mb4.md)
- 长串建索引：[`../index/cardinality-and-prefix.md`](../index/cardinality-and-prefix.md)
