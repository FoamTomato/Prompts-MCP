---
name: connection-pool-pool-sizing
description: 连接池大小估算与泄漏检测 — (核数*2)+磁盘数 估 maximumPoolSize、leakDetectionThreshold 测泄漏，反模式池过大压垮 DB。Use when 估算池大小 / 排查连接泄漏 / 池调大后 DB 反变慢时。
parent: ./index.md
paths:
- '*.java'
- '*.yml'
triggers:
  keywords:
  - 池大小估算
  - 连接泄漏
  - leakDetectionThreshold
  - maximumPoolSize
  - 池过大
effort: medium
context: inline
version: '1.0'
---
# 连接池 · 池大小估算与泄漏检测

> 本条只管「池开多大、怎么发现连接漏了」。各参数完整语义见 [`hikaricp-config.md`](./hikaricp-config.md)；要监控页看连接占用见 [`druid-monitoring.md`](./druid-monitoring.md)。

## 池大小估算

| 项 | 约定 |
|----|------|
| 起点公式 | `连接数 ≈ (CPU 核数 * 2) + 有效磁盘数`（HikariCP 官方经验值，需压测校准） |
| 多服务实例 | 每实例的池都连同一 DB，**总连接 = 实例数 * 单池大小**，别超 DB `max_connections` |
| 短事务优先 | 缩短持有时间比扩池更有效；事务里别夹 RPC/远程调用 |
| 上限约束 | 单池一般个位数到几十，几百是危险信号 |

> 公式与数字为业界量级参考，落地需结合压测自测。

## 连接泄漏检测

| 项 | 约定 |
|----|------|
| `leakDetectionThreshold` | 连接借出超此毫秒未还则告警（如 60000=60s），生产排查期开 |
| 典型泄漏 | 手动 `getConnection()` 后未 close、异常路径漏归还 |
| 根治 | 用 `try-with-resources` 或框架托管（MyBatis/JdbcTemplate 自动归还） |

## 正例

```java
// ✅ try-with-resources 保证归还，杜绝泄漏
try (Connection conn = dataSource.getConnection();
     PreparedStatement ps = conn.prepareStatement(sql)) {
    ps.executeUpdate();
}   // conn 自动归还池，异常路径也归还
```

```yaml
# ✅ 排查期开泄漏检测；池大小按公式估（8 核 → ~18），非拍大数
spring:
  datasource:
    hikari:
      maximum-pool-size: 18
      leak-detection-threshold: 60000   # 借出 >60s 未还即告警
```

## 反例

```yaml
# ❌ 池开到 200，DB max_connections=300，3 个实例 → 600 连接打爆 DB
# 现象：连接池"够用"但 DB 上下文切换/锁竞争飙升，整体反而更慢
spring:
  datasource:
    hikari:
      maximum-pool-size: 200
```

```java
// ❌ 手动取连接不归还：每次请求漏一个，池被耗尽后全部 connection-timeout
Connection conn = dataSource.getConnection();
conn.prepareStatement(sql).executeUpdate();   // 无 close，泄漏
```

## 自检

- [ ] `maximumPoolSize` 按 `(核数*2)+磁盘数` 估并压测校准，而非随手填大数？
- [ ] 算过 `实例数 * 单池大小` 没超 DB `max_connections`？
- [ ] 没有把连接开到几百这种「池过大压垮 DB」的反模式？
- [ ] 取连接走 try-with-resources / 框架托管，排查期开了 `leakDetectionThreshold`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`hikaricp-config.md`](./hikaricp-config.md)（各参数完整语义）
- 兄弟：[`druid-monitoring.md`](./druid-monitoring.md)（监控页看连接占用）
- 相关：[`../mysql/index.md`](../mysql/index.md)（DB 侧 max_connections 上限）
