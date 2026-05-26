---
name: framework-fastapi-index
description: FastAPI 后端使用约定索引（Router / Schema / 中间件 / LLM 接入 / 对象存储）
parent: ../index.md
children:
  - { name: router, path: router/index.md, tag: folder, note: APIRouter 拆分 / 路径规范 / 依赖注入 }
  - { name: schema, path: schema/index.md, tag: folder, note: Pydantic 输入/输出模型 / 分层 }
  - { name: middleware, path: middleware/index.md, tag: folder, note: CORS / 异常处理器 / 日志中间件 }
  - { name: llm, path: llm/index.md, tag: folder, note: LLM provider 接入 + 流式响应 }
  - { name: storage, path: storage/index.md, tag: folder, note: 文件上传 / 对象存储抽象 }
when_to_descend: |
  写 / 改 `backend/**/*.py` 中 FastAPI 路由、Pydantic 模型、中间件、LLM 调用、文件上传相关代码。
---

# FastAPI · 后端使用约定

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| router | 文件夹 | APIRouter 拆分 + 路径规范 |
| schema | 文件夹 | Pydantic 输入/输出模型 |
| middleware | 文件夹 | CORS / 异常 / 日志 |
| llm | 文件夹 | LLM provider 接入 + SSE 流式 |
| storage | 文件夹 | 文件上传 + 对象存储 |

## 何时下钻

- 新增接口 → `router/index.md`
- 接口入参 / 出参定义 → `schema/index.md`
- 全局错误处理 / 跨域 → `middleware/index.md`
- 调 LLM / 流式返回 → `llm/index.md`
- 处理用户上传文件 → `storage/index.md`

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../tortoise/index.md`](../tortoise/index.md)
