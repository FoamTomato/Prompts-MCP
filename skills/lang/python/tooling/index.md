---
name: lang-python-tooling-index
description: Python 工程化工具链索引（ruff / 类型检查 / pre-commit / CI / 结构化日志配置）。Use when 配置 lint / typecheck / 钩子 / 流水线 / 日志初始化。
parent: ../index.md
children:
  - { name: py-ruff-lint-format, path: ruff-lint-format.md, tag: skill, note: ruff 一统 lint+format，取代 flake8/black/isort }
  - { name: py-type-checker-ci, path: type-checker-ci.md, tag: skill, note: mypy strict / pyright / ty 接入 CI }
  - { name: py-pre-commit-hooks, path: pre-commit-hooks.md, tag: skill, note: pre-commit 编排 ruff/mypy 钩子 }
  - { name: py-ci-pipeline, path: ci-pipeline.md, tag: skill, note: lint→typecheck→test→coverage 门禁 }
  - { name: py-structured-logging-config, path: structured-logging-config.md, tag: skill, note: structlog + pydantic-settings 日志初始化配置 }
when_to_descend: 搭建/调整 Python 项目的 lint、类型检查、提交钩子、CI 流水线或日志初始化。
---

# Python · 工程化工具链索引

| 你在做什么 | 进哪个 |
|-----------|-------|
| 配 linter / formatter，替掉 flake8/black/isort | [ruff-lint-format](./ruff-lint-format.md) |
| 把类型检查（mypy/pyright/ty）跑进 CI | [type-checker-ci](./type-checker-ci.md) |
| 装提交前钩子，让本地和 CI 跑同一套检查 | [pre-commit-hooks](./pre-commit-hooks.md) |
| 写 GitHub Actions 流水线、设覆盖率门禁 | [ci-pipeline](./ci-pipeline.md) |
| 初始化结构化日志、用环境变量配置级别/格式 | [structured-logging-config](./structured-logging-config.md) |
