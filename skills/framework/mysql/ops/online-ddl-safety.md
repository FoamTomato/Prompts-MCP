---
name: mysql-online-ddl-safety
description: MySQL 大表 Online DDL 安全 — 加字段/改索引优先 ALGORITHM=INPLACE 免锁，改类型改主键等 COPY 操作用 gh-ost/pt-osc 影子表切换。Use when 给大表加字段或加索引 / 评审线上 DDL / 怕改表锁住业务时。
parent: ./index.md
paths:
- '*.sql'
- '**/migrations/**'
- '*.xml'
triggers:
  keywords:
  - Online DDL
  - 在线改表
  - gh-ost
  - pt-online-schema-change
  - 锁表
  - ALGORITHM INPLACE
  - 大表加字段
effort: high
context: inline
version: '1.0'
---
# MySQL · 大表 Online DDL 安全

> 本条只管「大表怎么改结构不锁死业务」。建表/迁移文件模板见 [`../../../lang/sql/ddl/index.md`](../../../lang/sql/ddl/index.md)；改索引本身怎么设计见 [`../index/index.md`](../index/index.md)。

## 核心风险

DDL 在老版本/某些操作下会**持有元数据锁（MDL）甚至重建整表**，大表上锁几分钟即business 全停。改表前必须判断：这个改动是 INPLACE 免拷贝，还是要 COPY 重建表？

## 原生 Online DDL（8.0）

```sql
-- 优先 INPLACE（多数加列、加二级索引支持），加 LOCK=NONE 期间不阻塞读写
ALTER TABLE orders ADD COLUMN remark VARCHAR(200) NOT NULL DEFAULT '',
  ALGORITHM=INPLACE, LOCK=NONE;
```

| 操作 | 通常支持 | 注意 |
|------|---------|------|
| 加列（末尾） | INPLACE | 8.0 instant 更快（仅改元数据） |
| 加二级索引 | INPLACE | 占 IO，低峰执行 |
| 改列类型 / 改字符集 | 多为 COPY | **重建整表**，大表禁直接上 |
| 加主键 / 改主键 | COPY | 风险最高 |

> 写 `ALGORITHM=INPLACE, LOCK=NONE`：若该操作不支持会**直接报错**而非偷偷降级锁表，是一道保险。

## 高风险改动用影子表工具

改列类型、改主键等 COPY 类操作，用 `gh-ost` 或 `pt-online-schema-change`：建影子表 → 双写/追 binlog 同步 → 低峰原子切换 → 删旧表。可限流、可暂停、可回滚。

```bash
# gh-ost 示例（无触发器，更可控）
gh-ost --host=... --database=app --table=orders \
  --alter="MODIFY amount DECIMAL(14,2) NOT NULL" --execute
```

## 通用纪律

- 任何大表 DDL **先在预发等量数据上演练**，记录耗时与锁情况。
- **低峰执行**，配监控（主从延迟、锁等待）随时可中止。
- 加列尽量放末尾、带默认值、走 instant/inplace。

## 自检

- [ ] 判断过该 DDL 是 INPLACE 免重建还是 COPY 重建表？
- [ ] 普通加列/加索引是否带 `ALGORITHM=INPLACE, LOCK=NONE` 做保险？
- [ ] 改列类型/改主键等 COPY 操作是否走 gh-ost/pt-osc 而非直接 ALTER？
- [ ] 是否在等量预发演练过、确认低峰执行并有监控可中止？

## 相关

- 父：[`./index.md`](./index.md)
- 迁移模板：[`../../../lang/sql/ddl/index.md`](../../../lang/sql/ddl/index.md)
- 索引设计：[`../index/index.md`](../index/index.md)
