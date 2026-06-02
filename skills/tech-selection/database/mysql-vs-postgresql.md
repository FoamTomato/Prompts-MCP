---
name: tech-selection-mysql-vs-pg
description: 关系库选 MySQL 还是 PostgreSQL — PG 在 JSONB/复杂查询/GIS/扩展上更优，MySQL 在极端写密集/既有资产上够用。Use when 新项目选关系库 / 对比 MySQL 与 PostgreSQL / 评审关系库选型时。
parent: ./index.md
paths:
- '*.java'
- '*.yml'
- '*.xml'
- '*.sql'
triggers:
  keywords:
  - 关系库选型
  - 数据库选型
  - PostgreSQL
  - MySQL
  - JSONB
  - 分库分表
effort: medium
context: inline
version: '1.0'
---
# 关系库 · MySQL vs PostgreSQL

> 本条只管「关系库选 MySQL 还是 PG」。文档库见 [`when-mongodb.md`](./when-mongodb.md)；该不该用关系库见 [`decision-tree.md`](./decision-tree.md)。

## 选型边界

| 倾向 PostgreSQL（更优） | 倾向 MySQL（够用） |
|---|---|
| 半结构化数据 JSONB + GIN 索引 | 极端写密集的简单 OLTP |
| 复杂查询：CTE（全语句）/ 窗口函数（ROWS+RANGE） | 既有 LAMP / 遗留系统 |
| GIS：PostGIS | 团队只熟 MySQL 运维 |
| 扩展生态：pgvector（向量）/ FDW（外部表） | 读写简单、无复杂分析 |
| 更强的 SQL 标准遵从 | 需成熟分库分表中间件（ShardingSphere） |

## 默认建议

> **新项目默认优先 PostgreSQL** —— 能力基本是 MySQL 的超集；唯有「极端写吞吐」或「已有 MySQL 资产/团队」才选 MySQL。

注意：能力是超集 ≠ 必须上 PG。团队熟悉度、既有资产、运维生态也是权重，不能只看功能多。

## 反例

- ❌ 团队全员只会 MySQL 运维、系统读写极简，却为「PG 功能多」强上 PG —— 运维风险盖过收益。
- ❌ 重度依赖 JSONB 复杂查询 / 向量检索 / PostGIS，却选 MySQL 再用应用层硬凑 —— 该选 PG。

## 自检

- [ ] 本项目真用得上 JSONB / 窗口函数 / GIS / 向量这些 PG 优势？
- [ ] 选 MySQL 的理由是「极端写吞吐 / 既有资产」而非惯性？
- [ ] 新项目无特殊约束时默认优先了 PostgreSQL？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`when-mongodb.md`](./when-mongodb.md)（文档库何时合适）
- 兄弟：[`decision-tree.md`](./decision-tree.md)（关系/文档/KV 总决策树）
