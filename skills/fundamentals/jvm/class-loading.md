---
name: jvm-class-loading
description: 类加载规约 — 双亲委派为何不能乱破、SPI 何时合法打破（JDBC/Dubbo）、何时才该自定义 ClassLoader。Use when 处理 ClassNotFound/NoClassDefFound / 写 SPI 扩展 / 考虑自定义 ClassLoader 时。
parent: ./index.md
paths:
- '*.java'
- '*.yml'
triggers:
  keywords:
  - 类加载
  - 双亲委派
  - SPI
  - ClassLoader
  - ServiceLoader
  - NoClassDefFound
effort: medium
context: inline
version: '1.0'
---
# JVM · 类加载规约

> 本条只管「类加载该怎么用、何时打破默认」。元空间因类加载泄漏 OOM 见 [`oom-troubleshooting.md`](./oom-troubleshooting.md) 的元空间分支。

## 规则

| 决策 | 规约 |
|------|------|
| 默认行为 | **遵守双亲委派**：类优先交父加载器，保证 `java.*` 等核心类不被替换、全局唯一 |
| 加载冲突排查 | `NoClassDefFound`/`ClassNotFound` 先查依赖冲突（同类多版本）、再查是否被多个 ClassLoader 各加载一份 |
| SPI 扩展 | 用 `ServiceLoader` + `META-INF/services`，**只在框架需要加载实现方的类时**才用线程上下文类加载器打破委派 |
| 自定义 ClassLoader | **绝大多数业务不需要**；仅热部署 / 插件隔离 / 同类多版本共存等场景才写 |

## SPI：合法打破委派的场景

双亲委派下，父加载器（如启动类加载器加载的 JDBC 接口）**看不到**子加载器路径上的实现（如应用 classpath 的 MySQL Driver）。SPI 用**线程上下文类加载器**绕过这一限制：

```java
// JDBC：DriverManager 通过 ServiceLoader 找到 classpath 上的 Driver 实现
ServiceLoader<Driver> loaders = ServiceLoader.load(Driver.class);
for (Driver d : loaders) { /* 由线程上下文 ClassLoader 加载实现 */ }
```

```text
典型 SPI 案例（都是"接口在上层、实现在下层"）：
- JDBC：java.sql.Driver 接口 ←→ 各数据库 Driver 实现
- Dubbo：@SPI 自有扩展机制（带自适应/激活），比 JDK ServiceLoader 更强
- SLF4J：门面接口 ←→ logback/log4j2 绑定实现
```

## 何时才自定义 ClassLoader

```text
需要 → 热部署（改了类不重启即生效）、插件系统（各插件类隔离）、
       同一个类的多版本在一个 JVM 共存（如多租户加载不同版本规则）
不需要 → 普通 Spring 业务：交给框架和默认加载器，自己写纯属引入隐患
```

## 反例

```text
❌ 为"加载个配置类"自定义 ClassLoader：徒增复杂度和泄漏风险
❌ 把核心包 java.*/javax.* 放进自定义路径想覆盖：被双亲委派挡回，且本就是安全机制
❌ 自定义 ClassLoader 用完不释放引用：类卸不掉 → 元空间泄漏（见 oom-troubleshooting）
❌ 遇到 NoClassDefFound 就加 ClassLoader hack：八成是依赖版本冲突，先排依赖
```

## 自检

- [ ] 默认遵守双亲委派，没有无理由打破？
- [ ] 用 SPI 而非反射硬编码来加载可插拔实现？
- [ ] 确认当前场景真的需要自定义 ClassLoader（热部署/插件/多版本），而不是图省事？
- [ ] `NoClassDefFound` 先排查了依赖冲突，而非直接上 ClassLoader hack？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`oom-troubleshooting.md`](./oom-troubleshooting.md)（类加载泄漏导致元空间 OOM）
