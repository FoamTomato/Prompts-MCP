---
name: sql-partition-required
description: 大表 SELECT 必带分区字段（按 Quill 数据规模不强制，预留）。Use when 写 SQL / 迁移脚本 / 评审涉及 `partition-required`
  的 PR。
parent: ./index.md
paths:
- py/migrations/**/*.py
- '**/*.sql'
triggers:
  keywords:
  - partition
  - 分区
  - big table
effort: medium
context: inline
version: '1.0'
---
# SQL · 大表必带分区字段

## 状态

Quill 当前数据规模未到必须分区表的程度（textbooks / presentations / sessions 等表行数 < 10M）。本规则**为未来扩展预留**。

## 规则（达到规模后启用）

对**分区表**的 SELECT 必须在 WHERE 含分区键，否则触发全分区扫描。

## 假设的 Quill 分区表

未来如 `llm_call_logs`（按 `partition_dt` 月分区）：

```sql
-- ❌ 全分区扫描（扫所有月份）
SELECT count(*) FROM llm_call_logs WHERE user_id = 123;

-- ✅ 限定分区
SELECT count(*) FROM llm_call_logs
WHERE partition_dt BETWEEN '20260501' AND '20260524'
  AND user_id = 123;
```

## 命名约定

Quill 分区字段统一 `partition_dt` 列，类型 `VARCHAR(8)` 存 `yyyyMMdd`。

## 何时引入分区

| 表 | 触发阈值 |
|----|--------|
| `llm_call_logs` | 总行数 > 5M 或 单月 > 1M |
| `referral_rewards` | 单月 > 100K |
| `assets` | 总行数 > 10M |

引入后这条规则升级为 hook 强制校验。

## 自检（当前阶段）

- [ ] 关心的查询是否在已分区表上？
- [ ] 如是，WHERE 是否含 `partition_dt`？

## 相关

- 父：[`./index.md`](./index.md)
- 配套：[`../ddl/alembic-migration-template.md`](../ddl/alembic-migration-template.md)

