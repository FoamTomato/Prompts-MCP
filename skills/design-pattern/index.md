---
name: design-pattern-index
description: 设计模式索引（Repository / Factory / Strategy / DDD 分层 / Pipeline / Assertion）
parent: ../index.md
children:
  - { name: repository, path: repository/index.md, tag: folder, note: 持久化薄壳，禁业务 }
  - { name: factory, path: factory/index.md, tag: folder, note: LLM provider 等多实现选择 }
  - { name: strategy, path: strategy/index.md, tag: folder, note: 导出器 / 渲染策略可替换 }
  - { name: ddd-layering, path: ddd-layering/index.md, tag: folder, note: Controller 薄 / Service 编排 / Domain 纯 }
  - { name: pipeline, path: pipeline/index.md, tag: folder, note: Step 方法链命名 }
  - { name: assertion, path: assertion/index.md, tag: folder, note: 断言式异常处理 — Asserts 类 + ApiException + 边界 try/except（W3.5 新增） }
when_to_descend: |
  任务涉及"结构性决策"：分层、抽象、可替换实现、多步流程编排、异常处理设计。
---

# Design Pattern · 设计模式

> 状态：**W1 占位** —— 子目录 W2 起新写（项目当前无对应 skill）。

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| repository | 文件夹 | Repo 只做 CRUD，禁业务逻辑 |
| factory | 文件夹 | LLM provider 等多实现选择 |
| strategy | 文件夹 | 导出器 / 渲染策略可替换 |
| ddd-layering | 文件夹 | Controller 薄 / Service 编排 / Domain 纯 |
| pipeline | 文件夹 | 多步流程的 Step 方法命名 |
| **assertion** | 文件夹 | **W3.5 新增**：断言式异常处理（Asserts 类 + ApiException + 边界 try/except） |

## 何时下钻

- 新增 `backend/repositories/*.py` / `py/repositories/*.py` → `repository/`
- 新增 LLM / OSS 多 provider 切换代码 → `factory/`
- 写 PPT / 试卷 / PDF 导出代码 → `strategy/`
- 设计新的 Service 层 → `ddd-layering/`
- 写多步 LLM 编排（如 outline → slides → render）→ `pipeline/`

## 下钻决策表

| 任务 | 选哪个子项 |
|------|----------|
| 写 PresentationService | ddd-layering + repository |
| 写 LLMProvider 抽象 | factory |
| 写 paper PDF 导出 | strategy |
| 写 outline_review 流式编排 | pipeline |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行维度：[`../lang/index.md`](../lang/index.md) · [`../framework/index.md`](../framework/index.md) · [`../habit/index.md`](../habit/index.md)
