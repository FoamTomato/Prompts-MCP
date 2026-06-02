---
name: jvm-heap-params
description: JVM 堆启动参数规约 — -Xmx=-Xms 避免扩容抖动、元空间设上限、HeapDumpOnOutOfMemoryError 必加。Use when 写 JVM 启动参数 / 配 -Xmx-Xms / 设元空间上限时。
parent: ./index.md
paths:
- '*.java'
- '*.yml'
triggers:
  keywords:
  - 堆参数
  - Xmx
  - Xms
  - 元空间
  - Metaspace
  - HeapDumpOnOutOfMemoryError
effort: medium
context: inline
version: '1.0'
---
# JVM · 堆参数规约

> 本条只管「堆/元空间启动参数怎么设」。选哪个 GC 见 [`gc-selection.md`](./gc-selection.md)；参数设错后 OOM 怎么查见 [`oom-troubleshooting.md`](./oom-troubleshooting.md)。容器里堆按物理内存比例算（`-XX:MaxRAMPercentage`），别在容器里写死 `-Xmx`。

## 规则

| 参数 | 规约 | 理由 |
|------|------|------|
| `-Xmx` / `-Xms` | **设成相等** | 避免运行时堆动态扩容/缩容引发 GC 抖动与 STW |
| `-XX:MaxMetaspaceSize` | **必设上限** | 不设则元空间用本地内存，类加载泄漏会吃光机器内存 |
| `-XX:+HeapDumpOnOutOfMemoryError` | **必加** | OOM 瞬间自动 dump，否则现场全丢、无法复盘 |
| `-XX:HeapDumpPath` | 指向有空间的目录 | dump 文件可能和堆一样大，别写满磁盘 |
| 容器部署 | 用 `-XX:MaxRAMPercentage=75` 替代写死 `-Xmx` | 让 JVM 感知 cgroup 限额，随 Pod 规格自适应 |

## 正例

```yaml
# JDK17 在线服务（裸机/固定规格）
JAVA_OPTS: >-
  -Xms4g -Xmx4g
  -XX:MaxMetaspaceSize=512m
  -XX:+HeapDumpOnOutOfMemoryError
  -XX:HeapDumpPath=/var/log/dump/
```

```yaml
# 容器部署：不写死 Xmx，按容器内存比例
JAVA_OPTS: >-
  -XX:MaxRAMPercentage=75.0
  -XX:MaxMetaspaceSize=512m
  -XX:+HeapDumpOnOutOfMemoryError
  -XX:HeapDumpPath=/var/log/dump/
```

## 反例

```text
❌ -Xms512m -Xmx4g：启动后堆随负载反复扩缩，GC 抖动、停顿不稳
❌ 不设 MaxMetaspaceSize：动态生成类（CGLIB/热部署）泄漏后吃光本地内存，整机被拖垮
❌ 没加 HeapDumpOnOutOfMemoryError：线上 OOM 后只有一行报错，无 dump 可分析
❌ 容器里 -Xmx8g 但 Pod limit 只有 4g：被 OOMKilled（137），JVM 自己都来不及报 OOM
```

## 自检

- [ ] `-Xmx` 与 `-Xms` 相等？
- [ ] 设了 `-XX:MaxMetaspaceSize` 上限？
- [ ] 加了 `-XX:+HeapDumpOnOutOfMemoryError` 且 `HeapDumpPath` 指向有空间的目录？
- [ ] 容器部署用 `MaxRAMPercentage` 而非写死 `-Xmx`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`gc-selection.md`](./gc-selection.md)（选哪个 GC）
- 兄弟：[`oom-troubleshooting.md`](./oom-troubleshooting.md)（dump 出来后怎么分析）
