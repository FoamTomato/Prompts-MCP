---
name: lang-index
description: 语言级规则索引（Python / TypeScript / SQL）
parent: ../index.md
children:
  - { name: python, path: python/index.md, tag: folder, note: Python 命名 / async / import / 错误处理 / 类型 }
  - { name: typescript, path: typescript/index.md, tag: folder, note: TS 命名 / 类型严格 / async / 模块 / 错误处理 }
  - { name: sql, path: sql/index.md, tag: folder, note: SELECT 规则 / 禁项 / JOIN / DDL 模板 }
when_to_descend: |
  任务涉及具体语言文件（.py / .ts / .tsx / .sql / Alembic migration / Tortoise raw query / seed 脚本）。
---

# Lang · 语言级规则

> 状态：**W1 占位** —— 子目录 W2 起从 `.ai/skills/{py,frontend}/` 迁移并细分。

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| python | 文件夹 | 命名 / 异步 / import / 错误处理 / 类型 5 类规则 |
| typescript | 文件夹 | 命名 / 严格模式 / async / 模块 4 类规则 |
| sql | 文件夹 | SELECT / 禁项 / JOIN / DDL 4 类规则 |

## 何时下钻

- 写 / 改 `.py` 文件（含 backend/ / py/ / py/migrations/） → `python/`
- 写 / 改 `.ts` / `.tsx` 文件 → `typescript/`
- 写 / 改 `.sql` 文件 / Alembic 迁移 / Tortoise raw query / seed 脚本 → `sql/`

## 下钻决策表

| 任务 | 选哪个子项 |
|------|----------|
| 改 backend/services/*.py | python/naming + python/async + python/typing |
| 写新 React 组件 | typescript/typing + typescript/naming |
| 写 paper_editor 的 SQL 查询 | sql/select + sql/forbidden + sql/join |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行维度：[`../framework/index.md`](../framework/index.md) · [`../design-pattern/index.md`](../design-pattern/index.md) · [`../habit/index.md`](../habit/index.md)
