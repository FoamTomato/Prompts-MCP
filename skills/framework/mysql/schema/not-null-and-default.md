---
name: mysql-not-null-and-default
description: MySQL 列尽量 NOT NULL 加合理默认值 — NULL 让索引/聚合/比较语义复杂且占额外标记位，能给默认值就别留 NULL。Use when 建表定列可空性 / 给字段设默认值 / 排查 COUNT 或 != 漏掉 NULL 行时。
parent: ./index.md
paths:
- '*.sql'
- '*.java'
- '*.py'
triggers:
  keywords:
  - NOT NULL
  - 默认值
  - NULL 索引
  - nullable
  - default value
  - 三值逻辑
effort: medium
context: inline
version: '1.0'
---
# MySQL · NOT NULL 与默认值

> 本条只管「列要不要可空、给什么默认」。类型本身的选择见 [`column-type-choice.md`](./column-type-choice.md) / [`string-type-choice.md`](./string-type-choice.md)。

## 为什么尽量 NOT NULL

| 问题 | 说明 |
|------|------|
| 索引与统计变复杂 | NULL 在索引中要额外处理，影响优化器基数估算 |
| 比较走三值逻辑 | `col = NULL` 永远为 unknown，必须用 `IS NULL`；`!= 'x'` 会**漏掉 NULL 行** |
| 聚合被忽略 | `COUNT(col)` 不计 NULL、`SUM/AVG` 跳过 NULL，易算错 |
| 额外标记位 | 每个可空列在行里多占 NULL 标记，且语义含糊（NULL 是"未知"还是"空"？） |

## 规则

| 项 | 约定 |
|----|------|
| 默认 | 列**优先 NOT NULL** + 给业务合理默认值 |
| 数值 | `NOT NULL DEFAULT 0` |
| 字符串 | `NOT NULL DEFAULT ''` |
| 时间 | `NOT NULL DEFAULT CURRENT_TIMESTAMP(3)`（创建时间） |
| 真正需要"未知"语义时 | 才允许 NULL，并在查询里始终 `IS NULL`/`IS NOT NULL` 处理 |

> 「0/空串」与「NULL」语义不同时（如"评分未填" vs "评分 0 分"），NULL 是合理的；别为了规则把有意义的"未知"硬塞成 0。

## 反例

```sql
-- ❌ status 可空，查"非 A 状态"漏掉了 status IS NULL 的行
WHERE status != 'A'        -- NULL 行不会被选中，常是 bug

-- ❌ 数量列可空，SUM 把 NULL 跳过，统计偏小
qty INT NULL
```

## 正例

```sql
CREATE TABLE orders (
  id         BIGINT       NOT NULL AUTO_INCREMENT,
  status     TINYINT      NOT NULL DEFAULT 0,
  remark     VARCHAR(200) NOT NULL DEFAULT '',
  created_at DATETIME(3)  NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (id)
);
```

## 自检

- [ ] 列是否默认 NOT NULL + 合理默认值，只有真需要"未知"语义才留 NULL？
- [ ] 涉及可空列的 `!=`/`NOT IN` 查询是否考虑了 NULL 行漏选？
- [ ] 聚合（COUNT/SUM/AVG）是否清楚 NULL 会被忽略、结果无偏差？
- [ ] "0/空串" 与 "NULL" 的业务语义区分清楚，没有混用？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`column-type-choice.md`](./column-type-choice.md) · [`string-type-choice.md`](./string-type-choice.md)
