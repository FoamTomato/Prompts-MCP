---
name: connection-pool-druid-monitoring
description: Druid 连接池监控 — 监控页、SQL 防火墙、慢 SQL 统计，及何时为监控选 Druid 而非 HikariCP。Use when 需要连接池监控页 / 开 SQL 防火墙 / 统计慢 SQL / Druid 选型时。
parent: ./index.md
paths:
- '*.java'
- '*.yml'
triggers:
  keywords:
  - 连接池监控
  - Druid
  - SQL 防火墙
  - 慢 SQL 统计
  - StatViewServlet
effort: medium
context: inline
version: '1.0'
---
# 连接池 · Druid 监控与防火墙

> 本条只管「为监控/防火墙/慢 SQL 选 Druid 怎么配」。纯连接参数（maxLifetime 等）见 [`hikaricp-config.md`](./hikaricp-config.md)，Druid 同名参数语义一致；池大小见 [`pool-sizing.md`](./pool-sizing.md)。

## 何时选 Druid（否则用默认 HikariCP）

| 你的诉求 | 选 |
|---------|-----|
| 极致性能 / Spring Boot 默认 / 不需可视化 | **HikariCP** |
| 要监控页看 SQL 执行次数/耗时分布 | Druid `StatFilter` + `StatViewServlet` |
| 要拦危险 SQL（防注入、禁 DROP/全表删） | Druid `WallFilter` |
| 要在页面看慢 SQL 排行 | Druid `slowSqlMillis` |

> Druid 监控有性能开销，且 HikariCP 在纯吞吐上更快；不需要这些能力就别引入 Druid。

## 规则

| 项 | 约定 |
|----|------|
| filters | `stat`(监控)、`wall`(防火墙)、`slf4j`(日志) 按需开 |
| 慢 SQL | `slowSqlMillis` 设阈值（如 1000），`logSlowSql=true` |
| 监控页 | `StatViewServlet` 必须设登录账号密码，**生产禁匿名访问** |
| 防火墙 | `WallFilter` 拦 `multiStatementAllow`、`noneBaseStatementAllow` |

## 正例

```yaml
spring:
  datasource:
    druid:
      filters: stat,wall,slf4j
      filter:
        stat:
          slow-sql-millis: 1000      # >1s 记为慢 SQL
          log-slow-sql: true
      stat-view-servlet:
        enabled: true
        login-username: admin        # 生产必设，禁匿名
        login-password: ${DRUID_PWD}
        allow: 127.0.0.1             # 限 IP
```

## 反例

```yaml
# ❌ 监控页开放且无密码：/druid/ 直接暴露所有 SQL 与库结构
spring:
  datasource:
    druid:
      stat-view-servlet:
        enabled: true                # 无 login-username/password、无 allow 限制

# ❌ 不需要监控却引 Druid：白白吃 StatFilter 开销，不如用默认 HikariCP
```

## 自检

- [ ] 引 Druid 是因为确需监控/防火墙/慢 SQL，而非默认惯性？
- [ ] `StatViewServlet` 设了账号密码并限 IP，生产不匿名暴露？
- [ ] `slowSqlMillis` 设了阈值并开 `logSlowSql`？
- [ ] 危险 SQL 由 `WallFilter` 拦截（按需 multiStatement/DROP 策略）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`hikaricp-config.md`](./hikaricp-config.md)（连接参数，Druid 语义一致）
- 兄弟：[`pool-sizing.md`](./pool-sizing.md)（池大小与泄漏检测）
- 相关：[`../mysql/diagnosis/slow-query-triage.md`](../mysql/diagnosis/slow-query-triage.md)（DB 侧慢查询定位）
