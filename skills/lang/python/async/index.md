---
name: lang-python-async-index
description: Python 异步规范
parent: ../index.md
children:
  - { name: no-blocking-call, path: no-blocking-call.md, tag: skill, note: 禁 time.sleep / requests / 同步阻塞 }
  - { name: asyncio-pattern, path: asyncio-pattern.md, tag: skill, note: gather / wait / 锁 / 取消 }
  - { name: sse-streaming, path: sse-streaming.md, tag: skill, note: SSE 生成器模板 }
when_to_descend: 写 async / await / SSE 流式接口 / RQ worker。
---

# Python · 异步

| 子项 | 一句话 |
|------|-------|
| no-blocking-call | 所有 I/O 必须 await，禁 time.sleep / requests / 同步 SQL 客户端 |
| asyncio-pattern | gather 批并发 / 取消 / 超时 |
| sse-streaming | SSE 生成器模板（含 done 终止信号） |
