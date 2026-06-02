---
name: mysql-column-type-choice
description: MySQL 数值/时间/金额字段选型 — 整型能小不大、布尔用 TINYINT、金额必用 DECIMAL 禁 FLOAT、时间在 DATETIME 与 BIGINT 时间戳间取舍。Use when 建表选数值或时间字段 / 评审用 FLOAT 存钱 / 纠结存时间格式时。
parent: ./index.md
paths:
- '*.sql'
- '*.java'
- '*.py'
triggers:
  keywords:
  - 字段类型选型
  - 数据类型
  - DECIMAL 金额
  - FLOAT 精度
  - DATETIME timestamp
  - TINYINT 布尔
  - column type
effort: medium
context: inline
version: '1.0'
---
# MySQL · 数值/时间/金额字段选型

> 本条只管「数值、时间、金额选什么类型」。字符串类型见 [`string-type-choice.md`](./string-type-choice.md)；要不要 NOT NULL 见 [`not-null-and-default.md`](./not-null-and-default.md)。

## 总原则

**能小不大、能精确不浮点**。字段越小，每页存的行越多，索引越小，缓存命中越高。

## 数值

| 需求 | 选 | 别用 |
|------|-----|------|
| 主键 / 大范围计数 | `BIGINT` | —— |
| 一般整数 | `INT`，更小用 `SMALLINT`/`TINYINT` | 一律 BIGINT（浪费） |
| 布尔标记 | `TINYINT(1)`（0/1） | `BIT`、`VARCHAR('Y'/'N')` |
| 枚举状态 | `TINYINT` + 应用层枚举 | MySQL `ENUM`（改值要 DDL） |

## 金额（最常踩坑）

| 做法 | 说明 |
|------|------|
| ✅ `DECIMAL(p,s)` | 定点精确，如 `DECIMAL(12,2)` 存到分 |
| ✅ `BIGINT` 存「分」 | 用整数分存储，应用层除 100，零精度风险 |
| ❌ `FLOAT` / `DOUBLE` | 二进制浮点**有精度误差**，`0.1+0.2≠0.3`，绝不存钱 |

## 时间

| 选 | 适用 | 注意 |
|----|------|------|
| `DATETIME(3)` | 业务时间、需可读、跨时区由应用控 | 不随时区变，范围大 |
| `TIMESTAMP` | 需随会话时区自动转换 | 2038 年上限、范围小 |
| `BIGINT` 存毫秒戳 | 纯计算、跨系统传递 | 失去 SQL 可读性，慎用 |

> 统一团队约定：业务时间默认 `DATETIME(3)`，别同库混用 DATETIME / 时间戳 / 字符串日期。

## 反例

```sql
-- ❌ FLOAT 存余额：累加后出现 0.30000000004
balance FLOAT
-- ✅
balance DECIMAL(12,2) NOT NULL DEFAULT 0.00

-- ❌ VARCHAR 存日期：无法走时间范围索引、排序错乱
created_at VARCHAR(20)
-- ✅
created_at DATETIME(3) NOT NULL
```

## 自检

- [ ] 整型是否按实际范围选了最小够用类型，没有一律 BIGINT？
- [ ] 金额是否用 `DECIMAL` 或整数分，**绝无** FLOAT/DOUBLE？
- [ ] 时间是否用 `DATETIME`/`TIMESTAMP` 而非 VARCHAR 存日期字符串？
- [ ] 同库时间字段类型是否统一，没混用多种存法？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`string-type-choice.md`](./string-type-choice.md) · [`not-null-and-default.md`](./not-null-and-default.md)
