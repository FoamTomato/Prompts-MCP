---
name: lang-python-error-handling-index
description: Python 异常处理规范
parent: ../index.md
children:
  - { name: api-exception, path: api-exception.md, tag: skill, note: ApiException 三件套 }
  - { name: logger-exc-info, path: logger-exc-info.md, tag: skill, note: logger.error 必带 exc_info=True }
  - { name: no-bare-except, path: no-bare-except.md, tag: skill, note: 禁裸 except / 异常吞掉 }
when_to_descend: 写 try/except / Service 编排 / 失败回滚
---

# Error Handling · 子项索引

| 子项 | 一句话 |
|------|-------|
| api-exception | ApiException 三件套 |
| logger-exc-info | logger.error 必带 exc_info=True |
| no-bare-except | 禁裸 except / 异常吞掉 |
