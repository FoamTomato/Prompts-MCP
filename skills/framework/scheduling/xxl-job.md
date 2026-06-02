---
name: scheduling-xxl-job
description: XXL-Job 分布式任务调度 — 调度中心统一触发（免分布式锁）、可视化管理、失败重试、分片广播，国内中小项目首选。Use when 集群定时任务避免重复执行 / 要可视化运维与失败重试 / 大数据量分片处理时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 分布式调度
  - 分片广播
  - XXL-Job
  - '@XxlJob'
  - 失败重试
  - 调度中心
effort: medium
context: inline
version: '1.0'
---
# Scheduling · XXL-Job 分布式调度

> 本条只管「为什么/怎么用 XXL-Job 做集群调度」。单机简单定时用 [`scheduled-annotation.md`](./scheduled-annotation.md)，复杂 Cron 持久化用 [`quartz.md`](./quartz.md)。

> 数字/版本为业界量级参考，落地以官方文档为准。

## 何时选它

| 需求 | XXL-Job 怎么解 |
|------|--------------|
| 集群避免重复执行 | **调度中心统一触发**，按路由策略只派给一个执行器（无需自己加分布式锁） |
| 运维可视化 | Web 控制台管理任务、查看调度日志、手动触发/停止 |
| 失败自动恢复 | 配失败重试次数 + 超时控制 + 失败告警（邮件/钉钉） |
| 大数据量分批 | **分片广播**：同一任务派给 N 台执行器，按分片号各处理一段，水平扩展 |
| 路由策略 | 第一个/轮询/故障转移/一致性 Hash/分片广播 等可选 |

依赖 MySQL 存调度元数据；调度中心与执行器分离部署。

## 正例

```java
@Component
public class SyncJobHandler {

    // ✅ Bean 模式：方法标 @XxlJob，名字与控制台配置的 JobHandler 一致
    @XxlJob("syncOrderHandler")
    public void syncOrder() {
        // 读控制台传入的任务参数
        final String param = XxlJobHelper.getJobParam();
        XxlJobHelper.log("sync start, param={}", param);  // 日志回传控制台
        doSync(param);
        // 不调 handleFail 即默认成功；失败显式标记
    }

    // ✅ 分片广播：每台执行器只处理 id % total == index 的数据
    @XxlJob("shardingSyncHandler")
    public void shardingSync() {
        final int index = XxlJobHelper.getShardIndex();   // 当前分片序号
        final int total = XxlJobHelper.getShardTotal();   // 分片总数
        userMapper.selectByShard(index, total).forEach(this::handle);
    }
}
```

## 反例

```java
// ❌ 在 XXL-Job 任务里又叠一层 @Scheduled —— 触发权应只交给调度中心
@Scheduled(cron = "0 0 2 * * ?")
@XxlJob("badHandler")
public void bad() { /* ... */ }

// ❌ 分片广播任务不按分片号过滤数据 → 每台执行器全量处理，重复 N 倍
@XxlJob("fullScanHandler")
public void fullScan() {
    userMapper.selectAll().forEach(this::handle);  // 没用 shardIndex/shardTotal
}
```

## 自检

- [ ] 集群下用调度中心统一触发，**没有**再自己加 `@Scheduled` 或分布式锁？
- [ ] `@XxlJob` 的 handler 名与控制台 JobHandler 配置一致？
- [ ] 配了失败重试次数、超时时间、失败告警？
- [ ] 大数据量任务用分片广播，且按 `shardIndex/shardTotal` 过滤数据（不全量处理）？
- [ ] 任务进度/异常用 `XxlJobHelper.log` 回传，便于控制台排障？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`scheduled-annotation.md`](./scheduled-annotation.md)（单机简单定时，免调度中心）
- 兄弟：[`quartz.md`](./quartz.md)（复杂 Cron + 持久化的另一选择）
