---
name: lang-python-packaging-index
description: Python 打包与依赖管理规范（uv 工作流 / pyproject.toml / lockfile / 构建发布）。Use when 初始化项目 / 加依赖 / 锁版本 / 构建 wheel 发布。
parent: ../index.md
children:
  - { name: py-uv-workflow, path: uv-workflow.md, tag: skill, note: "uv venv/add/run/lock/tool 与 Python 版本管理" }
  - { name: py-pyproject-toml, path: pyproject-toml.md, tag: skill, note: "PEP 621 [project] 元数据 + 构建后端" }
  - { name: py-lockfile-reproducible, path: lockfile-reproducible.md, tag: skill, note: "uv.lock 提交 + 依赖组 + 可复现安装" }
  - { name: py-build-publish, path: build-publish.md, tag: skill, note: "uv build/publish + entry points + editable" }
when_to_descend: 建项目 / 装依赖 / 配 pyproject / 锁版本 / 打包发布到 PyPI
---

# Python · 打包与依赖管理 · 子项索引

| 你在做什么 | 进哪个 |
|-----------|-------|
| 建虚拟环境 / 加删依赖 / 跑命令 / 装 Python 版本 / 装 CLI 工具 | uv-workflow |
| 写 `pyproject.toml` 的元数据、依赖声明、可选依赖、构建后端 | pyproject-toml |
| 该不该提交 lockfile / 怎么分 dev/test 依赖组 / CI 复现安装 | lockfile-reproducible |
| 构建 wheel+sdist / 发布 PyPI / 配 entry points / editable 安装 | build-publish |

## 链接

- 父：[`../index.md`](../index.md)
- 关联：[`../../python/typing/index.md`](../../python/typing/index.md)（依赖里的类型 stub）
