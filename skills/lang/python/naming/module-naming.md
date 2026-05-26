---
name: python-module-naming
description: Python 模块/包命名 — 小写 + 单数 + 分层语义。Use when 写 Python 后端代码 / 评审涉及 `module-naming`
  的 PR。
parent: ./index.md
paths:
- backend/**/*.py
- '**/*.py'
triggers:
  keywords:
  - 模块命名
  - 包命名
  - __init__
  - 文件命名
effort: low
context: inline
version: '1.0'
---
# Python · 模块/包命名

## 规则

| 规则 | 示例 |
|------|------|
| 模块文件名小写 + 单数 | `service.py` / `repository.py` / `adapter.py` |
| 包目录名小写 + 复数（按职责） | `services/` / `routers/` / `models/` / `schemas/` |
| 多词用下划线 | `error_handler.py` / `request_id.py`（不要 errorHandler） |
| 业务模块按实体命名 | `services/tenant_manager.py` / `models/article.py` |
| 私有模块加前导下划线 | `_internal.py`（少用） |

## 分层包结构示例

```
backend/
├── core/          # 基础设施（config / db / redis / exceptions / response）
├── models/        # ORM 模型（按表）
├── schemas/       # Pydantic 请求/响应（按业务域）
├── adapters/      # ORM → Pydantic 规整层
├── routers/       # FastAPI 路由
├── services/      # 业务编排
├── agents/        # AI Agent 实现
├── tools/         # Agent 工具函数
├── middleware/    # 中间件
├── utils/         # 无状态工具
├── workers/       # 后台 worker
└── scripts/       # 种子脚本
```

业务域跨包时**同名对齐**：

```
schemas/article.py           # ArticleCreateReq / ArticleResponse
adapters/article.py          # to_response / to_list_response
routers/articles.py          # 复数（路由模块按 REST 资源）
services/article_cache.py    # 业务子能力（明确意图）
models/article.py            # ORM Model
```

## 反例

```python
# ❌ 驼峰
UserManager.py

# ❌ 一个文件什么都写（god module）
services/everything.py

# ❌ 包名复数 + 文件名复数 双复数
services/tenants.py     # → services/tenant_manager.py 或 services/tenant.py

# ❌ 模块名是动词
do_create_user.py        # → user_creator.py 或写到 service 里
```

## 自检

- [ ] 模块文件名是小写 + 名词？
- [ ] 业务实体跨包同名对齐？
- [ ] 没有 god module？（超过 400 行考虑按业务子能力拆）

## 相关

- 父：[`./index.md`](./index.md)
- 配套：[`../../../design-pattern/ddd-layering/index.md`](../../../design-pattern/ddd-layering/index.md)
