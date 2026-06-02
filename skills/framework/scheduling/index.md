---
name: framework-scheduling-index
description: Java 任务调度索引 — @Scheduled 单机定时 / @Async 异步 / XXL-Job 分布式调度 / Quartz 复杂持久化四个独立决策点。Use when 写定时任务 / 做异步执行 / 选调度框架 / 排查集群重复执行时。
parent: ../index.md
children:
  - { name: scheduling-scheduled-annotation, path: scheduled-annotation.md, tag: skill, note: "@Scheduled 单机定时，集群会重复执行需分布式锁兜底" }
  - { name: scheduling-async-execution, path: async-execution.md, tag: skill, note: "@Async 异步必须 @EnableAsync + 自定义线程池" }
  - { name: scheduling-xxl-job, path: xxl-job.md, tag: skill, note: "XXL-Job 分布式调度，可视化+失败重试+分片广播" }
  - { name: scheduling-quartz, path: quartz.md, tag: skill, note: "Quartz 复杂 Cron + 持久化，集群 JDBC JobStore" }
when_to_descend: 写 / 改定时任务、异步方法，或为定时任务选调度框架（单机 / 分布式 / 复杂持久化）。
---

# Scheduling · 任务调度索引

四个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 单机写个简单定时任务（fixedRate/cron） | [scheduled-annotation](scheduled-annotation.md) |
| 把方法改成异步执行、不阻塞调用方 | [async-execution](async-execution.md) |
| 多节点分布式调度、要可视化/重试/分片 | [xxl-job](xxl-job.md) |
| 复杂 Cron 编排、任务要持久化到 DB | [quartz](quartz.md) |

## 选型决策（先定哪一类，再下钻）

| 场景 | 选哪个 | 理由 |
|------|-------|------|
| 单机、简单、可接受集群重复 | `@Scheduled` | 零依赖，一个注解搞定 |
| 多节点集群、要避免重复执行 | **XXL-Job** | 调度中心统一触发，国内中小项目首选 |
| 复杂 Cron 编排 + 任务持久化 | **Quartz** | misfire 策略、JDBC JobStore 集群 |

> `@Scheduled` 集群下每个节点都会触发同一任务 → 重复执行。要么加分布式锁兜底（见 scheduled-annotation），要么直接上 XXL-Job 由调度中心统一派发。

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../spring-boot/index.md`](../spring-boot/index.md)
- 相关：[`../redis/index.md`](../redis/index.md)（分布式锁兜底 `@Scheduled` 集群重复）
