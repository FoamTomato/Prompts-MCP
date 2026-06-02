---
name: mysql-charset-utf8mb4
description: MySQL 字符集统一 utf8mb4 — utf8 是阉割版存不下 emoji/4 字节字符，库表列与连接全用 utf8mb4，JOIN 两列 collation 须一致否则隐式转换使索引失效。Use when 建库建表定字符集 / 排查 emoji 乱码 / 排查跨表 JOIN 没走索引时。
parent: ./index.md
paths:
- '*.sql'
- '*.yml'
- '*.properties'
- '*.xml'
triggers:
  keywords:
  - 字符集
  - utf8mb4
  - 排序规则
  - collation
  - emoji 乱码
  - charset
  - JOIN 隐式转换
effort: medium
context: inline
version: '1.0'
---
# MySQL · 字符集统一 utf8mb4

> 本条只管「字符集/排序规则怎么定、为什么 JOIN 没走索引」。WHERE 单列的隐式类型转换见 [`../../../lang/sql/forbidden/no-implicit-conversion.md`](../../../lang/sql/forbidden/no-implicit-conversion.md)（本条专管字符集/collation 这一类）。

## 规则

| 项 | 约定 | 原因 |
|----|------|------|
| 字符集 | 全用 `utf8mb4` | MySQL 的 `utf8` 是 3 字节阉割版，**存不下 emoji / 部分中日韩生僻字**（4 字节） |
| 排序规则 | 团队统一一种（如 `utf8mb4_0900_ai_ci` 或 `utf8mb4_general_ci`） | JOIN 两列 collation 不一致会触发隐式转换 |
| 作用范围 | 库 + 表 + 列 + **连接** 四处都要 utf8mb4 | 任一处不是 utf8mb4 都可能乱码 |

## 建库建表

```sql
-- ✅ 库级默认
CREATE DATABASE app DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

-- ✅ 表级显式（继承库默认也行，显式更稳）
CREATE TABLE t (
  name VARCHAR(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

连接层（JDBC / 客户端）也要 utf8mb4：

```
jdbc:mysql://host:3306/app?characterEncoding=utf8mb4
```

## collation 不一致 → JOIN 索引失效

```sql
-- ❌ a.code 是 utf8mb4_general_ci，b.code 是 utf8mb4_0900_ai_ci
-- JOIN 时需把一侧转换，索引失效退化全表扫
SELECT * FROM a JOIN b ON a.code = b.code;
-- ✅ 统一两表该列 collation，或建表时就一致
ALTER TABLE b MODIFY code VARCHAR(32) COLLATE utf8mb4_general_ci;
```

> 排查信号：两表各自单查都走索引，一 JOIN 就全表扫，先查 `SHOW FULL COLUMNS` 看两列 collation 是否一致。

## 自检

- [ ] 库、表、列、连接四处是否都是 utf8mb4，没有残留 utf8(3 字节)？
- [ ] 全库 collation 是否统一一种，避免 JOIN 隐式转换？
- [ ] 需要存 emoji / 生僻字的字段确认是 utf8mb4？
- [ ] JOIN 突然不走索引时，查过两列 collation 是否一致？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`string-type-choice.md`](./string-type-choice.md)
- WHERE 隐式转换：[`../../../lang/sql/forbidden/no-implicit-conversion.md`](../../../lang/sql/forbidden/no-implicit-conversion.md)
