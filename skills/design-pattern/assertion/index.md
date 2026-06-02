---
name: assertion-index
description: 断言式异常处理 — 失败立即抛 ApiException，业务代码线性直叙；4 个叶子下钻
parent: ../index.md
children:
  - { name: principle, path: principle.md, tag: skill, note: 三条精髓 + 12 个通用断言方法 }
  - { name: asserts-class, path: asserts-class.md, tag: skill, note: 场景化 Asserts 类命名约定 + 真实示范 }
  - { name: validator-vs-assertion, path: validator-vs-assertion.md, tag: skill, note: Pydantic 与 Asserts 各自的边界 + 5 个反例 }
  - { name: side-effect-cleanup, path: side-effect-cleanup.md, tag: skill, note: 与 ApiException 三件套配合的边界 try/except 模式 }
when_to_descend: |
  写业务校验代码 / 设计错误处理 / Code Review 时看到散落 if + raise / 评估新业务的 Asserts 类设计。
---

# Design Pattern · Assertion

## 一句话

**业务校验首选断言**：`<Domain>Asserts.<语义方法>(...)` 失败立即抛 ApiException，业务代码读起来像直叙。

## 来源

参考 Java `ImportAsserts` 范式。

## 何时下钻到这层

| 任务 | 选哪个子项 |
|------|---------|
| 新业务模块想加 Asserts 类 | asserts-class |
| 不确定 Asserts 与 Pydantic 怎么分工 | validator-vs-assertion |
| 在 service / pipeline 写 try/except | side-effect-cleanup |
| 想了解整体思想 | principle |

## 典型落点

代码层：
- 引擎：`py/core/assertion.py` 12 个静态方法
- 业务包装：`py/asserts/` 多个业务专属类（按领域命名）
- 前端镜像：`frontend/app/lib/assertion.ts` ApiError + Asserts 系列方法

## 链接

- 上层：[`../index.md`](../index.md)
- 配套：[`../../lang/python/error-handling/api-exception.md`](../../lang/python/error-handling/api-exception.md) · [`../../lang/typescript/error-handling/index.md`](../../lang/typescript/error-handling/index.md)
- 错误码字典：[`/.ai/skills/core/error_code_dict.md`](../../../../.ai/skills/core/error_code_dict.md)
