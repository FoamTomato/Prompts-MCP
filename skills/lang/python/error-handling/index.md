---
name: lang-python-error-handling-index
description: Python 异常处理规范
parent: ../index.md
children:
  - { name: api-exception, path: api-exception.md, tag: skill, note: ApiException 三件套 }
  - { name: logger-exc-info, path: logger-exc-info.md, tag: skill, note: logger.error 必带 exc_info=True }
  - { name: no-bare-except, path: no-bare-except.md, tag: skill, note: 禁裸 except / 异常吞掉 }
  - { name: exception-group, path: exception-group.md, tag: skill, note: "ExceptionGroup / except* 聚合并发错误 + add_note" }
  - { name: raise-from-chaining, path: raise-from-chaining.md, tag: skill, note: raise from 链式异常 / 保留根因 }
  - { name: eafp-vs-lbyl, path: eafp-vs-lbyl.md, tag: skill, note: EAFP vs LBYL 风格 / suppress 忽略预期异常 }
when_to_descend: 写 try/except / Service 编排 / 失败回滚 / 并发任务错误聚合
---

# Error Handling · 子项索引

| 你在做什么 | 进哪个 |
|------|-------|
| 抛业务异常、定义错误码 | api-exception |
| 记录错误日志、要带 traceback | logger-exc-info |
| 该不该 catch、catch 块怎么写 | no-bare-except |
| TaskGroup 多任务失败、一次抛多个错误、给异常加备注 | exception-group |
| 把底层异常转成领域异常、traceback 缺根因 | raise-from-chaining |
| 纠结用 try 还是 if 先检查、想静默忽略某个预期异常 | eafp-vs-lbyl |
