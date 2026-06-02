---
name: scheduling-scheduled-annotation
description: Spring @Scheduled 单机定时任务 — fixedRate/fixedDelay/cron 选择，集群多节点会重复执行需分布式锁兜底。Use when 写单机定时任务 / 排查集群重复执行 / 选 fixedRate 还是 cron 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 定时任务
  - 集群重复执行
  - '@Scheduled'
  - fixedDelay
  - cron 表达式
  - 分布式锁兜底
effort: medium
context: inline
version: '1.0'
---
# Scheduling · @Scheduled 单机定时

> 本条只管「单机怎么写定时任务、集群重复执行怎么兜底」。多节点统一调度见 [`xxl-job.md`](./xxl-job.md)，异步执行见 [`async-execution.md`](./async-execution.md)。

## 规则

| 维度 | 约定 |
|------|------|
| 启用 | 配置类标 `@EnableScheduling`，任务方法标 `@Scheduled` 且无参无返回值 |
| 固定频率 | `fixedRate`：上次**开始**后固定间隔触发（不等上次结束，可能堆积） |
| 固定延迟 | `fixedDelay`：上次**结束**后固定间隔触发（串行，更安全，常用默认） |
| 复杂周期 | `cron = "0 0 2 * * ?"`：六位 Spring cron（秒 分 时 日 月 周），加 `zone` 指定时区 |
| 默认单线程 | 默认所有 `@Scheduled` 共用一个线程，一个任务卡住会拖垮其余 → 配 `TaskScheduler` 线程池 |
| **集群重复** | 多节点部署，**每个节点都会触发同一任务** → 必须分布式锁兜底，抢到锁才执行 |

## 正例

```java
@Configuration
@EnableScheduling
public class SchedulerConfig {
    // ✅ 配线程池，避免任务互相阻塞
    @Bean
    public TaskScheduler taskScheduler() {
        ThreadPoolTaskScheduler s = new ThreadPoolTaskScheduler();
        s.setPoolSize(4);
        s.setThreadNamePrefix("sched-");
        return s;
    }
}

@Component
@RequiredArgsConstructor
public class OrderTimeoutJob {
    private final RedissonClient redisson;

    // ✅ cron 每天 02:00；集群下用分布式锁保证只一个节点执行
    @Scheduled(cron = "0 0 2 * * ?")
    public void cancelTimeout() {
        final RLock lock = redisson.getLock("job:cancelTimeout");
        // 抢不到锁说明别的节点在跑，直接跳过
        if (!lock.tryLock()) {
            return;
        }
        try {
            // 执行业务
            doCancel();
        } finally {
            lock.unlock();
        }
    }
}
```

## 反例

```java
// ❌ 集群 3 个节点 → 同一时刻触发 3 次，订单被重复取消/通知重复发
@Scheduled(cron = "0 0 2 * * ?")
public void cancelTimeout() {
    doCancel();   // 没有任何分布式互斥
}

// ❌ fixedRate 任务执行时间 > 间隔，又没线程池 → 任务堆积、互相阻塞
@Scheduled(fixedRate = 1000)
public void heavy() { /* 跑 5 秒 */ }
```

## 自检

- [ ] 配置类标了 `@EnableScheduling`，任务方法无参无返回值？
- [ ] 想要串行不堆积用 `fixedDelay`，需要固定节奏才用 `fixedRate`？
- [ ] 配了 `TaskScheduler` 线程池，避免多任务共用单线程互相阻塞？
- [ ] **集群部署时**用分布式锁（Redisson）兜底，避免每个节点重复执行？
- [ ] 重复执行风险高 / 要可视化重试时，已考虑直接上 XXL-Job？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`async-execution.md`](./async-execution.md)（任务体内异步执行）
- 兄弟：[`xxl-job.md`](./xxl-job.md)（集群统一调度，免分布式锁）
- 分布式锁：[`../redis/index.md`](../redis/index.md)（Redisson `RLock` 兜底集群重复）
