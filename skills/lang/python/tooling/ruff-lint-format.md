---
name: py-ruff-lint-format
description: Ruff 一统 lint+format，取代 flake8/black/isort/pylint/pyupgrade。Use when 配置 linter / 配置 formatter / 整理 import / 自动修复风格问题。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - ruff
  - lint
  - 格式化
  - formatter
  - isort
effort: medium
context: inline
version: '1.0'
---
# Python · Ruff 一统 lint 与 format

## 规则

| 规则 | 说明 |
|------|------|
| 一个工具替全套 | ruff 同时做 lint + format，替掉 flake8/black/isort/pylint/pyupgrade |
| 配置写进 `pyproject.toml` | 用 `[tool.ruff]`，不再维护 `.flake8`/`setup.cfg` |
| 显式选规则集 | `select` 列出启用的规则前缀，别只靠默认 |
| 修复用 `--fix` | `ruff check --fix` 自动修，剩下手动处理 |
| format 与 lint 分开 | `ruff format` 排版，`ruff check` 查错，二者互补 |
| 第三方代码用 import 排序 | `I` 规则替代 isort，无需单独配置 |

## 正例

`pyproject.toml`：

```toml
[tool.ruff]
line-length = 100
target-version = "py312"
src = ["src", "tests"]

[tool.ruff.lint]
# E/F=pyflakes+pycodestyle, I=isort, UP=pyupgrade,
# B=bugbear, SIM=simplify, RUF=ruff 专属
select = ["E", "F", "I", "UP", "B", "SIM", "RUF"]
ignore = ["E501"]  # 行宽交给 formatter，lint 不重复报

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S101"]  # 测试里允许 assert

[tool.ruff.format]
quote-style = "double"
```

常用命令：

```bash
ruff check --fix .      # lint + 自动修
ruff format .           # 排版
ruff check --diff .     # CI 里只看差异，不改盘
```

## 反例

```toml
# ❌ 同时装 black + isort + flake8 + ruff，规则互相打架
# → 只留 ruff，删掉 .flake8 / .isort.cfg

# ❌ 不写 select，默认只开 E/F，漏掉 import 排序和升级建议
[tool.ruff.lint]
# select 缺失 → I/UP/B 规则不生效

# ❌ lint 报行宽又让 formatter 排版，两边冲突反复跳动
[tool.ruff.lint]
select = ["E"]   # E501 未 ignore，与 formatter 抢行宽
```

```bash
# ❌ CI 里用 --fix 改动工作区，掩盖问题
ruff check --fix .   # CI 应只检测：去掉 --fix，加 --diff 或不加
```

## 自检

- [ ] 配置在 `pyproject.toml` 的 `[tool.ruff]`，没有残留 `.flake8`/`setup.cfg`？
- [ ] `select` 显式列出了规则集（至少 E/F/I）？
- [ ] 项目里已移除 black/isort/flake8，避免与 ruff 冲突？
- [ ] CI 用 `ruff check`（不带 `--fix`），本地才用 `--fix`？
- [ ] `ruff format` 与 `ruff check` 分别在脚本里调用？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`pre-commit-hooks.md`](./pre-commit-hooks.md) · [`ci-pipeline.md`](./ci-pipeline.md) · [`type-checker-ci.md`](./type-checker-ci.md)
