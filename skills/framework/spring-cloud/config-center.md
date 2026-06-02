---
name: spring-cloud-config-center
description: 配置中心 Nacos/Apollo — 配置外置、@RefreshScope 动态刷新、namespace 分环境隔离、敏感配置加密。Use when 把配置搬进配置中心 / 做动态刷新 / 按环境隔离配置 / 处理敏感配置时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 配置中心
  - Nacos 配置
  - Apollo
  - '@RefreshScope'
  - 动态刷新
  - 配置加密
effort: medium
context: inline
version: '1.0'
---
# Spring Cloud · 配置中心（Nacos/Apollo）

> 本条只管「配置怎么外置 + 动态刷新 + 分环境 + 加密」。Nacos 作为注册中心见 [`service-discovery.md`](./service-discovery.md)。

## 规则

| 项 | 规则 |
|----|------|
| 外置 | 环境相关配置（DB/Redis/第三方地址）放配置中心，**不进 jar 包**；本地只留 bootstrap 引导信息 |
| 动态刷新 | 需热更的 Bean 标 `@RefreshScope`，配置变更不重启即生效 |
| 分环境 | 用 `namespace` 隔离 dev/test/prod，用 `group` 隔离业务线，**绝不混用一个 namespace** |
| 优先级 | `dataId` 精确到 `${app}-${profile}.yaml`，profile 由启动参数指定，别硬编码环境 |
| 敏感配置 | 密码/密钥**加密存储**（Jasypt / Nacos 加密插件 / KMS），禁明文落配置中心 |

## 正例

```yaml
# bootstrap.yml —— 只放引导信息，业务配置全在 Nacos
spring:
  application:
    name: order-service
  cloud:
    nacos:
      config:
        server-addr: ${NACOS_ADDR}
        namespace: ${ENV_NAMESPACE}        # ✅ 按环境隔离
        group: ORDER_GROUP
        file-extension: yaml
  profiles:
    active: ${SPRING_PROFILES_ACTIVE}      # ✅ 环境由启动参数注入
```

```java
// ✅ @RefreshScope：Nacos 改了限额，不重启即生效
@RefreshScope
@Component
public class RateLimitConfig {
    @Value("${order.max-per-day:100}")
    private int maxPerDay;
}
```

```yaml
# ✅ 敏感值用 Jasypt 加密，配置中心只存密文
spring:
  datasource:
    password: ENC(G6N718UnHqJBO8x6c...)
```

## 反例

```yaml
# ❌ 数据库密码明文写进配置中心 / 代码仓库
spring:
  datasource:
    password: P@ssw0rd123

# ❌ 写死 prod，换环境要改代码重新打包
spring:
  profiles:
    active: prod
```

## 自检

- [ ] 环境相关配置在配置中心，没硬编码进 jar / 代码？
- [ ] 需热更的 Bean 标了 `@RefreshScope`？
- [ ] dev/test/prod 用不同 `namespace` 隔离，没混用？
- [ ] profile 由启动参数注入，没把环境写死？
- [ ] 密码/密钥加密存储，配置中心无明文敏感值？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`service-discovery.md`](./service-discovery.md)（同一个 Nacos 既做配置中心也做注册中心）
