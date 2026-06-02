---
name: scheduling-quartz
description: Quartz 调度框架 — 复杂 Cron 编排、Job/Trigger 分离、misfire 补偿策略，集群用 JDBC JobStore 持久化到数据库。Use when 写复杂 Cron 调度 / 任务要持久化恢复 / 配 Quartz 集群时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 复杂调度
  - 持久化任务
  - Quartz
  - JobStore
  - Trigger
  - misfire 补偿
effort: medium
context: inline
version: '1.0'
---
# Scheduling · Quartz 复杂调度

> 本条只管「Quartz 的复杂 Cron + 持久化 + 集群怎么配」。单机一个注解搞定用 [`scheduled-annotation.md`](./scheduled-annotation.md)，要可视化运维/分片用 [`xxl-job.md`](./xxl-job.md)。

## 何时选它

| 需求 | Quartz 怎么解 |
|------|-------------|
| 复杂 Cron 编排 | `CronTrigger` 七位 Cron（含年）、`SimpleTrigger` 固定间隔重复 N 次 |
| Job 与触发解耦 | `JobDetail`（做什么）与 `Trigger`（何时触发）分离，一个 Job 挂多个 Trigger |
| 任务持久化 | **JDBC JobStore**：Job/Trigger 状态存表，重启不丢、可恢复 |
| 集群不重复 | 集群模式靠数据库行锁抢占，**同一 Trigger 只一个节点执行** |
| 错过补偿 | misfire 策略：宕机/阻塞错过的触发，恢复后按策略补跑或忽略 |

代价：配置比 `@Scheduled` 重，无开箱可视化（要自己做或上 XXL-Job）。

## 正例

```java
@Configuration
public class QuartzConfig {

    // ✅ JobDetail：声明做什么，durably 让无 Trigger 也存活
    @Bean
    public JobDetail syncJobDetail() {
        return JobBuilder.newJob(SyncJob.class)
                .withIdentity("syncJob")
                .storeDurably()
                .build();
    }

    // ✅ CronTrigger：声明何时触发 + misfire 策略
    @Bean
    public Trigger syncTrigger(JobDetail syncJobDetail) {
        return TriggerBuilder.newTrigger()
                .forJob(syncJobDetail)
                .withSchedule(CronScheduleBuilder
                        .cronSchedule("0 0 2 * * ?")
                        .withMisfireHandlingInstructionFireAndProceed())
                .build();
    }
}

// 集群持久化配置（application.yml）：
// spring.quartz.job-store-type: jdbc
// spring.quartz.properties.org.quartz.jobStore.isClustered: true
```

## 反例

```java
// ❌ Job 里持有非线程安全的成员状态 —— 集群/并发触发互相污染
public class SyncJob implements Job {
    private int counter;  // 跨触发共享，多节点必错
    public void execute(JobExecutionContext ctx) { counter++; }
}

// ❌ 用 RAMJobStore（默认内存）还想集群 —— 重启即丢、多节点各跑各的、必重复
// spring.quartz.job-store-type: memory   ← 集群场景错误
```

## 自检

- [ ] 复杂编排才上 Quartz；单机简单定时用 `@Scheduled` 即可？
- [ ] `JobDetail` 与 `Trigger` 分离，Job 类**无可变成员状态**（线程安全）？
- [ ] 集群部署时用 **JDBC JobStore** + `isClustered: true`，没用内存 JobStore？
- [ ] 为 Trigger 配了 misfire 策略，明确宕机错过后补跑还是忽略？
- [ ] 需要可视化运维/失败重试/分片时，已评估改用 XXL-Job？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`scheduled-annotation.md`](./scheduled-annotation.md)（单机简单定时）
- 兄弟：[`xxl-job.md`](./xxl-job.md)（要可视化/重试/分片选它）
