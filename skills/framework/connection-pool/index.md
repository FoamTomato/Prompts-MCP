---
name: framework-connection-pool-index
description: 数据库连接池（HikariCP/Druid）规约 — HikariCP 参数与 maxLifetime、Druid 监控与防火墙、池大小估算与泄漏检测三个独立决策点。Use when 配 HikariCP 参数 / 选 Druid 做监控 / 估算池大小或排查连接泄漏时。
parent: ../index.md
children:
  - { name: connection-pool-hikaricp-config, path: hikaricp-config.md, tag: skill, note: "HikariCP 参数：maxLifetime 必须 < DB wait_timeout" }
  - { name: connection-pool-druid-monitoring, path: druid-monitoring.md, tag: skill, note: "Druid 监控页+SQL 防火墙+慢 SQL，何时选 Druid" }
  - { name: connection-pool-pool-sizing, path: pool-sizing.md, tag: skill, note: "池大小公式+leakDetectionThreshold，池过大反压垮 DB" }
when_to_descend: 写 / 改 Java 数据源连接池配置：填 HikariCP 参数、为监控引 Druid、估算池大小或排查连接泄漏与失效连接。
---

# 连接池 · 框架使用约定索引

三个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 填 HikariCP 参数、调超时、防拿到失效连接（maxLifetime） | [hikaricp-config](hikaricp-config.md) |
| 需要监控页 / SQL 防火墙 / 慢 SQL 统计，纠结要不要换 Druid | [druid-monitoring](druid-monitoring.md) |
| 估算 maximumPoolSize、排查连接泄漏、池过大压垮 DB | [pool-sizing](pool-sizing.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../mysql/index.md`](../mysql/index.md)（DB 侧 max_connections / wait_timeout）
- 平行：[`../mybatis/index.md`](../mybatis/index.md) · [`../spring-boot/index.md`](../spring-boot/index.md)
