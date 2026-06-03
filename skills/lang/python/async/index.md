---
name: lang-python-async-index
description: Python 异步规范
parent: ../index.md
children:
  - { name: no-blocking-call, path: no-blocking-call.md, tag: skill, note: 禁 time.sleep / requests / 同步阻塞 }
  - { name: asyncio-pattern, path: asyncio-pattern.md, tag: skill, note: gather / wait / 锁 / 取消 }
  - { name: sse-streaming, path: sse-streaming.md, tag: skill, note: SSE 生成器模板 }
  - { name: py-async-taskgroup-timeout, path: taskgroup-timeout.md, tag: skill, note: TaskGroup 结构化并发 + timeout }
  - { name: py-async-cancellation-handling, path: cancellation-handling.md, tag: skill, note: CancelledError 传播 / shield / 清理 }
  - { name: py-async-sync-bridge, path: sync-bridge.md, tag: skill, note: to_thread / run_in_executor 桥接同步 }
  - { name: py-async-async-pitfalls, path: async-pitfalls.md, tag: skill, note: 忘记 await / fire-and-forget 丢引用 }
when_to_descend: 写 async / await / SSE 流式接口 / RQ worker。
---

# Python · 异步

| 你在做什么 | 进哪个 |
|------|-------|
| async 内出现同步阻塞 I/O | no-blocking-call |
| gather 批并发 / 锁 / 信号量限流 | asyncio-pattern |
| 写 SSE 流式接口 | sse-streaming |
| 多任务并发要一败全停 / 给一组任务设超时 | taskgroup-timeout |
| 处理取消传播 / shield 保护关键收尾 | cancellation-handling |
| async 内要调同步库 / CPU 密集计算 | sync-bridge |
| 协程没执行 / 后台任务静默消失 | async-pitfalls |
