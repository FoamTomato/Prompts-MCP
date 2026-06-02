---
name: scheduling-async-execution
description: Spring @Async 异步执行 — 必须 @EnableAsync，且自定义线程池替代默认 SimpleAsyncTaskExecutor（每次新建线程不复用）。Use when 把方法改成异步 / 配异步线程池 / 排查 @Async 不生效时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 异步执行
  - 自定义线程池
  - '@Async'
  - '@EnableAsync'
  - SimpleAsyncTaskExecutor
  - 线程池隔离
effort: medium
context: inline
version: '1.0'
---
# Scheduling · @Async 异步执行

> 本条只管「方法怎么异步执行、用哪个线程池」。线程池核心参数调优见 [`../../lang/java/concurrency/thread-pool-config.md`](../../lang/java/concurrency/thread-pool-config.md)，定时触发见 [`scheduled-annotation.md`](./scheduled-annotation.md)。

## 规则

| 维度 | 约定 |
|------|------|
| 启用 | 配置类标 `@EnableAsync`，否则 `@Async` 注解被忽略、**同步执行不报错** |
| 自调用失效 | 同类内 `this.异步方法()` 不走代理 → 不异步；拆到另一个 Bean 调 |
| **禁默认线程池** | 不配线程池时用 `SimpleAsyncTaskExecutor`，**每次新建线程不复用** → 高并发线程暴涨 OOM |
| 自定义线程池 | 必须配 `ThreadPoolTaskExecutor`，指定 core/max/queue/拒绝策略/线程名前缀 |
| 多池隔离 | 不同业务用不同池（`@Async("ioPool")`），避免慢任务占满拖垮其他异步 |
| 返回值 | 无返回用 `void`，要拿结果用 `CompletableFuture<T>`；异常被框架吞，需 `AsyncUncaughtExceptionHandler` |

## 正例

```java
@Configuration
@EnableAsync
public class AsyncConfig {
    // ✅ 自定义线程池，复用线程、有界队列、明确拒绝策略
    @Bean("ioPool")
    public ThreadPoolTaskExecutor ioPool() {
        ThreadPoolTaskExecutor e = new ThreadPoolTaskExecutor();
        e.setCorePoolSize(8);
        e.setMaxPoolSize(16);
        e.setQueueCapacity(200);
        e.setThreadNamePrefix("async-io-");
        e.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        e.initialize();
        return e;
    }
}

@Service
public class MailService {
    // ✅ 指定线程池名，避免和别的异步业务抢线程
    @Async("ioPool")
    public void sendAsync(String to) {
        // 发邮件，不阻塞调用方
    }
}
```

## 反例

```java
// ❌ 没标 @EnableAsync → @Async 失效，方法仍在调用线程同步执行（且不报错）
@Service
public class MailService {
    @Async
    public void sendAsync(String to) { /* 实际同步执行 */ }
}

// ❌ 标了 @EnableAsync 但不配线程池 → 用 SimpleAsyncTaskExecutor
//    每次调用新建线程、不复用，请求一多线程数失控 → OOM
@Async
public void handle() { /* ... */ }

// ❌ 同类自调用：异步不生效
public void outer() { this.sendAsync("x"); }  // 走 this，绕过代理
```

## 自检

- [ ] 配置类标了 `@EnableAsync`（否则注解静默失效）？
- [ ] 配了自定义 `ThreadPoolTaskExecutor`，**没用**默认 `SimpleAsyncTaskExecutor`？
- [ ] 线程池指定了有界队列 + 拒绝策略 + 线程名前缀？
- [ ] 不同业务用不同池隔离，慢任务不拖垮其他异步？
- [ ] 没有同类内 `this.异步方法()` 自调用（否则不异步）？
- [ ] 要结果用 `CompletableFuture`，无返回的异常配了 `AsyncUncaughtExceptionHandler`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`scheduled-annotation.md`](./scheduled-annotation.md)（定时触发，常与异步配合）
- 线程池调参：[`../../lang/java/concurrency/thread-pool-config.md`](../../lang/java/concurrency/thread-pool-config.md)
