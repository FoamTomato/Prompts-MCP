---
name: framework-index
description: 框架/库使用约定索引（React / antd / FastAPI / Tortoise / GSAP）
parent: ../index.md
children:
  - { name: react, path: react/index.md, tag: folder, note: 组件 / hook / state / SSR }
  - { name: antd, path: antd/index.md, tag: folder, note: Form / Modal / Table / mcp-first 用法 }
  - { name: fastapi, path: fastapi/index.md, tag: folder, note: router / schema / middleware }
  - { name: tortoise, path: tortoise/index.md, tag: folder, note: model 类模板 / 事务上下文 }
  - { name: gsap, path: gsap/index.md, tag: folder, note: FLIP / Draggable 动画 }
when_to_descend: |
  任务涉及具体框架的使用：写 React 组件 / 用 antd 组件 / 写 FastAPI router / 操作 Tortoise ORM / 写 GSAP 动画。
---

# Framework · 框架使用约定

> 状态：**W1 占位** —— 子目录 W2 起从 `.ai/skills/frontend/` 和 `.ai/skills/py/` 迁移并细分。

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| react | 文件夹 | 组件 / hook / state / SSR 4 类 |
| antd | 文件夹 | Form / Modal / Table / mcp-first 4 类 |
| fastapi | 文件夹 | router / schema / middleware 3 类 |
| tortoise | 文件夹 | model 模板 / 事务 |
| gsap | 文件夹 | FLIP / Draggable |

## 何时下钻

- 新增 / 修改 `frontend/src/**/*.tsx` → `react/` + 视具体 UI 决定要不要进 `antd/`
- 新增 / 修改 `backend/routers/*.py` 或 `backend/schemas/*.py` → `fastapi/`
- 操作 ORM Model 或写 migration → `tortoise/`
- 写动画相关代码（`*.animations.ts` / `useGSAP` 等）→ `gsap/`

## 下钻决策表

| 任务 | 选哪个子项 |
|------|----------|
| D6 PresentationCard 卡片 | react/component + antd/table（如有）|
| H2 ContentTypeSelector | react/component + react/state |
| 写 referral 充值返现 API | fastapi/router + fastapi/schema |
| DB10 referral 三表迁移 | tortoise/model-class-pattern |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行维度：[`../lang/index.md`](../lang/index.md) · [`../design-pattern/index.md`](../design-pattern/index.md) · [`../habit/index.md`](../habit/index.md)
- antd MCP（写 antd 组件前查）：`antd_info` / `antd_demo` / `antd_token`
