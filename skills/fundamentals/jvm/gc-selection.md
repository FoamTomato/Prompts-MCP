---
name: jvm-gc-selection
description: 给 Java 服务选 GC 的决策 — G1 默认、ZGC 超大堆低延迟（JDK17+）、Parallel 吞吐批处理，以及何时该换。Use when 选 GC / 调 GC 停顿 / 配 -XX:+Use*GC 参数时。
parent: ./index.md
paths:
- '*.java'
- '*.yml'
triggers:
  keywords:
  - GC 选型
  - 垃圾回收器
  - G1
  - ZGC
  - Parallel GC
  - GC 停顿
effort: medium
context: inline
version: '1.0'
---
# JVM · GC 选型决策

> 本条只管「该用哪个 GC、何时换」，不讲 GC 算法原理。堆大小怎么设见 [`heap-params.md`](./heap-params.md)；GC 引发的 OOM 排查见 [`oom-troubleshooting.md`](./oom-troubleshooting.md)。性能数字为业界量级参考，落地需自测。

## 规则：默认 G1，按瓶颈换

| 你的场景 | 选 | 关键参数 |
|---------|-----|---------|
| 普通在线服务、堆 < 32G（绝大多数） | **G1**（JDK9+ 默认） | `-XX:MaxGCPauseMillis=200` |
| 堆很大（几十 G~TB）且要求停顿 < 10ms | **ZGC**（JDK17+ 转正、生产可用） | `-XX:+UseZGC` |
| 离线批处理 / 跑批，只追求总吞吐、不在乎单次停顿 | **Parallel** | `-XX:+UseParallelGC` |
| 还在用 CMS（JDK14 已移除） | **迁 G1** | 删 `-XX:+UseConcMarkSweepGC` |

## 决策：何时该换 GC

```text
现状 G1，但 P99 接口延迟被 GC 停顿拖高（jstat/GC 日志看到单次 STW > MaxGCPauseMillis）
  → 堆 < 32G：先调 MaxGCPauseMillis、加堆，别急着换
  → 堆很大且仍超目标，JDK17+：换 ZGC

现状 Parallel（老服务默认），是在线接口服务，偶发长 STW 抖动
  → 换 G1（停顿可控优先于吞吐）

跑批任务嫌总耗时长、不在乎停顿
  → 换 Parallel（吞吐优先）
```

## 正例：显式声明，不靠隐式默认

```yaml
# 在线服务（JDK17）：G1 + 停顿目标 + dump（dump 细节见 heap-params）
JAVA_OPTS: >-
  -XX:+UseG1GC
  -XX:MaxGCPauseMillis=200
  -Xlog:gc*:file=/var/log/gc.log:time,uptime:filecount=5,filesize=20m
```

## 反例

```text
❌ 大堆低延迟服务用 Parallel：吞吐高但单次 Full GC 停顿数秒，接口超时雪崩
❌ 离线跑批用 G1 还调小 MaxGCPauseMillis：频繁小 GC 反而拉低总吞吐
❌ 不开 GC 日志就靠感觉换 GC：换前换后无法对比，等于盲调
```

## 自检

- [ ] 启动参数**显式**写了 `-XX:+UseXxxGC`，没靠 JDK 默认隐式决定？
- [ ] 选型依据是真实瓶颈（停顿 / 吞吐），而非"听说 ZGC 快"？
- [ ] 用 ZGC 前确认运行在 JDK17+？
- [ ] 开了 GC 日志，换 GC 前后能用数据对比？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`heap-params.md`](./heap-params.md)（堆大小与元空间怎么设）
- 兄弟：[`oom-troubleshooting.md`](./oom-troubleshooting.md)（GC 频繁/堆满引发 OOM 时排查）
