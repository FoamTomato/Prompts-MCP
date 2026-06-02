---
name: connection-pool-hikaricp-config
description: HikariCP 核心参数 — connectionTimeout、idleTimeout，及 maxLifetime 必须 < DB wait_timeout 防失效连接。Use when 配 HikariCP 参数 / 调连接池超时 / 排查拿到失效连接时。
parent: ./index.md
paths:
- '*.java'
- '*.yml'
triggers:
  keywords:
  - 连接池参数
  - HikariCP
  - maxLifetime
  - connectionTimeout
  - wait_timeout
effort: medium
context: inline
version: '1.0'
---
# 连接池 · HikariCP 核心参数

> 本条只管「HikariCP 各参数怎么填、为何这么填」。池大小估算公式与泄漏检测见 [`pool-sizing.md`](./pool-sizing.md)；要不要换 Druid 见 [`druid-monitoring.md`](./druid-monitoring.md)。

## 规则

| 参数 | 约定 | 理由 |
|------|------|------|
| `maximum-pool-size` | 见 [`pool-sizing.md`](./pool-sizing.md) 公式，**不是越大越好** | 池过大反压垮 DB |
| `minimum-idle` | 一般 = maximumPoolSize（官方推荐固定池） | 避免频繁建/销连接抖动 |
| `connection-timeout` | 获取连接最长等待，默认 30s，建议 3~5s 快速失败 | 拖到 30s 请求堆积雪崩 |
| `idle-timeout` | 空闲回收，默认 10min；minIdle=maxPool 时此项失效 | 固定池下无需回收 |
| `max-lifetime` | 连接最大存活，**必须 < DB `wait_timeout`**（差 30~60s） | 否则拿到已被 DB 单边关闭的失效连接 |
| `validation-timeout` | 校验连接超时，默认 5s | 小于 connectionTimeout |

> `maxLifetime < wait_timeout` 是铁律：MySQL 默认 `wait_timeout=28800s`(8h)，但云 RDS/中间件常压到几分钟，必须按实际值反推。

## 正例

```yaml
# application.yml — maxLifetime 比 DB wait_timeout 至少小 60s
spring:
  datasource:
    hikari:
      maximum-pool-size: 12          # 按公式估算，非拍脑袋
      minimum-idle: 12               # 固定池，等于 max
      connection-timeout: 3000       # 3s 快速失败，不拖垮上游
      idle-timeout: 600000           # 10min
      max-lifetime: 1700000          # 1700s < DB wait_timeout(如 1800s)
      connection-test-query: SELECT 1
```

## 反例

```yaml
# ❌ max-lifetime 大于 / 等于 DB wait_timeout
spring:
  datasource:
    hikari:
      max-lifetime: 0                # 0=永不过期，DB 单边关连接后必拿到失效连接
      # 表现：偶发 "Communications link failure" / "connection is closed"

# ❌ connection-timeout 用默认 30s：DB 抖动时请求全卡 30s，线程池被占满
```

## 自检

- [ ] `max-lifetime` 严格 < DB `wait_timeout`（差 30~60s），且没设成 0？
- [ ] `connection-timeout` 调到秒级（3~5s）快速失败，而非默认 30s？
- [ ] `minimum-idle` = `maximum-pool-size`，用固定池避免抖动？
- [ ] `maximum-pool-size` 是按公式估的，不是越大越好（见 pool-sizing）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`pool-sizing.md`](./pool-sizing.md)（maximumPoolSize 怎么算、泄漏检测）
- 兄弟：[`druid-monitoring.md`](./druid-monitoring.md)（需要监控时换 Druid）
- 相关：[`../mysql/index.md`](../mysql/index.md)（DB 侧连接数与 wait_timeout）
